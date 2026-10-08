# -*- coding: utf-8 -*-
"""Build data/zones-statewide.json: the statewide legal zones added by the 30 Sep 2026 review.

Same record shape as zones-local.json (see docs/SCHEMA.md), plus two optional fields:
  pts     [[lat, lon], ...]  vertices published in the law that cannot be joined into a closed ring
                             honestly (shoreline-following descriptions); drawn as markers
  active  when the rule applies ("always", "1 Apr to 31 Jul", "during launch operations", ...)
and `cat`, which may now be one of: fedfish, mil, manatee, stateareas, nwr, local, fed.

Inputs (all in the repo or the dated raw pull; nothing here is typed by hand except popup prose):
  tools/geometry/2026-09-30/*.json      geometry parsed from CFR / FAC coordinate text by the
                                         research passes, with the original DMS in `note`
  raw/2026-09-30/fwc-manatee-noentry.json   FWC State Manatee Protection Zones, MapServer/9
  raw/2026-09-30/fws-refuges-fl.json        USFWS NWR System Boundaries FeatureServer/0
  raw/2026-09-30/enc-misc.json              NOAA ENC named sea areas (SEAARE), CC0
  raw/2026-09-30/tiger-places-2026-09-30.json   Census TIGERweb incorporated places
  data/law.json, data/piers.json, data/bridges.json

Where a rule's boundary exists only in words, the zone is drawn from the nearest published
geometry that contains it (a city polygon, a charted named water area) and the `flag` says
exactly how the drawing differs from the law. Distance buffers around structures are drawn at
125 per cent of the stated distance, the same margin the statewide pier buffers use.
"""
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
RAW = os.environ.get("RAW", os.path.join(ROOT, "raw", "2026-09-30"))
GEO = os.path.join(HERE, "geometry", "2026-09-30")

LAW = {e["id"]: e for e in json.load(io.open(os.path.join(ROOT, "data", "law.json"), encoding="utf-8"))["entries"]}
PIERS = json.load(io.open(os.path.join(ROOT, "data", "piers.json"), encoding="utf-8"))
BRIDGES = json.load(io.open(os.path.join(ROOT, "data", "bridges.json"), encoding="utf-8"))


def rawj(name):
    return json.load(io.open(os.path.join(RAW, name), encoding="utf-8"))


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def r5(p):
    return [round(p[0], 5), round(p[1], 5)]


def circle(lat, lon, radius_m, n=48):
    out = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        dlat = radius_m * math.cos(a) / 111320.0
        dlon = radius_m * math.sin(a) / (111320.0 * math.cos(math.radians(lat)))
        out.append(r5([lat + dlat, lon + dlon]))
    return out


def pip(pt, ring):
    y, x = pt
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        yi, xi = ring[i]
        yj, xj = ring[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi):
            inside = not inside
        j = i
    return inside


def in_rings(pt, rings):
    # even-odd across all rings handles holes
    return sum(1 for r in rings if pip(pt, r)) % 2 == 1


def centroid(ring):
    la = sum(p[0] for p in ring) / len(ring)
    lo = sum(p[1] for p in ring) / len(ring)
    return [round(la, 5), round(lo, 5)]


def effect(ids):
    for i in ids:
        if i in LAW:
            return LAW[i]["effect"]
    return ""


Z = []


def add(**z):
    for k in ("r", "line", "pts"):
        z.setdefault(k, [])
    z.setdefault("flag", None)
    z.setdefault("active", None)
    missing = [i for i in z["law"] if i not in LAW]
    assert not missing, (z["id"], missing)
    Z.append(z)


# ------------------------------------------------------------------ 1. research-pass geometry
CAT_OF = {"a2-federal": "fedfish", "a3-uscg-mil": "mil", "a4-state": "stateareas", "a1-currency": "stateareas"}
SKIP_IDS = {"bisclegare"}          # a1's Legare box duplicates a2's bnp-legare (verbatim source)
NPS_IDS = {"bnp-legare", "drto-rna"}


