# -*- coding: utf-8 -*-
"""Recompute the Palm Beach refuge fields of data/sites.json against the NOAA ENC coastline.

sites.json was built by tools/fetch-statewide.py, which set two fields against the OpenStreetMap coastline:

  ref   1 or 2 when the site lies inside Refuge Area No. 1 or 2 (PBC Code App. G §§ 13-55, 13-56):
        between the refuge latitudes and at least 750 yd east of the shoreline.
  edge  true when the site lies within 0.05 nm (about 93 m) of a refuge's north or south latitude. The
        test uses latitude only; the shoreline matters only in that edge is computed where the
        shoreline file has coverage (26.66 to 26.90 N here, as before).

This script applies the same two tests with the shoreline that tools/build-zones-palmbeach.py now uses
(tools/geometry/2026-10-07/shoreline-used-palmbeach.json, NOAA ENC, CC0) and the same inner edge the
drawn refuges use (725 yd: 750 yd less a 25 yd margin for a chart line that sits seaward of mean high
water). Every other field and the file's formatting are left alone. Run it after the Palm Beach builder.

    python3 tools/recompute-sites-ref-2026-10-07.py
"""
import json
import math
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SITES = os.path.join(ROOT, "data", "sites.json")
SHORE = os.path.join(ROOT, "tools", "geometry", "2026-10-07", "shoreline-used-palmbeach.json")

YD = 3 / 6076.115          # nautical miles per yard, as in fetch-statewide.py
REFUGE_YD = 725


def dms(d, m, s):
    return d + m / 60 + s / 3600


REF = {1: (dms(26, 44, 51), dms(26, 45, 48)), 2: (dms(26, 46, 38), dms(26, 47, 38))}
shore = json.load(open(SHORE))


def shore_lon(lat):
    """Identical to fetch-statewide.py: None outside the shoreline's latitude range."""
    if lat <= shore[0][0] or lat >= shore[-1][0]:
        return None
    lo, hi = 0, len(shore) - 1
    while hi - lo > 1:
        mm = (lo + hi) // 2
        if shore[mm][0] <= lat:
            lo = mm
        else:
            hi = mm
    a, b = shore[lo], shore[hi]
    t = 0 if b[0] == a[0] else (lat - a[0]) / (b[0] - a[0])
    return a[1] + t * (b[1] - a[1])


raw = open(SITES, encoding="utf-8").read()
sites = json.loads(raw)
# The file is written compact and without ASCII escapes; check that re-serialising is lossless first.
assert json.dumps(sites, ensure_ascii=False, separators=(",", ":")) == raw.rstrip("\n"), "unexpected format"

changed_ref, changed_edge = [], []
for s in sites:
    ref, edge = None, False
    sl = shore_lon(s["lat"])
    if sl is not None and 26.5 < s["lat"] < 27.0:
        off = (s["lon"] - sl) / (1 / (60 * math.cos(math.radians(s["lat"]))))
        for n, (a, b) in REF.items():
            if a <= s["lat"] <= b and off >= REFUGE_YD * YD:
                ref = n
        edge = min(abs(s["lat"] - e) * 60 for a, b in REF.values() for e in (a, b)) <= 0.05
    if ref != s.get("ref"):
        changed_ref.append((s["n"], s["lat"], s["lon"], s.get("ref"), ref))
    if edge != s.get("edge"):
        changed_edge.append((s["n"], s["lat"], s["lon"], s.get("edge"), edge))
    s["ref"], s["edge"] = ref, edge

with open(SITES, "w", encoding="utf-8") as f:
    f.write(json.dumps(sites, ensure_ascii=False, separators=(",", ":")) + ("\n" if raw.endswith("\n") else ""))

print("sites:", len(sites))
print("ref changed:", len(changed_ref))
for c in changed_ref:
    print("  %-40s %.5f %.5f  %s -> %s" % c)
print("edge changed:", len(changed_edge))
for c in changed_edge:
    print("  %-40s %.5f %.5f  %s -> %s" % c)
print("ref now: 1 =", sum(1 for s in sites if s["ref"] == 1), " 2 =", sum(1 for s in sites if s["ref"] == 2),
      " edge true =", sum(1 for s in sites if s["edge"]))
