# -*- coding: utf-8 -*-
"""Legal currency pass of 7 Oct 2026: season and sweep edits to the hand-maintained files.

Edits data/regs.json, data/coverage.json and both species files (data/species.json and
tools/src-2026-09-30/species.json, which carry identical species content) by key and id. Every edit
asserts that the old text is present before replacing it, and skips when the new text is already in
place, so a second run changes nothing. Sources: research-state.md section A.2 (every "NOW" row, plus
the two citation fixes it marks OK), research-federal.md (Gulf Islands "Federal parks" sweep) and
research-local.md (the ch. 59-1702 sweep and the new local rules), all in the 7 Oct 2026 staging pass.

Wording rule: the map's own voice states only what is closed or restricted. Season fields that said only
when a species is open are set to null where the region's `closed` field already states the closure;
js/species.js renders null as an empty cell.
"""
import io
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
N = [0]


def rep(obj, key, old, new, where):
    """Replace a whole value."""
    cur = obj.get(key)
    if cur == new:
        return
    assert cur == old, (where, key, cur)
    obj[key] = new
    N[0] += 1


def sub(obj, key, old, new, where):
    """Replace a substring; skipped when the new text is already present."""
    cur = obj.get(key) or ""
    if new in cur:
        return
    assert old in cur, (where, key, old[:60])
    obj[key] = cur.replace(old, new)
    N[0] += 1


def add_law(s, ids):
    for i in ids:
        if i not in s["law"]:
            s["law"].append(i)
            N[0] += 1


# ------------------------------------------------------------------ species (both copies)
OPEN_SWG = "Recurring: May 1 to Dec 31. 2026: open May 1 to Dec 31, 2026."
OLD_20F = ("Recurring: closed Feb 1 to Mar 31 seaward of the 20-fathom line (622.34(d)). Amendment 62 proposes "
           "removing this closure (91 FR 41611, proposed Jul 2026; final status not checked).")
OLD_20F_OTHER = OLD_20F + (" From Jan 1, 2027: closed Jan 1 to Jun 30 each year in the Gulf EEZ (Other SWG complex, "
                           "91 FR 36545).")
NEW_20F_OTHER = ("Closed 1 Jan to 30 Jun every year from 1 Jan 2027 (§ 622.34(h), 91 FR 36545). The former 1 Feb to "
                 "31 Mar closure beyond 20 fathoms was removed effective 2 Oct 2026 (91 FR 63502).")
NEW_20F_RED = ("No closed season. The former 1 Feb to 31 Mar closure beyond 20 fathoms was removed effective 2 Oct "
               "2026 (91 FR 63502).")


