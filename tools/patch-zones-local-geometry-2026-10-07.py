# -*- coding: utf-8 -*-
"""Geometry pass of 7 Oct 2026 for data/zones-local.json: public-domain sources replace OpenStreetMap and
Esri World Imagery. Run last, after patch-zones-local-2026-09-30.py, -2026-10-06.py and -2026-10-07.py.

Edits by zone id, and asserts the old coordinates before changing anything (a second run finds the new
coordinates and does nothing):

  mon26  The 122 OpenStreetMap canal centrelines are replaced by 508 USGS NHD high-resolution centrelines:
         CanalDitch flowlines plus the artificial paths that run through NHD CanalDitch areas
         (tools/geometry/2026-10-07/nhd-lowerkeys-canals.json, made by tools/extract-enc-2026-10-07.py).
         Also rewrites the OpenStreetMap sentence in the flag set by patch-zones-local-2026-10-07.py.
  ti58   127th Avenue: the street line is the US Census TIGER/Line road; both termini were read on its
         straight extension from USGS NAIP imagery (west at the Gulf waterline, east at the bay waterline).
         The John's Pass corridor was re-read against NAIP: its north-west edge between the Gulf tip of
         Madeira Beach and the bridge is moved onto the Madeira Beach shoreline, because the August
         outline left a strip of the pass outside the zone. The other corridor vertices are unchanged.
  3sis   Re-read from NAIP: the August centre sits on the pond in the middle of the Three Sisters Springs
         property; the springs are the clear-water pool 264 m south of it, with a run to the canal.
  spb94  Marker centre moved from the OpenStreetMap 75th Avenue / Blind Pass Road intersection to the
         TIGER/Line intersection (78 m south-west). It stays a marker, flagged as not the closure.

Screenshots of each NAIP reading are in raw/2026-10-07/naip/ (not in the repository).
"""
import io
import json
import math
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = os.path.join(ROOT, "data", "zones-local.json")
NHD = os.path.join(ROOT, "tools", "geometry", "2026-10-07", "nhd-lowerkeys-canals.json")
R = 5
M_PER_DEG = 111320.0


def circ(lat, lon, r_m, a0=0, a1=360, n=48):
    """Same construction as tools/build-zones-local.py."""
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        dlat = (r_m * math.cos(a)) / M_PER_DEG
        dlon = (r_m * math.sin(a)) / (M_PER_DEG * math.cos(math.radians(lat)))
        pts.append([round(lat + dlat, R), round(lon + dlon, R)])
    return pts


def sector(lat, lon, r_m, a0, a1):
    return [[round(lat, R), round(lon, R)]] + circ(lat, lon, r_m, a0, a1) + [[round(lat, R), round(lon, R)]]


def fingerprint(rings):
    return round(sum(a + b for r in rings for a, b in r), 5)


d = json.load(io.open(P, encoding="utf-8"))
Z = {z["id"]: z for z in d["zones"]}
done = []

# ------------------------------------------------------------------ mon26
z = Z["mon26"]
canals = json.load(io.open(NHD, encoding="utf-8"))["lines"]
new_lines = [c["pts"] for c in canals]
if z["line"] != new_lines:
    assert len(z["line"]) == 122 and fingerprint(z["line"]) == -17591.53966, "mon26: unexpected old geometry"
    z["line"] = new_lines
    done.append("mon26 geometry")
z["src"] = ("Canal centrelines from the USGS National Hydrography Dataset, high resolution (public domain), pulled "
            "7 Oct 2026: every CanalDitch flowline, and every artificial-path flowline that runs through an NHD "
            "CanalDitch area. Lower Keys only (24.53 to 24.80 N, 81.85 to 80.90 W); 508 lines, about 81 km, of which "
            "9 lines (2 km) are inside the City of Marathon. None is inside Key West.")
OLD_FLAG = ("OpenStreetMap canal coverage in the Keys is good but not complete, and this pull covers the LOWER Keys "
            "only.")
NEW_FLAG = ("NHD canal coverage in the Keys is not complete: it maps the residential canal subdivisions, but some "
            "waterways the earlier OpenStreetMap layer showed as canals are not NHD canals, about 10 km in all, "
            "mostly around the Key West island group. This pull covers the LOWER Keys only.")
if OLD_FLAG in z["flag"]:
    z["flag"] = z["flag"].replace(OLD_FLAG, NEW_FLAG)
    done.append("mon26 flag")
assert "OpenStreetMap canal coverage" not in z["flag"]

# ------------------------------------------------------------------ ti58
z = Z["ti58"]
D = 1500 * 0.3048
WEST = (27.77981, -82.78323)     # NAIP: Gulf waterline on the straight extension of TIGER 127th Ave
EAST = (27.78138, -82.78066)     # NAIP: Boca Ciega Bay waterline on the extension of TIGER 127th Ave E
JP_OLD = [[27.78016, -82.78741], [27.78126, -82.78598], [27.78236, -82.78439], [27.78349, -82.78288],
          [27.78465, -82.78157], [27.78603, -82.7803], [27.78739, -82.77921], [27.78605, -82.77705],
          [27.78461, -82.7782], [27.78309, -82.77961], [27.78177, -82.7811], [27.78054, -82.78273],
          [27.77946, -82.7843], [27.7784, -82.78567], [27.78016, -82.78741]]
