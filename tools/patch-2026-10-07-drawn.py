#!/usr/bin/env python3
"""7 Oct 2026, second step: text that said the Hollywood beach ban and the Jupiter and South Lake Worth
inlet bans were "not yet drawn", updated once tools/geometry/2026-10-07/new-zones.json added them to
zones-statewide.json. Run after tools/patch-2026-10-07.py. Idempotent: asserts each old text or its
replacement is present."""
import io, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EDITS = {
 "data/regs.json": [
  ("Browser reads on 7 Oct 2026 added Hollywood (no spearfishing within 100 yards of the public beach), Pinellas County",
   "Browser reads on 7 Oct 2026 added Hollywood (no spearfishing within 100 yards of the public beach, drawn), Pinellas County"),
  ("(read 7 Oct 2026; not yet drawn)",
   "(read 7 Oct 2026; drawn 175 yards from the chart coastline, the 150 yards of the rule plus margin)"),
  ("(§ 13-33; drawn so far only at Lake Worth Inlet)",
   "(§ 13-33; drawn at Jupiter, Lake Worth and South Lake Worth inlets, the broader reading of 'inlet'; Boca Raton Inlet is also closed by the city)"),
 ],
 "data/coverage.json": [
  ("the rules they turned up (Hollywood's 100-yard beach ban, Pinellas County's canal gear rule, Naples' bridge swimming ban, St. Petersburg's park-water fishing ban) are in the citation registry but not yet drawn.",
   "Hollywood's 100-yard beach ban is drawn; the other rules they turned up (Pinellas County's canal gear rule, Naples' bridge swimming ban, St. Petersburg's park-water fishing ban) are in the citation registry but not yet drawn."),
  ("Jupiter Inlet and South Lake Worth (Boynton) Inlet are not yet drawn, and neither are the Town of Palm Beach's",
   "Jupiter Inlet and South Lake Worth (Boynton) Inlet are now drawn from the chart; the Town of Palm Beach's"),
  ("guarded-beach fishing and swimming limits (§§ 74-162(e), 74-197). Posted",
   "guarded-beach fishing and swimming limits (§§ 74-162(e), 74-197) are not. Posted"),
  ("(the ban covers every county inlet; Jupiter Inlet and South Lake Worth Inlet are not yet drawn, 7 Oct 2026)",
   "(the ban covers every county inlet; Jupiter Inlet and South Lake Worth Inlet were drawn from the chart on 7 Oct 2026)"),
 ],
}
for f, pairs in EDITS.items():
    p = os.path.join(ROOT, f)
    s = io.open(p, encoding="utf-8").read()
    n = 0
    for old, new in pairs:
        if new in s:
            continue
        assert s.count(old) == 1, (f, old[:60])
        s = s.replace(old, new); n += 1
    io.open(p, "w", encoding="utf-8").write(s)
    print("%s: %d edit(s)" % (f, n))
