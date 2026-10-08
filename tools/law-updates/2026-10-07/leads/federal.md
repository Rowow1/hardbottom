# Federal track: bottom-to-top legal review, 7 Oct 2026

Scope: federal rules that close or restrict spearfishing, diving, spear-gear possession, or species by spear, in or off Florida. Checked against the 278-entry registry (`registry-index.tsv`, `data/law.json`), `OPEN-QUESTIONS.md` and the drawn zones.

Method and its limits: WebFetch and WebSearch only. WebFetch summarises; it does not return long verbatim text. "Confirmed on primary page" means the eCFR, Federal Register, nps.gov or fws.gov page was fetched and reported the provision, with short quotes where the tool gave them. Nothing below is verbatim-verified to the registry's standard. Every item marked for browser reading must be read word for word before it enters `data/law.json`. eCFR currency dates are given where the page showed them. Blog, press and forum pages are marked as leads.

---

## 1. Findings that change the map or registry

Ranked by how many dives they plausibly affect.

### F1. Gulf Amendment 62 removed the Feb to Mar shallow-water grouper closure (in force 2 Oct 2026)
- **Proposed citation:** 91 Fed. Reg. 63502 (6 Oct 2026) (Reef Fish Amendment 62, final rule), removing and reserving 50 C.F.R. § 622.34(d)
- **Primary URL:** https://www.federalregister.gov/documents/2026/10/06/2026-20435/reef-fish-fishery-of-the-gulf-of-america-amendment-62 (raw text: https://www.federalregister.gov/documents/full_text/text/2026/10/06/2026-20435.txt)
- **Effect:** Gulf federal waters beyond 20 fathoms are no longer closed to gag, red, black, scamp, yellowfin and yellowmouth grouper from 1 Feb to 31 Mar. The rule opens water rather than closing it. The gag closure in § 622.34(e) and the new Other SWG closure in § 622.34(h) (F4) still apply.
- **Where:** Gulf EEZ off Florida, seaward of the 20-fathom rhumb lines (old Table 4). No zone is drawn for it.
- **Effective:** 2 Oct 2026. The rule says it "relieves a restriction", so the 30-day delay was waived. The eCFR (current to 28 Sep 2026) still shows (d).
- **Related ids:** cfr-622-34-b is stale. Its effect line and excerpt still quote (d). Also stale: `species.json` eez_gulf "closed" text for gag, red, black, scamp, yellowfin and yellowmouth ("Amendment 62 proposes removing this closure"), and the `regs.json` grouper text ("Gulf federal waters beyond 20 fathoms closed 1 Feb to 31 Mar").
- **Status:** Confirmed on the FR full text.
- **Read verbatim in browser:** amendatory instruction 2, "In Sec. 622.34, remove Table 4 to paragraph (d) and remove and reserve paragraph (d).", plus the DATES line "This final rule is effective October 2, 2026."

### F2. South Atlantic scamp and yellowmouth: 1 fish per person (Amendment 55, in force 6 Jul 2026)
- **Proposed citation:** 50 C.F.R. § 622.187(b)(2)(v), as revised by 91 Fed. Reg. 33661 (4 Jun 2026)
- **Primary URL:** https://www.federalregister.gov/documents/2026/06/04/2026-11221/fisheries-of-the-caribbean-gulf-of-america-and-south-atlantic-snapper-grouper-fishery-of-the-south
- **Effect:** In South Atlantic federal waters (east coast and the Keys Atlantic side), a diver may keep one scamp or yellowmouth combined per day, inside the 3-fish grouper aggregate. Before this rule the limit was three. A new recreational accountability measure can shorten the following year's season and set the bag to zero (§ 622.193(i)(2)).
- **Where:** South Atlantic EEZ. Species panel only; no geometry.
- **Effective:** 6 Jul 2026.
- **Related ids:** cfr-622-187 needs updating (it does not mention the limit). `species.json` scamp and yellowmouth-grouper eez_sa "bag" reads "Within 3 grouper/tilefish aggregate" and is missing the 1-fish cap. That is stale.
- **Status:** Confirmed on the FR full text (summarised).
- **Read verbatim:** § 622.187(b)(2)(v): "No more than one fish may be a scamp or a yellowmouth grouper, combined." Check it on the eCFR page for § 622.187 and confirm the paragraph number.

