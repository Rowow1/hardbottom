# State law track: fresh review, 7 Oct 2026

Scope: Florida Statutes, Florida Administrative Code, FWC executive orders. Method: WebSearch and WebFetch only, no browser. WebFetch returns a model summary with short quotes, so nothing below is verbatim until the main session reads it in a browser. Where text came from Cornell LII rather than flrules.org it is marked LII; flrules.org was used for every effective date. Registry baseline: 278 ids, 81 state (/home/claude/review/registry-index.tsv). The full working log is at the end of this file.

## Findings that change the map or registry

Ranked by how many dives they touch.

### 1. Fla. Stat. § 379.2412, state preemption of saltwater fishing regulation (NEW)
- Primary URL: https://www.flsenate.gov/Laws/Statutes/2026/379.2412 (2026 edition; History ends s. 22, ch. 2022-142).
- Effect: reserves to the state "the power to regulate the taking or possession of saltwater fish". Exception: a local government may prohibit "saltwater fishing from real property owned by that local government" for health, safety or welfare.
- Where: statewide; bears on every city and county spearfishing ordinance on the map (about 45 local ids).
- Map: no geometry change; the project keeps every ordinance live. Registry: fs-790-33 says § 379.2425(3) is "one real preemption vector" and never cites § 379.2412. The explainer must add it. The property-owner exception is what supports pier, park and city-beach ordinances (Lee § 20-25, Fort Myers Beach § 18-24, Bonita § 28-31, Anna Maria pier, Naples pier); water-wide bans (Treasure Island, Venice, Cedar Key, St. Pete Beach, Bal Harbour, Sunny Isles) sit inside the reserved field. Still no case law found.
- Related: fs-790-33, every local id. Status: read on flsenate.gov through WebFetch in four segments; needs browser verbatim read.
- Read verbatim: the whole section (two sentences).

### 2. Fla. Admin. Code r. 62D-2.014(10), no speargun displayed or used on state park property (NEW)
- Primary URL: https://www.flrules.org/gateway/ruleNo.asp?id=62D-2.014 (current version eff. 4/30/2007). Text read on LII.
- Effect: "No person shall use or openly display in any state park weapons such as ... devices which fire a dart or projectile". A speargun fires a projectile. Carrying an assembled or visible speargun across park land to reach water outside the park is a violation. Gigs are excepted only "in areas where gigs may be legally used for saltwater fishing". Penalty via Fla. Stat. § 258.008(1) (noncriminal, up to $500, ejection).
- Where: every state park with a shore or jetty entry: Sebastian Inlet, Fort Pierce Inlet, St. Lucie Inlet, John U. Lloyd, Hugh Taylor Birch, Bill Baggs, Bahia Honda, Long Key, Fort Zachary Taylor, Honeymoon Island, St. Andrews, Big Lagoon and others.
- Related: fac-62d-2-014 (cites only (9)(d)). Status: secondary (LII). Open question for the popup: whether a pole spear with a band is a "device which fire[s] a ... projectile" (conservative reading: yes, treat it as covered).
- Read verbatim: r. 62D-2.014(10), the sentence beginning "No person shall use or openly display".

### 3. Fla. Admin. Code r. 68A-23.002(7), possession of spear guns in or on fresh water banned (registry MISSTATES)
- Primary URL: https://www.flrules.org/gateway/ruleNo.asp?id=68A-23.002 (eff. 6/7/2022). Text read on LII.
- Effect: "The use or possession of dynamite, traps, nets, seines, baskets, spear guns, ... is expressly prohibited in or upon the fresh waters of the state" unless permitted by rule or permit. (5) bars taking freshwater fish "by underwater swimming or diving".
- Registry error: regs.json freshwater card "The possession claim is weaker than FWC states" says only (9) exists and no flat possession ban applies outside park waters. (7) is that flat ban. Rewrite the card and cite (7).
- Where: all fresh water; this also includes the whole Steinhatchee River, which § 379.101(17) declares "fresh water from its source to mouth" (2026 text). ramps.json classes the Steinhatchee ramps "coastal", so a diver launching there sees no freshwater warning.
- Map: add the speargun-possession warning to the inland class and to the Steinhatchee River to its mouth (mouth undefined in statute; conservative reading is the river channel to the Gulf). NEW citation; touches regs.json freshwater section and neg-freshsalt.
- Read verbatim: r. 68A-23.002(7) first sentence; § 379.101(17) last sentence.