def activ(a):
    if not a or a == "always":
        return "At all times."
    return a[0].upper() + a[1:] + ("" if a.endswith(".") else ".")


for fn in ("a1-currency", "a2-federal", "a3-uscg-mil", "a4-state"):
    for g in json.load(io.open(os.path.join(GEO, fn + ".json"), encoding="utf-8")):
        if g["id"] in SKIP_IDS:
            continue
        law = [i for i in g["law"] if i in LAW]
        cat = "fed" if g["id"] in NPS_IDS else CAT_OF[fn]
        lines = g.get("lines") or g.get("line") or []
        pts = g.get("points") or []
        s = "<b>" + esc(effect(law)) + "</b>"
        if g.get("active"):
            s += "<div style=\"margin-top:6px\"><b>When:</b> " + esc(activ(g["active"])) + "</div>"
        flag = g.get("flag")
        if not g.get("rings") and (lines or pts) and not flag:
            flag = ("The law describes this area partly along a shoreline or by points that do not close into "
                    "a ring, so only the published points or lines are drawn. The closed water is larger than "
                    "what is shown; read the citation.")
        add(id=g["id"], n=g["name"], law=law, cat=cat, kind=g.get("kind", "warn"),
            r=g.get("rings") or [], line=lines, pts=pts if not g.get("rings") else [],
            s=s, src=(g.get("source") or "") + ". " + (g.get("note") or ""), flag=flag,
            active=g.get("active"))

# ------------------------------------------------------------------ 2. manatee No Entry zones
man = rawj("fwc-manatee-noentry.json")
for z in man["zones"]:
    ne = z["MASTER_CL"].startswith("NE")
    txt = z.get("TEXT_68C") or ""
    law = ["fac-68c-22-002-11", "fac-68c-22"] if ne else ["fac-68c-22"]
    s = ("<b>" + ("No Entry: closed to all vessels and all persons, swimming, diving, wading or fishing. "
                  if ne else "Motorboats prohibited. Swimmers and divers are not barred by this zone type. ")
         + "</b>" + esc(txt) + ". " + esc(z.get("NOTES_68C") or "") +
         "<div style=\"margin-top:6px\"><b>When:</b> " + esc(z.get("DATE1_68C") or "") +
         (" / " + esc(z["DATE2_68C"]) if z.get("DATE2_68C") and z.get("DATE2_68C") != z.get("DATE1_68C") else "") +
         "</div>")
    flag = None
    if (z.get("COUNTY") or "").upper() == "INDIAN RIVER":
        flag = ("R. 68C-22.007 (Indian River County) was amended effective 30 Jun 2026. FWC's GIS was last "
                "edited 13 May 2025, so this zone may have changed class. Read the current rule text.")
    add(id="man-" + str(z["OBJECTID"]), n="Manatee zone: " + txt + " (" + (z.get("COUNTY") or "").title() + ")",
        law=law, cat="manatee", kind="closed" if ne else "warn", r=z["g"], s=s,
        src="FWC State Manatee Protection Zones in Florida, MapServer/9, rule " + (z.get("SECT_68C") or "") +
            ". The service states that the Florida Administrative Code text prevails over the map.",
        flag=flag, active=z.get("DATE1_68C"))

