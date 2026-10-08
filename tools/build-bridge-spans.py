#!/usr/bin/env python3
"""Add the bridge spans to data/bridges.json.

Fla. Admin. Code r. 68B-20.003(2)(c) closes water within 100 yd of "that portion of any bridge on
which public fishing is legally permitted". The National Bridge Inventory gives one point per
bridge, so the map used to draw a 125 yd circle at that point. A long bridge runs far outside that
circle. This script buffers the bridge deck itself.

Input: tools/bridges-2026-10-08/decks.txt, written in the author's Chrome on 8 Oct 2026 for the
2,509 coastal and tidal bridge records the map buffers (confirmed or presumed). For each record the
page looked for a deck in two public-domain sources:
  C  NOAA ENC bridges (encdirect.noaa.gov: enc_harbour layers 87 Bridge_line and 141 Bridge_area,
     enc_approach 91 and 146). A charted bridge within 60 m of the NBI point is taken, then any charted
     bridge within 30 m of one already taken (the spans of one crossing). Harbour-band features are
     preferred where both bands chart the same span. A bridge area is reduced to the long axis of its
     smallest enclosing rectangle, with half its width kept so the buffer is measured from the deck
     edge.
  R  US Census TIGER/Line roads (TIGERweb Transportation layers 2, 6 and 8) over water (TIGERweb
     Areal Hydrography and USGS NHD Area and Waterbody, large scale). The road carrying the bridge is
     the TIGER road within 40 m of the NBI point; its stretches over mapped water that lie within 60
     m of the point, or within 60 m of such a stretch, are the deck (within 200 m for the records the
     first pass marked "far"). Run for every record: the chart often carries only the spans over the
     navigable channel, so a record can have both a C and an R line, and both are buffered.
  W  a second, wider chart search for every record left with no deck by C and R: the charted bridge
     nearest the NBI point, if within 250 m, plus the charted bridges within 30 m of it, chained as in
     C. Many NBI points sit on the approach road, more than 60 m from the charted deck (the US-41
     Caloosahatchee bridge, Crosstown Parkway, Fort Hamer Road). A W match may pick up a neighbouring
     structure; that closes more water, which is the conservative direction.
  A third road pass (the R lines after the W block) covers 40 stretches of mapped water beside a drawn
  deck that the passes above left uncovered, the west end of the Gandy Bridge among them: TIGER roads
  over TIGERweb Areal Hydrography inside each stretch, kept where they chain within 400 m to the
  record's deck or NBI point. A record may therefore have more than one R line; they are merged.
Format, one record per line after the header:
  <bridge index>|<C, R or W>|<deck>/<deck>/...   deck = "lat,lon;dlat,dlon;...:<half width m>"; a record
                                              may have one C line and one R line,
                                              1e-5 degree, first pair absolute
  #X <reason> <index> <index> ...             records with no deck: dry (the TIGER road crosses no
                                              mapped water near the point), noroad (no TIGER road
                                              within 40 m), far (mapped water only more than 60 m
                                              away), skip (no charted bridge; the road search was run
                                              only where the 7 Oct review had found a deck)
  #S <C, R or CR> <index> <index> ...         records whose deck (chart, roads or both) stays within 22 m
                                              of the NBI point, so the circle already covers it
  #F <index> <index>                          ferry crossings found in the 7 Oct review (not decks)

Output fields on each of the 2,509 records in data/bridges.json:
  rv  span | short | none | ferry
  ds  chart | roads | both | wide (where rv is span or short; wide = a W match)
  dk  deck lines, each a flat list [lat, lon, dlat, dlon, ...] in 1e-5 degree (span only)
  sp  buffer rings in the same encoding: the union of the 125 yd circle at the NBI point and a 125 yd
      band from the edge of every deck, so no record covers less water than its circle (span only)
Every input is a United States government work, so the fields carry no licence restriction. Re-running
is safe: the fields are stripped and rebuilt, and records are matched by index and checked by
position.
"""
import json, os, sys
from shapely.geometry import LineString, Point
from shapely.ops import unary_union
from pyproj import Transformer

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'bridges-2026-10-08', 'decks.txt')
OUT = os.path.join(HERE, '..', 'data', 'bridges.json')
BUF_M = 125 * 0.9144          # 100 yd rule, drawn at 125 yd, as in js/app.js
SHORT_M = 22.0                # a deck that stays this close to the NBI point adds nothing to the circle
TOL_M = 5.0                   # simplification tolerance; the ring may sit up to 5 m inside the 125 yd line

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


def dec(s):
    pts, a, o = [], 0, 0
    for k, p in enumerate(s.split(';')):
        x, y = map(int, p.split(','))
        a, o = (x, y) if k == 0 else (a + x, o + y)
        pts.append((a / 1e5, o / 1e5))
    return pts