def species(d):
    S = {s["id"]: s for s in d["species"]}
    touched = set()

    def R(i, region, key, old, new):
        rep(S[i]["regions"][region], key, old, new, i + "/" + region)
        touched.add(i)

    def U(i, region, key, old, new):
        sub(S[i]["regions"][region], key, old, new, i + "/" + region)
        touched.add(i)

    # red snapper
    R("red-snapper", "atlantic", "season",
      "2026: Oct 9 to Oct 22, 2026 (EO 26-33). A second season in Dec 2026 is possible if NMFS agrees.",
      "Closed outside 9 to 22 Oct 2026 (EO 26-33). FWC may announce a December 2026 season.")
    R("red-snapper", "gulf", "season",
      "2026 (private vessels, state and federal waters): May 22 to Jul 31; Sep 1 to Oct 4; Oct 9 to 25; Oct 30 to "
      "Nov 1; Nov 7 to 8, 14 to 15, 21 to 22, 26 to 29; Dec 5 to 6, 12 to 13, 19 to 20, 25 to 27, 2026; Jan 1 to 4, "
      "2027.",
      "Closed 5 to 8 Oct, 26 to 29 Oct, 2 to 6 Nov, 9 to 13 Nov, 16 to 20 Nov, 23 to 25 Nov, 30 Nov to 4 Dec, 7 to "
      "11 Dec, 14 to 18 Dec, 21 to 24 Dec and 28 to 31 Dec 2026, and from 5 Jan 2027 until FWC announces the 2027 "
      "season (FWC notice under r. 68B-14.0038(1), secondary).")
    R("red-snapper", "eez_sa", "season",
      "2026 federal season: Oct 9 to 12:01 a.m. Oct 12, 2026 (91 FR 60334). Florida EFP trips: Oct 9 to 22, 2026.",
      "Closed outside 12:01 a.m. 9 Oct to 12:01 a.m. 12 Oct 2026 (91 FR 60334), except on Florida "
      "exempted-fishing-permit trips, which close after 22 Oct 2026.")

    # gag
    sub(S["gag"], "spear_note",
        "Spear harvest only in the short 2026 open seasons; closed otherwise; closed on 30 Sep 2026 in the Atlantic, "
        "last open day in the Gulf.",
        "Closed in the Atlantic and all Monroe waters from 2 Aug 2026 to 30 Apr 2027, and in the Gulf from 1 Oct "
        "2026 to 31 Aug 2027.", "gag")
    touched.add("gag")
    R("gag", "atlantic", "season", "Recurring: opens May 1. 2026: May 1 to Aug 1, 2026.",
      "Closed from 2 Aug 2026 to 30 Apr 2027. The 2027 closing date has not been set.")
    R("gag", "gulf", "season",
      "Rule default Sep 1 to Nov 10 (r. 68B-14.0039(1)). 2026: Sep 1 to Sep 30, 2026 (EO 26-26).",
      "Closed from 1 Oct 2026 (EO 26-26, to 31 Dec 2026) and under the rule closed outside 1 Sep to 10 Nov "
      "(r. 68B-14.0039(1)): closed 1 Oct 2026 to 31 Aug 2027 unless FWC changes the 2027 dates.")
    R("gag", "gulf", "closed", "2026: closes 12:01 a.m. Oct 1, 2026.",
      "Closed 12:01 a.m. 1 Oct 2026 to 31 Aug 2027 (EO 26-26; then r. 68B-14.0039(1)).")
    R("gag", "keys", "season", "2026: May 1 to Aug 1, 2026.", "Closed from 2 Aug 2026 to 30 Apr 2027.")
    U("gag", "keys", "closed", "(EO 26-10 names 'all state waters off Monroe County')",
      "(EO 26-10: 'including all state waters of Monroe County')")
    R("gag", "eez_sa", "season", "2026: May 1 to Aug 1, 2026.",
      "Closed from 12:01 a.m. 2 Aug 2026 to 30 Apr 2027 (91 FR 21389; then § 622.183(b)(1)).")
    R("gag", "eez_gulf", "season", "2026: Sep 1 to 12:01 a.m. Oct 1, 2026 (91 FR 29920).",
      "Closed from 12:01 a.m. 1 Oct 2026 to 31 Aug 2027 (91 FR 29920; then § 622.34(e)).")

    # Atlantic shallow-water grouper: the open-season line repeats the closure in `closed`
    for i in ("black-grouper", "red-grouper", "scamp", "yellowfin-grouper", "yellowmouth-grouper", "red-hind",
              "rock-hind", "graysby", "coney"):
        for region in ("atlantic", "keys", "eez_sa"):
            R(i, region, "season", OPEN_SWG, None)

    # Gulf EEZ: 20-fathom closure removed by 91 FR 63502 (effective 2 Oct 2026)
    for i in ("black-grouper", "scamp", "yellowfin-grouper", "yellowmouth-grouper"):
        R(i, "eez_gulf", "closed", OLD_20F_OTHER, NEW_20F_OTHER)
        add_law(S[i], ["fr-91-63502", "fr-91-36545"])
    R("red-grouper", "eez_gulf", "closed", OLD_20F, NEW_20F_RED)
    add_law(S["red-grouper"], ["fr-91-63502"])

    # snowy grouper
    R("snowy-grouper", "atlantic", "season", "Recurring: May 1 to Jun 30 (r. 68B-14.0039(4)). 2026: May 1 to Jun 6, 2026.",
      "Closed outside 1 May to 30 Jun every year (r. 68B-14.0039(4)); in 2026 closed from 7 Jun (EO 26-18).")

    # hogfish
    sub(S["hogfish"], "spear_note", "Atlantic and Keys: open May 1 to Oct 31 only.",
        "Atlantic and Keys: closed 1 Nov to 30 Apr every year.", "hogfish")
    touched.add("hogfish")
    R("hogfish", "atlantic", "season", "Recurring: May 1 to Oct 31 (r. 68B-14.0042(1)). 2026: May 1 to Oct 31, 2026.",
      "Closed 1 Nov 2026 to 30 Apr 2027.")
    R("hogfish", "keys", "season", "2026: May 1 to Oct 31, 2026.", "Closed 1 Nov 2026 to 30 Apr 2027.")
    R("hogfish", "eez_sa", "season", "2026: May 1 to Oct 31, 2026.", "Closed 1 Nov 2026 to 30 Apr 2027.")

    # greater amberjack
    R("greater-amberjack", "gulf", "season", "2026: Sep 1 to Oct 13, 2026 (EO 26-25).",
      "Closed from 12:01 a.m. 14 Oct 2026 to 31 Aug 2027.")
    U("greater-amberjack", "gulf", "closed",
      "2026: closed 12:01 a.m. Oct 14, 2026 through Aug 31, 2027 (EO 26-25).",
      "2026: closed 12:01 a.m. Oct 14, 2026 through Aug 31, 2027 (EO 26-25). (EO 26-25 expires 1 Nov 2026; the "
      "rule closure continues.)")
    R("greater-amberjack", "eez_gulf", "season", "2026: Sep 1 to 12:01 a.m. Oct 14, 2026 (NOAA FB26-029).",
      "Closed from 12:01 a.m. 14 Oct 2026 to 31 Aug 2027 (temporary rule 91 FR 32360 to 31 Jul 2027; then "
      "§ 622.34(c)).")
    R("greater-amberjack", "atlantic", "season", "Open Jan to Mar and May to Dec.", None)
    R("greater-amberjack", "eez_sa", "season", "Open outside April.", None)
    add_law(S["greater-amberjack"], ["fr-91-32360"])

    # open-only season phrasing where `closed` already states the closure
    R("gray-triggerfish", "gulf", "season", "Open Mar 1 to May 31 and Aug 1 to Dec 31.", None)
    R("gray-triggerfish", "eez_gulf", "season", "Open Mar 1 to May 31 and Aug 1 to Dec 31.", None)
    R("flounder", "atlantic", "season", "Open Dec 1 to Oct 14. 2026: open through Oct 14, 2026.", None)
    R("flounder", "gulf", "season", "Open Dec 1 to Oct 14. 2026: open through Oct 14, 2026.", None)
    R("red-porgy", "atlantic", "season", "Recurring: May 1 to Jun 30 (r. 68B-14.0043(1)). 2026: May 1 to Jun 30, 2026.",
      None)
    R("blueline-tilefish", "atlantic", "season",
      "Recurring: May 1 to Aug 31 (r. 68B-14.0039(5)). 2026: May 1 to Aug 31, 2026.", None)
    R("blueline-tilefish", "eez_sa", "season", "Recurring: May 1 to Aug 31.", None)
    R("yellowedge-misty-grouper", "atlantic", "season",
      "Open year-round (not in the Atlantic Jan to Apr closure list).", None)

    for i in touched:
        if S[i].get("checked") != "2026-10-07":
            S[i]["checked"] = "2026-10-07"
    d["version"] = "2026-10-07"