# North-west edge from the Gulf tip of Madeira Beach to the bridge abutment, read from NAIP at zoom 18.
NW_EDGE = [[27.78289, -82.78436], [27.78305, -82.78393], [27.78322, -82.7836], [27.78343, -82.78335],
           [27.78365, -82.78296]]
JP_NEW = JP_OLD[:2] + NW_EDGE + JP_OLD[4:]
new_r = [sector(WEST[0], WEST[1], D, 180, 360), sector(EAST[0], EAST[1], D, 0, 180), JP_NEW]
if z["r"] != new_r:
    assert [len(r) for r in z["r"]] == [51, 51, 15] and fingerprint(z["r"]) == -6435.05797, "ti58: unexpected old geometry"
    assert z["r"][0][0] == [27.78047, -82.78211] and z["r"][1][0] == [27.78129, -82.78082] and z["r"][2] == JP_OLD
    z["r"] = new_r
    done.append("ti58 geometry")
z["src"] = ("127th Avenue is the US Census TIGER/Line road (TIGERweb Transportation). Both termini were read on the "
            "street's straight extension from USGS NAIP imagery (public domain, 2024 refresh) on 7 Oct 2026: west "
            "at the Gulf waterline, 27.77981 N 82.78323 W; east at the Boca Ciega Bay waterline, 27.78138 N "
            "82.78066 W. 1,500 ft = 457.2 m, drawn as half-discs. John’s Pass is a corridor hand-digitised in "
            "August 2026 and re-read against NAIP on 7 Oct 2026, when its north-west edge between the Gulf tip of "
            "Madeira Beach and the bridge was moved onto the Madeira Beach shoreline.")
OLD_TI = ("Also: OpenStreetMap’s 127th Avenue does not reach the Gulf beach, so the western terminus used here is "
          "the end of the mapped street, not the mean high water mark. Both need a plat or a site visit.")
NEW_TI = ("Also: the termini are read from imagery. The west centre is the waterline on the day of the photograph, "
          "which at low tide lies seaward of mean high water (that errs toward closing more water); the east centre "
          "is where the street's line meets the bay. Both need a plat or a site visit.")
if OLD_TI in z["flag"]:
    z["flag"] = z["flag"].replace(OLD_TI, NEW_TI)
    done.append("ti58 flag")
assert "OpenStreetMap" not in z["flag"] and "OpenStreetMap" not in z["src"]

# ------------------------------------------------------------------ 3sis
z = Z["3sis"]
C = (28.88861, -82.58916)        # NAIP: centre of the Three Sisters spring pool
new_r = [circ(C[0], C[1], 200)]
if z["r"] != new_r:
    assert len(z["r"]) == 1 and len(z["r"][0]) == 49 and fingerprint(z["r"]) == -2631.21637, "3sis: unexpected old geometry"
    z["r"] = new_r
    done.append("3sis geometry")
z["src"] = ("200 m circle centred on the Three Sisters Springs pool at 28.88861 N, 82.58916 W, read from USGS NAIP "
            "imagery (public domain) on 7 Oct 2026: the clear-water pool with three vents, ringed by the boardwalk, "
            "whose run enters the canal to the south.")
z["flag"] = ("CORRECTED 7 Oct 2026: the August centre (28.89098 N, 82.58931 W) sat on the pond in the middle of the "
             "Three Sisters Springs property, not on the springs, which lie 264 m south of it; the circle now covers "
             "the spring pool, its run and the canal mouth, and only the south edge of the pond. APPROXIMATE CIRCLE. "
             "USFWS publishes no GIS layer for the Kings Bay Manatee Refuge or the Three Sisters area; the boundary "
             "exists only as Federal Register text (77 FR 15617). The wider refuge is \"all waters of Kings Bay, "
             "including all tributaries and adjoining waterbodies, upstream of the confluence of Kings Bay and "
             "Crystal River\", which is far larger than the circle drawn.")

# ------------------------------------------------------------------ spb94
z = Z["spb94"]
B = (27.742808, -82.750458)      # TIGER/Line: 75th Ave meets Blind Pass Rd
new_r = [circ(B[0], B[1], 150)]
if z["r"] != new_r:
    assert len(z["r"]) == 1 and fingerprint(z["r"]) == -2695.3219, "spb94: unexpected old geometry"
    z["r"] = new_r
    done.append("spb94 geometry")
z["src"] = ("Marker only: the 75th Avenue / Blind Pass Road intersection, 27.74281 N 82.75046 W, from US Census "
            "TIGER/Line roads (TIGERweb Transportation, 7 Oct 2026).")

io.open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
print("zones-local.json:", ", ".join(done) if done else "already applied")
