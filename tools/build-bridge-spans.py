#!/usr/bin/env python3
"""Add the reviewed bridge spans to data/bridges.json.

Fla. Admin. Code r. 68B-20.003(2)(c) closes water within 100 yd of "that portion of any bridge on
which public fishing is legally permitted". The National Bridge Inventory gives one point per
bridge, so the map used to draw a 125 yd circle at that point. A long bridge runs far outside that
circle. This script buffers the bridge deck itself.

Input: tools/jetties-2026-10-07/bridges-reviewed.txt, written in the author's Chrome on 7 and 8 Oct
2026 while every coastal and tidal bridge (presumed or confirmed, 2,509 records) was read on USGS
NAIP imagery with the OpenStreetMap bridge decks drawn over it. Format:
  #W  one OSM bridge deck per line, "lat,lon;dlat,dlon;..." in units of 1e-5 degree, the first pair
      absolute and the rest deltas. Line order is the deck index.
  #B  "bridge index:deck index,deck index,..." for the 1,441 records whose matched deck runs more
      than 22 m from the NBI point. Bridge index is the position in data/bridges.json.
  #N  space-separated "<bridge index><k>" for records reviewed and kept as a circle:
      n = no deck within 60 m, l = loose match (60 to 250 m, rejected), f = ferry line, not a deck.
Reviewed records in neither list have a deck that stays within 22 m of the point, so the circle
already covers it.

Output fields on each reviewed record in data/bridges.json:
  rv  span | short | none | loose | ferry
  dk  matched deck lines, each a flat list [lat, lon, dlat, dlon, ...] in 1e-5 degree
  sp  buffer rings in the same encoding: the union of the 125 yd circle at the NBI point and a
      125 yd band along every matched deck, so no record covers less water than before.
Deck geometry is from OpenStreetMap (ODbL 1.0, see LICENSE-DATA). Re-running is safe: the three
fields are stripped and rebuilt, and records are matched by index and checked by position.
"""
import json, os, sys
from shapely.geometry import LineString, Point
from shapely.ops import unary_union
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'jetties-2026-10-07', 'bridges-reviewed.txt')
OUT = os.path.join(HERE, '..', 'data', 'bridges.json')
BUF_M = 125 * 0.9144          # 100 yd rule, drawn at 125 yd, as in js/app.js
TOL_M = 5.0                   # simplification tolerance; the ring may sit up to 5 m inside the 125 yd line, well clear of 100 yd

fwd = Transformer.from_crs('EPSG:4326', 'EPSG:3086', always_xy=True).transform
inv = Transformer.from_crs('EPSG:3086', 'EPSG:4326', always_xy=True).transform

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

lines = open(SRC).read().split('\n')
iw, ib, inn = lines.index('#W'), lines.index('#B'), lines.index('#N')
DECKS = []
for ln in lines[iw + 1:ib]:
    pts, x, y = [], 0, 0
    for k, p in enumerate(ln.split(';')):
        a, b = map(int, p.split(','))
        x, y = (a, b) if k == 0 else (x + a, y + b)
        pts.append((x / 1e5, y / 1e5))
    DECKS.append(pts)
SPAN = {int(k): [int(t) for t in v.split(',')] for k, v in (l.split(':') for l in lines[ib + 1:inn])}
KEEP = {int(t[:-1]): {'n': 'none', 'l': 'loose', 'f': 'ferry'}[t[-1]] for t in lines[inn + 1].split()}

B = json.load(open(OUT))
for b in B:
    for f in ('rv', 'dk', 'sp'):
        b.pop(f, None)

reviewed = [i for i, b in enumerate(B) if b['st'] != 'excluded' and b.get('iw') in ('coastal', 'tidal')]
if len(reviewed) != 2509:
    sys.exit('expected the 2,509 coastal and tidal records reviewed on 8 Oct 2026, found %d; '
             'bridges.json has changed since the review' % len(reviewed))
for i in list(SPAN) + list(KEEP):
    if i not in reviewed:
        sys.exit('record %d is not a coastal or tidal presumed/confirmed bridge' % i)

npts = 0
for i in reviewed:
    b = B[i]
    if i in KEEP:
        b['rv'] = KEEP[i]
        continue
    if i not in SPAN:
        b['rv'] = 'short'
        continue
    decks = [DECKS[j] for j in SPAN[i]]
    c = Point(fwd(b['lon'], b['lat']))
    gl = [LineString([fwd(lo, la) for la, lo in d]) for d in decks]
    near = min(g.distance(c) for g in gl)
    if near > 250:
        sys.exit('record %d (%s): matched deck is %.0f m from the NBI point' % (i, b['n'], near))
    g = unary_union([c.buffer(BUF_M, quad_segs=16)] + [l.buffer(BUF_M, quad_segs=8) for l in gl]).simplify(TOL_M)
    polys = [g] if g.geom_type == 'Polygon' else list(g.geoms)
    rings = []
    for p in polys:
        ring = [inv(x, y)[::-1] for x, y in p.exterior.coords]
        rings.append(enc(ring)); npts += len(ring)
    b['rv'] = 'span'
    b['dk'] = [enc(d) for d in decks]
    b['sp'] = rings

json.dump(B, open(OUT, 'w'), separators=(',', ':'))
import collections
print(collections.Counter(b.get('rv') for b in B), npts, 'ring points', os.path.getsize(OUT), 'bytes')