for p, kw in (("data/species.json", dict(ensure_ascii=False, separators=(",", ":"))),
              ("tools/src-2026-09-30/species.json", dict(ensure_ascii=False, indent=1))):
    fp = os.path.join(ROOT, p)
    d = json.load(io.open(fp, encoding="utf-8"))
    species(d)
    io.open(fp, "w", encoding="utf-8").write(json.dumps(d, **kw))

# ------------------------------------------------------------------ regs.json
fp = os.path.join(ROOT, "data", "regs.json")
R = json.load(io.open(fp, encoding="utf-8"))


def section(name, heading):
    for row in R[name]:
        if row[0] == heading:
            return row
    raise KeyError((name, heading))


def body(name, heading, old, new):
    row = section(name, heading)
    if row[1] == new:
        return
    assert row[1] == old, (name, heading, row[1][:80])
    row[1] = new
    N[0] += 1


def bsub(name, heading, old, new):
    row = section(name, heading)
    if new in row[1]:
        return
    assert old in row[1], (name, heading, old[:60])
    row[1] = row[1].replace(old, new)
    N[0] += 1


body("seasons", "Read this first",
     "Values below are for <b>2026</b> and were checked on 30 Sep 2026. Seasons move by FWC executive order and "
     "federal temporary rule; check FWC and NOAA before every trip. Where a date comes from an FWC notice or news "
     "release rather than the text of an order or rule, it says so.",
     "Values below were checked on <b>7 Oct 2026</b>. Seasons move by FWC executive order and federal temporary "
     "rule; check FWC and NOAA before every trip. Where a date comes from an FWC notice or news release rather than "
     "the text of an order or rule, it says so.")