# ------------------------------------------------------------------ 3. National Wildlife Refuges
REF = {
    "HOBE SOUND": ("warn", ["cfr-50-32-28-g"], "Fishing by rods and reels and poles and lines only, so spearfishing is excluded on the conservative reading."),
    "PINELLAS": ("warn", ["cfr-50-32-28-m"], "Fishing only from vessels around Tarpon Key."),
    "EGMONT KEY": ("warn", ["cfr-50-32-28-d"], "Two attended poles per angler, so spearfishing is excluded on the conservative reading."),
    "CEDAR KEYS": ("warn", ["cfr-50-32-28-b"], "300-foot buffer around Snake Key closed to all entry 1 March to 30 June."),
    "DARLING": ("warn", ["cfr-50-32-28-h"], "No bows or spears from Wildlife Drive; refuge waters are otherwise governed by state law."),
    "TEN THOUSAND ISLANDS": ("warn", ["cfr-50-32-28"], "Spears and gigs banned in the freshwater and brackish marsh; open salt water not addressed."),
    "MERRITT ISLAND": ("warn", ["cfr-50-32-28-k", "fac-68b-3-008"], "Refuge fishing permit required; night fishing only from a vessel. The Volusia inland salt waters rule also reaches Mosquito Lagoon."),
    "KEY WEST": ("warn", ["cfr-50-27-21", "cfr-922-164-b1"], "Not opened in 50 C.F.R. part 32, which on its face closes it to taking; FWS's own pages say refuge waters are open to fishing under state law. The conflict is unresolved."),
    "GREAT WHITE HERON": ("warn", ["cfr-50-27-21"], "Not opened in 50 C.F.R. part 32, which on its face closes it to taking; FWS's own pages say refuge waters are open to fishing under state law. The conflict is unresolved."),
    "PASSAGE KEY": ("closed", ["cfr-50-27-21"], "Closed to the public (FWS). Not opened to fishing in part 32."),
    "ISLAND BAY": ("warn", ["cfr-50-27-21"], "Closed to the public (FWS). The refuge is the islands; the surrounding water is a state aquatic preserve."),
    "MATLACHA PASS": ("warn", ["cfr-50-27-21"], "Closed to the public (FWS). The refuge is the islands; the surrounding water is a state aquatic preserve."),
    "PINE ISLAND": ("warn", ["cfr-50-27-21"], "Closed to the public (FWS). The refuge is the islands; the surrounding water is a state aquatic preserve."),
    "CROCODILE LAKE": ("closed", ["cfr-50-27-21"], "Closed to the public (FWS). Not opened to fishing in part 32."),
    "CRYSTAL RIVER": ("warn", ["cfr-50-17-108", "cfr-50-17-108-a", "cfr-50-27-21"], "Kings Bay manatee refuge and sanctuaries apply; Three Sisters Springs bans scuba and spear fishing."),
}
ref = rawj("fws-refuges-fl.json")
for u in ref["refuges"]:
    nm = u["ORGNAME"]
    hit = next((k for k in REF if k in nm.upper()), None)
    if not hit:
        continue            # inland or no spear-relevant rule found; not drawn
    kind, law, txt = REF[hit]
    add(id="nwr-" + u["LIT"].lower(), n=nm.title().replace("Nwr", "NWR"), law=law, cat="nwr", kind=kind,
        r=u["g"], s="<b>" + esc(txt) + "</b>",
        src="USFWS Division of Realty, National Wildlife Refuge System Boundaries FeatureServer/0 (interest "
            "boundary, last edited 24 Aug 2026). The boundary includes land; the rule reaches only refuge "
            "waters.",
        flag=("Refuge boundaries on this layer include land and interest parcels. Whether the refuge "
              "boundary extends over the water shown has not been confirmed for this unit."
              if hit in ("HOBE SOUND", "PINELLAS", "EGMONT KEY", "PASSAGE KEY", "ISLAND BAY", "MATLACHA PASS",
                         "PINE ISLAND", "KEY WEST", "GREAT WHITE HERON") else None))

# ------------------------------------------------------------------ 4. charted named waters (ENC)
misc = rawj("enc-misc.json")


def enc_area(name, band=None, near=None):
    best = None
    for s in misc["sea_area_named"]:
        if s.get("OBJNAM") != name:
            continue
        if band and s["band"] != band:
            continue
        if near:
            c = centroid(s["g"][0])
            if abs(c[0] - near[0]) > 0.08 or abs(c[1] - near[1]) > 0.08:
                continue
        n = sum(len(r) for r in s["g"])
        if best is None or n > sum(len(r) for r in best["g"]):
            best = s
    assert best, name
    return best


