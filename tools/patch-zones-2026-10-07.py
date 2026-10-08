# -*- coding: utf-8 -*-
"""Zones from the legal review of 7 and 8 Oct 2026. Run after build-zones-local.py and
build-zones-statewide.py (and after the earlier dated patches); idempotent.

Geometry pulled in the author's Chrome on 8 Oct 2026, hash-checked on transfer, saved in
tools/law-updates/2026-10-07/geom/ (no OpenStreetMap input, so the zone files stay CC BY 4.0):
  pulled.txt   CLW  US Census TIGERweb incorporated place 'Clearwater city' (GEOID 1212875), simplified
                    at 0.00004 degree, parcels under 0.0000002 square degree dropped
  enc-nhd.txt  PON  NOAA ENC shoreline construction at Ponce Inlet, harbour band, cell US5FL7GL.000 (CC0):
                    charted rip rap, north jetty, south jetty
               STN  USGS NHD flowline 'Steinhatchee River' (nhd MapServer/6), segments chained,
                    simplified at 0.00015 degree (public domain)
Encoding: parts separated by '|', first pair absolute and later pairs deltas, units of 1e-5 degree.
Other input: data/jetties.json (the Mexico Beach west jetty, traced on USGS NAIP imagery).

The Jupiter Inlet, South Lake Worth Inlet and Hollywood zones of this review were dropped in favour
of the chart-based versions already in zones-statewide.json (loc-inlet-jupiter, loc-inlet-boynton,
loc-hollywood-beach); Boynton gains the § 18-1 citation here.

Every zone names the registry entry it rests on and says in `src` what the drawn shape is. Where the
ordinance's own boundary cannot be drawn, `flag` says which reading was drawn and why.
"""
import io, json, os, sys
from shapely.geometry import LineString, Polygon, MultiPolygon, Point
from shapely.ops import unary_union, transform
from pyproj import Transformer

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
G = os.path.join(ROOT, "tools", "law-updates", "2026-10-07", "geom")
FT, YD = 0.3048, 0.9144
fwd = Transformer.from_crs("EPSG:4326", "EPSG:3086", always_xy=True).transform
inv = Transformer.from_crs("EPSG:3086", "EPSG:4326", always_xy=True).transform


def dec(s):
    out = []
    for part in s.split("|"):
        pts, a, o = [], 0, 0
        for k, p in enumerate(part.split(";")):
            x, y = map(int, p.split(","))
            a, o = (x, y) if k == 0 else (a + x, o + y)
            pts.append((a / 1e5, o / 1e5))
        out.append(pts)
    return out


def dec_i(a):
    out, la, lo = [], 0, 0
    for k in range(0, len(a), 2):
        la, lo = (a[k], a[k + 1]) if k == 0 else (la + a[k], lo + a[k + 1])
        out.append((la / 1e5, lo / 1e5))
    return out


def m(latlons):
    return [fwd(lo, la) for la, lo in latlons]


def rings_ll(geom, tol=1.0):
    geom = geom.simplify(tol) if tol else geom
    polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    out = []
    for p in polys:
        r = [[round(y, 5), round(x, 5)] for x, y in (inv(*c) for c in p.exterior.coords)]
        if r[0] != r[-1]:
            r.append(r[0])
        out.append(r)
    return out


raw = {}
for f in ("pulled.txt", "enc-nhd.txt"):
    for ln in io.open(os.path.join(G, f), encoding="utf-8").read().split("\n"):
        if ":" in ln and not ln.startswith("#"):
            k, v = ln.split(":", 1)
            raw[k] = v
J = {z["id"]: z for z in json.load(io.open(os.path.join(ROOT, "data", "jetties.json"), encoding="utf-8"))["zones"]}
B = json.load(io.open(os.path.join(ROOT, "data", "bridges.json"), encoding="utf-8"))

local, state = [], []

# ---- Clearwater, § 21.06(1) --------------------------------------------------------------------
clw = dec(raw["CLW"])


def area(r):
    return sum(r[i][1] * r[i + 1][0] - r[i + 1][1] * r[i][0] for i in range(len(r) - 1)) / 2.0


outers = [r for r in clw if area(r) < 0]          # clockwise in (lon, lat): an outer ring
city = unary_union([Polygon(m(r)).buffer(0) for r in outers])
local.append(dict(id="clw2106", n="Clearwater: firing spring, air or gas projectile weapons banned citywide, spearfishing excepted only where designated",
    law=["clearwater-21-06", "fs-379-2412"], cat="local", kind="closed", r=rings_ll(city, 2.0),
    s="<b>Firing any weapon propelled by compressed air, gas or a spring is unlawful anywhere in the city; the only "
      "spearfishing exception is 'in any area where such activity has been designated as being permissible' by "
      "the city, the state or the United States</b> (§ 21.06(1)). No designation was found.",
    src="Boundary: US Census TIGERweb 2025 incorporated place 'Clearwater city' (GEOID 1212875), which includes the "
        "water the city claims. Unincorporated enclaves inside the city are not cut out.",
    flag="The ordinance describes its area in words only. The whole incorporated area is drawn, enclaves included, "
         "which over-states the closure on land. Whether the city treats state-law legality as 'designated as "
         "permissible' is an open question for the city clerk, as at Treasure Island."))

