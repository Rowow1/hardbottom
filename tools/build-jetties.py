#!/usr/bin/env python3
"""Build data/jetties.json: the r. 68B-20.003(2)(d) jetty buffers, one structure at a time.

Inputs:
  jetties-2026-10-07/review.py   one record per structure, written while reading each site on USGS NAIP
                                 imagery on 7 and 8 Oct 2026 (see the file header)
  jetties-2026-10-07/osm-enc-reviewed.txt
                                 NOAA ENC shoreline-construction features the review kept, one per line:
                                 "E<enc index>:<WATLEV>:<part>|<part>", coordinates in 1e-5 degree. Until
                                 8 Oct 2026 it also held the OpenStreetMap ways named in review.py; those
                                 were removed when the jetties were rebuilt from the chart.
  jetties-2026-10-08/enc-jetties.txt, encsel.py
                                 the NOAA ENC features that replace those ways (rebuild of 8 Oct 2026)
  jetties-2026-10-08/standins.txt
                                 a circle for each reviewed stretch that the chart does not carry

The rule closes water "Within 100 feet of the unsubmerged portion of any jetty, except that
spearfishing shall be allowed along the last 500 yards of any jetty that extends more than 1,500
yards from the shoreline." The buffer is drawn at 150 ft (50 per cent margin, as in the Palm Beach
layer). Where a traced jetty runs more than 1,500 yd seaward of the shoreline, the (d) buffer is
not drawn along the last 400 yd: the rule lifts it along 500 yd, and the 100 yd difference is the
margin. That stretch is drawn as a separate amber note, because other rules may still close it.
"""
import json, os, sys
from shapely.geometry import LineString, Polygon, Point, mapping
from shapely.ops import unary_union, transform, substring
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'jetties-2026-10-07')
OUT = os.path.join(HERE, '..', 'data', 'jetties.json')

FT = 0.3048
YD = 0.9144
BUF_M = 150 * FT            # 100 ft rule, drawn at 150 ft
CHART_M = float(os.environ.get('CHART_M', '10'))  # rebuilt structures: chart lines can sit on one face of a
                                                   # wide structure or off it by a few metres, so 10 m more
LONG_M = 1500 * YD          # the long-jetty threshold
EXEMPT_M = 400 * YD         # 500 yd in the rule, 400 yd drawn (100 yd margin)
MARGIN_M = 300 * YD         # a jetty must clear 1,500 yd by 300 yd (20 per cent) on the imagery before the exception is drawn

fwd = Transformer.from_crs('EPSG:4326', 'EPSG:3086', always_xy=True).transform   # Florida GDL Albers, metres
inv = Transformer.from_crs('EPSG:3086', 'EPSG:4326', always_xy=True).transform

def to_m(latlons):
    return [fwd(lon, lat) for lat, lon in latlons]

def ring_ll(geom):
    """Shapely polygon in metres -> list of [lat, lon] rings, 5 dp."""
    out = []
    polys = [geom] if geom.geom_type == 'Polygon' else list(geom.geoms)
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            pts = []
            for x, y in ring.coords:
                lon, lat = inv(x, y)
                pts.append([round(lat, 5), round(lon, 5)])
            out.append(pts)
    return out

def line_ll(line):
    pts = []
    for x, y in line.coords:
        lon, lat = inv(x, y)
        pts.append([round(lat, 5), round(lon, 5)])
    return pts

# ---------- read the review and the pulled geometry ----------
import math, re
from importlib import util as _u
_spec = _u.spec_from_file_location('encsel', os.path.join(HERE, 'jetties-2026-10-08', 'encsel.py'))
ENC8 = _u.module_from_spec(_spec); _spec.loader.exec_module(ENC8)
STANDIN = {}
for raw in open(os.path.join(HERE, 'jetties-2026-10-08', 'standins.txt')).read().split('\n'):
    if raw.strip():
        k, ll, r, ln = raw.split('|')
        la, lo = map(float, ll.split(','))
        STANDIN.setdefault(k, []).append((la, lo, int(r), int(ln)))
# The shore point of the long-jetty test, where a rebuilt structure needs one: the landward end of the
# charted jetty (NOAA ENC, cell US5FL8CE).
SHORE8 = {'stmarys-s': [30.70043, -81.42858]}
ns = {}
exec(open(os.path.join(SRC, 'review.py')).read(), ns)
J = ns['J']

GEOM = {}
for raw in open(os.path.join(SRC, 'osm-enc-reviewed.txt')).read().split('\n'):
    raw = raw.strip()
    if not raw:
        continue
    if raw.startswith('E'):
        key, wl, rest = raw.split(':', 2)
        parts = [[[int(a) / 1e5, int(b) / 1e5] for a, b in (q.split(',') for q in part.split(';'))]
                 for part in rest.split('|')]
        GEOM[key] = dict(parts=parts, watlev=None if wl == 'null' else int(wl), src='enc')
    else:
        key, rest = raw.split(':', 1)
        parts = [[[int(a) / 1e5, int(b) / 1e5] for a, b in (q.split(',') for q in rest.split(';'))]]
        GEOM[key] = dict(parts=parts, watlev=None, src='osm')