otb = enc_area("Old Tampa Bay", band="C")
add(id="st-oldtampabay", n="Old Tampa Bay north of the Gandy Bridge: spears not on the allowed gear list",
    law=["fac-68b-25-003"], cat="stateareas", kind="closed", r=otb["g"],
    s="<b>" + esc(LAW["fac-68b-25-003"]["effect"]) + "</b> The rule lists the only gear that may be used here "
      "(hook and line, landing or dip net, cast net, permitted crab and shrimp traps). A spear is not on the list.",
    src="Geometry: NOAA ENC named sea area 'Old Tampa Bay', coastal band, cell " + otb["DSNM"] + " (CC0).",
    flag="The rule covers Old Tampa Bay north of the Gandy Bridge AND every creek and bayou emptying into it. "
         "The drawn polygon is NOAA's charted 'Old Tampa Bay' area, whose south edge sits near the Gandy Bridge; "
         "the creeks and bayous are not drawn. Treat all of them as closed.")

tc = enc_area("Turkey Creek", band="H")
cc = enc_area("Crane Creek", band="H", near=[28.076, -80.60])
add(id="st-turkeycrane", n="Turkey Creek and Crane Creek (Brevard): spears not on the allowed gear list",
    law=["fac-68b-3-009"], cat="stateareas", kind="closed", r=tc["g"] + cc["g"],
    s="<b>" + esc(LAW["fac-68b-3-009"]["effect"]) + "</b>",
    src="Geometry: NOAA ENC named sea areas 'Turkey Creek' (" + tc["DSNM"] + ") and 'Crane Creek' (" + cc["DSNM"] + "), harbour band (CC0).",
    flag="The rule's line is across each creek mouth at the Indian River Lagoon; the charted creek polygons end "
         "where the chart's detail ends and do not cover the full upstream reach. Treat the whole creeks as closed.")

# ------------------------------------------------------------------ 5. local ordinances
TIG = {p["b"]: p for p in rawj("tiger-places-2026-09-30.json")["places"]}


def city(b):
    return TIG[b]["rings"]


def city_zone(zid, b, law, kind, s, flag):
    add(id=zid, n=b + ": " + LAW[law[0]]["title"], law=law, cat="local", kind=kind, r=city(b),
        s="<b>" + esc(LAW[law[0]]["effect"]) + "</b>" + (s or ""),
        src="Boundary: US Census TIGERweb 2025 incorporated place '" + TIG[b]["n"] + "' (GEOID " + TIG[b]["geoid"] +
            "), which includes the water parcels the city claims.",
        flag=flag)


WORDS = ("The ordinance describes its area in words only. The whole incorporated area is drawn, which "
         "over-states the closure on land and may under- or over-state how far it reaches offshore; ")

city_zone("loc-venice", "Venice", ["venice-46-114"], "closed", "",
          WORDS + "the ordinance says 'within or near' city waters and never defines 'near', so the rule may reach "
          "beyond this outline. Venice Inlet is treated as closed.")
city_zone("loc-cedarkey", "Cedar Key", ["cedarkey-2-4-02"], "closed", " Gigs are included.",
          WORDS + "the section does not state how far into the Gulf the city limits run.")
city_zone("loc-balharbour", "Bal Harbour", ["balharbour-12-7"], "closed", "",
          WORDS + "'waters within Bal Harbour Village' follow the village limits, whose seaward edge is not surveyed here.")
city_zone("loc-lbts", "Lauderdale-by-the-Sea", ["lbts-5-4"], "closed",
          " A gun that cannot be loaded cannot be used, so for band and pneumatic guns this works as a town-wide use ban.",
          WORDS + "the loading ban applies anywhere in the Town, land or water.")
city_zone("loc-ti222", "Treasure Island", ["ti-22-2", "ti-58-34"], "closed",
          " Spearfishing is excepted only where the city has designated it permissible; no designation was found.",
          WORDS + "no designated spearfishing area was located. Whether the city treats state-law legality as "
          "'designated as permissible' is an open question for the city clerk.")