body("seasons", "Gag",
     "24 in TL. <b>Atlantic state waters, including all of Monroe, and South Atlantic federal waters: closed since 2 "
     "Aug 2026 for the rest of 2026</b> (FWC EO 26-10, dates from FWC's announcement; 50 C.F.R. closure 91 FR 21389). "
     "<b>Gulf state waters</b> (not Monroe): open 1 to 30 Sep 2026 only, <b>closed from 1 Oct 2026</b> (EO 26-26, "
     "from FWC's announcement). Gulf federal waters closed 1 Oct to 31 Dec 2026 (91 FR 29920).",
     "24 in TL. <b>Atlantic state waters, including all of Monroe, and South Atlantic federal waters: closed from 2 "
     "Aug 2026 to 30 Apr 2027</b> (FWC EO 26-10 to 31 Dec, then r. 68B-14.0039(2); 91 FR 21389, then 50 C.F.R. "
     "§ 622.183(b)(1)). The 2027 closing date has not been set. <b>Gulf state waters</b> (not Monroe) <b>and Gulf "
     "federal waters: closed from 1 Oct 2026 to 31 Aug 2027</b> (EO 26-26 to 31 Dec, then r. 68B-14.0039(1); "
     "91 FR 29920, then § 622.34(e)).")
body("seasons", "Red snapper",
     "<b>Atlantic:</b> state season <b>9 to 22 Oct 2026</b>, 1 fish, no minimum size, hook and line, bandit gear, "
     "handline or spear only, trip declaration required; closed outside those dates (FWC EO 26-33, read from the "
     "order). Federal South Atlantic season 9 Oct to 12:01 a.m. 12 Oct 2026 (91 FR 60334); Florida "
     "exempted-fishing-permit trips run to 22 Oct. <b>Gulf</b> (FWC notice, secondary): open through 4 Oct; 9 to 25 "
     "Oct; 30 Oct to 1 Nov; 7 to 8, 14 to 15, 21 to 22 and 26 to 29 Nov; 5 to 6, 12 to 13, 19 to 20 and 25 to 27 Dec "
     "2026; 1 to 4 Jan 2027. 16 in TL, 2 fish.",
     "<b>Atlantic, state and federal waters: closed outside 9 to 22 Oct 2026</b>; 1 fish, no minimum size, hook and "
     "line, bandit gear, handline or spear only, trip declaration required (FWC EO 26-33, read from the order). "
     "Federal waters close at 12:01 a.m. 12 Oct 2026 except on Florida exempted-fishing-permit trips, which run to "
     "22 Oct (91 FR 60334). A December season is possible but not announced. <b>Gulf</b>, private vessels, state "
     "and federal waters (FWC notice, secondary): <b>closed 5 to 8 Oct, 26 to 29 Oct, 2 to 6 Nov, 9 to 13 Nov, 16 "
     "to 20 Nov, 23 to 25 Nov, 30 Nov to 4 Dec, 7 to 11 Dec, 14 to 18 Dec, 21 to 24 Dec and 28 to 31 Dec 2026, and "
     "from 5 Jan 2027</b> until FWC announces the 2027 season. 16 in TL, 2 fish.")