### F3. South Atlantic gag and black grouper vessel limit (Regulatory Amendment 36, effective 28 Oct 2026)
- **Proposed citation:** 50 C.F.R. § 622.187(b)(2)(i)(A), (B), as revised by 91 Fed. Reg. 61160 (28 Sep 2026)
- **Primary URL:** https://www.federalregister.gov/documents/2026/09/28/2026-19801/fisheries-of-the-caribbean-gulf-of-america-and-south-atlantic-snapper-grouper-fishery-of-the-south
- **Effect:** From 28 Oct 2026, a private recreational vessel may keep two gag and black grouper combined per day. For-hire vessels may keep two per trip. The per-person limit of one gag or black is unchanged. Today the vessel limit counts gag and black separately (two black per vessel, and the gag-only vessel limit). After 28 Oct it is one combined count. This affects every boat with two or more divers.
- **Where:** South Atlantic EEZ. Species panel only.
- **Related ids:** cfr-622-187 (its excerpt quotes the old gag-only vessel text). `species.json` black-grouper eez_sa "vessel": "2 black per vessel per day, private", and the atlantic "vessel" text, become stale on 28 Oct. The registry already notes Reg. Am. 36 only for the § 622.183 sea bass pot text (cfr-622-183, cfr-622-183-a2).
- **Status:** Confirmed on the FR full text (summarised).
- **Read verbatim:** the new § 622.187(b)(2)(i)(A): "The vessel limit for gag and black grouper on a vessel operating as a private recreational vessel is two fish per day" (the summariser reports it continues "in any combination").

### F4. Gulf Other SWG closure, 1 Jan to 30 Jun, from 2027: upgrade the source to the FR
- **Proposed citation:** 50 C.F.R. § 622.34(h), added by 91 Fed. Reg. 36545 (17 Jun 2026)
- **Primary URL:** https://www.federalregister.gov/documents/2026/06/17/2026-12175/reef-fish-fishery-of-the-gulf-of-america-shallow-water-grouper-management-measures
- **Effect:** From 1 Jan 2027, black grouper, scamp, yellowfin and yellowmouth are closed in the Gulf EEZ from 1 Jan to 30 Jun each year, with a zero bag. Amendment 62 does not touch this paragraph.
- **Related id:** fr-91-36545. It is currently secondary and cites the NOAA bulletin. Replace that URL with the FR document.
- **Status:** Confirmed on the FR full text.
- **Read verbatim:** "The recreational sector for Other SWG in or from the Gulf EEZ is closed from January 1 through June 30, each year."

### F5. 50 C.F.R. § 27.43: spears and gigs prohibited on every national wildlife refuge unless subchapter C authorises them (NEW)
- **Proposed citation:** 50 C.F.R. § 27.43
- **Primary URL:** https://www.ecfr.gov/current/title-50/chapter-I/subchapter-C/part-27/subpart-D/section-27.43
- **Effect:** The rule bans possessing a spear on a refuge, separately from taking fish. The registry relies on § 27.21 (no taking unless part 32 opens the refuge) and on refuge-specific method lists. It misses this possession rule. Part 32 never expressly authorises spears in Florida salt water. On the conservative reading, spearing is therefore not authorised even in refuges that § 32.28 opens to salt-water fishing without a gear list: St. Marks ("tidal and coastal waters 24 hours per day"), Lower Suwannee, Cedar Keys, Chassahowitzka, Pelican Island and Merritt Island. The counter-reading is that § 32.5(c) applies state law, under which spearing is legal gear, and that this is enough authorisation. Draw the closing reading and flag it.
- **Where:** Refuge waters, where the refuge boundary covers water. St. Marks (FWS says about 32,000 acres of bay and estuary lie within its boundary), Lower Suwannee, Cedar Keys and Chassahowitzka cover much of the nearshore Big Bend and Nature Coast. Only Cedar Keys (`nwr-cks`) and Merritt Island (`nwr-mrt`) of these are drawn. St. Marks, Lower Suwannee, Chassahowitzka, St. Vincent and Pelican Island are not drawn at all.
- **Effective:** 46 FR 47230 (1981); unchanged.
- **Related ids:** NEW. Interacts with cfr-50-27-21, the cfr-50-32-28-* family and open question 17 (refuge water boundaries).
- **Status:** Confirmed on the eCFR page. The full sentence came back in three fragments, all in order.
- **Read verbatim:** "The use or possession of cross bows, bows and arrows, air guns, spears, gigs, or other weapons on national wildlife refuges is prohibited except as may be authorized under the provision of this subchapter C." Also read § 25.11(a) (the subchapter reaches "areas of land and water held by the United States in fee title" and lesser interests). That text bears on whether state-owned bottom inside a refuge boundary is covered. It is the same question as Key West and Great White Heron (open question 1).

