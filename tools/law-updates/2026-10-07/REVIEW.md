# Second statewide legal review, jetties and bridges: 7 and 8 October 2026

The map now draws every jetty buffer from the structure itself and every coastal bridge buffer along
the deck, and the registry holds 326 citations (302 verbatim, 24 secondary) with "Rules current as of
8 Oct 2026". This review ran in parallel with the 7 October legal currency pass (commit 46a5ea5). Where
both found the same rule, the map keeps one entry, usually the 7 October one; this note covers what
the second pass added on top. It is not legal advice, and posted signage controls.

Repository commit: d03f006. Sources: `tools/law-updates/2026-10-07/r1-review.json` (registry pass),
`reads.md` (every passage read, with the page it came from), `tools/jetties-2026-10-07/` (jetty and
bridge review records), `tools/patch-zones-2026-10-07.py` and `tools/patch-regs-species-2026-10-07.py`.

## 1. Jetties: 75 structures traced

Every inlet jetty, groin and breakwater from St. Marys to Pickens and the Keys was read one at a time on
USGS NAIP imagery, with the OpenStreetMap ways and NOAA ENC shoreline-construction features drawn over
it. Where neither source carried a structure that the imagery showed, the line was traced by hand.

- **Rule drawn:** r. 68B-20.003(2)(d) closes water within 100 **feet** of the unsubmerged portion of any
  jetty. Each buffer is drawn at 150 ft around the structure as traced.
- **Classes:** 55 inlet or fishing jetties are drawn closed (red). 20 groins, breakwaters and revetments
  that may or may not count as a jetty are drawn amber, because the rule does not define a jetty.
- **Submerged parts:** ENC features charted as always under water or floating are not buffered, because
  the rule reaches only the unsubmerged portion. Features that cover and uncover are buffered.
- **Long-jetty exception:** the rule lifts the buffer along the last 500 yd of a jetty that extends more
  than 1,500 yd from the shoreline. It is drawn only where the traced jetty clears 1,500 yd by at least
  300 yd, and then only along the last 400 yd. Two qualify: St. Marys south (about 2,870 yd seaward) and
  St. Johns north (about 2,230 yd). St. Johns south (about 1,680 yd) is close to the line and is drawn
  fully buffered.
- **Measured, not assumed:** the seaward lengths come from the traced line measured from the point
  where it meets the visible beach. The rule does not define "the shoreline"; see open question 31.

The FWC inventory's 18 "Fishing Jetty" points keep their 125 yd circles as well, because a jetty used as
a public fishing pier may also fall under the 100 yd pier buffer in (2)(b).

## 2. Bridges: 1,441 buffers drawn along the deck

All 2,509 coastal and tidal bridge records that the map buffers (confirmed or presumed fishable) were
compared with the OpenStreetMap bridge decks on imagery, in panels.

| Outcome | Records | What the map draws |
|---|---|---|
| Deck matched and runs more than 22 m from the inventory point | 1,441 | 125 yd band along the deck, unioned with the old circle |
| Deck stays within 22 m of the point | 508 | The circle, which already covers it |
| No deck within 60 m | 508 | The circle, with a popup note that the bridge may run past it |
| Nearest deck 60 to 250 m away, not the same bridge | 50 | The circle, with the same note |
| Ferry crossing, not a deck | 2 | The circle |

Motorways and their links were never matched, since limited-access bridges carry no buffer. Causeway
fill is not buffered; only the bridge decks are, following the rule's "that portion of any bridge". The
Gandy Bridge buffer now runs its full 4 km. The 558 records that kept only a circle are listed by the
`rv` field in `bridges.json`, and a long bridge among them is under-drawn (open question 33).

## 3. Registry changes from the second pass

Every excerpt below was read in the author's Chrome at the primary host on 7 or 8 October, and an
independent check re-read eight of them live on eCFR, Online Sunshine, the Federal Register and Cornell
LII. The check also found 12 defects in the first draft of this pass, all fixed before commit (listed in
section 6).

**Federal.**
- 36 C.F.R. §§ 1.4 and 2.4: in every National Park System unit a speargun is a weapon, and a loaded
  weapon is prohibited in any vessel, anchored or under way. Unload before climbing back aboard.
- 50 C.F.R. § 27.43: using or possessing spears or gigs on a national wildlife refuge is prohibited
  unless a refuge rule authorizes it. Crystal River NWR is now drawn closed, on the Service's own
  statement that no fishing is allowed in refuge waters.
- 50 C.F.R. § 622.187(b)(2)(v) and (b)(8): one scamp or yellowmouth within the South Atlantic grouper
  bag, and no more than 10 of any one snapper-grouper species within the 20-fish aggregate.
- 50 C.F.R. §§ 622.10(a), 622.186(a): fish from federal waters keep head and fins until landed.
- 36 C.F.R. § 7.45(d)(9): gear and catch illegal in Everglades National Park may cross it only by four
  named passes and Chokoloskee Bay. § 2.3(d)(1): park fresh waters are hook and line only.
- 50 C.F.R. § 17.108(c)(14)(iv): in Kings Bay, all waterborne activity, spear fishing included, is
  prohibited next to the sanctuaries and the four springs, year-round across the two seasonal provisions.

**State.**
- Fla. Stat. § 379.2412 is the fishing preemption statute: saltwater fish regulation is reserved to the
  state, but a local government may prohibit fishing from property it owns. § 790.33 reaches firearms
  and ammunition only. The `fs-790-33` entry was corrected. The map still draws every local rule as live.
