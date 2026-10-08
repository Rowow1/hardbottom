# -*- coding: utf-8 -*-
"""Build the structure, habitat and reference layers added on 30 Sep 2026 from the dated raw pulls.

Inputs: raw/2026-09-30/*.json (see raw/2026-09-30/manifest.json for every service URL, layer id,
query and record count) and the research outputs under tools/src-2026-09-30/.
Outputs (all [lat, lon], 5 dp):
  data/enc.json            NOAA ENC point features: wrecks, obstructions, fish havens, rocks   (replaces 22 Aug file)
  data/enc-areas.json      NOAA ENC fish haven and wreck areas
  data/seabed.json         NOAA ENC seabed nature-of-surface (SBDARE) points and areas
  data/contours.json       NOAA ENC depth contours 12, 18, 30, 60, 100, 120 ft               (replaces 30 ft only)
  data/hardbottom-sw.json  FWC/FWRI hardbottom outside the Unified Reef Map tract, WFS pavement, worm reef
  data/buoys.json          FKNMS mooring and boundary buoys (2025 public layer)
  data/stations.json       NOAA CO-OPS tide and current prediction stations, NDBC stations
  data/enc-restricted.json NOAA ENC restricted and military practice areas (reference only)
  data/mpa.json            NOAA MPA Inventory sites in Florida (reference only)
  data/spots.json          curated named dive spots with media links
  data/species.json        species rules for the "can I spear this?" panel
"""
import io
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
RAW = os.environ.get("RAW", os.path.join(ROOT, "raw", "2026-09-30"))
SRC = os.path.join(HERE, "src-2026-09-30")
FT = 0.3048


def rj(p):
    return json.load(io.open(p, encoding="utf-8"))


def wj(name, obj):
    p = os.path.join(ROOT, "data", name)
    io.open(p, "w", encoding="utf-8").write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
    print("%-22s %8.0f KB" % (name, os.path.getsize(p) / 1024))


def dp(pts, eps):
    """Douglas-Peucker on [lat, lon] lists, eps in degrees."""
    if len(pts) < 5:
        return pts
    import math
    def dist(p, a, b):
        if a == b:
            return math.hypot(p[0] - a[0], p[1] - a[1])
        t = ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
        t = max(0, min(1, t))
        return math.hypot(p[0] - (a[0] + t * (b[0] - a[0])), p[1] - (a[1] + t * (b[1] - a[1])))
    keep = [0, len(pts) - 1]
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        best, bi = 0, None
        for k in range(i + 1, j):
            d = dist(pts[k], pts[i], pts[j])
            if d > best:
                best, bi = d, k
        if best > eps and bi is not None:
            keep.append(bi)
            stack += [(i, bi), (bi, j)]
    return [pts[k] for k in sorted(set(keep))]


def simp(rings, eps):
    out = []
    for r in rings:
        s = dp(r, eps)
        if len(s) >= 4:
            out.append(s)
    return out


BAND = {"C": 0, "A": 1, "H": 2}

# ------------------------------------------------------------------ ENC points
rk = rj(os.path.join(RAW, "enc-rocks.json"))
enc = []
for w in rk["wrecks"]:
    enc.append({"k": "wreck", "lat": w["g"][0], "lon": w["g"][1], "n": w.get("OBJNAM") or "",
                "cat": w.get("CATWRK") or "", "d": w.get("VALSOU"), "wl": w.get("WATLEV"),
                "inf": w.get("INFORM") or ""})
for o in rk["obstructions"]:
    fh = (o.get("CATOBS") or "") == "fish haven"
    enc.append({"k": "fishhaven" if fh else "obstruction", "lat": o["g"][0], "lon": o["g"][1],
                "n": o.get("OBJNAM") or "", "cat": o.get("CATOBS") or "", "d": o.get("VALSOU"),
                "wl": o.get("WATLEV"), "inf": o.get("INFORM") or ""})
for r in rk["rocks"]:
    enc.append({"k": "rock", "lat": r["g"][0], "lon": r["g"][1], "n": r.get("OBJNAM") or "",
                "cat": "underwater or awash rock", "d": r.get("VALSOU"), "wl": r.get("WATLEV"),
                "inf": r.get("INFORM") or ""})
for e in enc:
    for k in list(e):
        if e[k] in ("", None):
            del e[k]
print(Counter(e["k"] for e in enc))
wj("enc.json", enc)

areas = []
for o in rk["obstruction_areas"]:
    if (o.get("CATOBS") or "") == "fish haven":
        areas.append({"k": "fishhaven", "n": o.get("OBJNAM") or "", "d": o.get("VALSOU"),
                      "inf": o.get("INFORM") or "", "r": simp(o["g"], 0.00005)})
for w in rk["wreck_areas"]:
    areas.append({"k": "wreckarea", "n": w.get("OBJNAM") or "", "cat": w.get("CATWRK") or "",
                  "inf": w.get("INFORM") or "", "r": simp(w["g"], 0.00005)})
areas = [a for a in areas if a["r"]]
wj("enc-areas.json", areas)

# ------------------------------------------------------------------ seabed
sb = rj(os.path.join(RAW, "enc-seabed.json"))
classes = []
ci = {}


def cidx(s):
    s = (s or "unknown").strip()
    if s not in ci:
        ci[s] = len(classes)
        classes.append(s)
    return ci[s]


