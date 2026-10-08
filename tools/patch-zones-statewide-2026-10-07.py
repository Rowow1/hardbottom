# -*- coding: utf-8 -*-
"""Legal currency pass of 7 Oct 2026 for data/zones-statewide.json.

One source of truth for the 7 Oct 2026 statewide-zone edits, used two ways:
  * tools/build-zones-statewide.py imports patch() and applies it before writing, so a rebuild from
    raw/2026-09-30/ reproduces the result;
  * run on its own, this script applies the same edits to the committed data/zones-statewide.json, for
    machines without the raw pull (raw/ is not in git).

Edits, each from the 7 Oct 2026 research reports:
  * man-66 removed. The adopted r. 68C-22.007 (effective 30 Jun 2026) has no No Entry zone; the Vero
    Beach power-plant canals are Idle Speed all year, which does not bar divers (fac-68c-22-007).
  * nwr-hbs, nwr-pin, nwr-pak: the FWS page wording read on 7 Oct 2026 added to the flag. No geometry.
  * loc-fortpierce, loc-lakepark, loc-deerfield-pier, loc-pompano-hillsboro, loc-sib, loc-hallandale:
    flags updated now that the sections have been read whole.
  * penncpz-*: the "SECONDARY TRANSCRIPTION" warning in src replaced; all 35 corners were checked against
    the adopted rule text (flrules tid 30968625) and match to within 0.0002 minutes. No geometry change.
  * loc-boca-inlet: also cites pbc-13-32 (the county inlet ban covers every Palm Beach County inlet).
  * loc-deerfield-beach added: a warn marker at the one published point on the Deerfield Beach municipal
    beach (FWC's inventory position for the Deerfield Beach International Pier), citing
    deerfield-50-112-beach. Not a boundary; no geometry is invented.
Never changes coordinates of existing zones. Idempotent.
"""
import io
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REMOVED = {"man-66": "r. 68C-22.007 as amended 30 Jun 2026 has no No Entry zone (fac-68c-22-007)"}

NWR_EXTRA = {
    "nwr-hbs": (" FWS's refuge page (read 7 Oct 2026) says 'Refuge waters include Intracoastal Waterway and surf "
                "fishing at North Beach', so the refuge does include water in the Intracoastal Waterway and the "
                "surf; it gives no seaward or lateral limit."),
    "nwr-pin": (" FWS's refuge pages (read 7 Oct 2026) say 'Pinellas Key NWR is closed to public use year-round' "
                "and speak only of 'the islands'; they give no water boundary."),
    "nwr-pak": (" FWS's refuge page (read 7 Oct 2026) says 'the refuge is closed to all public use' and describes "
                "a sandbar 'often completely below water during high tide'; it gives no water boundary."),
}

FLAGS = {
    "loc-fortpierce": (
        "GEOMETRY NOT MAPPED. The section was read whole on 7 Oct 2026. The eight no-fishing places are shown only "
        "on a diagram kept by the city clerk and are posted on site (§ 28-4(b), (c)). Park areas are defined to "
        "include waterways, canals and beaches; read conservatively, that is every city waterway, canal and beach. "
        "The marker is a city centroid."),
    "loc-lakepark": (
        "GEOMETRY NOT MAPPED. The section was read whole on 7 Oct 2026: diving is forbidden in the marina area "
        "outright, and the only exception is angling and small cast nets from designated bulkhead areas. 'Marina "
        "area' is not defined. The marker is a town centroid, not the marina."),
    "loc-deerfield-pier": (
        "The statewide 100-yard pier buffer already closes this water to spearfishing. The same section also bars "
        "swimming more than 50 yards off the city beach without lifeguard permission (see the Deerfield Beach "
        "beach marker)."),
    "loc-pompano-hillsboro": (
        "The ordinance's boundary, read in full, is described in words and plat lots only: the Hillsboro Inlet and "
        "Hillsboro Bay centrelines from 'the easterly boundary of the State of Florida' to the Intracoastal "
        "Waterway, then named Hillsboro Shores lots. The charted inlet is drawn; Hillsboro Bay and the ICW part "
        "are not. The seaward start is read as the 3 nm state line, the reading that closes more water."),
    "loc-sib": (
        "The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states "
        "the closure on land and may under- or over-state how far it reaches offshore. The last sentence of § 108-4 "
        "has no dangerous-conditions trigger; the article heading suggests one. Drawn as standing, the reading that "
        "closes more water. No designated area was found."),
    "loc-hallandale": (
        "The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states "
        "the closure on land and may under- or over-state how far it reaches offshore; the rule reaches the "
        "'public beach' seaward of the erosion control line, and whether that carries into the water is not "
        "stated. Designated areas are set by the parks department, not in the code; none was found."),
}