DECK, NOD, FERRY, SHORT = {}, {}, set(), {}
for raw in open(SRC, encoding='utf-8').read().split('\n'):
    raw = raw.strip()
    if not raw or raw.startswith('#END'):
        continue
    if raw.startswith('#F'):
        FERRY |= {int(t) for t in raw.split()[1:]}
        continue
    if raw.startswith('#S'):
        t = raw.split()
        for k in t[2:]:
            SHORT[int(k)] = t[1]
        continue
    if raw.startswith('#X'):
        t = raw.split()
        for k in t[2:]:
            NOD[int(k)] = t[1]
        continue
    if raw.startswith('#'):
        continue
    i, src, rest = raw.split('|', 2)
    i = int(i)
    if src == '-':
        NOD[i] = rest
        continue
    decks = []
    for part in rest.split('/'):
        line, hw = part.rsplit(':', 1)
        decks.append((dec(line), float(hw)))
    if src == 'W' and (i in DECK or i not in NOD):
        sys.exit('record %d: a wide match must replace a no-deck record' % i)
    if src == 'W':
        del NOD[i]
    if i in DECK:                                  # a record with both a charted deck and a road deck
        DECK[i] = (DECK[i][0] + src, DECK[i][1] + decks)
    else:
        DECK[i] = (src, decks)

B = json.load(open(OUT))
for b in B:
    for f in ('rv', 'ds', 'dk', 'sp'):
        b.pop(f, None)

reviewed = [i for i, b in enumerate(B) if b['st'] != 'excluded' and b.get('iw') in ('coastal', 'tidal')]
if len(reviewed) != 2509:
    sys.exit('expected the 2,509 coastal and tidal records of 8 Oct 2026, found %d; '
             'bridges.json has changed since the decks were pulled' % len(reviewed))
for i in list(DECK) + list(NOD) + list(FERRY) + list(SHORT):
    if i not in reviewed:
        sys.exit('record %d is not a coastal or tidal presumed/confirmed bridge' % i)
missing = [i for i in reviewed if i not in DECK and i not in NOD and i not in FERRY and i not in SHORT]
if missing:
    sys.exit('%d records have no line in decks.txt, e.g. %s' % (len(missing), missing[:5]))

npts = 0
for i in reviewed:
    b = B[i]
    if i in FERRY:
        b['rv'] = 'ferry'
        continue
    if i in SHORT:
        b['rv'] = 'short'
        b['ds'] = {'C': 'chart', 'R': 'roads'}.get(SHORT[i], 'both')
        continue
    if i not in DECK:
        b['rv'] = 'none'
        continue
    src, decks = DECK[i]
    c = Point(fwd(b['lon'], b['lat']))
    gl = [(LineString([fwd(lo, la) for la, lo in d]) if len(d) > 1 else Point(fwd(d[0][1], d[0][0])), hw)
          for d, hw in decks]
    near = min(g.distance(c) for g, hw in gl)
    lim = {'R': 200, 'W': 250}.get(src, 60)    # the relaxed road search reached 200 m, the wide chart search 250 m
    if near > lim + max(hw for g, hw in gl):
        sys.exit('record %d (%s): deck is %.0f m from the NBI point' % (i, b['n'], near))
    hc, hr = 'C' in src, 'R' in src
    b['ds'] = 'wide' if src == 'W' else 'both' if hc and hr else 'chart' if hc else 'roads'
    reach = max(c.distance(Point(p)) + hw for g, hw in gl for p in g.coords)
    if reach <= SHORT_M or not any(len(d) > 1 for d, hw in decks):   # a lone point is not a deck to trace
        b['rv'] = 'short'
        continue
    g = unary_union([c.buffer(BUF_M, quad_segs=16)] +
                    [l.buffer(BUF_M + hw, quad_segs=8) for l, hw in gl]).simplify(TOL_M)
    polys = [g] if g.geom_type == 'Polygon' else list(g.geoms)
    rings = []
    for p in polys:
        ring = [inv(x, y)[::-1] for x, y in p.exterior.coords]
        rings.append(enc(ring)); npts += len(ring)
    b['rv'] = 'span'
    b['dk'] = [enc(d) for d, hw in decks if len(d) > 1]
    b['sp'] = rings

json.dump(B, open(OUT, 'w'), separators=(',', ':'))
import collections
print(collections.Counter(b.get('rv') for b in B), collections.Counter(b.get('ds') for b in B if b.get('rv') == 'span'),
      npts, 'ring points', os.path.getsize(OUT), 'bytes')