body("seasons", "Hogfish",
     "<b>Atlantic and Keys</b> (and Gulf waters south of 25°09′ N): open 1 May to 31 Oct only, <b>closes 1 Nov "
     "2026</b>, r. 68B-14.0042 and 50 C.F.R. § 622.183(b)(4). 16 in fork, <b>one fish</b>. Gulf north of 25°09′ N: "
     "14 in fork, 5 fish, open all year.",
     "<b>Atlantic and Keys</b> (and Gulf waters south of 25°09′ N), state and federal waters: <b>closed 1 Nov to 30 "
     "Apr every year</b>; in 2026 to 2027, closed 1 Nov 2026 to 30 Apr 2027. r. 68B-14.0042 and 50 C.F.R. "
     "§ 622.183(b)(4). 16 in fork, <b>one fish</b>. Gulf north of 25°09′ N: 14 in fork, 5 fish, no closed season.")
body("seasons", "Shallow-water grouper",
     "Atlantic and all Monroe waters: gag, black, red, scamp, yellowfin, yellowmouth, red hind, rock hind, coney and "
     "graysby closed 1 Jan to 30 Apr, r. 68B-14.0039(2). 3-grouper aggregate in the Atlantic and Monroe, 4 in the "
     "Gulf. Gulf federal waters beyond 20 fathoms closed 1 Feb to 31 Mar. <b>From 1 Jan 2027</b> Gulf federal waters "
     "close to black grouper, scamp, yellowfin and yellowmouth grouper from 1 Jan to 30 Jun each year (91 FR 36545, "
     "from NOAA's bulletin).",
     "Atlantic and all Monroe waters: gag, black, red, scamp, yellowfin, yellowmouth, red hind, rock hind, coney and "
     "graysby closed 1 Jan to 30 Apr, r. 68B-14.0039(2). 3-grouper aggregate in the Atlantic and Monroe, 4 in the "
     "Gulf. <b>From 1 Jan 2027 Gulf federal waters are closed to black grouper, scamp, yellowfin and yellowmouth "
     "grouper from 1 Jan to 30 Jun every year</b> (50 C.F.R. § 622.34(h), 91 FR 36545). The Gulf federal closure "
     "beyond 20 fathoms (1 Feb to 31 Mar) was removed effective 2 Oct 2026 (91 FR 63502). The Edges stays closed to "
     "all fishing 1 Jan to 30 Apr.")
body("seasons", "Greater amberjack",
     "Atlantic: 28 in fork, 1 fish, closed in April. <b>Gulf: 34 in fork, 1 fish; the 2026 season closes 14 Oct "
     "2026</b> and stays closed through 31 Aug 2027 in state waters (FWC EO 26-25, read from the order); federal Gulf "
     "waters close the same day (NOAA Fisheries Bulletin FB26-029).",
     "Atlantic: 28 in fork, 1 fish, closed in April. <b>Gulf: 34 in fork, 1 fish; state and federal waters closed "
     "from 14 Oct 2026 to 31 Aug 2027</b> (FWC EO 26-25 to 1 Nov 2026, then r. 68B-14.004(1); federal temporary rule "
     "91 FR 32360 to 31 Jul 2027, then 50 C.F.R. § 622.34(c)).")

# statewide notes
bsub("statewide", "Manatee zones: state No Entry and federal sanctuaries",
     "r. 68C-22.002(11): 21 zones in 10 counties, most at power-plant canals;",
     "r. 68C-22.002(11): 20 zones in 9 counties, most at power-plant canals (the Vero Beach power-plant zone in "
     "Indian River County became Idle Speed all year on 30 Jun 2026 and no longer bars divers);")
