# -*- coding: utf-8 -*-
"""Turn the 7 Oct 2026 raw pulls into the small public-domain geometry files the builders read.

Inputs (raw/2026-10-07/, not in the repository; listed with endpoints, layer ids and queries in
raw/2026-10-07/manifest.json):
  enc-coalne-eastfacing.txt         NOAA ENC Direct, harbour band, Coastline_line (COALNE), the vertices
                                    that face the open Atlantic (no other coastline segment east of them)
  enc-lakeworth-inlet.txt           harbour band SLCONS lines and areas, COALNE, BRIDGE areas at Lake Worth Inlet
  enc-inlets-jupiter-boynton.txt    the charted "Jupiter Inlet" SEAARE polygon; SLCONS, BRIDGE and LNDARE
                                    (clipped to a box) at South Lake Worth (Boynton) Inlet
  tiger-hollywood-hallandale.txt    TIGERweb incorporated places, Hollywood and Hallandale Beach (clipped)
  nhd-lowerkeys-canal-centrelines.txt  USGS NHD high resolution: CanalDitch flowlines (ftype 336) and the
                                    artificial paths (ftype 558) that run through NHD CanalDitch areas

Line format: fields separated by "|", the last two being the vertex count and the vertices as
delta-encoded integers "dlat,dlon;dlat,dlon;..." (1e-6 degrees). The NHD file has no count field and
uses 1e-5 degrees.

Outputs:
  tools/geometry/2026-10-07/enc-palmbeach.json   shoreline, jetties, groin, bridge, Peanut Island east shore
  tools/geometry/2026-10-07/proposal-inputs.json Hollywood and inlet inputs for the new-rule proposals
  tools/geometry/2026-10-07/nhd-lowerkeys-canals.json  canal centrelines for zones-local.json mon26

All three are United States government works (NOAA ENC is CC0; NHD and TIGER are public domain).
"""
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.environ.get("RAW_2026_10_07", os.path.join(ROOT, "raw", "2026-10-07"))
OUT = os.path.join(ROOT, "tools", "geometry", "2026-10-07")


def dec(s, scale=1e6):
    y = x = 0
    out = []
    for d in s.split(";"):
        a, b = d.split(",")
        y += int(a)
        x += int(b)
        out.append([round(y / scale, 6), round(x / scale, 6)])
    return out


