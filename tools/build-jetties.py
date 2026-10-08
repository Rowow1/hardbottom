#!/usr/bin/env python3
"""Build data/jetties.json: the r. 68B-20.003(2)(d) jetty buffers, one structure at a time.

Inputs (all in tools/jetties-2026-10-07/):
  review.py               one record per structure, written while reading each site on USGS NAIP
                          imagery on 7 and 8 Oct 2026 (see the file header)
  osm-enc-reviewed.txt    geometry of the OpenStreetMap ways and NOAA ENC shoreline-construction
                          features that the review kept, as pulled in the author's Chrome. One feature
                          per line: "<osm way id>:lat,lon;lat,lon;..." or "E<enc index>:<WATLEV>:<part>|<part>",
                          coordinates in units of 1e-5 degree.

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
    for w in j['ways']:
        geoms += feature_geoms(str(w)); srcs.append('OpenStreetMap way %s' % w)
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
            base = GEOM[str(j['ways'][0])]['parts'][0]
            ext = LineString(to_m([base[-1]] + pts))
            geoms.append(ext); srcs.append('extension traced on imagery (%s)' % j['img'])
    marker = (j.get('add') or {}).get('marker')

    zone = dict(id='jetty-' + j['key'], n=j['name'], cty=j['county'], kind=j['cls'],
                law=['fac-68b-20-003-2'], seen=j['seen'], note=j['note'], fwc=j['fwc'],
                src='; '.join(dict.fromkeys(srcs)) or 'marker only', r=[], line=[], pts=[],
                exempt=None)
    if marker:
        zone['pts'] = marker
    if not geoms:
        if not marker:
            missing.append(j['key'])
        zones.append(zone)
        continue

    # Long-jetty test on the traced or single-line centreline, measured from the shoreline point.
    exempt_line = None
    centre = traced
    if centre is None and len(j['ways']) == 1 and not j['enc']:
        g0 = geoms[0]
        if g0.geom_type == 'LineString':
            centre = g0
            if 'tip' in (j.get('add') or {}):
                centre = LineString(list(g0.coords) + list(geoms[-1].coords)[1:])
    seaward = None
    if centre is not None and j.get('shore'):
        sx, sy = fwd(j['shore'][1], j['shore'][0])
        d_shore = centre.project(Point(sx, sy))
        seaward = centre.length - d_shore
        zone['seaward_yd'] = round(seaward / YD)
        if seaward > LONG_M + MARGIN_M:
            exempt_line = substring(centre, centre.length - EXEMPT_M, centre.length)
        elif seaward > LONG_M - MARGIN_M:
            zone['near_long'] = True

    body = unary_union([g.buffer(BUF_M, cap_style='round', join_style='round') for g in geoms])
    if exempt_line is not None:
        # Remove the exempt stretch: water within the buffer that is nearer the exempt last 400 yd
        # than any other part of the structure.
        kept = substring(centre, 0, centre.length - EXEMPT_M)
        others = [g for g in geoms if g is not centre and g is not traced]
        keep_body = unary_union([kept.buffer(BUF_M)] + [g.buffer(BUF_M) for g in others])
        ex_body = exempt_line.buffer(BUF_M).difference(keep_body)
        body = keep_body
        zone['exempt'] = dict(r=ring_ll(ex_body.simplify(1.0)), line=line_ll(exempt_line),
                              seaward_yd=round(seaward / YD))
    zone['r'] = ring_ll(body.simplify(1.0))
    zone['line'] = [line_ll(g) for g in geoms if g.geom_type == 'LineString']
    zone['line'] += [line_ll(g.exterior) for g in geoms if g.geom_type == 'Polygon']
    zones.append(zone)

if missing:
    sys.exit('no geometry for ' + ', '.join(missing))

out = dict(version='2026-10-08',
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