bsub("statewide", "National parks",
     "<b>Gulf Islands National Seashore:</b> the 2021 Superintendent's Compendium banned pole spears, spear guns, "
     "Hawaiian slings and any other projectile device in all Seashore waters, but the compendium updated 1 Sep 2026 "
     "no longer contains that provision and the park's fishing page refers spearfishing questions to FWC. Status "
     "unresolved: call the park at 850-934-2600 before spearing within one mile of Perdido Key, Fort Pickens or "
     "Santa Rosa Island.",
     "<b>Gulf Islands National Seashore:</b> the 2021 Superintendent's Compendium banned pole spears, spear guns, "
     "Hawaiian slings and any other projectile device in all Seashore waters. The compendium updated 1 Sep 2026, "
     "read in full on 7 Oct 2026, has no spearfishing or projectile rule, so the park adds no spear closure of its "
     "own and Florida's rules apply (36 C.F.R. § 2.3(e)). Fishing is closed at the Fort Pickens and Ship Island "
     "ferry docks, the Davis Bayou boat ramp dock, the Ship Island boardwalk and the designated swim beaches while "
     "lifeguards are on duty, and diving is prohibited within 200 ft of the Fort Pickens fishing pier. Two stale "
     "nps.gov pages still print the 2021 ban: call the park at 850-934-2600 to confirm it was rescinded. Seashore "
     "water runs one mile from the low tide line at Perdido Key, Fort Pickens and Santa Rosa, and 100 yards at "
     "Naval Live Oaks.")
bsub("statewide", "Monroe County canals",
     "City Code § 18-27 (read 30 Sep 2026).",
     "City Code § 18-27 (read 30 Sep 2026). Around the lobster seasons, Monroe County Code § 26-98 bars diving and "
     "snorkeling in any manmade water body or marina and within 300 ft of improved residential or commercial "
     "shoreline, from three days before the mini-season through the first five days of the commercial season, in "
     "incorporated and unincorporated Monroe County (read 7 Oct 2026; not drawn).")
bsub("statewide", "Local ordinances",
     "Every local rule is treated as live. See the county notes.",
     "Browser reads on 7 Oct 2026 added Hollywood (no spearfishing within 100 yards of the public beach), Pinellas "
     "County (no spearing in any manmade saltwater canal), Naples (no swimming within 100 ft of a public bridge), "
     "Town of Palm Beach (no fishing off or within 50 yards of a guarded beach), Deerfield Beach (no swimming beyond "
     "50 yards of the city beach without lifeguard permission) and St. Petersburg (no fishing in park waters unless "
     "signed); they are in the citation registry and not yet drawn. Every local rule is treated as live. See the "
     "county notes.")

# county notes
C = R["counties"]


def csub(county, old, new):
    sub(C[county], "txt", old, new, county)


csub("Palm Beach",
     "PBC Code App. G ch. 13 art. II (Laws of Fla. 59-1699, 59-1702): a night ban (§ 13-32), an absolute inlet ban "
     "(§ 13-33), diver-flag rules (§§ 13-36 to 13-38), a 150 ft standoff from anchored boats (§ 13-35), no sale of "
     "speared fish (§ 13-58), and <b>two refuge areas where spearfishing on underwater breathing apparatus is "
     "prohibited</b> (§§ 13-55, 13-56).",
     "PBC Code App. G ch. 13 art. II. From Laws of Fla. ch. 59-1702 (§§ 13-31 to 13-39): <b>no underwater "
     "spearfishing in any county salt water from one hour after sunset to one hour before sunrise</b> (§ 13-32), "
     "<b>none at any time within any inlet in the county</b>, Jupiter, Lake Worth, South Lake Worth (Boynton) and "
     "Boca Raton (§ 13-33; drawn so far only at Lake Worth Inlet), diver-flag rules (§§ 13-36 to 13-38) and a 150 ft "
     "standoff from anchored boats (§ 13-35); these reach freedivers too. From ch. 59-1699 (§§ 13-54 to 13-59): no "
     "sale of speared fish (§ 13-58) and <b>two refuge areas where spearfishing on underwater breathing apparatus is "
     "prohibited</b> (§§ 13-55, 13-56).")
