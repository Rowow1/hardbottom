# -*- coding: utf-8 -*-
"""Legal currency pass of 7 Oct 2026 for data/zones-local.json. Run after patch-zones-local-2026-10-06.py.

Sets the prose fields (s, flag) and law ids below, from the 7 Oct 2026 research reports. Never touches
coordinates, and never touches ti58 or 3sis. Closure-only wording, no em or en dashes. Idempotent.

  npsguis  Gulf Islands NS: the 1 Sep 2026 compendium was read in full and has no spearfishing or
           projectile rule; the water boundary is confirmed from the park's own page; the fishing and diving
           closures are listed. Still amber: the park has not confirmed the 2021 ban was rescinded.
  mon26    Monroe County Code § 26-98 (lobster-season diving and snorkeling ban) read verbatim; cited here
           as text, not drawn, because no dataset marks improved shoreline.
"""
import io
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = os.path.join(ROOT, "data", "zones-local.json")

T = {
    "npsguis": {
        "law": ["guis-compendium", "nps-guis-fishing-fl", "cfr-36-1-4-2-4", "cfr-36-2-3"],
        "s": ("The 2021 Superintendent's Compendium <b>banned spear guns, pole spears, Hawaiian slings and every "
              "other projectile device in all Seashore waters</b>. The compendium updated 1 Sep 2026, read in full on "
              "7 Oct 2026, has no spearfishing or projectile rule, so the park adds no spear closure of its own and "
              "Florida's rules and closures apply (36 C.F.R. § 2.3(e)). <b>Fishing is closed</b> at the Fort Pickens "
              "and Ship Island ferry docks, the Davis Bayou boat ramp dock, the Ship Island boardwalk and the "
              "designated swim beaches while lifeguards are on duty. <b>No diving or swimming within 200 feet of the "
              "Fort Pickens fishing pier</b>, and no persons in the water within 40 feet of the Pensacola Bay ferry "
              "dock at Quietwater Beach. Until the park confirms the 2021 ban was rescinded, treat Seashore waters as "
              "restricted."),
        "flag": ("UNCONFIRMED RESCISSION: the 2021 projectile-gear ban is not in the 1 Sep 2026 compendium, whose full "
                 "text has no spear, projectile, Hawaiian sling or section 2.3 provision, but two nps.gov pages still "
                 "print the ban (the 'Fishing at Gulf Islands National Seashore' page dated 28 Feb 2022, and an older "
                 "home.nps.gov copy of the Florida fishing page). Call Gulf Islands National Seashore (850-934-2600) "
                 "to confirm the ban was removed on purpose. The water boundary is confirmed by the park's Florida "
                 "fishing page (28 Aug 2026): north to the Gulf Intracoastal Waterway and one mile seaward of the low "
                 "tide line at Perdido Key, Fort Pickens and Santa Rosa, and 100 yards from the low tide line at Naval "
                 "Live Oaks. The NPS polygon drawn here has not been checked against that description."),
    },
    "mon26": {
        "add_law": ["monroe-26-art4"],
        "s": ("Unlawful to use, fire or discharge a speargun <b>on or below the surface of any manmade canal</b> in "
              "unincorporated Monroe County. The § 26-1 definition catches any device that can propel a projectile "
              "more than <b>24 inches</b>, pole spears and Hawaiian slings included, regardless of power source. "
              "Conviction forfeits the gun to the Sheriff for destruction. <b>Lobster seasons:</b> from three days "
              "before the mini-season through the first five days of the commercial lobster season, <b>no diving or "
              "snorkeling at all</b> in any manmade water body or marina, or within 300 ft of improved residential or "
              "commercial shoreline, anywhere in Monroe County unless a city ordinance conflicts (§ 26-98)."),
        "flag": ("PARTIAL COVERAGE, and drawn as centrelines rather than water polygons. NHD canal coverage in the "
                 "Keys is not complete: it maps the residential canal subdivisions, but some waterways the earlier "
                 "OpenStreetMap layer showed as canals are not NHD canals, about 10 km in all, mostly around the Key "
                 "West island group. This pull covers the LOWER Keys only. That is the stretch "
                 "that matters, because everything above Long Key is already closed by Fla. Stat. § 379.2425. Canals "
                 "inside the City of Marathon are covered by City of Marathon Code § 18-27, read verbatim on 30 Sep "
                 "2026. Absence of a line here is not evidence that a canal is unrestricted. The seasonal § 26-98 "
                 "diving and snorkeling ban (read 7 Oct 2026) also reaches marinas, other manmade water bodies and "
                 "water within 300 ft of improved shoreline; none of that is drawn, because no dataset marks improved "
                 "shoreline."),
    },
}

d = json.load(io.open(P, encoding="utf-8"))
n = 0
for z in d["zones"]:
    t = T.get(z["id"])
    if not t:
        continue
    assert z["id"] not in ("ti58", "3sis")
    for k, v in t.items():
        if k == "add_law":
            for i in v:
                if i not in z["law"]:
                    z["law"].append(i)
                    n += 1
        elif z.get(k) != v:
            z[k] = v
            n += 1
io.open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
print("zones-local.json: 7 Oct 2026 text applied, %d field change(s)" % n)
