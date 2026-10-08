# -*- coding: utf-8 -*-
"""Dated corrections to data/zones-local.json from the 30 Sep 2026 legal review.

tools/build-zones-local.py built this file on 22 Aug 2026 from raw GIS pulls (spear-geo-batch1.json,
spear-osm-batch2.json) that are not kept in the repo. Rather than re-derive the geometry, these
edits change only popup text, kind, law ids and flags, never coordinates. Idempotent.
"""
import io
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = os.path.join(ROOT, "data", "zones-local.json")
d = json.load(io.open(P, encoding="utf-8"))
Z = {z["id"]: z for z in d["zones"]}

# Gulf Islands NS: the 2021 compendium banned projectile fishing gear in all Seashore waters; the compendium
# updated 1 Sep 2026 no longer contains it (browser check 30 Sep 2026). Drawn amber with both facts.
z = Z["npsguis"]
z["kind"] = "warn"
z["law"] = ["guis-compendium", "cfr-36-2-3"]
z["s"] = ("The 2021 Superintendent's Compendium <b>banned spear guns, pole spears, Hawaiian slings and every other "
          "projectile device in all Seashore waters</b>. The compendium updated 1 Sep 2026 no longer contains that "
          "provision, and the park's fishing page now refers spearfishing questions to FWC. Until the park confirms "
          "whether the ban was rescinded, treat Seashore waters as restricted. The Fort Pickens ferry pier is closed "
          "to fishing, no diving or swimming is permitted within 200 feet of the Fort Pickens fishing pier, and the "
          "designated swim beaches are closed to fishing when lifeguards are on duty.")
z["flag"] = ("UNRESOLVED: a projectile-gear ban published in 2021 does not appear in the 1 Sep 2026 compendium. A "
             "missing clause on a web page is not proof of rescission. Call Gulf Islands National Seashore "
             "(850-934-2600). The water boundary runs one mile seaward of the low tide line at Perdido Key, Fort "
             "Pickens and Santa Rosa, and 100 yards at Naval Live Oaks; the NPS polygon drawn here should be "
             "checked against that description.")

# Monroe canals: Marathon's section is now known.
z = Z["mon26"]
z["law"] = [i if i != "marathon-canal" else "marathon-18-27" for i in z["law"]]
if z.get("flag") and "Marathon" in z["flag"]:
    z["flag"] = z["flag"].replace("Canals inside the City of Marathon are also covered by the ban per the Monroe State "
                                  "Attorney, but Marathon’s own code section has not been located.",
                                  "Canals inside the City of Marathon are covered by City of Marathon Code § 18-27, read "
                                  "verbatim on 30 Sep 2026.")

# Biscayne NP: Legare Anchorage is now drawn; the channel dive closure and the state rule closures are new.
z = Z["npsbisc"]
z["law"] = ["bnp-status", "bnp-compendium-dive", "fac-68b-7-008-5", "fac-68b-7-008-1", "cfr-36-2-3"]
z["s"] = ("No federal regulation bans spearfishing in the park, but it is <b>not open everywhere</b>. The "
          "Superintendent's Compendium closes swimming, snorkeling and diving within <b>100 feet of every marked "
          "navigational channel</b>, in Boca Chita, Elliott Key and Convoy Point harbors, and at Legare "
          "Anchorage (drawn separately). State rule 68B-7.008 closes a bonefish area to <b>all fishing 1 March "
          "to 31 May</b> and five reef areas to lobster (drawn separately). The 2015 General Management Plan "
          "marine reserve was never implemented as a spearfishing closure.")
z["flag"] = ("The 100-foot marked-channel dive closure is not drawn: it needs a channel or aids-to-navigation "
             "layer for the park. Treat every marked channel as closed to diving.")

# Dry Tortugas: add the Research Natural Area.
z = Z["npsdrto"]
if "cfr-36-7-27-rna" not in z["law"]:
    z["law"] = z["law"] + ["cfr-36-7-27-rna"]
if "Research Natural Area" not in z["s"]:
    z["s"] += (" The <b>Research Natural Area</b> (the northwest 46 square miles, south line 24°36′N from "
               "82°51′W to 82°58′W) is closed to all fishing and anchoring; mooring buoys are mandatory. Night "
               "diving beyond 1 nm of Garden Key Light needs a permit (compendium, 31 Aug 2026).")

# Presidential Security Zone, East: no-entry since 5 Sep 2025.
z = Z["pszeast"]
z["law"] = ["cfr-33-165-785"]
z["s"] = ("<b>Entry prohibited</b> without Captain of the Port authorization when the zone is enforced "
          "(since 5 Sep 2025; previously steady-speed transit). Enforced when the President, First Family or "
          "other Secret Service protectees are present or expected. COTP Miami (305) 535-4472, VHF 16.")
z["src"] = ("Coordinates verbatim from 33 C.F.R. § 165.785 as amended by USCG-2025-0319, 90 FR 42814. The "
            "printed East zone Point 2 reads 80°20′9″W, a typo for 80°02′09″W; the drawing uses 80°02′09″W.")
for k in ("pszcenter", "pszwest"):
    Z[k]["law"] = ["cfr-33-165-785"]

# Key Colony Beach: park swimming ban cross-reference.
if "kcb-12-9" not in Z["kcb5"]["law"]:
    Z["kcb5"]["law"].append("kcb-12-9")

# Treasure Island: § 58-34 now read verbatim; § 22-2 citywide discharge ban.
if "ti-22-2" not in Z["ti58"]["law"]:
    Z["ti58"]["law"].append("ti-22-2")

d["version"] = "2026-09-30"
io.open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
law = {e["id"] for e in json.load(io.open(os.path.join(ROOT, "data", "law.json"), encoding="utf-8"))["entries"]}
bad = [(z["id"], i) for z in d["zones"] for i in z["law"] if i not in law]
assert not bad, bad
print("zones-local patched:", len(d["zones"]))