csub("Palm Beach",
     "§ 74-200 sets buddy, certification, BC and flag requirements for diving off guarded beaches.",
     "§ 74-200 sets buddy, certification, BC and flag requirements for diving off guarded beaches. Read 7 Oct 2026: "
     "§ 74-162(e) bars fishing in the waters off any guarded Town beach and 50 yards north or south of it, and "
     "§ 74-197 bars swimming more than 300 ft from mean low water off a guarded beach (not drawn).")
csub("Martin",
     "Martin County code: no spear rule found in a whole-code search (30 Sep 2026).",
     "Martin County code: no spear rule found in a whole-code search (30 Sep 2026; repeated 7 Oct 2026 across the "
     "code, the land development regulations and the comprehensive plan). The old fish and wildlife chapter 83 was "
     "repealed on 21 Oct 2025; chapter 83 now limits saltwater fishing from county bridges to one pole.")
csub("Broward",
     "Hallandale Beach, no spearfishing or scuba on the public beach;",
     "Hallandale Beach, no spearfishing or scuba on the public beach except in a designated area (none in the "
     "code);")
csub("Broward",
     "Deerfield Beach, no snorkeling within 50 yards of the pier.",
     "Deerfield Beach, no snorkeling within 50 yards of the pier, no swimming more than 50 yards off the city beach "
     "without the lifeguard's permission, and no fishing off the beach from 8 a.m. to dusk (§ 50-112(b), (p), read "
     "7 Oct 2026). <b>Hollywood:</b> § 99.03(F), spearfishing is prohibited within 100 yards of the public beach, "
     "which runs from the Hallandale line to John U. Lloyd Beach State Park and 50 yards offshore; loaded spearguns "
     "are barred on the beach and in public swimming areas (read 7 Oct 2026; not yet drawn).")
csub("Broward",
     "Fort Lauderdale, Hillsboro Beach and county codes negative; Hollywood and Lighthouse Point not yet read.",
     "Fort Lauderdale, Hillsboro Beach and county codes negative; Lighthouse Point not yet read, and Hollywood's "
     "code outside the beach chapter not yet searched.")
csub("Monroe",
     "Gag closed in all Monroe state waters since 2 Aug 2026.",
     "Gag closed in all Monroe state waters from 2 Aug 2026 to 30 Apr 2027.")
csub("Monroe",
     "A county 300 ft lobster-season diving rule is reported but not read.",
     "<b>Lobster seasons:</b> Monroe County Code § 26-98 bars diving and snorkeling in any manmade water body or "
     "marina and within 300 ft of improved residential or commercial shoreline, from three days before the "
     "mini-season through the first five days of the commercial season, in the cities too unless a city ordinance "
     "conflicts (read 7 Oct 2026; not drawn, because no dataset marks improved shoreline). No county bridge diving "
     "ban is codified.")
csub("Collier",
     "<b>Naples:</b> § 42-52, no spearfishing or gigging within 100 ft of the city pier (read 30 Sep 2026).",
     "<b>Naples:</b> § 42-52, no spearfishing or gigging within 100 ft of the city pier (read 30 Sep 2026), and "
     "§ 42-3, no swimming within 100 ft of any public bridge in the city (read 7 Oct 2026; not drawn).")
csub("Pinellas",
     "Not yet read: Pinellas County, St. Petersburg, Tarpon Springs, the Redingtons.",
     "<b>Pinellas County:</b> § 14-97 (Ord. 25-28, Dec 2025) allows only hook and line, a handheld cast net or "
     "blue-crab traps in any manmade saltwater canal in the county, so <b>spearing is excluded in every manmade "
     "canal</b>, apparently inside cities too (read 7 Oct 2026; not drawn). <b>St. Petersburg:</b> § 21-44 bars "
     "fishing by any method in city park waters unless signs designate otherwise (read 7 Oct 2026; not drawn). Not "
     "yet read: Tarpon Springs, the Redingtons.")