city_zone("loc-sib", "Sunny Isles Beach", ["sib-108-4"], "closed", "",
          WORDS + "the section sits inside a dangerous-conditions provision; it may apply only during those "
          "conditions. Drawn as standing, the reading that closes more water.")
city_zone("loc-hallandale", "Hallandale Beach", ["hallandale-16-23"], "warn", "",
          WORDS + "the rule reaches the 'public beach' seaward of the erosion control line; whether that carries "
          "into the water is not stated. No designated area was found.")
city_zone("loc-lantana", "Lantana", ["lantana-5-18"], "warn", "",
          WORDS + "the rule covers the municipal beach 'and the waters'; the seaward extent is not stated.")
city_zone("loc-delray", "Delray Beach", ["delray-101-34"], "warn",
          " Scuba only: breath-hold diving and freediving are not restricted by this section.",
          WORDS + "the code defines the municipal beach to include ocean waters within city limits.")
city_zone("loc-dania", "Dania Beach", ["dania-6-12"], "closed", "",
          WORDS + "the spear-gear sentence covers the public beach and 'the water' with no stated seaward limit.")

# pier and structure buffers
PM = {p["n"]: p for p in PIERS}


def pier_zone(zid, pier_name, law, dist_m, label, kind="closed", flag=None):
    p = PM[pier_name]
    add(id=zid, n=label, law=law, cat="local", kind=kind, r=[circle(p["lat"], p["lon"], dist_m * 1.25)],
        s="<b>" + esc(LAW[law[0]]["effect"]) + "</b> Drawn at 125 per cent of the stated distance.",
        src="Centre: FWC Fishing Piers, Jetties and Bridges inventory, '" + pier_name + "' (" +
            str(p["lat"]) + ", " + str(p["lon"]) + "). Radius from the ordinance, plus 25 per cent margin.",
        flag=flag)


FT = 0.3048
YD = 0.9144
pier_zone("loc-lwb-ocean", "Lake Worth Pier", ["lwb-7-33"], 500 * FT, "Lake Worth Beach: 500 ft of the ocean pier")
pier_zone("loc-lwb-bryant", "Bryant Park", ["lwb-7-33"], 500 * FT, "Lake Worth Beach: 500 ft of the Bryant Park pier")
pier_zone("loc-lwb-snook", "Old Lake Worth Bridge Fishing Pier", ["lwb-7-33"], 500 * FT,
          "Lake Worth Beach: 500 ft of the Snook Island pier",
          flag="The Snook Island pier is not named in FWC's inventory. The circle is centred on the Old Lake Worth "
               "Bridge fishing pier, the nearest inventoried structure at Snook Island. Confirm on site.")
pier_zone("loc-pompano-pier", "Fisher Family Pier", ["pompano-98-12"], 100 * FT,
          "Pompano Beach: 100 ft of the municipal pier",
          flag="FWC lists the rebuilt Pompano Beach pier as 'Fisher Family Pier'. The statewide 100-yard pier "
               "buffer already covers this water; the city rule adds swimming.")
pier_zone("loc-lbts-pier", "Anglins Fishing Pier", ["lbts-5-4"], 300 * FT,
          "Lauderdale-by-the-Sea: 300 ft of the fishermen's pier (no surface, skin or scuba diving)")
pier_zone("loc-dania-pier", "Dania Beach Pier", ["dania-6-12"], 100 * YD,
          "Dania Beach: 100 yards of the Ocean Park pier (no swimming or diving)")
pier_zone("loc-annamaria-pier", "Anna Maria City Pier", ["annamaria-110-122"], 50 * YD,
          "Anna Maria: 50 yards of the City Pier", kind="warn",
          flag="Smaller than the statewide 100-yard pier buffer, which already closes this water to spearfishing.")
pier_zone("loc-deerfield-pier", "Deerfield Beach International Pier", ["deerfield-50-112"], 50 * YD,
          "Deerfield Beach: 50 yards of the pier (no swimming or snorkeling)", kind="warn",
          flag="Secondary: the section's lead-in was not read. The statewide 100-yard pier buffer already closes "
               "this water to spearfishing.")
