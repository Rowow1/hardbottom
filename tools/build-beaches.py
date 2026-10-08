#!/usr/bin/env python3
"""Build data/beaches.json: the r. 68B-20.003(2)(a) beach buffer along Florida's sandy coast.

Fla. Admin. Code r. 68B-20.003(2)(a) closes water "Within 100 yards of any public bathing beach".
FWC's rule says "any", and Florida's beaches are public below the mean high-water line, so the map
draws the reading that closes more water: every stretch of open-coast sandy beach is treated as a
public bathing beach.

Input: tools/beaches-2026-10-08/waterline.txt, pulled in the author's Chrome on 8 Oct 2026:
  - FDEP Coastal Range Monuments (ca.dep.state.fl.us/arcgis/rest/services/OpenData/COASTAL_ENV_PERM/
    MapServer/10, 4,457 monuments in 30 counties). The R-series monuments are the state's survey
    baseline along its sandy beaches; the V-series are supplementary monuments.
  - NOAA ENC coastline (Coastline_line, enc_harbour layer 84 and enc_approach layer 88).
  For each monument the page took the nearest point of the charted coastline, within 800 m, from
  which a 3 km line continuing away from the monument meets no other coastline: the open-water
  shore, not a lagoon or bay shore behind the beach. Monuments of one county and series were then
  chained in number order, breaking the chain wherever two consecutive shore points lie more than
  600 m apart (an inlet, a gap in the monument line, or a stretch with no open-water shore).
Line format: county|first monument|last monument|count|seaward bearing (degrees, mathematical, from
the monuments to the shore)|shore points, delta-encoded [lat, lon] in 1e-5 degree. Transfer checked
with a 32-bit rolling hash (2419461672).

Output: one zone per chain of two or more monuments, buffered 150 yd (the 100 yd rule plus 50 yd,
as in the Palm Beach layer) on the seaward side of the chained shore points, with round ends.
Chains of a single monument are not drawn; they are counted in the output note.
"""
import io, json, math, os
from shapely.geometry import LineString, Point
from shapely.ops import unary_union
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'beaches-2026-10-08', 'waterline.txt')
OUT = os.path.join(HERE, '..', 'data', 'beaches.json')
YD = 0.9144
BUF_M = 150 * YD
TOL_M = 5.0
fwd = Transformer.from_crs('EPSG:4326', 'EPSG:3086', always_xy=True).transform
inv = Transformer.from_crs('EPSG:3086', 'EPSG:4326', always_xy=True).transform
COUNTY = {'DADE': 'Miami-Dade', 'SANTAROSA': 'Santa Rosa', 'ST JOHNS': 'St. Johns', 'ST LUCIE': 'St. Lucie',
          'PALM BEACH': 'Palm Beach', 'INDIAN RIVER': 'Indian River'}


def county(c):
    return COUNTY.get(c, c.title())


def dec(s):
    pts, a, o = [], 0, 0
    for k, p in enumerate(s.split(';')):
        x, y = map(int, p.split(','))
        a, o = (x, y) if k == 0 else (a + x, o + y)
        pts.append((a / 1e5, o / 1e5))
    return pts


def enc(latlons):
    out, pa, po = [], None, None
    for la, lo in latlons:
        a, o = round(la * 1e5), round(lo * 1e5)
        if pa is None:
            out += [a, o]
        else:
            if a == pa and o == po:
                continue
            out += [a - pa, o - po]
        pa, po = a, o
    return out


def mnum(name):
    return name.split('-', 1)[1] if '-' in name else name


zones, singles, short = [], 0, 0
for raw in io.open(SRC, encoding='utf-8').read().split('\n'):
    raw = raw.strip()
    if not raw or raw.startswith('#'):
        continue
    c, first, last, n, bearing, pts = raw.split('|')
    pts = dec(pts)
    # Drop repeated points (two monuments that met the shore at the same place).
    clean = [pts[0]] + [p for i, p in enumerate(pts[1:], 1) if p != pts[i - 1]]
    if len(clean) < 2:
        singles += 1
        continue
    m = [fwd(lo, la) for la, lo in clean]
    line = LineString(m)
    if line.length < 50:
        short += 1
        continue
    b = math.radians(float(bearing))
    sea = (math.cos(b), math.sin(b))
    left = line.buffer(BUF_M, single_sided=True)
    # A one-sided buffer to the left of the line's direction; keep the side that faces the sea.
    lc, oc = left.centroid, line.centroid
    side = left if (lc.x - oc.x) * sea[0] + (lc.y - oc.y) * sea[1] > 0 else line.buffer(-BUF_M, single_sided=True)
    body = unary_union([side, Point(m[0]).buffer(BUF_M, 16), Point(m[-1]).buffer(BUF_M, 16)]).simplify(TOL_M)
    polys = [body] if body.geom_type == 'Polygon' else list(body.geoms)
    rings = [enc([inv(x, y)[::-1] for x, y in p.exterior.coords]) for p in polys]
    series = first.split('-')[0]
    cn = county(c)
    rng = mnum(first) if first == last else '%s to %s' % (mnum(first), mnum(last))
    zones.append(dict(
        id='beach-%s-%s-%s' % (c.lower().replace(' ', ''), first.lower(), last.lower()),
        n='%s County beach, %s-monuments %s' % (cn, series, rng),
        cty=cn, kind='closed' if series == 'R' else 'warn', law=['fac-68b-20-003-2'],
        mon=[first, last, int(n)], ri=rings, li=enc(clean),
        len_m=round(line.length)))

zones.sort(key=lambda z: (z['cty'], z['id']))
out = dict(version='2026-10-08',
           note='Fla. Admin. Code r. 68B-20.003(2)(a) beach buffer, 100 yd drawn at 150 yd seaward of the '
                'charted shore (NOAA ENC) along every chain of FDEP range monuments. kind closed: R-series '
                'monuments, the sandy-beach baseline. kind warn: V-series (supplementary) monuments, whose '
                'shore may not be a bathing beach. %d single-monument stretches and %d chains under 50 m are '
                'not drawn. Built by tools/build-beaches.py.' % (singles, short),
           zones=zones)
json.dump(out, open(OUT, 'w'), separators=(',', ':'))
import collections
print(len(zones), collections.Counter(z['kind'] for z in zones), 'singles', singles, 'short', short,
      'km', round(sum(z['len_m'] for z in zones) / 1000), os.path.getsize(OUT), 'bytes')