csub("Indian River",
     "The Vero Beach power-plant manatee zone was probably changed from No Entry to Idle Speed on 30 Jun 2026.",
     "The Vero Beach power-plant canals were a seasonal manatee No Entry zone until 30 Jun 2026; they are now Idle "
     "Speed all year, r. 68C-22.007(1)(a)7., which does not bar divers.")
for county in ("Santa Rosa", "Escambia"):
    csub(county,
         "the 1 Sep 2026 compendium does not repeat it, so the status is unresolved (call 850-934-2600)",
         "the 1 Sep 2026 compendium, read in full on 7 Oct 2026, has no spear or projectile rule; two stale nps.gov "
         "pages still print the ban, so call 850-934-2600 to confirm it was rescinded")

io.open(fp, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1))

# ------------------------------------------------------------------ coverage.json
fp = os.path.join(ROOT, "data", "coverage.json")
V = json.load(io.open(fp, encoding="utf-8"))
T = V["tiers"]
sub(T["none"], "body",
    "26 jurisdictions still need a browser read and some bay-side towns were not checked.",
    "Browser reads on 7 Oct 2026 covered the Town of Palm Beach, Martin County, Pinellas County, St. Petersburg, "
    "Naples, Hollywood's beach chapter, Santa Rosa County and the Santa Rosa Island Authority; the rules they turned "
    "up (Hollywood's 100-yard beach ban, Pinellas County's canal gear rule, Naples' bridge swimming ban, St. "
    "Petersburg's park-water fishing ban) are in the citation registry but not yet drawn. The rest of the 26 "
    "jurisdictions listed on 30 Sep 2026 still need a browser read, and some bay-side towns were not checked.",
    "tiers.none")
sub(T["partial"], "body",
    "and a reported county 300 ft lobster-season diving rule has not been read.",
    "and the county's 300 ft lobster-season diving and snorkeling rule (§ 26-98, read 7 Oct 2026) is not drawn "
    "because no dataset marks improved shoreline.",
    "tiers.partial")
sub(T["full"], "body",
    "which is not drawn, and posted signage",
    "which is not drawn. The 7 Oct 2026 pass found that the county's § 13-33 inlet ban reaches every inlet in the "
    "county: Jupiter Inlet and South Lake Worth (Boynton) Inlet are not yet drawn, and neither are the Town of Palm "
    "Beach's guarded-beach fishing and swimming limits (§§ 74-162(e), 74-197). Posted signage",
    "tiers.full")
G = {g["id"]: g for g in V["regions"]}
sub(G["cov-full-pbc"], "detail",
    "the § 13-33 inlet ban in both readings,",
    "the § 13-33 inlet ban at Lake Worth Inlet in both readings (the ban covers every county inlet; Jupiter Inlet "
    "and South Lake Worth Inlet are not yet drawn, 7 Oct 2026),",
    "cov-full-pbc")
sub(G["cov-full-pbc"], "detail",
    "South Palm Beach, Manalapan and Tequesta: no spear rule.",
    "South Palm Beach, Manalapan and Tequesta: no spear rule. Read 7 Oct 2026, not drawn: Town of Palm Beach "
    "§ 74-162(e) (no fishing off or within 50 yards of a guarded beach) and § 74-197 (no swimming beyond 300 ft of "
    "a guarded beach).",
    "cov-full-pbc")
sub(G["cov-part-monroe"], "detail",
    "the county's reported 300 ft lobster-season diving rule,",
    "the county's 300 ft lobster-season diving and snorkeling rule (§ 26-98, read 7 Oct 2026; no dataset marks "
    "improved shoreline),",
    "cov-part-monroe")
if V.get("generated") != "2026-10-07":
    V["generated"] = "2026-10-07"
    N[0] += 1
io.open(fp, "w", encoding="utf-8").write(json.dumps(V, ensure_ascii=False, indent=1))

print("patch-2026-10-07: %d change(s)" % N[0])