pier_zone("loc-naples-pier", "Naples Pier", ["naples-42-52"], 100 * FT,
          "Naples: 100 ft of the city pier", kind="warn",
          flag="Smaller than the statewide 100-yard pier buffer, which already closes this water to spearfishing.")
pier_zone("loc-lee-lynnhall", "Lynn Hall Memorial Park", ["lee-20-25"], 100 * YD,
          "Lee County: Lynn Hall Park Pier, spear fishing banned", flag=(
              "The county rule bans spears in all county park waters including 'adjacent littoral waters', whose "
              "extent is not defined. Only the Lynn Hall pier is drawn; every Lee County beach park is covered."))


def bridges_in(b, pad=0.0):
    rings = city(b)
    return [x for x in BRIDGES if x.get("iw") != "inland" and in_rings([x["lat"], x["lon"]], rings)]


for b, law, dist, label in (("Melbourne", "melbourne-40-2", 100 * FT, "Melbourne: 100 ft of a public bridge"),
                            ("Marco Island", "marco-54-173", 50 * FT, "Marco Island: 50 ft of a bridge"),
                            ("Sarasota", "sarasota-city-10-66", 100 * YD, "City of Sarasota: 100 yards of a city bridge")):
    bs = bridges_in(b)
    if not bs:
        continue
    add(id="loc-br-" + b.lower().replace(" ", ""), n=label + " (" + str(len(bs)) + " bridges)", law=[law],
        cat="local", kind="closed", r=[circle(x["lat"], x["lon"], dist * 1.25, 32) for x in bs],
        s="<b>" + esc(LAW[law]["effect"]) + "</b> Drawn at 125 per cent of the stated distance around every "
          "NBI bridge point inside the city limits.",
        src="Centres: FHWA National Bridge Inventory points in data/bridges.json that fall inside the TIGER city "
            "polygon. Radius from the ordinance plus 25 per cent.",
        flag="NBI gives one point per bridge, not the span. Long bridges and causeways need the buffer along their "
             "whole length, and piers, docks and wharves named by the ordinance are not drawn.")

# words-only local rules drawn from charted water areas
bri = enc_area("Boca Raton Inlet", band="A")
add(id="loc-boca-inlet", n="Boca Raton Inlet: no swimming, diving or scuba", law=["boca-9-3"], cat="local",
    kind="closed", r=bri["g"], s="<b>" + esc(LAW["boca-9-3"]["effect"]) + "</b>",
    src="Geometry: NOAA ENC named sea area 'Boca Raton Inlet', " + bri["DSNM"] + " (CC0).",
    flag="The ordinance runs from the jetty tips to a line 200 yards north of the A1A inlet bridge, which reaches "
         "into Lake Boca Raton beyond the charted inlet polygon. The Palmetto Park Road bridge zone on the ICW "
         "(100 ft north to 1,200 ft south, full width) is not drawn.")
hbi = enc_area("Hillsboro Inlet", band="H")
add(id="loc-pompano-hillsboro", n="Hillsboro Inlet (Pompano Beach side): no swimming or diving", law=["pompano-91-22"],
    cat="local", kind="closed", r=hbi["g"], s="<b>" + esc(LAW["pompano-91-22"]["effect"]) + "</b>",
    src="Geometry: NOAA ENC named sea area 'Hillsboro Inlet', " + hbi["DSNM"] + " (CC0).",
    flag="Secondary: the ordinance's own boundary description has not been read. It also covers Hillsboro Bay and "
         "part of the ICW south of the inlet, which are not drawn.")
