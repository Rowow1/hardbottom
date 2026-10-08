# Current legal review: status note

**As of 8 October 2026.** This is the standing state of the legal layer and replaces the 30 September
note. Read it before assuming anything on the map is settled. The dated accounts are
`research/legal-review-2026-09-30.md` (the statewide review), `research/currency-2026-10-07-*.md` (the
7 October legal currency pass) and `research/legal-review-2026-10-08.md` (the second review of 7 and
8 October, with the jetty and bridge work and the dive-planning tips). The flagged features and the
questions that need a person are in `research/open-questions.md`.

Nothing in this project is legal advice. Posted signage on site controls over anything on the map.

## What changed since 30 September

- **Registry:** 326 entries, version 2026-10-08, shown on the map as "Rules current as of 8 Oct 2026":
  302 `verbatim`, 24 `secondary`, none `unverified`. The 7 October pass took it from 278 to 295; the
  second review added the rest. The dated passes live in `tools/law-updates/2026-10-07/`
  (`research-*.json`, `editorial.json`, then `r1-review.json`, applied in that order by
  `tools/law_updates.py`).
- **Reading standard:** every excerpt added in October was read in the author's Chrome at the primary
  host (eCFR renderer, Online Sunshine, federalregister.gov full text, Cornell LII for Florida rules,
  Municode's content service and American Legal pages), not through a summarising fetch. The second
  review logs every passage in `reads.md`, and an independent agent re-read eight of them live.
- **Jetties:** 75 structures traced on USGS NAIP imagery and drawn with the 100 ft buffer at 150 ft;
  20 that may or may not count as jetties drawn amber; the long-jetty exception drawn at St. Marys south
  and St. Johns north only.
- **Bridges:** 1,441 of the 2,509 coastal and tidal fishable bridges now carry the 125 yd buffer along
  the traced deck. The rest keep the circle at the inventory point, with a popup note when the deck was
  not matched.
- **Zones:** Palm Beach rebuilt from the NOAA ENC coastline; Jupiter and South Lake Worth inlets,
  Hollywood's beach zone, Clearwater citywide, the Mexico Beach channel (marker), Ponce Inlet 300 ft and
  the Steinhatchee River added; Crystal River NWR closed; the Vero Beach manatee No Entry zone removed.
- **Licensing:** the zone files and `sites.json` are free of OpenStreetMap data since 7 October. The new
  `jetties.json` and the bridge deck fields are not; they are ODbL until rebuilt from ENC (backlog).

## What is verified, and how far to trust it

A `verbatim` chip now means the excerpt matched the page text at the primary host, read in a browser.
For the entries added before October, that rests on the 30 September browser check (208 matched in
full, six corrected). Secondary entries are mostly agency pages or bulletins (the Crystal River refuge
page, FWC executive orders published as images, the State Reef Fish Survey FAQ) and section text that
did not render.

Still partial: the text of r. 68B-14.0036 in force since 1 April 2026 (the .doc does not render), r.
68B-35.004(5) (the permit exception), the Naples ch. 90-469 canal table and Collier § 210-67 Exhibit A,
Melbourne Beach § 40-33 and Cocoa Beach § 5-56.

## Settled traps

These were verified and are not to be re-litigated without new primary law.

- Fla. Stat. § 379.101(33) is the salt-water definition: "Salt water", singular, tested by water that has
  become "unpalatable because of the saline content" alone. § 379.101(17) makes the Steinhatchee River
  fresh water from source to mouth; it is the only river named.
- The jetty buffer in r. 68B-20.003(2)(d) is **100 feet**. Beaches, piers and fishing bridges are 100
  **yards**.
- R. 68B-20.003(1)(a) reopens Collier County notwithstanding the statutory closure in § 379.2425.
- Palm Beach has fixed security zones under 33 C.F.R. § 165.785 at Mar-a-Lago; the East zone has been
  no-entry when enforced since September 2025.
- **Possession of a speargun on fresh water is prohibited**, r. 68A-23.002(7) ("use or possession ... in
  or upon the fresh waters of the state"). The September note that FWC overstated this is withdrawn.
- **In national parks a loaded speargun in any vessel is prohibited**, 36 C.F.R. § 2.4(c), and a speargun
  is a weapon under § 1.4.
- **The fishing preemption statute is § 379.2412**, not § 790.33 (see below).
- The fresh/salt boundary is closed as unsolvable (below).

## Currency watch

| Item | Date | What to do |
|---|---|---|
| R. 68B-14.0036, Atlantic gag and black grouper | Proposed 5 Oct 2026, notice 31448290; comments to 26 Oct 2026 | Would match the federal combined vessel limit. Read the text in force since 1 Apr 2026 and the proposal; update the species cards when adopted. |
| SA Regulatory Amendment 36, 91 FR 61160 | Effective 28 Oct 2026 | Gag and black grouper become 2 per private vessel per day combined in South Atlantic federal waters. Already in the registry and the cards; re-read § 622.187 on eCFR after 28 Oct. |
| 91 FR 36545, Gulf other shallow-water grouper | From 1 Jan 2027 | Black grouper, scamp, yellowfin and yellowmouth closed 1 Jan to 30 Jun in Gulf federal waters. Read verbatim; FWC has no matching state rule yet. |
| Gulf greater amberjack, 91 FR 32360 | 14 Oct 2026 to 31 Jul 2027, then § 622.34(c) to 31 Aug 2027 | Federal waters closed to 31 Aug 2027; state waters under EO 26-25 then r. 68B-14.004. |
| Executive Order 14430 | Signed 17 Sep 2026 | Watch the Federal Register for NOAA, FKNMS, NPS and FWS proposals that follow it. |
| FKNMS state and federal split | Ongoing | The 2025 Blueprint governs federal waters, the 1997 zoning state waters; eCFR still renders the 1997 text. Confirm with FKNMS, 305-809-4700. |
| Warsaw Hole spawning SMZ | Sunset 2 Aug 2027 | Re-check after the Council acts on Regulatory Amendment 39. |
| Western Dry Rocks, r. 68B-6.004 | Rule lapses after 31 Mar 2028 | Re-check before the April 2028 season. |
| Annual FWC season orders | Each year | EO 26-10, 26-26, 26-33, 26-25 and 26-18 all expire; re-read each season. |
| Gulf descending device, § 622.30(c) | Expired 14 Jan 2026 | Continuation proposed 30 Jul 2026 (secondary). The state rule, r. 68B-14.005(3), still requires one. |
| Broward County § 13-5 (Sp. Acts 1921, ch. 8636) | Status unknown | Check ch. 68B-3 for a repeal; until then treat Broward's inside waters as closed to spearing. |
| Local codes generally | Each supplement | Re-search each jurisdiction at least yearly. |

## The fresh/salt line: unsolved, unchanged

Florida's test for salt water is a taste test, Fla. Stat. § 379.101(33). Fisheries law has no salinity
threshold, no per-river list beyond the Steinhatchee, and no FWC GIS layer. The 1,500 mg/L chloride line
in r. 62-302.200(30) belongs to DEP water-quality classification, not to FWC licensing. The map keeps its
coastal, tidal and inland classification, which has no legal force. In brackish water carry both licences
and treat the stricter regime as controlling, and remember that a speargun may not even be carried on
fresh water. Do not reopen this without new primary law.

## Where the geometry is still soft

1. **Beach buffers outside Palm Beach County.** R. 68B-20.003(2)(a) closes 100 yd from every public
   bathing beach. Only Palm Beach County and Hollywood (a city rule) are drawn. Assume the buffer applies
   at every public beach.
2. **Piers not in the FWC inventory** have no circle. Assume 100 yd.
3. **Bridges without a matched deck** (558 records) keep a 125 yd circle at the inventory point; a long
   bridge in that group is under-drawn.
4. **Volusia "inland salt waters"** (`vol`). Undefined; assume the whole Halifax River and Mosquito
   Lagoon system.
5. **Words-only local closures drawn as whole city polygons:** Venice, Cedar Key, Bal Harbour,
   Lauderdale-By-The-Sea, Treasure Island, Clearwater, Sunny Isles Beach, Hallandale Beach, Lantana,
   Delray Beach, Dania Beach, St. Pete Beach and Key Colony Beach. The offshore edge is soft.
6. **Canal gear rules** (Pinellas County, Cape Coral, Sanibel, Naples, Collier, Brevard, Satellite Beach)
   are text only. Only the Lower Keys canals are drawn.
7. **Biscayne's 100 ft channel closure** and the eleven federal manatee sanctuaries are not drawn.
8. **Key West and Great White Heron refuges** stay amber: § 27.21 and the Service's pages disagree.
9. **The long-jetty exception** measures from the visible beach line; the rule does not define "the
   shoreline".
10. **Military shoreline bands** drawn as lines or anchor points, and the MacDill and Patrick chords
    not satellite-checked.

## The standing posture on local ordinances

Treat every local ordinance as live and enforceable. The preemption picture as read so far:

- **Fishing preemption, § 379.2412** (read verbatim 7 Oct 2026): "The power to regulate the taking or
  possession of saltwater fish ... is expressly reserved to the state", but a local government may
  prohibit saltwater fishing "from real property owned by that local government". Ordinances about city
  piers, parks, beaches and marinas fit the exception. Ordinances that regulate taking fish in open
  water stand on contested ground.
- **Special acts** printed in county codes (Palm Beach chs. 59-1699 and 59-1702, the canal acts of Cape
  Coral, Sanibel, Naples and Brevard, Broward's 1921 act) are state law, so § 379.2412 does not displace
  them in the same way. FWC repealed many county fisheries acts in ch. 68B-3 and left the two Palm Beach
  acts standing.
- **Weapons preemption, § 790.33**, covers firearms and ammunition only.
- **Restricted areas, § 379.2425(3)**, are FWC's to establish on a local government's application.

No Florida court has construed any of this against a local spearfishing rule. Nobody should plan a dive
around an argument they would have to win after being cited. The map draws every local rule as live.

## Coverage position

Federal, state and military layers are read and drawn statewide. Local codes have been keyword-searched
across most of the coast (211 jurisdictions tracked on 30 September, with browser reads on 7 and
8 October for Hollywood, Pinellas County, St. Petersburg, Naples, Town of Palm Beach, Deerfield Beach,
Clearwater, Sanibel, Satellite Beach, Bradenton Beach, Broward County and others). The jetty and bridge
buffers are now drawn statewide; the beach buffer is not. Absence of a line anywhere on the map is not
evidence that water is open. The region-by-region local coverage table of 30 September is in
`research/legal-review-2026-09-30.md` and `research/municipal-ordinance-sweep.md`; the October reads
have not yet been folded into the sweep document.