pts = [[p["g"][0], p["g"][1], cidx(p.get("NATSUR"))] for p in sb["points"]]
sareas = [{"c": cidx(a.get("NATSUR")), "r": simp(a["g"], 0.00005)} for a in sb["areas"]]
wj("seabed.json", {"source": "NOAA ENC Direct SBDARE (nature of surface), coastal/approach/harbour bands, "
                             "pulled 30 Sep 2026. CC0. Not for navigation.",
                   "classes": classes, "pts": pts, "areas": [a for a in sareas if a["r"]]})

# ------------------------------------------------------------------ contours
ct = rj(os.path.join(RAW, "enc-contours.json"))
lines = []
for c in ct["contours"]:
    ft = round(c["VALDCO"] / FT)
    lines.append({"ft": ft, "p": [dp(path, 0.00005) for path in c["g"]]})
print(Counter(l["ft"] for l in lines))
wj("contours.json", lines)

# ------------------------------------------------------------------ hardbottom outside the URM tract
hb = rj(os.path.join(RAW, "fwc-hardbottom.json"))
out = []
for p in hb["statewide"]:
    out.append({"c": p.get("DESCRIPT") or "Hardbottom", "s": p.get("METADATA") or "", "y": p.get("SOURCEDATE") or "",
                "r": simp(p["g"], 0.00003)})
for p in hb["wfs"]:
    out.append({"c": "Pavement (West Florida Shelf)", "s": "West Florida Shelf Benthic Habitats",
                "b": p.get("ClassLv2") or "", "y": p.get("ImageDate") or "", "r": simp(p["g"], 0.00003)})
for p in hb["worm"]:
    out.append({"c": "Worm reef", "s": "Worm Reef Habitats, Florida east coast", "r": simp(p["g"], 0.00003)})
out = [o for o in out if o["r"]]
print(Counter(o["c"] for o in out))
wj("hardbottom-sw.json", out)

# ------------------------------------------------------------------ FKNMS buoys
bu = rj(os.path.join(RAW, "fknms-buoys.json"))
buoys = [{"n": b.get("Location") or "", "no": b.get("Buoy_Number") or "", "t": b.get("BuoyType") or "",
          "d": b.get("Depth__ft_"), "reg": b.get("FKNMSRegion") or "", "res": b.get("Resource_Shipwreck_") or "",
          "lat": b["g"][0], "lon": b["g"][1]} for b in bu["buoys"] if b.get("g")]
print(Counter(b["t"] for b in buoys).most_common(8))
wj("buoys.json", buoys)

# ------------------------------------------------------------------ stations
st = rj(os.path.join(RAW, "stations.json"))
S = []
for s in st["tide_prediction_stations"]:
    S.append({"k": "tide", "id": s["id"], "n": s["name"], "st": s.get("state") or "", "ref": s.get("type") == "R",
              "lat": s["g"][0], "lon": s["g"][1]})
seen = set()
for s in st["current_prediction_stations"]:
    if s["id"] in seen:
        continue
    seen.add(s["id"])
    S.append({"k": "current", "id": s["id"], "bin": s.get("bin"), "n": s["name"], "lat": s["g"][0], "lon": s["g"][1]})
for s in st["ndbc_active"]:
    S.append({"k": "buoy", "id": s["id"], "n": s["name"], "o": s.get("owner") or "", "t": s.get("type") or "",
              "lat": s["g"][0], "lon": s["g"][1]})
print(Counter(s["k"] for s in S))
wj("stations.json", S)

# ------------------------------------------------------------------ ENC restricted areas (reference)
rs = rj(os.path.join(RAW, "enc-restricted.json"))
best = {}
keep = []
for kind, arr in (("restricted", rs["restricted"]), ("military", rs["military"])):
    for a in arr:
        nm = a.get("OBJNAM") or ""
        key = (kind, nm, a.get("CATREA") or "", a.get("INFORM") or "")
        if nm:
            if key in best and BAND[best[key]["band"]] >= BAND[a["band"]]:
                continue
            best[key] = dict(a, _k=kind)
        else:
            if a["band"] == "C" or a["band"] == "A":
                keep.append(dict(a, _k=kind))
recs = list(best.values()) + keep
R = []
for a in recs:
    R.append({"k": a["_k"], "n": a.get("OBJNAM") or "", "cat": a.get("CATREA") or "",
              "inf": a.get("INFORM") or "", "cell": a.get("DSNM") or "", "r": simp(a["g"], 0.0001)})
R = [r for r in R if r["r"]]
print("restricted", len(R), Counter(r["cat"] for r in R).most_common(6))
wj("enc-restricted.json", R)

# ------------------------------------------------------------------ MPA inventory (reference)
mp = rj(os.path.join(RAW, "mpa-inventory-fl.json"))
M = []
for s in mp["sites"]:
    rings = simp(s.get("g") or [], 0.0004)
    if not rings:
        continue
    M.append({"id": s.get("Site_ID"), "n": s.get("Site_Name"), "gov": s.get("Gov_Level"), "st": s.get("State"),
              "lvl": s.get("Prot_Lvl"), "ag": s.get("Mgmt_Agen"), "fish": s.get("Fish_Rstr"),
              "iucn": s.get("IUCNcat"), "yr": s.get("Estab_Yr"), "url": s.get("URL"), "km2": s.get("AreaKm"),
              "r": rings})
print("mpa", len(M), Counter(m["fish"] for m in M).most_common(6))
wj("mpa.json", M)

# ------------------------------------------------------------------ spots and species
sp = rj(os.path.join(SRC, "spots.json"))
wj("spots.json", sp)
spc = rj(os.path.join(SRC, "species.json"))
wj("species.json", spc)
