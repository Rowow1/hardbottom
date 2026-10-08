#!/usr/bin/env python3
"""One-off, run on 8 Oct 2026: where the 7 Oct jetty review kept an OpenStreetMap way and the NOAA ENC
chart (enc-jetties.txt, selected as in tools/build-jetties.py) carries no shoreline construction within
25 m of it, record one stand-in point per uncharted stretch and the radius of a circle that covers the
stretch plus the 150 ft drawn buffer. Output: standins.txt ("<jetty key>|lat,lon|radius m|stretch m").

Input: the OpenStreetMap ways in tools/jetties-2026-10-07/osm-enc-reviewed.txt as it stood at commit
3bb9b91 (the file no longer carries OpenStreetMap coordinates). Run with that file restored, e.g.
  git show 3bb9b91:tools/jetties-2026-10-07/osm-enc-reviewed.txt > /tmp/osm-enc-reviewed.txt
  OSM_FILE=/tmp/osm-enc-reviewed.txt python3 tools/jetties-2026-10-08/make-standins.py

The output holds fewer than 100 positions taken once from fewer than 100 OpenStreetMap features, an
insubstantial extract under the OSMF Community Guideline on substantial extracts; see LICENSE-DATA.md.
"""
import math, os, sys
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union
from pyproj import Transformer
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
fwd = Transformer.from_crs('EPSG:4326', 'EPSG:3086', always_xy=True).transform
inv = Transformer.from_crs('EPSG:3086', 'EPSG:4326', always_xy=True).transform
ns = {}
exec(open(os.path.join(HERE, '..', 'jetties-2026-10-07', 'review.py')).read(), ns)
from importlib import util
spec = util.spec_from_file_location('encsel', os.path.join(HERE, 'encsel.py')); E = util.module_from_spec(spec); spec.loader.exec_module(E)
OSM = {}
for raw in open(os.environ['OSM_FILE']).read().split('\n'):
    raw = raw.strip()
    if raw and not raw.startswith('E'):
        k, rest = raw.split(':', 1)
        OSM[k] = [[int(a) / 1e5, int(b) / 1e5] for a, b in (q.split(',') for q in rest.split(';'))]
m = lambda pts: [fwd(lo, la) for la, lo in pts]
out = []
for j in ns['J']:
    if j['cls'] == 'none' or not j['ways']:
        continue
    old = unary_union([LineString(m(OSM[str(w)])) for w in j['ways'] if len(OSM[str(w)]) > 1])
    enc = E.geoms_m(j['key'])
    adds = [LineString(m(j['line']))] if j.get('line') else []
    cover = unary_union(enc + adds).buffer(25) if (enc or adds) else None
    gap = old.difference(cover) if cover is not None else old
    for g in (gap.geoms if hasattr(gap, 'geoms') else [gap]):
        if g.length <= 15:
            continue
        c = g.interpolate(0.5, normalized=True)
        r = max(Point(c).distance(Point(p)) for p in g.coords) + 150 * 0.3048
        r = math.ceil(r / 10) * 10
        lon, lat = inv(c.x, c.y)
        out.append('%s|%.5f,%.5f|%d|%d' % (j['key'], lat, lon, r, round(g.length)))
open(os.path.join(HERE, 'standins.txt'), 'w').write('\n'.join(out) + '\n')
print(len(out), 'stand-ins')