- R. 68A-23.002(7): using **or possessing** a speargun in or upon fresh water is prohibited. The sidebar
  had said FWC overstated this; that note is withdrawn.
- Fla. Stat. § 316.130(17): no jumping or diving from a publicly owned bridge, signed or not.
- R. 68B-14.006(4) (reef fish landed whole), r. 68B-14.005(3) (descending device or venting tool aboard
  when harvesting reef fish from a vessel, spearfishing included), r. 68B-21.006 (snook: hook and line
  only, and no snook aboard with spear gear), r. 68B-32.006(2) (tarpon), r. 68B-35.004 (permit and
  African pompano in federal waters), § 379.354(3), (7)(f), (8)(d) and § 327.331 flag sizes and
  distances. § 379.101(17): the Steinhatchee River is fresh water from source to mouth, now drawn.

**Local.**
- Drawn: Clearwater § 21.06 (projectile weapons banned citywide, spearfishing excepted only where
  designated, the same structure as Treasure Island), Mexico Beach § 95.03 (canal channel and entrance,
  marker), Volusia § 20-121(c)(2) (no swimming within 300 ft of a pier or jetty; drawn at 350 ft around
  the Ponce Inlet jetties as charted), Boynton Inlet § 18-1 added to the inlet zone.
- Text only, no geometry yet: canal gear acts in Cape Coral, Sanibel, Naples, unincorporated Collier,
  unincorporated Brevard and Satellite Beach (hook and line, cast nets or crab traps only); St. Petersburg
  § 7-5 (seven bridge and right-of-way locations and the pier district); Pinellas County § 90-7(e);
  Bradenton Beach § 46-46; Town of Palm Beach § 74-162(b); Broward County § 13-5, a 1921 special act
  limiting food fish in "inside waters" to hook and line or cast net, whose status is open.

## 4. Tips for planning a dive

These follow from the rules above and are the points most likely to cost a dive or a ticket.

1. **Unload before you get back on the boat in any national park unit.** Biscayne, Dry Tortugas,
   Everglades, Canaveral and Gulf Islands all fall under § 2.4(c), and an anchored boat is still a vessel.
2. **Never carry a speargun on a freshwater river or lake**, even to reach the coast. Possession alone is
   a violation under r. 68A-23.002(7). The Steinhatchee is fresh to its mouth.
3. **Keep fish whole until you are ashore.** No fillets on the boat, on a pier, on a fishing bridge or on
   a jetty, in state or federal waters.
4. **Do not keep a hook-caught snook on a boat with spear gear aboard.** R. 68B-21.006(3) makes the
   combination a violation by itself.
5. **Carry a descending device or venting tool** on any boat harvesting reef fish in state waters, and a
   rigged descending device for snapper-grouper in South Atlantic federal waters. Neither rule exempts
   spearfishing boats.
6. **Jetties are 100 feet, everything else is 100 yards.** On the map, a jetty buffer that looks thin next
   to a bridge buffer is correct. Amber jetty outlines are structures that may count as jetties: treat
   them as closed.
7. **A circle on a long bridge means the deck was not matched.** Treat the whole bridge as buffered.
8. **Residential canals are mostly closed to spears** in Pinellas, Lee (Cape Coral, Sanibel), Collier
   (listed canals and Naples), Brevard and the Lower Keys, even though none of the canal rules except the
   Keys one is drawn.
9. **Do not enter the water from a bridge deck.** § 316.130(17) applies everywhere, and Naples adds a
   100 ft swimming ban around its public bridges.
10. **Gag and black grouper in South Atlantic federal waters become 2 per boat combined from 28 Oct 2026**,
    and FWC has proposed the same for Atlantic state waters (notice 31448290, comments to 26 Oct 2026).

## 5. Open questions added

Numbered as in `OPEN-QUESTIONS.md` (27 to 33): Broward § 13-5 status and reading; where the canal-rule
canals are; permit and African pompano under r. 68B-35.004(5)(a); the Atlantic state-water gag and black
grouper vessel limits under r. 68B-14.0036; where "the shoreline" is for the long-jetty exception; bridges
where a city bans fishing from the deck (St. Petersburg § 7-5 and others), whose buffers the map keeps;
and the 558 bridges without a matched deck.

## 6. What the independent check corrected

An agent that had not seen the work compared every excerpt with `reads.md`, re-read eight at the
primary hosts and reviewed the map text. It found, and the commit fixes: the § 2.4(c) loaded-weapon rule
had been stated as "under power" only; a St. Petersburg § 7-5 quotation not yet in the read log; three
claims in county notes with no read behind them (Melbourne Beach, Cocoa Beach, Lighthouse Point); stale
notes on four corrected entries; the Gulf amberjack reopening date (closed to 31 Aug 2027, not 31 Jul);
the Boynton sand-plant area ("75 ft or its area of influence, whichever is greater"); dashes and an
outdated argument in the `fs-790-33` full text; three phrases in the map's own voice that read as
permissive; the Monroe lobster window (two windows, not one continuous one); and two zone flags that did
not say what was left undrawn.

## 7. Licence status of the new layers

The jetty review and the bridge decks start from OpenStreetMap ways, so `jetties.json` and the bridge
`dk` and `sp` fields are ODbL 1.0 (LICENSE-DATA.md section 2a). This runs against the 7 October move to
OSM-free data files. The zones added in this pass use no OSM input. Rebuilding the jetty and deck
geometry from NOAA ENC shoreline construction and bridge areas is in the backlog; it is a decision for the
author whether to do that before launch.