WATLEV = {1: 'partly submerged at high water', 2: 'always dry', 3: 'always under water',
          4: 'covers and uncovers', 5: 'awash', 7: 'floating', None: 'not charted'}

def feature_geoms(key):
    g = GEOM.get(key)
    if not g:
        sys.exit('missing geometry for ' + key)
    out = []
    for part in g['parts']:
        m = to_m(part)
        if len(m) >= 4 and part[0] == part[-1]:
            out.append(Polygon(m).buffer(0))
        elif len(m) >= 2:
            out.append(LineString(m))
        else:
            out.append(Point(m[0]))
    return out

zones, notes, missing = [], [], []
for j in J:
    if j['cls'] == 'none':
        continue
    geoms, srcs = [], []
    rebuilt = bool(j['ways'])
    standins = []
    if rebuilt:
        # Rebuilt on 8 Oct 2026 from the NOAA chart: the OpenStreetMap ways the review had checked are
        # replaced by the charted shoreline construction along them, and any reviewed stretch the chart
        # does not carry gets a stand-in circle.
        for f in ENC8.features(j['key']):
            # Floating structures carry no buffer. A feature charted as always under water (3) is drawn
            # here, because it lies along a structure the 7 Oct review saw above water on the imagery:
            # where the chart and the photograph disagree, the reading that closes more water is drawn.
            if f['wat'] == '7':
                continue
            for part in f['parts']:
                mm = to_m(part)
                geoms.append(LineString(mm) if len(mm) > 1 else Point(mm[0]))
            srcs.append('NOAA ENC %s, %s (%s)' % (f['cat'], ENC8.WATLEV.get(f['wat'], f['wat']), f['cell']))
        for la, lo, r, ln in STANDIN.get(j['key'], []):
            x, y = fwd(lo, la)
            standins.append(dict(pt=[la, lo], r=r, stretch=ln, geom=Point(x, y).buffer(r - BUF_M, 32)))
        if standins:
            srcs.append('stand-in circles where the chart does not carry the structure')
    for e in j['enc']:
        g = GEOM.get('E%d' % e)
        if g and g['watlev'] in (3, 7):
            continue                       # always under water, or floating: no unsubmerged portion
        geoms += feature_geoms('E%d' % e)
        srcs.append('NOAA ENC shoreline construction (%s)' % WATLEV.get(g['watlev'] if g else None))
    traced = None
    if j.get('line'):
        traced = LineString(to_m(j['line']))
        geoms.append(traced); srcs.append('traced on imagery (%s)' % j['img'])
    for k, pts in (j.get('add') or {}).items():
        if k == 'tip' and j['ways']:
            # Join the tip read on the imagery to the nearest end of the charted structure.
            tx, ty = fwd(pts[-1][1], pts[-1][0])
            ends = [c for g in geoms if g.geom_type == 'LineString' for c in (g.coords[0], g.coords[-1])]
            near = min(ends, key=lambda c: math.hypot(c[0] - tx, c[1] - ty))
            ext = LineString([near] + to_m(pts))
            geoms.append(ext); srcs.append('extension traced on imagery (%s)' % j['img'])
    marker = (j.get('add') or {}).get('marker')

    zone = dict(id='jetty-' + j['key'], n=j['name'], cty=j['county'], kind=j['cls'],
                law=['fac-68b-20-003-2'], seen=j['seen'], note=j['note'], fwc=j['fwc'],
                src='; '.join(dict.fromkeys(srcs)) or 'marker only', r=[], line=[], pts=[],
                exempt=None)
    if marker:
        zone['pts'] = marker
    if not geoms and not standins:
        if not marker:
            missing.append(j['key'])
        zones.append(zone)
        continue

    # Long-jetty test on the traced or single-line centreline, measured from the shoreline point.
    exempt_line = None
    centre = traced
    shore = SHORE8.get(j['key']) if rebuilt else j.get('shore')
    if centre is None and rebuilt and shore:
        # Chain the charted lines from the shore point seaward: from the current point, step onto an
        # unused line with an end within 100 m, choosing the one whose other end lies farthest from the
        # shore, until no line carries the chain farther out.
        sx, sy = fwd(shore[1], shore[0])
        lines = [g for g in geoms if g.geom_type == 'LineString']
        def far_end(g, c):
            a, b = g.coords[0], g.coords[-1]
            return list(g.coords) if math.hypot(a[0] - c[0], a[1] - c[1]) <= math.hypot(b[0] - c[0], b[1] - c[1]) else list(g.coords)[::-1]
        cur = (sx, sy); chain = [cur]; used = set()
        while True:
            best = None
            here = math.hypot(cur[0] - sx, cur[1] - sy)
            for i, g in enumerate(lines):
                if i in used:
                    continue
                for c in (g.coords[0], g.coords[-1]):
                    if math.hypot(c[0] - cur[0], c[1] - cur[1]) <= 100:
                        fe = far_end(g, cur)[-1]
                        out_d = math.hypot(fe[0] - sx, fe[1] - sy)
                        if out_d > here + 10 and (best is None or out_d > best[0]):
                            best = (out_d, i)
            if best is None:
                break
            used.add(best[1]); seg = far_end(lines[best[1]], cur); chain += seg; cur = seg[-1]
        if len(chain) > 2:
            centre = LineString(chain)
    seaward = None
    if centre is not None and shore:
        sx, sy = fwd(shore[1], shore[0])
        d_shore = centre.project(Point(sx, sy))
        seaward = centre.length - d_shore
        zone['seaward_yd'] = round(seaward / YD)
        if seaward > LONG_M + MARGIN_M:
            exempt_line = substring(centre, centre.length - EXEMPT_M, centre.length)
        elif seaward > LONG_M - MARGIN_M:
            zone['near_long'] = True

    bm = BUF_M + (CHART_M if rebuilt else 0)
    body = unary_union([g.buffer(bm, cap_style='round', join_style='round') for g in geoms] +
                       [st['geom'].buffer(BUF_M) for st in standins])
    if rebuilt:
        zone['seen'] = re.sub(r'(;|,)? ?(the )?(whole )?(OSM|OpenStreetMap)( and ENC)?( outline| line| lines)?( "[^"]*")? (matches|match)( the [a-z ]+)?', '', zone['seen'] or '')
        zone['note'] = (zone['note'] or '')
        zone['note'] = re.sub(r'Whole OSM line drawn', 'Whole structure drawn', zone['note'])
        zone['note'] = re.sub(r'OpenStreetMap line matches the edge of the rock on the imagery\.', '', zone['note']).strip()
        add = 'Drawn from the NOAA chart (ENC shoreline construction), rebuilt 8 Oct 2026.'
        if standins:
            add += (' %d stretch%s of the structure seen on the imagery %s not on the chart; a circle of %s m '
                    'around %s is drawn in %s place, which closes more water than the structure itself would.'
                    % (len(standins), 'es' if len(standins) > 1 else '', 'are' if len(standins) > 1 else 'is',
                       ', '.join(str(st['r']) for st in standins), 'them' if len(standins) > 1 else 'it',
                       'their' if len(standins) > 1 else 'its'))
            zone['standin'] = [dict(pt=st['pt'], r=st['r']) for st in standins]
        zone['note'] = (zone['note'] + ' ' + add).strip()
    if exempt_line is not None:
        # Remove the exempt stretch: water within the buffer that is nearer the exempt last 400 yd
        # than any other part of the structure.
        kept = substring(centre, 0, centre.length - EXEMPT_M)
        # Every other part of the structure keeps its buffer; the lines the centreline was chained
        # from are part of the centreline and do not.
        others = [g for g in geoms if g is not centre and g is not traced
                  and g.difference(centre.buffer(5)).length > 1]
        keep_body = unary_union([kept.buffer(bm)] + [g.buffer(bm) for g in others] +
                                [st['geom'].buffer(BUF_M) for st in standins])
        ex_body = exempt_line.buffer(bm).difference(keep_body)
        body = keep_body
        zone['exempt'] = dict(r=ring_ll(ex_body.simplify(1.0)), line=line_ll(exempt_line),
                              seaward_yd=round(seaward / YD))
    zone['r'] = ring_ll(body.simplify(1.0))
    zone['line'] = [line_ll(g) for g in geoms if g.geom_type == 'LineString']
    zone['line'] += [line_ll(g.exterior) for g in geoms if g.geom_type == 'Polygon']
    if standins and not zone['line']:
        zone['pts'] = [st['pt'] for st in standins]
    zones.append(zone)

if missing:
    sys.exit('no geometry for ' + ', '.join(missing))

out = dict(version='2026-10-08b',
           note='Fla. Admin. Code r. 68B-20.003(2)(d) jetty buffers, read structure by structure on USGS '
                'NAIP imagery. The rule is 100 ft from the unsubmerged portion of a jetty; every buffer is '
                'drawn at 150 ft. kind closed: an inlet or fishing jetty. kind warn: a shore structure that '
                'may count as a jetty (groin, breakwater, revetment, detached breakwater). Built by '
                'tools/build-jetties.py.',
           zones=zones)
json.dump(out, open(OUT, 'w'), separators=(',', ':'))
import collections
print(len(zones), collections.Counter(z['kind'] for z in zones),
      'exempt:', [z['id'] for z in zones if z['exempt']],
      'seaward yd:', {z['id']: z.get('seaward_yd') for z in zones if z.get('seaward_yd')},
      os.path.getsize(OUT), 'bytes')