### F6. NPS weapon possession: 36 C.F.R. §§ 1.4(a) and 2.4(b) (NEW), plus the Everglades transit corridors, § 7.45(d)(9) (NEW)
- **Proposed citations:** 36 C.F.R. § 1.4(a) (definition of "weapon"); § 2.4(b)(1), (b)(2)(i)(B), (b)(3)(i); § 7.45(d)(9)
- **Primary URLs:** https://www.ecfr.gov/current/title-36/chapter-I/part-1/section-1.4 ; https://www.ecfr.gov/current/title-36/chapter-I/part-2/section-2.4 ; https://www.ecfr.gov/current/title-36/chapter-I/part-7/section-7.45
- **Effect:** "Weapon" includes a "speargun, hand-thrown spear". § 2.4(b)(1) prohibits "Possessing a weapon, trap or net" in any park unit. The exception applies where "The taking of fish is authorized by law in accordance with § 2.3". A further exception allows gear "packed, cased or stored in a manner that will prevent their ready use" in a vessel. Taking fish by spear is not authorised in Everglades or Dry Tortugas, so in those parks an uncased speargun aboard is an offence in itself. Dry Tortugas' § 7.27 breakdown rule already covers its waters; Everglades has no equivalent entry in the registry. § 7.45(d)(9) adds that gear legal in state waters but illegal in the park may be carried through Everglades only "over Indian Key Pass, Sand Fly Pass, Rabbit Key Pass, Chokoloskee Pass and across Chokoloskee Bay, along the most direct route to or from Everglades City, Chokoloskee Island or Fakahatchee Bay." A boat running from Flamingo or Florida Bay with spearguns aboard is exposed.
- **Where:** `npsever` (Florida Bay, Ten Thousand Islands park waters). The four passes could be markers.
- **Effective:** § 2.4 last amended 83 FR 47073 (2018). § 1.4 last amended 91 FR 52032 (12 Aug 2026, micromobility rule; the weapon definition is unchanged). § 7.45 last amended 72 FR 13706 (2007).
- **Related ids:** NEW. Attach to `npsever`, and to `npsdrto` alongside cfr-36-7-27.
- **Status:** Confirmed on the eCFR pages (fragments).
- **Read verbatim:** the § 1.4 "Weapon" definition; § 2.4(b)(1) and (b)(3)(i); § 7.45(d)(9) in full.

### F7. Crystal River NWR: FWS says there is no fishing in refuge waters
- **Proposed citation:** 50 C.F.R. § 27.21 (Crystal River is not in § 32.7(i)), supported by the FWS refuge fishing page
- **URL:** https://www.fws.gov/refuge/crystal-river/visit-us/activities/fishing
- **Effect:** "There is no fishing allowed in refuge waters", including the interior of Three Sisters Springs. "All established manatee sanctuaries (closed waters) prohibit all fishing." This supports drawing refuge waters (King Spring/Tarpon Hole, Warden Key) as closed year-round. `nwr-cry` is currently `warn`, with seasonal Three Sisters text only.
- **Related ids:** cfr-50-27-21, cfr-50-17-108, cfr-50-17-108-a; zone `nwr-cry`.
- **Status:** FWS page confirmed. This is the agency's own statement and is consistent with § 27.21, which is the authority to cite.
- **Read verbatim:** the two sentences quoted above on the FWS page.

