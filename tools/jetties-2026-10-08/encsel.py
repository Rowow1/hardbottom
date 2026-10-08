"""Read enc-jetties.txt and select the NOAA ENC shoreline-construction features used for each jetty.

enc-jetties.txt was pulled in the author's Chrome on 8 Oct 2026 from encdirect.noaa.gov (enc_harbour
layers 85 and 138, enc_approach 89 and 143, enc_berthing 38 and 62), within a box 0.002 degree
around each structure of the 7 Oct review whose geometry had come from OpenStreetMap. For each
structure the page measured, per scale band, how much of each charted feature lay within 25 m of the
reviewed line (nf, per cent; nl, metres; tot, metres) and kept the largest-scale band that covered
the structure best. Coordinates: delta-encoded [lat, lon] in 1e-5 degree, simplified at 1.5 m.
Transfer was checked with a 32-bit rolling hash (2476718344).

A feature is used when most of it lies along the structure (nf >= 50), or when at least 60 m of it
does and it is not a seawall (nf >= 30, nl >= 60): long seawalls that merely touch a jetty root are
left out. Features charted as always under water (WATLEV 3) or floating (7) are kept in the file but
carry no buffer, because the rule reaches only the unsubmerged portion.
"""
import os
from shapely.geometry import LineString, Point
from pyproj import Transformer
HERE = os.path.dirname(os.path.abspath(__file__))
fwd = Transformer.from_crs('EPSG:4326', 'EPSG:3086', always_xy=True).transform
WATLEV = {'1': 'partly submerged at high water', '2': 'always dry', '3': 'always under water',
          '4': 'covers and uncovers', '5': 'awash', '7': 'floating', '': 'water level not charted'}

def dec5(s):
    out = []
    for part in s.split('/'):
        a = o = 0; pts = []
        for q in part.split(';'):
            x, y = map(int, q.split(',')); a += x; o += y; pts.append([round(a / 1e5, 5), round(o / 1e5, 5)])
        out.append(pts)
    return out

SEL = {}
for ln in open(os.path.join(HERE, 'enc-jetties.txt'), encoding='utf-8'):
    p = ln.rstrip('\n').split('|')
    if len(p) != 9:
        continue
    f = dict(band=p[1][0], layer=int(p[1][1:]), cat=p[2].strip() or 'not categorised', wat=p[3],
             cell=p[4], nf=int(p[5]), nl=int(p[6]), tot=int(p[7]), parts=dec5(p[8]))
    if f['nf'] >= 50 or (f['nf'] >= 30 and f['nl'] >= 60 and f['cat'] != 'seawall'):
        SEL.setdefault(p[0], []).append(f)

def features(key):
    return SEL.get(key, [])

def geoms_m(key, buffered_only=False):
    out = []
    for f in features(key):
        if buffered_only and f['wat'] in ('3', '7'):
            continue
        for part in f['parts']:
            m = [fwd(lo, la) for la, lo in part]
            out.append(LineString(m) if len(m) > 1 else Point(m[0]))
    return out