### 4. Species gear rules that apply "within or without Florida Waters" (registry uses r. 68B-20.005 only)
All LII text, flrules dates. species.json says for these species in the EEZ "No federal spear rule found ... Conservative reading". The species chapters settle the EEZ question with their own text.
- r. 68B-21.006 snook (eff. 9/1/2013): (1) hook and line only "Within or without Florida Waters"; (3) "A person may not possess a snook while also in possession of, using, or transporting a net, seine, or other fishing gear that is not expressly permitted". A spearfisher may not have any snook aboard or in hand (a buddy's rod-caught fish) while carrying a speargun. Only a stowed cast net is excepted. This touches mixed rod-and-spear boat trips statewide.
- r. 68B-37.006 spotted seatrout (9/1/2013): cast net or hook and line only, within or without Florida Waters.
- r. 68B-32.006 tarpon (9/1/2013): no "spearing, snagging, or snatch hooking", within or without Florida Waters.
- r. 68B-34.006 bonefish (9/1/2013): target "only with hook and line gear", within or without Florida Waters.
- r. 68B-22.006(1) red drum (1/1/1998): "Spearing or snagging (snatch hooking) of redfish in or from state waters is prohibited."
- r. 68B-35.004 (11/15/2012), opposite direction: permit and African pompano may be taken in the adjacent federal EEZ by hook and line "or spearing" ((2)(a), (3)). species.json's EEZ note for both is therefore wrong. The state-water spear ban (r. 68B-20.005 and r. 68B-35.004) stands. Map posture may stay conservative but the note must cite this rule and say the state rule allows it.
- Related: fac-68b-20-005 and species ids snook, spotted-seatrout, tarpon, bonefish, red-drum, permit, african-pompano. All NEW citations. Read verbatim: each rule's gear subsection on flrules (.doc).

### 5. Fla. Admin. Code r. 68B-14.0036, proposed Atlantic gag and black grouper change (NEW, pending)
- Notice 31448290, FAR Vol. 52/193, 5 Oct 2026, comments to 26 Oct 2026: https://www.flrules.org/Gateway/View_notice.asp?id=31448290. Purpose: "establish consistent regulations between gag and black grouper"; effect: "modify recreational limits for gag and black grouper in Atlantic state waters". Not in force.
- Registry consequence: species.json (gag, black-grouper: Atlantic and Keys) shows "2 per vessel per day ... FWC states the same for state waters". The 2026 amendment (notice 30105616) touched only Gulf lane snapper, and this new proposal implies the state rule may not carry the vessel limit yet. Main session must read the current text (tid 30630580) before keeping that line, and should mark it "federal; state rule pending".
- Read verbatim: r. 68B-14.0036(2) as in force from 1 Apr 2026, and the proposed .doc.

### 6. Fla. Admin. Code r. 68B-14.006(4), fish landed whole (NEW, sidebar)
- https://www.flrules.org/gateway/ruleNo.asp?id=68B-14.006 (eff. 4/1/2020; LII text): "all fish harvested from Florida or adjacent federal Exclusive Economic Zone (EEZ) waters pursuant to the requirements of this chapter shall be landed in a whole condition." Possession of filleted reef fish in state waters, on piers, bridges and jetties is prohibited (gutting and gills allowed; Bahamas exception). Applies to every speared reef fish. Not a zone; sidebar or species note.

### 7. Smaller items (NEW, sidebar or note)
- § 316.130(17) (not (18)): "No pedestrian may jump or dive from a publicly owned bridge." No signage needed; noncriminal traffic infraction under (19). https://www.flsenate.gov/Laws/Statutes/2026/316.130. Relevant to bridge entries. The brief named (18); (18) is limited-access highways.
- § 379.354(7)(f): individual scuba divers on a for-fee dive vessel with the vessel licence "are not required to obtain individual fishing licenses". fs-379-354 carries this as "Secondary ... confirm wording"; now read on flsenate 2026, promote after browser read.
- § 258.008(3) (History ends s. 7, ch. 2019-141): capturing or injuring a wild animal or collecting animal specimens in a state park without Division permission is a second-degree misdemeanor. Reinforces the state-park closure; cite beside fac-62d-2-014.
- § 258.157(2) with § 258.156: in the Savannas State Reserve (St. Lucie, Martin) "firearm" includes "a spearfish gun"; possession is a misdemeanor. Savannas is freshwater marsh, already covered by item 3; low value.
- § 379.2425(4): violation is a Level Two violation under § 379.401(2)(a)16 (second-degree misdemeanor first offence; escalating mandatory fines). Add to fs-379-2425 penalty line if absent.

## Stale or wrong in the registry

- fs-790-33: incomplete; omits § 379.2412 (finding 1).
- regs.json, freshwater card "The possession claim is weaker than FWC states": wrong; r. 68A-23.002(7) (eff. 6/7/2022) bans possession of spear guns in or on fresh water (finding 3).
- neg-freshsalt and regs.json "Only one river is legally designated": correct in substance; add the pin cite § 379.101(17) and the possession consequence.
- species.json EEZ notes for snook, spotted-seatrout, tarpon, bonefish: "No federal spear rule found" stays true, but the state rules themselves reach "within or without Florida Waters"; cite rr. 68B-21.006, 68B-37.006, 68B-32.006, 68B-34.006. For permit and african-pompano the conservative EEZ note contradicts r. 68B-35.004(2)(a), (3) (finding 4).
- species.json gag and black-grouper Atlantic and Keys vessel limit "FWC states the same for state waters": unsupported pending a read of r. 68B-14.0036 (finding 5).
- fac-68b-14-0035, fac-68b-14-0036 notes: the open question "whether the 2026 amendment also added Atlantic gag and black grouper vessel limits" is answered by notice 30105616 (lane snapper only). Effective date 4/1/2026 confirmed for both.
- Effective dates confirmed current on flrules.org, 7 Oct 2026 (no change needed): 68B-20.002 1/1/1998; 68B-20.003 8/1/2014; 68B-20.004 8/1/2014; 68B-20.005 1/1/1998; 68B-4.012 8/1/2014; 68B-5.006 11/26/2014; 68B-3.008 8/14/2024; 68B-3.009 2/1/2017; 68B-3.038 2/1/2017; 68B-6.002 and 6.003 7/1/2001; 68B-6.004 4/1/2021 (sunset 31 Mar 2028); 68B-7.008 11/4/2025; 68B-11.003 7/3/1984; 68B-11.004 7/15/1996; 68B-14.0038 5/5/2024; 68B-14.0039 5/5/2024; 68B-14.004 5/20/2025; 68B-14.0041 1/16/2018; 68B-14.0042 5/5/2024; 68B-14.0043 4/1/2023; 68B-14.005 4/1/2023; 68B-14.008 7/1/2022; 68B-14.009 9/1/2026; 68B-24.005 11/1/2018; 68B-24.006 5/1/2017; 68B-24.0065 7/1/2026; 68B-24.0067 7/1/2020; 68B-24.007 5/1/2017; 68B-25.003 8/14/2024; 68B-42.0036 4/1/2019; 68B-42.007 8/14/2024; 68B-44.006 7/1/2019; 68A-19.005 3/1/2010; 62D-2.014 4/30/2007; 68C-22.007 6/30/2026; 68C-22.011 4/27/2025. Statutes 379.2425, 327.331, 316.1305, 379.354, 379.353: 2026 editions, no 2025 or 2026 amendment.
- regs.json seasons card "Puffer fish": says take is prohibited in "Martin and St. Lucie" only; r. 68B-3.007 (eff. 7/15/2004, LII text) covers Volusia, Brevard, Indian River, St. Lucie and Martin. Spearing puffers is banned everywhere anyway (r. 68B-20.005(28)); the error matters for gigging and hook and line.
- fwc-eo-26-10, -18, -26: still secondary; PDFs are image-only. FWC releases (13 May and 7 Aug 2026, leads) agree with the registry effect lines.

## Confirmed negatives

- No 2026 session law amends ch. 379 or § 316.1305/§ 316.130 (2026 Table of Section Changes, https://www.flsenate.gov/PublishedContent/Laws/Statutes/Links/Table_of_Section_Changes__2026_.pdf).
- § 327.331 unchanged since ch. 2016-171 (https://www.flsenate.gov/Laws/Statutes/2026/327.331). Distances still 100 ft (rivers, inlets, channels) and 300 ft elsewhere.
- § 327.46 amended by ch. 2026-36 (CS/HB 1103, eff. 1 Jul 2026): local extension of vessel restricted areas; vessel-only, no swim or dive rule (https://laws.flrules.org/2026/36).
- Ch. 258 2026 amendments (258.004, .393, .397, .42 by ch. 2026-1; 258.603 new by ch. 2026-42): none restricts fishing, spearing or diving. § 258.397(4)(c) Biscayne Bay net ban is old and gear-specific.
- Ch. 790 2026 amendments (790.052, .115, .233): firearms only.
- § 379.2431: no statutory diving closure; No Entry zones live in r. 68C-22.002(11).
- § 379.249 and ch. 68E-9 (all rules 7/1/2001): artificial reef program has no fishing or spearing restriction in state law. State artificial reefs carry no special spear rule; the only SMZ spear bans are federal (registry cfr-622-182).
- Ch. 68B-20: four rules, no pending notices.
- Ch. 68D-24 springs protection rules (.0035 eff. 1/20/2026, .0037 Weeki Wachee): vessel-only. https://www.flrules.org/gateway/ChapterHome.asp?Chapter=68D-24
- Ch. 68B-24: no state 300-ft sport-season diving rule; no new lobster rule since 68B-24.0065 (7/1/2026).
- 68B-5.002 Pennekamp and 68B-5.005 fish feeding: no spear rule (fish feeding by divers banned; harvest exception).
- 68B-14.006: no Pulley Ridge, Steinhatchee or artificial-reef area rule. Pulley Ridge is federal only (registry cfr entries).
- 18-20.019 (Boca Ciega and Pinellas aquatic preserves): dock rules only.
- Cownose ray (68B-44.002): workshops May to Jul 2026, staff final rule on 5 Aug 2026 agenda; no Proposed or Final notice on flrules, nothing in force.
- FWC executive orders issued after 30 Sep 2026: EO 26-34, 26-35, both hunting. No marine order since the last pass (https://myfwc.com/about/inside-fwc/executive-orders).
- FWC Commission agendas Feb, May, Aug 2026: no spearfishing, lionfish, Keys, Biscayne or Blue Heron Bridge item.

## Could not resolve

- r. 68B-14.0036 text in force since 1 Apr 2026 (tid 30630580) and the 5 Oct 2026 proposed text: .doc returns binary to WebFetch; curl blocked by proxy.
- r. 68C-22.007 notice of change 30914208 (19 May 2026): text in a .doc; the registry's claim that (1)(e) Vero Beach became Idle Speed is still unconfirmed. LII still shows the 2002 No Entry text.
- FWC EO 26-10, 26-18, 26-26: image-only PDFs.
- Geographic reach of r. 68B-20.005 versus r. 68B-35.004's EEZ spear allowance for permit and African pompano: which controls in federal waters is not stated; read both and decide the map posture.
- r. 62D-2.014(10): whether a pole spear counts as a projectile device; only a Division or FWC answer settles it.
- Not read: each county rule in ch. 68D-24; ch. 68A-15 WMA rules for coastal WMAs (Guana River, Big Bend); r. 18-20.004 management criteria; 68B-3 repeal-only rules .003 to .005 and .034 to .050 individually; FKNMS state-water status beyond the registry (Blueprint still blocked in state waters per news leads).

---

# Working log
## Progress log

### Item 1 (statutes), in progress

- § 379.2412 "State preemption of power to regulate" (2026 Fla. Stat., Online Sunshine). Not in registry. Reserves to the state the power to regulate taking or possession of saltwater fish; exception lets a local government ban saltwater fishing on property it owns for public health, safety or welfare. History ends s. 22, ch. 2022-142. Bears on fs-790-33, which says there is "one real preemption vector" (§ 379.2425(3)).
- § 379.2425 (2026 edition): (1) defines spearfishing; (2)(a) closures; (2)(b) prima facie possession; (3) restricted areas; (4) Level Two violation. History ends s. 3, ch. 2016-107. No 2026 amendment.
- § 327.331 (2026 edition, flsenate.gov): History ends s. 1, ch. 2016-171. No amendment since. Distances unchanged: divers 100 ft in rivers, inlets, navigation channels; 300 ft elsewhere; vessels same distances and must slow to idle within them (subs. (4) to (6)). Registry fs-327-331 current. Note (3): diver may not display device on a river, inlet or navigation channel so as to unreasonably create a navigational hazard.
- § 327.46 amended by s. 4, ch. 2026-36 (CS/HB 1103, "local administration of vessel restrictions", eff. 1 Jul 2026). Lets local governments extend boating-restricted areas near blind corners etc. Vessel-only. Local vessel-exclusion zones at "public bathing beach or swim area" bar vessels, not swimmers or divers. NEGATIVE for spearfishing.
- § 316.1305 (2026): History ends s. 18, ch. 96-350. Unchanged; fs-316-1305 current.
- § 316.130(17), not (18): "No pedestrian may jump or dive from a publicly owned bridge." (18) is limited-access highways. Statewide, no signage required; noncriminal traffic infraction (19). Not in registry as its own entry. Affects shore/bridge entry for diving (jumping in off a bridge to dive). Lead for a sidebar note, not a zone.
- § 379.354 (2026): History ends s. 2, ch. 2020-123. (7)(f): individual scuba divers on a for-fee dive vessel holding the vessel licence "are not required to obtain individual fishing licenses". Registry fs-379-354 carries this only as "Secondary ... confirm wording". Promote after browser read.
- § 379.353 (2026): History ends s. 4, ch. 2024-251. No 2026 change.
- 2026 Table of Section Changes (flsenate.gov PDF): NO section of ch. 379 amended in 2026. Ch. 327: 327.4107, .4108, .4111, .46, .73, .74 (all ch. 2026-36, vessel admin). Ch. 258: 258.004, .393, .397, .42 (ch. 2026-1), 258.603 new (ch. 2026-42, spoil island naming). Ch. 253: 253.0341, 253.42. Ch. 790: 790.052, .115, .233. None of these touches fishing, spearing or diving (258.397 and 258.42 read: no spear/dive text; 258.397(4)(c) net ban only, pre-existing).
- Ch. 790: no 2026 change relevant. § 790.33 still firearms/ammunition only (registry position stands).
- § 379.2412 full text read (flsenate 2026, 4 segments): "The power to regulate the taking or possession of saltwater fish, as defined in s. 379.101, is expressly reserved to the state." Exception: a local government may prohibit "saltwater fishing from real property owned by that local government" for public health, safety or welfare. This is the express field preemption statute for saltwater fishing; the registry's fs-790-33 entry calls § 379.2425(3) the "one real preemption vector" and never cites § 379.2412. Map effect: none (project posture treats every ordinance as live). Registry effect: fs-790-33 is incomplete; the preemption explainer must cite § 379.2412, and the property-owner exception is the hook that saves pier, park and beach ordinances (Lee § 20-25, Fort Myers Beach § 18-24, Bonita § 28-31, Anna Maria pier, etc.) while water-wide city bans (Treasure Island, Venice, Cedar Key, St. Pete Beach, Bal Harbour, Sunny Isles) sit squarely inside the reserved field. Keep them drawn; change the explanation.
- § 379.2431 (2026): manatee "No Entry" zones referenced but defined in rule (68C-22.002(11)); no statutory diving closure. History ends s. 4, ch. 2016-107.

### Item 1 done. Item 2 (ch. 68B-20 whole chapter)

flrules.org ChapterHome 68B-20, read 7 Oct 2026: 68B-20.002 Definitions 1/1/1998; 68B-20.003 8/1/2014; 68B-20.004 8/1/2014; 68B-20.005 1/1/1998. No pending notices. Four rules only; registry covers all four. 68B-20.003 structure (Cornell LII, secondary): (1) lawful except; (2)(a)-(e) buffers and park waters; (3) bag/size/season apply to speared fish; (4) sale; (5) no authority to take otherwise-prohibited fish; (6) buy/sell/possess fish taken in violation unlawful; (7) powerheads/bangsticks/rebreathers per 68B-4.012; (8) repeal of Brevard, Citrus, Collier, Hernando, Hillsborough, Pasco, Sarasota spearing special acts. 68B-20.005 list re-read on LII: 28 items, unchanged ("Jewfish"). Registry fac-68b-20-* current; nothing stale.
Related: 68B-4.012 effective 8/1/2014 (current). 68B-4 chapter: no spear rule besides .012 (titles). 68B-5: .002 Pennekamp 7/27/2010, .005 fish feeding 1/1/2002, .006 lionfish 11/26/2014, .007 Skyway Fishing Pier State Park gear/course 11/16/2023 (state park; already closed to spearfishing by 62D-2.014(9)(d)); not in registry, low value.

### Item 6 (FWC executive orders), done early because it is quick

FWC EO index (myfwc.com/about/inside-fwc/executive-orders, read 7 Oct 2026) lists EO 26-01 to 26-35. Marine fisheries orders: 26-02 (Brevard/Collier dead-fish removal, expired 20 Feb 2026), 26-07 (seatrout size, expired 31 May 2026), 26-10 (Atlantic gag closed from 2 Aug 2026, Monroe included per FWC release 13 May 2026), 26-11 (Atlantic red snapper, rescinded by 26-16), 26-16, 26-17 (Lionfish Challenge, lobster bonus 29 to 30 Jul 2026, spent), 26-18 (Atlantic snowy closed from 7 Jun 2026), 26-25 (Gulf amberjack closes 14 Oct 2026), 26-26 (Gulf gag 1 to 30 Sep 2026, excl. Monroe, per FWC release 7 Aug 2026), 26-27 and 26-28 (bay scallop Pasco and Gulf County zones; hand/dip-net species, not spear), 26-33 (Atlantic red snapper Oct 9 to 22). Orders issued after 30 Sep 2026: 26-34 and 26-35, both hunting. No new marine EO since the last pass.
- PDFs for 26-10, 26-18, 26-26 still return no machine-readable text through WebFetch. They stay secondary; the FWC news releases (leads) agree with the registry's effect lines.
- Effect on 7 Oct 2026: Gulf gag CLOSED in state waters (since 1 Oct); Gulf amberjack open until 14 Oct; Atlantic red snapper opens 9 Oct; flounder closes 15 Oct (rule). Registry already carries all of these.
- No 2026 Atlantic blueline tilefish closure order (2025 had EO 25-09). Rule season May 1 to Aug 31 governs.

### Item 4 (species chapters), partial: species-specific gear rules the registry does not cite

The species panel (data/species.json) cites only r. 68B-20.005 for snook, red drum, spotted seatrout, tarpon, bonefish, permit, pompano and African pompano, and for the EEZ says "No federal spear rule found ... Conservative reading". Each species chapter has its own gear rule (Cornell LII text, secondary until read on flrules):
- r. 68B-21.006 snook (eff. 9/1/2013): (1) "Within or without Florida Waters, a person may harvest or attempt to harvest a snook only by or with the use of hook and line gear." (2)(c) bars spearing. (3) "A person may not possess a snook while also in possession of, using, or transporting a net, seine, or other fishing gear that is not expressly permitted in subsection (1)." A speargun is such gear: a spearfisher may not have a snook aboard or in hand (e.g. a buddy's hook-and-line fish) while carrying a speargun. Only the cast-net-stowed exception exists.
- r. 68B-37.006 spotted seatrout (9/1/2013): only cast net or hook and line, "within or without Florida Waters".
- r. 68B-32.006 tarpon (9/1/2013): no spearing "within or without Florida Waters".
- r. 68B-34.006 bonefish (9/1/2013): target "only with hook and line gear", within or without Florida Waters.
- r. 68B-22.006(1) red drum (1/1/1998): "Spearing or snagging (snatch hooking) of redfish in or from state waters is prohibited."
- r. 68B-35.004 pompano/permit/African pompano (11/15/2012): state waters hook and line only (pompano also seine, cast net). BUT (2)(a) and (3): in adjacent federal EEZ waters, permit and African pompano may be taken by "hook and line ... or spearing". This is a state rule that expressly ALLOWS spearing permit and African pompano in the adjacent EEZ, contrary to species.json's conservative EEZ note. R. 68B-20.005 (1998) has no stated geographic reach; r. 68B-35.004 (2012) is the later, specific rule. Map posture can stay "prohibited" in state waters; the EEZ note must change.
- r. 68B-39.006 mullet (5/16/2019): spearing is a listed gear, "except spearfishing is prohibited in fresh water". Mullet not in species.json; low value.
Chapter dates read on flrules ChapterHome 7 Oct 2026: 68B-21 (.002 to .005 1/1/2024); 68B-22 (.006 1/1/1998); 68B-37 (.002, .004, .005, .007 4/1/2026; .003 5/27/2026; .006 9/1/2013); 68B-32 (.004, .009 2/4/2019); 68B-34 all 9/1/2013; 68B-35 (.006 4/1/2018); 68B-16 queen conch harvest prohibited (9/1/2013); 68B-40 and 68B-66 empty; 68B-44.004 1/12/2026; 68B-44.008 7/1/2019.
- Cownose ray: workshops May to Jul 2026, staff final rule on FWC agenda 5 Aug 2026 (Item 7A, 2-ray bag proposed). flrules 68B-44.002 shows no Proposed or Final notice after the 30 Jun 2026 workshops, so nothing in force. Watch item only.

### Item 3 (ch. 68B-14), done

flrules ChapterHome 68B-14 read 7 Oct 2026: .001 4/1/2020; .002 4/1/2023; .0035 4/1/2026; .00355 10/26/2023; .0036 4/1/2026; .0038 5/5/2024; .0039 5/5/2024; .004 5/20/2025; .0041 1/16/2018; .0042 5/5/2024; .0043 4/1/2023; .005 4/1/2023; .006 4/1/2020; .008 7/1/2022; .009 9/1/2026; .0091 7/1/2022. All registry dates match.
- NEW since 30 Sep: Proposed amendment to r. 68B-14.0036, notice 31448290, FAR Vol. 52/193, published 5 Oct 2026, comment period to 26 Oct 2026. Purpose: "establish consistent regulations between gag and black grouper"; effect: "modify recreational limits for gag and black grouper in Atlantic state waters" to match federal. Not in force. Consequence: species.json says Atlantic and Keys state waters carry "2 gag per vessel per day ... FWC states the same for state waters" and the same for black grouper. The proposal implies the state rule may not yet carry those vessel limits; the current text (tid 30630580) could not be read (binary .doc via WebFetch). Main session: read the 1 Apr 2026 .doc and the proposed .doc.
- The 2025 proposal 30105616 (basis of the 1 Apr 2026 amendments to .0035 and .0036) covers only Gulf lane snapper: 10 in TL and a 20-fish Gulf bag. That resolves the registry's open note on fac-68b-14-0035/-0036 ("Whether the 2026 amendment also added Atlantic gag and black grouper vessel limits ... is unknown"): the 2026 amendment did not, per its notice.
- r. 68B-14.006 (4/1/2020): (4) fish must be landed whole; possession of filleted fish prohibited in state waters, on piers, bridges, jetties. Relevant to divers who fillet on the boat. Not a closure; sidebar.
- r. 68B-14.0039 workshops only (Sep 2025, Feb 2026); no proposed rule. r. 68B-14.009: final 9/1/2026 (tid 31244881) matches registry.

### Item 5 (other state chapters), in progress

- r. 62D-2.014 current version 4/30/2007 (flrules; no later notices). (9)(d) "Spearfishing is prohibited in all state parks." matches fac-62d-2-014.
- NEW: r. 62D-2.014(10) (Cornell LII, secondary): "No person shall use or openly display in any state park weapons such as ... devices which fire a dart or projectile". A speargun or pole spear with a band is a device that fires a projectile. Effect: carrying an assembled or visible speargun across state park land (a beach access, a jetty, a boat ramp in a park) is itself a violation, even when the dive is outside park water. Gigs are excepted only "in areas where gigs may be legally used for saltwater fishing". Not in registry (grep: no "openly display", no "62D-2.014(10)"). Applies to every state park with a shore entry: Bahia Honda, Fort Zachary Taylor, Long Key, Curry Hammock, John U. Lloyd, Hugh Taylor Birch, St. Lucie Inlet, Sebastian Inlet, Fort Pierce Inlet, Anclote Key, Honeymoon Island, St. Andrews, Big Lagoon, etc. Also (7): no swimming, bathing or wading where the Division posts it prohibited.
- ch. 68D-24 boating restricted areas (flrules list 7 Oct 2026): 68D-24.0035 springs protection zones (1/20/2026), .0036 Nichols Spring, .0037 Weeki Wachee (anchoring, mooring, beaching, grounding of vessels only), .0041 Dutchman Key eff. 10/18/2026 (future, vessel channel), .008 Broward 2/3/2026, .109 Withlacoochee 2/2/2026, .017 Palm Beach 5/20/2025. Spring-zone rules read (.0035, .0037): vessel-only; no swim, dive or fishing restriction. NEGATIVE for spearfishing. Not every county rule read individually.
- ch. 68C-22 (flrules list): .002 Definitions 12/23/2003; .007 Indian River 6/30/2026; .011 Citrus 4/27/2025; .029 Cape Canaveral Energy Center refuge 1/24/2023. Matches registry notes.
- ch. 68A-19: .005 CWA general 3/1/2010. Matches fac-68a-19-005.
- MISSTATEMENT in regs.json (freshwater, "The possession claim is weaker than FWC states"): it says no rule bans possessing spear gear in fresh water except park waters. R. 68A-23.002(7) (eff. 6/7/2022, flrules; text Cornell LII, secondary) reads: "The use or possession of dynamite, traps, nets, seines, baskets, spear guns, ... is expressly prohibited in or upon the fresh waters of the state" unless permitted by rule or permit. That is a flat possession ban on spear guns in or on fresh water. (9) is the separate fish-plus-device rule the entry quotes. FWC's public statement is backed by rule text; the regs.json paragraph must be corrected. Also (5): freshwater fish "may not be taken by underwater swimming or diving".
- Steinhatchee: § 379.101(17) (2026) "The Steinhatchee River shall be considered fresh water from its source to mouth." Registry neg-freshsalt and regs.json mention this without the subsection number. With 68A-23.002(7), possessing a speargun anywhere on the Steinhatchee, to its mouth, is prohibited. Steinhatchee ramps are classed "coastal" in ramps.json ("salt or brackish"). Map effect: the river to its mouth should carry the freshwater speargun-possession warning. Mouth location is not defined in the statute.
- r. 68B-20.003(2)(e) re-read (LII): possession of "spearing equipment" in or on any Division of Recreation and Parks water prohibited "except when such equipment is not loaded and is properly stored upon watercraft passing nonstop". Registry matches.
- Lobster: 68B-24.005 11/1/2018 (no later notices); 68B-24.004 (2005) sport-season bag 6 in Monroe and Biscayne NP, 12 elsewhere; 68B-24.0065 final 7/1/2026 tid 30968625 (matches registry); 68B-24.0067 7/1/2020 Biscayne CRPA lobster closure (registry cites inside fac-68b-7-008-1, fine); 68B-24.007 5/1/2017 (registry fac-68b-24-007-4 matches; (3) traps not within 100 ft of ICW, bridges, seawalls, no diver rule). No new lobster rule.

### Item 7 (commonly missed rules), done
- Lobster sport season: r. 68B-24.005(2) (11/1/2018) dive, bully or hoop net only; Monroe no night diving, no Pennekamp. r. 68B-24.004(2): 6 per day in Monroe and Biscayne NP, 12 elsewhere. Registry current. No state 300 ft rule (local only, registry correct).
- Biscayne Bay-Card Sound sanctuary ch. 68B-11: dates 7/3/1984 and 7/15/1996, unchanged; registry current.
- Artificial reefs: no state spear rule (§ 379.249, ch. 68E-9). Federal SMZs only.
- Pulley Ridge: federal only; nothing in 68B-14.
- Steinhatchee: § 379.101(17) fresh to mouth; see finding 3.
- State Reef Fish Survey: r. 68B-14.009 (9/1/2026) final tid 31244881; registry current; trigger "aboard a vessel" unchanged per registry read.
- Volusia r. 68B-3.008(3)(a) (8/14/2024) re-read on LII: gear list excludes spears except barbed spear of 3 prongs or fewer for legal flounder and sheepshead. (3)(e) 500 ft beach and jetty limits apply to haul seines only, not spears. Registry current.
- Puffer r. 68B-3.007 (7/15/2004): take prohibited in Volusia, Brevard, Indian River, St. Lucie and Martin waters. regs.json "Puffer fish" card says only "Martin and St. Lucie". MISSTATED: three counties missing. Add to "Stale or wrong".