### F8. Kings Bay manatee refuge: added spring closures and the year-round diving rule
- **Proposed citation:** 50 C.F.R. § 17.108(c)(14)(iv), (c)(14)(ix)(C)
- **URL:** https://www.ecfr.gov/current/title-50/chapter-I/subchapter-B/part-17/subpart-J/section-17.108
- **Effect:** When the temporary provisions in (v) or (vi) are in effect, swimming, diving (skin and scuba), snorkeling and fishing are barred near the sanctuaries and at Three Sisters, House, Jurassic and Idiot's Delight No. 2 springs. (ix)(C) prohibits "Diving from the surface on to a resting or feeding manatee(s)" year-round.
- **Related id:** cfr-50-17-108 cites only (c)(14)(ii)(A). Extend it.
- **Status:** Confirmed on the eCFR page (summarised). Section unchanged since 77 FR 15631 (2012).
- **Read verbatim:** (c)(14)(iv) in full.

### F9. FKNMS: no anchoring in federal-water SPAs, Conservation Areas and Restoration Areas from 19 Jan 2027
- **Proposed citation:** 15 C.F.R. § 922.164(e)(3), (f)(2), (g)(1), (h)(1), as promulgated by 90 Fed. Reg. 6104 (17 Jan 2025), effective 19 Jan 2027
- **Primary URL:** https://www.federalregister.gov/documents/2025/01/17/2025-00496/regulations-for-the-florida-keys-national-marine-sanctuary-management-review-blueprint-for-restoration
- **Effect:** These zones already ban fishing by any means. From 19 Jan 2027 a dive boat also may not anchor in them, so a diver going there must use a mooring buoy or drift. The large-vessel mooring rule (§ 922.163(a)(5)(x)) starts the same day. Federal sanctuary waters only; the Governor's certification keeps it out of state waters.
- **Where:** the federal-water SPAs, Conservation Areas and Restoration Areas in `fknms.json`.
- **Related ids:** NEW (cfr-922-164-d covers the fishing ban only).
- **Status:** Confirmed on the FR full text (DATES section).
- **Read verbatim:** "NOAA is delaying the effective date of Sec. Sec. 922.163(a)(5)(x) and 922.164(e)(3), (f)(2), (g)(1), and (h)(1) until January 19, 2027."

### F10. Big Cypress: federal basis for the freshwater spear ban
- **Proposed citation:** 36 C.F.R. § 2.3(d)(1)
- **URL:** https://www.ecfr.gov/current/title-36/chapter-I/part-2/section-2.3
- **Effect:** In every park unit, fishing in fresh waters by any means other than attended hook and line is prohibited. This is the direct federal ban for Big Cypress and for Everglades' fresh water. `npsbicy` cites only § 2.3(e) (salt water) and the state rule.
- **Related ids:** cfr-36-2-3 (add (d)(1)); zone `npsbicy`.
- **Status:** Confirmed on the eCFR page (paraphrased). Read (d)(1) verbatim.

### F11. Gulf greater amberjack 2026 to 2027 closure: upgrade the source to the FR
- **Proposed citation:** 91 Fed. Reg. 32360 (1 Jun 2026)
- **Effect:** Recreational Gulf AJ closes 14 Oct 2026 through 31 Jul 2027.
- **Related id:** noaa-fb26-029 (secondary, NOAA bulletin). Replace it with this FR cite.
- **Status:** Confirmed via the FR API. **Read verbatim:** "This temporary rule is effective from October 14, 2026, through July 31, 2027."