def rows(name, scale=1e6):
    for line in open(os.path.join(RAW, name), encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = line.split("|")
        pts = dec(p[-1], scale)
        assert len(pts) == int(p[-2]), (name, p[:4])
        yield p[:-2], pts


def r5(pts):
    return [[round(a, 6), round(b, 6)] for a, b in pts]


# ---------------------------------------------------------------- Palm Beach shoreline
sec = None
pbc, hwd = [], []
for line in open(os.path.join(RAW, "enc-coalne-eastfacing.txt"), encoding="utf-8"):
    line = line.strip()
    if line.startswith("#"):
        sec = line
        continue
    p = line.split("|")
    pts = dec(p[2])
    assert len(pts) == int(p[1])
    (pbc if "pbc" in sec else hwd).append({"cell": p[0], "pts": pts})

# The Palm Beach builder works on 26.66 to 26.90 N, the same window the OpenStreetMap extraction covered.
shore = sorted({(a, b) for r in pbc for a, b in r["pts"] if 26.66 <= a <= 26.90})
shore = [list(p) for p in shore]
# One latitude, one longitude: the builder interpolates longitude by latitude.
lats = [p[0] for p in shore]
assert len(lats) == len(set(lats)), "duplicate latitude in the Palm Beach window"

feat = {}
for head, pts in rows("enc-lakeworth-inlet.txt"):
    key = head[0] if head[0] != "BHB" else "BHB" + str(len(pts))
    feat[key] = {"layer": head[1], "cat": head[3], "watlev": head[4], "cell": head[6] if len(head) > 6 else "",
                 "pts": pts}

peanut = [r["pts"] for r in pbc if r["cell"] == "US5PABBA.000" and len(r["pts"]) == 17
          and abs(r["pts"][0][1] + 80.044188) < 1e-6]
peanut_s = [r["pts"] for r in pbc if r["cell"] == "US5PABBA.000" and len(r["pts"]) == 2
            and abs(r["pts"][0][1] + 80.045234) < 1e-6]
assert len(peanut) == 1 and len(peanut_s) == 1

enc_pb = {
    "meta": {
        "source": "NOAA ENC Direct to GIS, encdirect.noaa.gov/arcgis/rest/services/encdirect/enc_harbour/MapServer "
                  "(harbour usage band, the largest scale charted along this coast; the berthing band has no "
                  "features here). Pulled 7 Oct 2026. See raw/2026-10-07/manifest.json.",
        "licence": "NOAA ENC data, CC0 1.0 (US government work).",
        "coords": "[lat, lon] WGS84, 6 dp",
        "cells": sorted({r["cell"] for r in pbc}),
    },
    "shoreline": {
        "note": "Coastline_line (COALNE, layer 84) vertices with no other coastline segment east of them, "
                "26.66 to 26.90 N, sorted by latitude. Cells US5FL6AN, US5PABBA, US5PABCA, US5FL6DN.",
        "pts": shore,
    },
    "north_jetty": {"note": "Shoreline_Construction_line (layer 85), CATSLC rip rap, WATLEV 2 (always dry), cell "
                            "US5PABBA. Runs from the north jetty tip west along the north side of the inlet.",
                    "pts": feat["LWI1"]["pts"]},
    "north_jetty_seawall": {"note": "SLCONS line, seawall, WATLEV 2, at the north jetty head.", "pts": feat["LWI0"]["pts"]},
    "south_jetty": {"note": "SLCONS line (layer 85), CATSLC rip rap, WATLEV 2, cell US5PABBA. Runs from the "
                            "shore at the jetty root east to the exposed tip, then back west along the south side "
                            "of the inlet.", "pts": feat["LWI3"]["pts"]},
    "south_jetty_submerged": {"note": "SLCONS area (layer 138), CATSLC pier, WATLEV 3 (always under water): the "
                                      "submerged seaward extension of the south jetty. Not 'unsubmerged', so the "
                                      "jetty buffer does not attach to it.", "pts": feat["LWI18"]["pts"]},
    "groin": {"note": "SLCONS line, CATSLC groin, WATLEV 4 (covers and uncovers).", "pts": feat["LWI12"]["pts"]},
    "blue_heron_bridge": {"note": "Bridge_area (layer 141), CATBRG fixed bridge, cell US5PABCA: the western span "
                                  "(vertical clearance 19.8 m) and the eastern span. The bridge over Phil Foster "
                                  "Park island is not charted (it is over land).",
                          "areas": [feat["BHB75"]["pts"], feat["BHB10"]["pts"]]},
    "peanut_east_shore": {"note": "COALNE vertices on the east shore of Peanut Island facing the inlet throat, "
                                  "cell US5PABBA, plus the two east-facing vertices at its south-west corner.",
                          "pts": peanut[0], "sw_corner": peanut_s[0]},
}

# ---------------------------------------------------------------- proposals
prop = {"meta": {"note": "Inputs for .staging/new-zones-geometry.json. ENC is CC0; TIGER is public domain.",
                 "pulled": "2026-10-07"}}
prop["hollywood_shore_runs"] = [{"cell": r["cell"], "pts": r["pts"]} for r in hwd]
for head, pts in rows("tiger-hollywood-hallandale.txt"):
    prop.setdefault("tiger", []).append({"name": head[1], "geoid": head[2], "ring": pts,
                                         "note": "TIGERweb Places_CouSub_ConCity_SubMCD layer 4, clipped in the "
                                                 "browser to lon -80.135 to -80.095, lat 25.965 to 26.075"})
for head, pts in rows("enc-inlets-jupiter-boynton.txt"):
    key = "jupiter" if head[0] == "JUP" else "boynton"
    prop.setdefault(key, []).append({"layer": head[1], "cat": head[2], "cell": head[3], "pts": pts})

# ---------------------------------------------------------------- NHD canals
canals = []
for line in open(os.path.join(RAW, "nhd-lowerkeys-canal-centrelines.txt"), encoding="utf-8"):
    if not line.strip():
        continue
    ftype, place, enc = line.strip().split("|")   # this file carries no vertex count
    canals.append({"ftype": int(ftype), "place": "Marathon" if place == "M" else "unincorporated",
                   "pts": [[round(a, 5), round(b, 5)] for a, b in dec(enc, 1e5)]})
nhd = {"meta": {"source": "USGS National Hydrography Dataset, high resolution, hydro.nationalmap.gov/arcgis/rest/"
                          "services/nhd/MapServer layer 6 (Flowline, large scale) and layer 9 (Area, large scale). "
                          "Pulled 7 Oct 2026.",
                "selection": "Box 24.53 to 24.80 N, 81.85 to 80.90 W. Kept: every ftype 336 (CanalDitch) flowline, "
                             "and every ftype 558 (ArtificialPath) flowline whose middle vertex lies inside an NHD "
                             "Area feature with FTYPE 336 (CanalDitch). Simplified in the browser with "
                             "Douglas-Peucker at 0.00004 deg, the tolerance the August OpenStreetMap build used.",
                "place": "Point-in-polygon of each line's middle vertex against TIGERweb incorporated places "
                         "(Key West, Marathon, Layton, Key Colony Beach): no line falls in Key West.",
                "licence": "Public domain (US government work)."},
       "lines": canals}

os.makedirs(OUT, exist_ok=True)
for name, obj in (("enc-palmbeach.json", enc_pb), ("proposal-inputs.json", prop), ("nhd-lowerkeys-canals.json", nhd)):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    print(name, os.path.getsize(os.path.join(OUT, name)), "bytes")
print("shoreline pts", len(shore), "canal lines", len(canals))