# ---- Mexico Beach, § 95.03 ---------------------------------------------------------------------
mbw = J["jetty-mexicobeach-w"]["line"][0]
local.append(dict(id="mxb9503", n="Mexico Beach canal channel and jetties: no swimming",
    law=["mexicobeach-95-03"], cat="local", kind="closed", r=[], pts=[mbw[-1]],
    s="<b>Swimming is prohibited in the boat channel of the city canal, from the uppermost marina to the Gulf low "
      "water mark, and within 100 feet on each side of the entrance jetties</b> (§ 95.03). A spearfisher is "
      "swimming.",
    src="Marker at the seaward end of the west jetty as traced on USGS NAIP imagery (data/jetties.json).",
    flag="The canal channel and the 100 ft bands are not drawn. Only a west jetty was found on the imagery, while "
         "the ordinance speaks of jetties in the plural; the jetty layer draws 150 ft around the west jetty. Treat "
         "the whole channel up to the marina, and 100 ft on each side of its entrance, as closed."))

# ---- Volusia beach code, § 20-121(c)(2) --------------------------------------------------------
pon = dec(raw["PON"])[1:]          # part 0 is charted rip rap along the inlet shore, not a jetty
pj = unary_union([LineString(m(p)) for p in pon])
local.append(dict(id="vol20121", n="Ponce Inlet jetties: no swimming within 300 ft (Volusia beach code)",
    law=["volusia-20-121"], cat="local", kind="closed", r=rings_ll(pj.buffer(350 * FT), 1.0),
    s="<b>No swimming or bathing within 300 feet in any direction of a pier or jetty</b> on Volusia's beaches "
      "(§ 20-121(c)(2)). A spearfisher in the water is swimming.",
    src="350 ft (300 ft plus 50 ft margin) around the Ponce Inlet north and south jetties as charted: NOAA ENC "
        "shoreline construction, harbour band, cell US5FL7GL.000 (CC0), pulled 8 Oct 2026. The charted rip rap "
        "along the north shore of the inlet is not treated as a jetty.",
    flag="The beach code governs the county's beaches; how far it reaches into the inlet and offshore is not "
         "settled. Ocean piers are already inside the wider 125 yd pier circles."))

# ---- Steinhatchee River, § 379.101(17) ---------------------------------------------------------
ste = dec(raw["STN"])[0]
state.append(dict(id="st-steinhatchee", n="Steinhatchee River: fresh water by statute, no spearing and no speargun aboard",
    law=["fs-379-101-17", "fac-68a-23-002-7"], cat="stateareas", kind="closed", r=[],
    line=[[[round(a, 5), round(b, 5)] for a, b in ste]], pts=[], active=None,
    s="<b>The Steinhatchee River is fresh water from its source to its mouth</b> (§ 379.101(17)), so spearing is "
      "prohibited on it and a speargun may not be used or possessed in or upon it (r. 68A-23.002(7)).",
    src="Line: USGS National Hydrography Dataset flowline 'Steinhatchee River' (nhd MapServer/6, 100 segments "
        "chained into one line), simplified to about 15 m, from 29.99 N to the river's end in Deadman Bay.",
    flag="The statute does not say where the mouth is. The line runs from the head of the "
         "NHD-named river (about 29.99 N) to the end of the mapped flowline in Deadman Bay. Treat the whole river, "
         "bank to bank and source to mouth, as closed."))

# ---- write -------------------------------------------------------------------------------------
LP = os.path.join(ROOT, "data", "zones-local.json")
SP = os.path.join(ROOT, "data", "zones-statewide.json")
dl = json.load(io.open(LP, encoding="utf-8"))
ds = json.load(io.open(SP, encoding="utf-8"))
ids = {z["id"] for z in local}
dl["zones"] = [z for z in dl["zones"] if z["id"] not in ids] + local
ids = {z["id"] for z in state}
ds["zones"] = [z for z in ds["zones"] if z["id"] not in ids] + state
for z in ds["zones"]:
    if z["id"] == "nwr-cry":
        z["kind"] = "closed"
        for i in ("fws-crystal-river", "cfr-50-27-43", "cfr-50-17-108-c14"):
            if i not in z["law"]:
                z["law"].append(i)
        z["s"] = ("<b>No fishing of any kind in refuge waters</b>, Three Sisters Springs, the King Spring and Tarpon Hole "
                  "area and the waters around Warden Key included; the manatee sanctuaries prohibit all fishing "
                  "(FWS). Part 32 does not open the refuge, so 50 C.F.R. § 27.21 closes it, and spears may not be "
                  "used or possessed on it (§ 27.43).")
    if z["id"] == "loc-inlet-boynton" and "pbc-18-1" not in z["law"]:
        z["law"].append("pbc-18-1")
        z["s"] = (z["s"] + " The county also bans swimming in the inlet and entering it from a jetty, bulkhead or "
                  "bridge, and closes the ocean within 75 ft of the sand transfer plant, or its area of influence "
                  "if larger (§ 18-1).")
for z in dl["zones"]:
    if "fs-790-33" in z["law"] and "fs-379-2412" not in z["law"]:
        z["law"].append("fs-379-2412")       # the fishing preemption statute sits beside the firearms one
io.open(LP, "w", encoding="utf-8").write(json.dumps(dl, ensure_ascii=False, separators=(",", ":")))
io.open(SP, "w", encoding="utf-8").write(json.dumps(ds, ensure_ascii=False, separators=(",", ":")))
for z in local + state:
    n = sum(len(r) for r in z.get("r") or []) + sum(len(l) for l in z.get("line") or []) + len(z.get("pts") or [])
    print("%-18s %-7s %5d vertices" % (z["id"], z["kind"], n))