### F12. Smaller items to add as notes
- **De Soto National Memorial** (not in registry): the compendium (page updated 17 Jul 2026) prohibits anchoring, mooring or beaching watercraft in the park. There is no spear rule, and the park fishing page applies state law to saltwater spear fishing, sunrise to sunset. https://www.nps.gov/deso/learn/management/superintendents-compendium.htm . Read the anchoring sentence verbatim.
- **Pelican Island NWR** (not drawn): "Refuge waters are open year-round, except the posted buffer around Pelican Island (proper), which is closed year-round" (FWS page, secondary). Also subject to F5. https://www.fws.gov/refuge/pelican-island/visit-us/activities/fishing
- **Storm port-condition safety zones** (not in registry): § 165.849 (Sector Mobile, NEW, 91 FR 55479, effective 28 Sep 2026, Florida waters west of 84°04'34"W), plus the older §§ 165.706 (Miami), 165.707 (Keys), 165.720 (Jacksonville, Fernandina, Canaveral) and 165.781 (Western Florida). At ZULU, regulated areas are "closed to all vessel traffic except those specifically authorized by the COTP". These are vessel-movement closures announced by Broadcast Notice to Mariners. One generic entry would cover them; no geometry needed.
- **Fort Matanzas and Castillo compendia** (both approved 13 Jan 2026) and the **Timucuan** compendium (updated 3 Jun 2026) match ne-fl-nps-compendia. That entry can move from secondary once read verbatim. Fort Matanzas: "Jumping, diving, snorkeling, or swimming from the Monument's docks is prohibited."

---

## 2. Stale or wrong in the registry

| id | Problem | Fix |
|---|---|---|
| cfr-622-34-b | Still states the § 622.34(d) Gulf SWG Feb to Mar closure; removed effective 2 Oct 2026 (F1) | Rewrite the effect and excerpt; cite 91 FR 63502 |
| (species.json, regs.json) | Gulf grouper eez_gulf "closed" text and the regs.json grouper paragraph still carry the 20-fathom Feb to Mar closure (F1) | Remove it; keep the § 622.34(h) 2027 closure |
| cfr-622-187 | Missing scamp/yellowmouth 1-fish (Am. 55, 6 Jul 2026); gag/black vessel limit changes 28 Oct 2026 (F2, F3). Several numbers marked as summarised | Re-read § 622.187 after 28 Oct 2026 and update. species.json scamp and yellowmouth eez_sa bag, and black-grouper vessel text |
| fr-91-36545 | Secondary, NOAA bulletin URL | Upgrade to FR document 2026-12175 (F4) |
| noaa-fb26-029 | Secondary bulletin | Replace with 91 FR 32360 (F11) |
| cfr-622-188-a4 | Note says the Gulf descending-device continuation was "proposed 30 Jul 2026". The NOAA action page shows "Information Gathering", issued 30 Jul 2026, with no FR proposed rule. § 622.30(c) is shown on eCFR as "effective until January 14, 2026" | Reword: the Gulf requirement has lapsed and no rule is proposed in the FR |
| cfr-50-17-108 | Cites only (c)(14)(ii)(A) | Add (c)(14)(iv) and (ix)(C) (F8) |
| cfr-36-2-3 | Cites only (e) | Add (d)(1), freshwater hook-and-line only (F10) |
| nwr-cry (zone) | Drawn warn with seasonal text | FWS states no fishing in refuge waters year-round (F7) |
| cfr-635-21-h | Accurate today. Proposed rule 91 FR 52653 would revise § 635.71(b)(32) and replace (b)(35) | No change now; re-read after any final rule |
| cfr-600-725 | Secondary. Current eCFR rows (section last amended 6 Apr 2026) match the 2025 govinfo text for SA snapper-grouper, Gulf reef fish and both CMP rows | Read verbatim in a browser and upgrade |
| fr-91-60334 | The 2026 SA red snapper federal season (9 to 12 Oct) is over after 12 Oct | Mark as expired after 12 Oct 2026 |

No error was found in: cfr-622-182 (SMZs, unchanged since 2022), cfr-622-183-a2 (Warsaw Hole sunset 2 Aug 2027; Reg. Am. 39 on sunsetting is still at council-committee stage, with no FR proposed rule), cfr-622-180-b, cfr-622-74, cfr-622-410, cfr-36-7-27, cfr-36-7-45, bnp-compendium-dive, cana-compendium, cfr-922-164-d (eCFR § 922.164 still has no change after 2017), cfr-50-32-28 family, or the § 165.703 and § 165.785 updates.

---

## 3. Confirmed negatives (checked; these do not restrict spearfishing further)

- **50 C.F.R. § 622.188(b)**: spearfishing gear is authorised for South Atlantic snapper-grouper. (a)(4) has no spearfishing exemption from the descending device; registry correct. https://www.ecfr.gov/current/title-50/chapter-VI/part-622/subpart-I/section-622.188
- **Part 622 Federal Register, Jul 2025 to 7 Oct 2026**: the only permanent South Atlantic, Gulf reef fish or CMP rules are Am. 59 (red snapper ACL, 2025), Am. 55, Reg. Am. 36, 91 FR 36545 and Am. 62. Everything else is a quota closure, holdback or season notice. Pending proposals with no diver effect: SA Reg. Am. 37 (black sea bass, 91 FR 60076, comments to 22 Oct 2026), Coral Am. 11 / Shrimp Am. 12 (Oculina rock-shrimp access area, trawl only, 91 FR 59098, comments to 17 Nov 2026), SA Abbreviated Framework 5 (blueline tilefish ACL, 91 FR 42908), Gulf Am. 58B (deep-water grouper ACL, 91 FR 24500), CMP Framework 14 (Gulf Spanish mackerel ACL, 91 FR 46042). FR API: https://www.federalregister.gov/api/v1/documents.json?conditions[cfr][title]=50&conditions[cfr][part]=622&order=newest
- **Gulf HAPCs § 622.74**: unchanged since 85 FR 65746 (2020). Only (b), the Tortugas reserves, bans fishing for any species. Florida Middle Grounds has no anchoring or diver rule. https://www.ecfr.gov/current/title-50/chapter-VI/part-622/subpart-B/section-622.74
- **§ 622.185** (SA sizes): last amended 88 FR 65822 (2023); no 2026 change.
- **§ 622.10** (landing intact): finfish from the Gulf EEZ must be kept with head and fins intact (registry has no entry; this is a handling rule, not a closure). https://www.ecfr.gov/current/title-50/chapter-VI/part-622/subpart-A/section-622.10
- **Part 635 HMS**: § 635.21(h) and § 635.71(b)(30) to (35) are current and match the registry (eCFR to 1 Oct 2026). § 635.4(c)(1): a recreational HMS vessel "must obtain an HMS Angling permit". Mobulid ray retention ban, 91 FR 29371 (effective 22 Jun 2026), concerns retention only. **Proposed (watch):** HMS gear revisions, 91 FR 52653 (14 Aug 2026), comments to 13 Oct 2026. These would allow commercial sale of speargun-caught BAYS tuna under General, commercial-endorsed Charter/Headboat and Caribbean permits. Bluefin, sharks and billfish would not be added, and the in-water and no-powerhead rules are unchanged.
- **Other national marine sanctuaries**: Florida Keys is the only one in Florida. In designation: Hudson Canyon, Lake Erie, Pacific Islands Heritage. https://sanctuaries.noaa.gov/
- **FKNMS codification**: there is still no FR effective-date or codification notice for the Blueprint as of 7 Oct 2026 (FR phrase search since 18 Jan 2025). eCFR § 922.164 has had "No changes found for this content after 1/03/2017". Open question 15 stands.
- **FKNMS temporary coral-nursery special-use areas** (2023 to 2024): all expired, the last on 25 Oct 2024 (89 FR 68100).
- **NPS**: Biscayne compendium approved 17 Sep 2025, page updated 22 Jun 2026, no 2026 version; no FR special regulation for the Biscayne Marine Reserve Zone (FR search since 2024 finds none). Canaveral compendium 2026 has no spear rule. Gulf Islands has only a PWC rule (FR 2026-17198, 24 Aug 2026). The Everglades 2026 compendium adds no spear rule (underwater lights limited to handheld dive lights). Big Cypress compendium signed 22 Jul 2026 has no spear or gig rule. § 7.86(e)(1) defers to the general regulations and Florida law. NPS FR rules since Sep 2025 include nothing on fishing or weapons.
- **NWR § 32.28 and § 32.7**: § 32.28 last amended 88 FR 74063 (2023). The 2026 to 2027 station-specific rule (91 FR 56290, 1 Sep 2026) added no Florida refuge to § 32.7(i). Method lists that exclude spears are all freshwater or inland except those already in the registry: Loxahatchee (rods and poles; gigging and bow fishing allowed except from structures), Florida Panther ("We only allow hook and line"), Lake Woodruff ("We only allow use of hook and line"), St. Vincent (rods and poles in refuge lakes only). https://www.ecfr.gov/current/title-50/chapter-I/subchapter-C/part-32/section-32.28
- **§ 17.108(c)(1) to (13)** manatee refuges are speed rules only, with no diving or fishing ban in the text. The Florida manatee reclassification and critical habitat rules (2024 to 2025) are still only proposed.
- **ESA**: § 223.208 (Acropora take; last amended 2014), pillar coral endangered (Dec 2024), Caribbean coral and Nassau grouper critical habitat (these bind federal agencies, not divers), queen conch threatened (no 4(d) take rule found). These are species and take rules, not area closures.
- **33 C.F.R. part 334**: no Florida action in the FR since 2022. **Part 165**: no permanent Florida security or regulated zone added or removed since the Sep and Nov 2025 changes already in the registry, apart from the storm zone § 165.849. §§ 165.726 (Miami River RNA, mooring), 165.753 (Tampa Bay RNA, vessels 50 m and over broadcast) and 165.782 (restricted visibility) restrict no diving or fishing. The § 165.801 Table 7 proposal (91 FR 31398) has no final rule. Temporary zones live now: Key West Main Ship Channel and Fleming Key Cut, 500 ft around military support vessels, to 14 Oct 2026 (91 FR 58821); St. Johns River ship channel, Jacksonville, enforced during power-line work to 5 Mar 2027 (91 FR 50714); Miami Marine Stadium races 22 to 25 Oct 2026 (91 FR 64116).
- **36 C.F.R. part 327** (Army Corps projects): § 327.8(c) bars fishing in swimming areas and on boat ramps. § 327.13(a) allows weapons used for fishing "as permitted under § 327.8". No spear-specific ban.
- **EO 14430** (91 FR 60293, signed 17 Sep 2026): no agency action citing it in the FR as of 7 Oct 2026. It does not mention spearfishing, the Keys, parks or refuges. Watch dates: § 5(a) rescission actions from about 17 Oct 2026; § 6(d) sanctuary artificial-reef policy within 120 days (about 15 Jan 2027). https://www.federalregister.gov/documents/2026/09/22/2026-19417/restoring-american-saltwater-angling-and-recreation

---

## 4. Could not resolve

1. **F5 scope (§ 27.43)**: does part 32's opening of salt-water fishing "as governed by State regulations" count as authorising spears? Do refuge boundaries at St. Marks, Lower Suwannee, Cedar Keys, Chassahowitzka and Pelican Island cover the water (§ 25.11: "land and water held by the United States in fee title")? Ask the FWS Southeast Region refuge law-enforcement office. Same question as open questions 1 and 17.
2. **Gulf Islands NS projectile ban**: the compendium page (updated 1 Sep 2026) shows headings only, with no PDF link found. Still unresolved; call 850-934-2600.
3. **Dry Tortugas compendium**: no current compendium page found (URLs 404; the management index lists none). § 7.27 is current.
4. **§ 600.725(v) Secretarial Atlantic HMS rows**: the page truncated before them.
5. **FKNMS Blueprint Management Areas**: the preamble says Key Largo and Looe Key are kept as "Management Areas". The codified Blueprint text on speargun possession (current § 922.164(b)(1)(iv), cfr-922-164-b1) was not reached in the FR text. `fknms.json` carries "spearing" only for invertebrates. Read the Blueprint regulatory text for § 922.164 Management Areas in a browser (govinfo PDF 2025-00496, regulatory text near the end).
6. **Archie Carr NWR and National Key Deer NWR**: not in § 32.7, so § 27.21 closes taking. Whether either refuge has water is unconfirmed (FWS pages silent; Key Deer includes Blue Hole and backcountry islands). Neither is drawn.
7. **Gulf descending device**: no FR proposal found. Whether NOAA will reinstate the requirement, and whether it will exempt spearfishing, is unknown.