jp = enc_area("Johns Pass", band="H")
add(id="loc-madeira-johnspass", n="John's Pass: no swimming, diving or spearfishing (Madeira Beach side)",
    law=["madeira-78-3", "ti-58-34"], cat="local", kind="closed", r=jp["g"],
    s="<b>" + esc(LAW["madeira-78-3"]["effect"]) + "</b>",
    src="Geometry: NOAA ENC named sea area 'Johns Pass', " + jp["DSNM"] + " (CC0).",
    flag="The ordinance's limits are the two 128th Avenue extension lines, bay side and Gulf side, which no dataset "
         "carries. The charted pass polygon is drawn instead. Treasure Island § 58-34 covers the south side and "
         "1,500 ft beyond each end.")

# marker-only local rules (no geometry the law can be tied to)
def marker(zid, b, law, kind, label, flag):
    c = centroid(max(city(b), key=len))
    add(id=zid, n=label, law=law, cat="local", kind=kind, pts=[c],
        s="<b>" + esc(LAW[law[0]]["effect"]) + "</b>",
        src="Marker at the centroid of the TIGER incorporated place '" + TIG[b]["n"] + "'. Not a boundary.",
        flag=flag)


marker("loc-miamibeach", "Miami Beach", ["miamibeach-82-441"], "warn",
       "Miami Beach: spear fishing banned from bridges, at the 29th to 33rd Street jetty area and in swim zones",
       "GEOMETRY NOT MAPPED. Lifeguard-tower swim zones (400 ft either side of each tower, 300 ft out, buoyed) and "
       "the 29th to 33rd Street jetty area are not in any dataset. The marker is a city centroid, not the closure.")
marker("loc-fmb", "Fort Myers Beach", ["fmb-18-24"], "warn", "Fort Myers Beach: spears prohibited in town parks and park waters",
       "GEOMETRY NOT MAPPED. Town parks and their waters are not drawn; the marker is a town centroid.")
marker("loc-bonita", "Bonita Springs", ["bonita-28-31"], "warn", "Bonita Springs: spears prohibited in city parks and park waters",
       "GEOMETRY NOT MAPPED. City parks (e.g. Little Hickory Island beach park) are not drawn; the marker is a city centroid.")
marker("loc-fortpierce", "Fort Pierce", ["fortpierce-28-4"], "warn", "Fort Pierce: spearing banned at listed places and in park areas",
       "GEOMETRY NOT MAPPED. Secondary: the section needs a full re-read. Park areas are defined to include waterways and beaches.")
marker("loc-dunedin", "Dunedin", ["dunedin-86-108"], "warn", "Dunedin: no spears from the marina docks and seawalls",
       "GEOMETRY NOT MAPPED. The marker is a city centroid, not the marina.")
marker("loc-lakepark", "Lake Park", ["lakepark-76-89"], "warn", "Lake Park: no swimming, diving or fishing in the Harbor Marina",
       "GEOMETRY NOT MAPPED. Secondary: only a fragment of the section was read.")
marker("loc-juno", "Juno Beach", ["juno-16-4"], "warn", "Juno Beach: loaded spear gun banned on beaches, the pier and public places",
       "NOT a water closure. Carrying an unloaded gun across the beach and loading it in the water is not addressed.")

# ------------------------------------------------------------------ dated corrections
# The 7 Oct 2026 legal currency pass (man-66 removed, refuge and local flags, the Deerfield Beach marker).
# The same function patches the committed JSON directly when raw/ is not available.
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "patch_zs_20261007", os.path.join(ROOT, "tools", "patch-zones-statewide-2026-10-07.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
_mod.patch(Z, LAW, PIERS)

# ------------------------------------------------------------------ write
data = {"version": "2026-09-30",
        "note": "Statewide legal zones added by the 30 Sep 2026 review. Same shape as zones-local.json plus "
                "`pts` and `active`. Built by tools/build-zones-statewide.py.",
        "zones": Z}
out = os.path.join(ROOT, "data", "zones-statewide.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
from collections import Counter
print("zones:", len(Z), Counter(z["cat"] for z in Z), Counter(z["kind"] for z in Z),
      "flagged:", sum(1 for z in Z if z["flag"]), "bytes:", os.path.getsize(out))