PENN_OLD = ("SECONDARY TRANSCRIPTION: the numbers came through a PDF summariser (the struck-through ten-zone table "
            "and the new seven-zone table are interleaved in the FAR text); confirm every corner against the flrules "
            ".doc (tid 30968625) before publishing.")
PENN_NEW = ("CHECKED 7 Oct 2026: every corner matches the adopted rule text (flrules .doc, tid 30968625, history "
            "'Amended 7-1-26') to within 0.0002 minutes.")

DEERFIELD_PIER = "Deerfield Beach International Pier"


def deerfield_beach(law, piers):
    p = next(x for x in piers if x["n"] == DEERFIELD_PIER)
    return {
        "id": "loc-deerfield-beach",
        "n": "Deerfield Beach: no swimming beyond 50 yards of the city beach without lifeguard permission",
        "law": ["deerfield-50-112-beach"],
        "cat": "local", "kind": "warn",
        "r": [], "line": [],
        "pts": [[p["lat"], p["lon"]]],
        "s": ("<b>Off the Deerfield Beach municipal beach, swimming more than 50 yards out from mean high water "
              "needs the supervising lifeguard's permission, and fishing off the beach, which includes shore-entry "
              "spearfishing, is unlawful from 8 a.m. to dusk.</b> City Code § 50-112(b), (p)."),
        "src": ("Marker at FWC's Fishing Piers, Jetties and Bridges inventory position for '" + DEERFIELD_PIER +
                "' (" + str(p["lat"]) + ", " + str(p["lon"]) + "), the only published point on the municipal "
                "beach. Not a boundary."),
        "flag": ("GEOMETRY NOT MAPPED. The municipal beach runs the length of the city's oceanfront and the "
                 "50-yard line is not drawn. A freediver or snorkeler is swimming, so on the conservative reading "
                 "the limit applies to divers; lifeguard permission can lift it, which is why this is drawn amber."),
        "active": None,
    }


def patch(zones, law=None, piers=None):
    """Apply the 7 Oct 2026 edits to a list of zone dicts in place; returns the new list."""
    zones[:] = [z for z in zones if z["id"] not in REMOVED]
    Z = {z["id"]: z for z in zones}
    for i, extra in NWR_EXTRA.items():
        z = Z.get(i)
        if z and extra.strip() not in (z.get("flag") or ""):
            z["flag"] = (z.get("flag") or "") + extra
    for i, f in FLAGS.items():
        if i in Z:
            Z[i]["flag"] = f
    for i, z in Z.items():
        if i.startswith("penncpz-") and PENN_OLD in (z.get("src") or ""):
            z["src"] = z["src"].replace(PENN_OLD, PENN_NEW)
    z = Z.get("loc-boca-inlet")
    if z and "pbc-13-32" not in z["law"]:
        z["law"].append("pbc-13-32")
    if "loc-deerfield-beach" not in Z and piers is not None:
        new = deerfield_beach(law, piers)
        k = next((n for n, z in enumerate(zones) if z["id"] == "loc-deerfield-pier"), len(zones) - 1)
        zones.insert(k + 1, new)
    # Hollywood beach buffer and the two Palm Beach inlets (pbc-13-32), geometry from NOAA ENC
    add = json.load(io.open(os.path.join(ROOT, "tools", "geometry", "2026-10-07", "new-zones.json"),
                            encoding="utf-8"))["zones"]
    for nz in add:
        if nz["id"] not in Z:
            zones.append(nz)
            Z[nz["id"]] = nz
    return zones


if __name__ == "__main__":
    P = os.path.join(ROOT, "data", "zones-statewide.json")
    d = json.load(io.open(P, encoding="utf-8"))
    piers = json.load(io.open(os.path.join(ROOT, "data", "piers.json"), encoding="utf-8"))
    before = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    patch(d["zones"], piers=piers)
    after = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    io.open(P, "w", encoding="utf-8").write(after)
    print("zones-statewide.json: %s, %d zones" % ("changed" if after != before else "no change", len(d["zones"])))
