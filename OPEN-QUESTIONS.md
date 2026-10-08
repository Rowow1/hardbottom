# Open questions: what this map cannot yet answer

> **Release note (6 Oct 2026).** Zone names and popup text were reworded for the public release so that the map only states what is closed or restricted; the lines below keep the 30 September wording except where noted. Biscayne National Park is now drawn amber. Source questions raised during the licence review (two positions read from Esri imagery, unlocated use constraints for three FWC habitat layers) are listed in `DATA-SOURCES.md`.

> **Update after the browser pass (30 Sep 2026, morning).** Three findings changed after this document was drafted. (1) Gulf Islands National Seashore: the current compendium (updated 1 Sep 2026) no longer contains the 2021 projectile-gear ban, and the park's Florida fishing page now refers spearfishing questions to FWC. Zone `npsguis` is drawn amber (`warn`), not closed, with both facts and a call-the-park flag; `guis-compendium` stays `secondary`. The water boundary is one mile seaward of the low tide line at Perdido Key, Fort Pickens and Santa Rosa, and 100 yards at Naval Live Oaks. (2) Marathon's canal speargun ban is City of Marathon Code § 18-27, read verbatim on the city's own code site (`marathon-18-27`, which supersedes `marathon-canal`). (3) Eleven more local rules were found and added: Town of Palm Beach §§ 74-161 (no spearfishing gear on five named beaches) and 74-200, Tampa §§ 16-76 and 16-41(a), Redington Shores § 77-2, Naples § 42-52 (100 ft of the city pier, drawn), Ormond Beach § 15-6, Volusia County § 82-51, Wakulla County § 23.005(a)(5), Santa Rosa County § 14-52 (Navarre Beach posted bathing areas) and Escambia County § 74-36(18). Pompano Beach § 91.22 is now verbatim. The registry holds 278 entries. Where the text below disagrees with this note, this note is current.


**Regenerated from the map data on 30 September 2026.** The first part lists every feature in `data/zones-local.json` and `data/zones-statewide.json` whose `flag` is set: the app shows each with a warning mark before its name, a dashed outline and an "Open question" block in the popup. The second part ranks the questions that need a person (a phone call, a clerk, a plat or a browser read) rather than more desk research. The third part is the fresh/salt line, which is unsolved by design.

The project's rule applies throughout: where the law defines a boundary that no public dataset carries, the map says so rather than inventing geometry. A plausible polygon that turns out to be wrong is worse than an honest marker. Where a rule is ambiguous, the map draws the reading that closes more water and the flag says which reading was drawn.

---

## Flagged map features

The groups below sort the 110 flags by why the geometry differs from the law. Each line gives the zone id, the display name, its map kind (`closed`, `warn`, `open` or `line`), the file it lives in, the citations it joins to, and the flag text. Where several features in a group share identical flag text, the text is printed once at the head of the group as "shared text A" (or B) and each feature refers to it. Zones with an `active` value (when the rule applies) show it at the end of the line. The text is lightly normalised (dashes replaced by colons, commas or parentheses); the data files hold the originals, and a flag in the data files is the one to fix.

Flagged map features: 110 in total (10 in zones-local.json, 100 in zones-statewide.json), grouped into 12 categories below.

### 1. Local ordinances with words-only boundaries, drawn as the whole incorporated area (12)

- `spb54`, St. Pete Beach: speargun discharge banned citywide (closed; zones-local). Citations: City of St. Pete Beach Code § 54-4; Fla. Stat. § 790.33; Fla. Stat. § 379.2425(3); Fla. Admin. Code ch. 68B-3. Flag: The city limits shown are the TIGER municipal boundary, which includes the water parcels the city claims. How far St. Pete Beach's police power actually reaches into the Gulf is unresolved: Florida municipalities generally have jurisdiction only to their charter boundary, and sovereign submerged lands beyond it are state water. Treat the offshore edge of this polygon as soft.
- `kcb5`, Key Colony Beach: seasonal diving and snorkeling closure (warn; zones-local). Citations: City of Key Colony Beach Code § 5-11; Fla. Stat. § 379.2425; City of Key Colony Beach Code § 12-9. Flag: The 300 ft "improved shoreline" buffer is NOT drawn: no dataset distinguishes improved from unimproved shoreline. The whole city polygon is shown instead, which over-states the closure inland and under-states nothing.
- `loc-venice`, Venice: Spear fishing prohibited within or near city waters (closed; zones-statewide). Citations: City of Venice Code § 46-114. Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; the ordinance says 'within or near' city waters and never defines 'near', so the rule may reach beyond this outline. Venice Inlet is treated as closed.
- `loc-cedarkey`, Cedar Key: Spearing fish and other sea life prohibited within city limits (closed; zones-statewide). Citations: City of Cedar Key Code § 2-4.02.00. Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; the section does not state how far into the Gulf the city limits run.
- `loc-balharbour`, Bal Harbour: Discharging spearguns (compressed air, spring or band) in village waters prohibited (closed; zones-statewide). Citations: Village of Bal Harbour Code § 12-7. Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; 'waters within Bal Harbour Village' follow the village limits, whose seaward edge is not surveyed here.
- `loc-lbts`, Lauderdale-by-the-Sea: Loading a spear gun anywhere in town prohibited; no spearfishing on the public beach; 300 ft dive-free zone around the pier (closed; zones-statewide). Citations: Town of Lauderdale-By-The-Sea Code §§ 5-4, 5-5, 5-7(a). Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; the loading ban applies anywhere in the Town, land or water.
- `loc-ti222`, Treasure Island: Discharge of air, gas or spring-powered projectile weapons banned citywide, spearfishing excepted only where designated (closed; zones-statewide). Citations: City of Treasure Island Code § 22-2; City of Treasure Island Code § 58-34. Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; no designated spearfishing area was located. Whether the city treats state-law legality as 'designated as permissible' is an open question for the city clerk.
- `loc-sib`, Sunny Isles Beach: No fishing by spear in the Atlantic except in designated areas (closed; zones-statewide). Citations: City of Sunny Isles Beach Code § 108-4. Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; the section sits inside a dangerous-conditions provision; it may apply only during those conditions. Drawn as standing, the reading that closes more water.
- `loc-hallandale`, Hallandale Beach: Spearfishing and scuba on the public beach prohibited except in a designated area (warn; zones-statewide). Citations: City of Hallandale Beach Code § 16-23. Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; the rule reaches the 'public beach' seaward of the erosion control line; whether that carries into the water is not stated. No designated area was found.
- `loc-lantana`, Lantana: Spearguns, slings and harpoons prohibited on the municipal beach and in its waters (warn; zones-statewide). Citations: Town of Lantana Code § 5-18. Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; the rule covers the municipal beach 'and the waters'; the seaward extent is not stated.
- `loc-delray`, Delray Beach: Scuba diving prohibited from all areas of the municipal beach (warn; zones-statewide). Citations: City of Delray Beach Code § 101.34(B). Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; the code defines the municipal beach to include ocean waters within city limits.
- `loc-dania`, Dania Beach: Spearfishing gear banned on the beach and in the water; scuba confined to a designated area; 100-yard pier zone (closed; zones-statewide). Citations: City of Dania Beach Code § 6-12(b), (c). Flag: The ordinance describes its area in words only. The whole incorporated area is drawn, which over-states the closure on land and may under- or over-state how far it reaches offshore; the spear-gear sentence covers the public beach and 'the water' with no stated seaward limit.

### 2. Local ordinances drawn from a charted or published water area that differs from the words of the law (6)

- `ti58`, Treasure Island: John's Pass spearfishing ban (closed; zones-local). Citations: City of Treasure Island Code § 58-34; City of Treasure Island Code § 22-2. Flag: THE ORDINANCE HAS NO LATERAL LIMIT. It gives a distance out from two points but never says how wide the zone is. Half-discs of 1,500 ft radius are drawn here as the conservative reading: they cover every interpretation. A narrow reading would be a corridor only as wide as 127th Avenue. Also: OpenStreetMap's 127th Avenue does not reach the Gulf beach, so the western terminus used here is the end of the mapped street, not the mean high water mark. Both need a plat or a site visit.
- `sar130`, Sarasota County: no diving or spearfishing in marked channels (closed; zones-local). Citations: Sarasota County Code § 130-33(j). Flag: UNDER-INCLUSIVE. The polygon drawn is the FEDERAL project channel only. The ordinance says "any marked navigable channel", which also catches locally marked channels: New Pass, Big Pass, Venice Inlet approaches, and marked residential and marina channels that USACE does not maintain and no single dataset publishes. Assume more channel is closed than is drawn here.
- `mon26`, Lower Keys: speargun discharge banned in manmade canals (line; zones-local). Citations: Monroe County Code § 26-5; City of Marathon Code § 18-27; Fla. Stat. § 379.2425. Flag: PARTIAL COVERAGE, and drawn as centrelines rather than water polygons. OpenStreetMap canal coverage in the Keys is good but not complete, and this pull covers the LOWER Keys only: the stretch that matters, because everything above Long Key is already closed by Fla. Stat. § 379.2425. Canals inside the City of Marathon are also covered by the ban per the Monroe State Attorney, but Marathon's own code section has not been located. Absence of a line here does NOT mean a canal is open.
- `loc-boca-inlet`, Boca Raton Inlet: no swimming, diving or scuba (closed; zones-statewide). Citations: City of Boca Raton Code §§ 9-3, 9-4, 11-85. Flag: The ordinance runs from the jetty tips to a line 200 yards north of the A1A inlet bridge, which reaches into Lake Boca Raton beyond the charted inlet polygon. The Palmetto Park Road bridge zone on the ICW (100 ft north to 1,200 ft south, full width) is not drawn.
- `loc-pompano-hillsboro`, Hillsboro Inlet (Pompano Beach side): no swimming or diving (closed; zones-statewide). Citations: City of Pompano Beach Code § 91.22. Flag: Secondary: the ordinance's own boundary description has not been read. It also covers Hillsboro Bay and part of the ICW south of the inlet, which are not drawn.
- `loc-madeira-johnspass`, John's Pass: no swimming, diving or spearfishing (Madeira Beach side) (closed; zones-statewide). Citations: City of Madeira Beach Code § 78-3; City of Treasure Island Code § 58-34. Flag: The ordinance's limits are the two 128th Avenue extension lines, bay side and Gulf side, which no dataset carries. The charted pass polygon is drawn instead. Treasure Island § 58-34 covers the south side and 1,500 ft beyond each end.

### 3. Local structure buffers drawn from point inventories (8)

Shared text A, used by 3 features in this group: "NBI gives one point per bridge, not the span. Long bridges and causeways need the buffer along their whole length, and piers, docks and wharves named by the ordinance are not drawn."

- `loc-lwb-snook`, Lake Worth Beach: 500 ft of the Snook Island pier (closed; zones-statewide). Citations: City of Lake Worth Beach Code §§ 7-33(e), 7-78(b). Flag: The Snook Island pier is not named in FWC's inventory. The circle is centred on the Old Lake Worth Bridge fishing pier, the nearest inventoried structure at Snook Island. Confirm on site.
- `loc-pompano-pier`, Pompano Beach: 100 ft of the municipal pier (closed; zones-statewide). Citations: City of Pompano Beach Code § 98.12. Flag: FWC lists the rebuilt Pompano Beach pier as 'Fisher Family Pier'. The statewide 100-yard pier buffer already covers this water; the city rule adds swimming.
- `loc-annamaria-pier`, Anna Maria: 50 yards of the City Pier (warn; zones-statewide). Citations: City of Anna Maria Code § 110-122(3). Flag: Smaller than the statewide 100-yard pier buffer, which already closes this water to spearfishing.
- `loc-deerfield-pier`, Deerfield Beach: 50 yards of the pier (no swimming or snorkeling) (warn; zones-statewide). Citations: City of Deerfield Beach Code § 50-112(d). Flag: Secondary: the section's lead-in was not read. The statewide 100-yard pier buffer already closes this water to spearfishing.
- `loc-lee-lynnhall`, Lee County: Lynn Hall Park Pier, spear fishing banned (closed; zones-statewide). Citations: Lee County Code § 20-25(b); § 20-31(5). Flag: The county rule bans spears in all county park waters including 'adjacent littoral waters', whose extent is not defined. Only the Lynn Hall pier is drawn; every Lee County beach park is covered.
- `loc-br-melbourne`, Melbourne: 100 ft of a public bridge (14 bridges) (closed; zones-statewide). Citations: City of Melbourne Code § 40-2. Flag: shared text A.
- `loc-br-marcoisland`, Marco Island: 50 ft of a bridge (16 bridges) (closed; zones-statewide). Citations: City of Marco Island Code § 54-173. Flag: shared text A.
- `loc-br-sarasota`, City of Sarasota: 100 yards of a city bridge (23 bridges) (closed; zones-statewide). Citations: City of Sarasota Code §§ 10-62, 10-64 to 10-66. Flag: shared text A.

### 4. Local rules with no mappable geometry (marker only, or not a water closure) (8)

- `spb94`, St. Pete Beach: Blind Pass, no swimming or skin diving (warn; zones-local). Citations: City of St. Pete Beach Code § 94-1. Flag: GEOMETRY NOT MAPPED: this is a 150 m marker circle on a street intersection, NOT the closure. Three separate problems. (1) The ordinance's northern edge is "an extension of the centerline of 75th Avenue", a line the city never surveyed and no dataset carries. (2) OpenStreetMap has no water feature named Blind Pass anywhere near here (only Blind Pass ROAD) so the extent of "the waters of Blind Pass" is itself unresolved; the named inlet sits about 1.3 km NORTH of 75th Avenue, which makes "south of 75th Avenue" read as the back-bay channel rather than the inlet. (3) The § 94-1(2) Pass-a-Grille zone is not drawn at all. Resolving this needs the city plat or a call to St. Pete Beach.
- `loc-miamibeach`, Miami Beach: spear fishing banned from bridges, at the 29th to 33rd Street jetty area and in swim zones (warn; zones-statewide). Citations: City of Miami Beach Code §§ 82-441, 82-467. Flag: GEOMETRY NOT MAPPED. Lifeguard-tower swim zones (400 ft either side of each tower, 300 ft out, buoyed) and the 29th to 33rd Street jetty area are not in any dataset. The marker is a city centroid, not the closure.
- `loc-fmb`, Fort Myers Beach: spears prohibited in town parks and park waters (warn; zones-statewide). Citations: Town of Fort Myers Beach Code § 18-24(k)(1). Flag: GEOMETRY NOT MAPPED. Town parks and their waters are not drawn; the marker is a town centroid.
- `loc-bonita`, Bonita Springs: spears prohibited in city parks and park waters (warn; zones-statewide). Citations: City of Bonita Springs Code § 28-31(b). Flag: GEOMETRY NOT MAPPED. City parks (e.g. Little Hickory Island beach park) are not drawn; the marker is a city centroid.
- `loc-fortpierce`, Fort Pierce: spearing banned at listed places and in park areas (warn; zones-statewide). Citations: City of Fort Pierce Code §§ 28-1, 28-4, 28-31(18). Flag: GEOMETRY NOT MAPPED. Secondary: the section needs a full re-read. Park areas are defined to include waterways and beaches.
- `loc-dunedin`, Dunedin: no spears from the marina docks and seawalls (warn; zones-statewide). Citations: City of Dunedin Code §§ 86-108, 50-9. Flag: GEOMETRY NOT MAPPED. The marker is a city centroid, not the marina.
- `loc-lakepark`, Lake Park: no swimming, diving or fishing in the Harbor Marina (warn; zones-statewide). Citations: Town of Lake Park Code § 76-89. Flag: GEOMETRY NOT MAPPED. Secondary: only a fragment of the section was read.
- `loc-juno`, Juno Beach: loaded spear gun banned on beaches, the pier and public places (warn; zones-statewide). Citations: Town of Juno Beach Code § 16-4. Flag: NOT a water closure. Carrying an unloaded gun across the beach and loading it in the water is not addressed.

### 5. State rules whose boundary is undefined in law or only partly drawn (4)

- `vol`, Volusia County: inland salt waters, spearing restricted (warn; zones-local). Citations: Fla. Admin. Code r. 68B-3.008(3)(a). Flag: THE BOUNDARY IS UNDEFINED IN LAW. Rule 68B-3.008 never defines "inland salt waters" of Volusia County, and FWC publishes no boundary. What is drawn is the ICW channel as a landmark, NOT the extent of the rule. Treat the ENTIRE Halifax River / Mosquito Lagoon system, and every connected tidal creek, as covered. This is one of the two worst unmapped-boundary problems in the dataset.
- `man-66`, Manatee zone: No Entry (Nov 15 - March 31) Idle Speed (Apr 1 - Nov 14) (Indian River) (closed; zones-statewide). Citations: Fla. Admin. Code r. 68C-22.002(11); ch. 68C-22 No Entry zones; Fla. Admin. Code ch. 68C-22. Flag: R. 68C-22.007 (Indian River County) was amended effective 30 Jun 2026. FWC's GIS was last edited 13 May 2025, so this zone may have changed class. Read the current rule text. Active: NOV 15 - MAR 31.
- `st-oldtampabay`, Old Tampa Bay north of the Gandy Bridge: spears not on the allowed gear list (closed; zones-statewide). Citations: Fla. Admin. Code r. 68B-25.003(2). Flag: The rule covers Old Tampa Bay north of the Gandy Bridge AND every creek and bayou emptying into it. The drawn polygon is NOAA's charted 'Old Tampa Bay' area, whose south edge sits near the Gandy Bridge; the creeks and bayous are not drawn. Treat all of them as closed.
- `st-turkeycrane`, Turkey Creek and Crane Creek (Brevard): spears not on the allowed gear list (closed; zones-statewide). Citations: Fla. Admin. Code r. 68B-3.009(1)-(2). Flag: The rule's line is across each creek mouth at the Indian River Lagoon; the charted creek polygons end where the chart's detail ends and do not cover the full upstream reach. Treat the whole creeks as closed.

### 6. National parks and the Three Sisters manatee area (4)

- `npsbisc`, Biscayne National Park: closures inside the park (warn; zones-local; drawn green as `open` until 6 Oct 2026). Citations: 36 C.F.R. pt. 7 (no BNP section); Fla. Admin. Code ch. 68B-7; Biscayne National Park Superintendent's Compendium (approved 17 Sep 2025), 36 CFR 2.1, 3.16 and 3.18; Fla. Admin. Code r. 68B-7.008(5); Fla. Admin. Code r. 68B-7.008(1); 36 C.F.R. § 2.3(e). Flag: The 100-foot marked-channel dive closure is not drawn: it needs a channel or aids-to-navigation layer for the park. Treat every marked channel as closed to diving.
- `npsguis`, Gulf Islands National Seashore (warn; zones-local; the 1 Sep 2026 compendium no longer contains the 2021 projectile ban). Citations: Gulf Islands National Seashore Superintendent's Compendium (2021 onward), 36 CFR 1.5; park fishing pages; 36 C.F.R. § 2.3(e). Flag: The ban is sourced from the 2021 compendium release and a 2022 NPS fishing page. The current (2026) compendium text did not render for the research tools; read it before relying on the exact wording. The Seashore's offshore water boundary distance is also unconfirmed.
- `3sis`, Three Sisters Springs: scuba and spearfishing prohibited (seasonal) (closed; zones-local). Citations: 50 C.F.R. § 17.108(c)(14)(ii)(A). Flag: CORRECTED 22 Aug 2026: the previous centre was 350 m south of the springs, over a residential street. APPROXIMATE CIRCLE. USFWS publishes no GIS layer for the Kings Bay Manatee Refuge or the Three Sisters area: the boundary exists only as Federal Register text (77 FR 15617). The wider refuge is "all waters of Kings Bay, including all tributaries and adjoining waterbodies, upstream of the confluence of Kings Bay and Crystal River", which is far larger than the circle drawn.
- `drto-rna`, Dry Tortugas NP: Research Natural Area (partial outline) (closed; zones-statewide). Citations: 36 C.F.R. § 7.27(a)(14), (b)(3)(i), (e)(1), (e)(2); 36 C.F.R. § 7.27(b)(2), (b)(4)(ii). Flag: The law describes this area partly along a shoreline or by points that do not close into a ring, so only the published points or lines are drawn. The closed water is larger than what is shown; read the citation.

### 7. Federal fishery areas drawn as a partial outline or a line (2)

Shared text A, used by 2 features in this group: "The law describes this area partly along a shoreline or by points that do not close into a ring, so only the published points or lines are drawn. The closed water is larger than what is shown; read the citation."

- `gulf-tortugas-n`, Tortugas North marine reserve, EEZ portion (partial outline) (closed; zones-statewide). Citations: 50 C.F.R. § 622.410; 50 C.F.R. § 622.74(a) to (e). Flag: shared text A.
- `gulf-stressed`, Gulf reef fish stressed area, seaward line (powerheads prohibited shoreward) (warn; zones-statewide). Citations: 50 C.F.R. § 622.35(a)(1); app. B to pt. 622, table 2. Flag: shared text A.

### 8. National wildlife refuges: whether the refuge boundary covers the water is unconfirmed (9)

Shared text A, used by 9 features in this group: "Refuge boundaries on this layer include land and interest parcels. Whether the refuge boundary extends over the water shown has not been confirmed for this unit."

- `nwr-egk`, Egmont Key National Wildlife Refuge (warn; zones-statewide). Citations: 50 C.F.R. § 32.28(d)(4). Flag: shared text A.
- `nwr-gwh`, Great White Heron National Wildlife Refuge (warn; zones-statewide). Citations: 50 C.F.R. §§ 27.21, 32.7(i); § 26.21(a). Flag: shared text A.
- `nwr-isb`, Island Bay National Wildlife Refuge (warn; zones-statewide). Citations: 50 C.F.R. §§ 27.21, 32.7(i); § 26.21(a). Flag: shared text A.
- `nwr-kew`, Key West National Wildlife Refuge (warn; zones-statewide). Citations: 50 C.F.R. §§ 27.21, 32.7(i); § 26.21(a); 15 C.F.R. § 922.164(b)(1)(iv). Flag: shared text A.
- `nwr-map`, Matlacha Pass National Wildlife Refuge (warn; zones-statewide). Citations: 50 C.F.R. §§ 27.21, 32.7(i); § 26.21(a). Flag: shared text A.
- `nwr-hbs`, Nathaniel P. Reed Hobe Sound National Wildlife Refuge (warn; zones-statewide). Citations: 50 C.F.R. § 32.28(g)(4)(iii). Flag: shared text A.
- `nwr-pak`, Passage Key National Wildlife Refuge (closed; zones-statewide). Citations: 50 C.F.R. §§ 27.21, 32.7(i); § 26.21(a). Flag: shared text A.
- `nwr-pii`, Pine Island National Wildlife Refuge (warn; zones-statewide). Citations: 50 C.F.R. §§ 27.21, 32.7(i); § 26.21(a). Flag: shared text A.
- `nwr-pin`, Pinellas National Wildlife Refuge (warn; zones-statewide). Citations: 50 C.F.R. § 32.28(m)(4). Flag: shared text A.

### 9. Coast Guard security zones and regulated areas (33 C.F.R. part 165) drawn as lines, markers or envelopes (18)

Shared text A, used by 2 features in this group: "Vertex order corrected from the CFR listing (A-B-C-D drawn as A-B-D-C) because the literal order self-intersects."

- `uscg-165-703-a1ii-skyway`, Sunshine Skyway Bridge main span security zone (closed; zones-statewide). Citations: 33 C.F.R. § 165.703. Flag: Only the two CFR points across the main span are drawn. The zone is the Cut A channel under the main span plus the bridge columns, base and dolphins within the span; it does not include waters outside the main span. Active: always (no diving, anchoring, loitering); transit allowed.
- `uscg-165-703-a1iv-seaportmanatee`, Seaport Manatee security zone (closed; zones-statewide). Citations: 33 C.F.R. § 165.703. Flag: Drawn as the four-point envelope. The legal zone is only the 50-yard band along shore, seawall and piers inside it. Active: always.
- `uscg-165-703-a1vi-portsutton`, Port Sutton security zone (closing line) (closed; zones-statewide). Citations: 33 C.F.R. § 165.703. Flag: Only the closing line is drawn. Everything inside Port Sutton Channel landward of the line is closed. Active: always.
- `uscg-165-703-a1vii-hookerspoint`, Port of Tampa, west side of Hooker's Point, security zone (closed; zones-statewide). Citations: 33 C.F.R. § 165.703. Flag: Line only. The closed water is the 50-yard band between this line and the shore. Active: always.
- `uscg-165-703-a1viii-stpete-seawall`, St. Petersburg Harbor (Bayboro) security zone, seawall (closed; zones-statewide). Citations: 33 C.F.R. § 165.703. Flag: Line only between the two approximate CFR positions; the zone is the 50-yard band off the seawall plus the Coast Guard south moorings. Active: always.
- `uscg-165-703-a1viii-stpete-piers`, St. Petersburg Harbor (Bayboro) security zone, piers (closed; zones-statewide). Citations: 33 C.F.R. § 165.703. Flag: Line only; 50-yard pier buffer not drawn. Active: always.
- `uscg-165-703-a1ix-crystalriver-npp`, Crystal River power plant channel security zone (closed; zones-statewide). Citations: 33 C.F.R. § 165.703. Flag: shared text A. Active: always.
- `uscg-165-703-a1x-demorygap`, Crystal River Demory Gap Channel security zone (closed; zones-statewide). Citations: 33 C.F.R. § 165.703. Flag: shared text A. Active: always.
- `uscg-165-703-a1xii-weedon`, Weedon Island power plant security zone (closed; zones-statewide). Citations: 33 C.F.R. § 165.703. Flag: Line only. Closing leg is not stated in the CFR and was not guessed. Active: always.
- `uscg-165-705-zoneB-middlebasin`, Port Canaveral Middle Basin security zone (Zone B) (closed; zones-statewide). Citations: 33 C.F.R. § 165.705. Flag: Drawn as the CFR line only. The basin north and east of this line, to the land perimeter, is closed at all times. Active: always.
- `uscg-165-729-zoneC-gateslip`, Blount Island Gate Slip (Back River) safety and security zone, Zone C (warn; zones-statewide). Citations: 33 C.F.R. §§ 165.728, 165.729; 33 C.F.R. § 334.515. Flag: The law describes this area partly along a shoreline or by points that do not close into a ring, so only the published points or lines are drawn. The closed water is larger than what is shown; read the citation. Active: when a Maritime Prepositioned Ship is moored at Gate Terminal.
- `uscg-165-722-nasjax-anchors`, NAS Jacksonville security zone (St. Johns River) (closed; zones-statewide). Citations: 33 C.F.R. § 165.722. Flag: Markers only. Closed water is the band within 400 ft of mean high water along the NAS Jacksonville shore between the first and last markers. Active: always.
- `uscg-165-760-b3-pe-northport-line`, Port Everglades Mid-Port to North-Port fixed security zone (line) (closed; zones-statewide). Citations: 33 C.F.R. §§ 165.759 to .761, .785. Flag: Line only; zone is all water west of it to the port shoreline. Active: always.
- `uscg-165-760-b3-pe-southport-line`, Port Everglades Southport fixed security zone (line) (closed; zones-statewide). Citations: 33 C.F.R. §§ 165.759 to .761, .785. Flag: Line only; zone is all water between this line and the pier face. Active: always.
- `uscg-165-764-sectorkeywest`, Coast Guard Sector Key West security zone, Trumbo Point (closed; zones-statewide). Citations: 33 C.F.R. § 165.764; 33 C.F.R. § 334.610. Flag: Markers only. See 334.610 Area 3 for a drawn approximation of the same waters. Active: always.
- `uscg-165-777-westbasin`, Port Canaveral West Basin cruise ship security zone (line) (warn; zones-statewide). Citations: 33 C.F.R. § 165.777. Flag: Line only; the basin northwest of it is the zone. Active: when activated (MARSEC 2/3 cruise arrivals).
- `uscg-165-801-t7r7-pcola-airshow-box`, Pensacola Beach Air Show 'Show Box' safety zone (warn; zones-statewide). Citations: 33 C.F.R. § 165.801, Table 7. Flag: Box computed from distances in the CFR text, not from listed corners. The CFR measures 1000 yards south of Pensacola Beach, not of the reference point; the reference point appears to sit on the beach but this was not satellite-checked. Active: 2nd weekend in July, 4 days, per Notice of Enforcement.
- `uscg-165-775-a1-rna-outer`, Cape Canaveral launch RNA, outer boundary points (warn; zones-statewide). Citations: 33 C.F.R. § 165.775. Flag: Markers only. Active: launch periods only.

### 10. Army Corps restricted areas and danger zones (33 C.F.R. part 334) drawn as markers or lines only (28)

Shared text A, used by 2 features in this group: "The law describes this area partly along a shoreline or by points that do not close into a ring, so only the published points or lines are drawn. The closed water is larger than what is shown; read the citation."

Shared text B, used by 7 features in this group: "Markers only."

- `usace-334-500-a5-mayport-dangerzone`, NAVSTA Mayport munitions danger zone (line) (warn; zones-statewide). Citations: 33 C.F.R. § 334.500. Flag: Line only; closure along the basin shoreline not drawn. Active: during munitions movement, unannounced.
- `usace-334-500-a2a3-mayport-anchors`, NAVSTA Mayport restricted areas, St. Johns River and Atlantic (anchor points) (closed; zones-statewide). Citations: 33 C.F.R. § 334.500. Flag: Markers only. Closed water is the band within 380 ft of the NAVSTA Mayport shoreline and around the south jetty tip between these markers. Active: always.
- `usace-334-510-navyfuelpier`, Navy Fuel Depot pier restricted area, St. Johns River (waterward line) (closed; zones-statewide). Citations: 33 C.F.R. § 334.510. Flag: Waterward line only. The area is the water between this line and the shore, bounded by lines from each end on 328.5 deg T. Active: always.
- `usace-334-515-blountisland-anchors`, Blount Island Command restricted areas (anchor points) (closed; zones-statewide). Citations: 33 C.F.R. § 334.515. Flag: Markers only; offset legs follow the shoreline. Active: always.
- `usace-334-525-ksc-anchors`, Atlantic Ocean off Kennedy Space Center restricted area (anchor points) (warn; zones-statewide). Citations: 33 C.F.R. § 334.525. Flag: Markers only; the seaward edge is 1.5 nm off the KSC shoreline between the markers. Active: during launches or threats.
- `usace-334-540-bananariver-ccafs`, Banana River at Cape Canaveral SFS restricted area (line) (warn; zones-statewide). Citations: 33 C.F.R. § 334.540. Flag: Line only; closure along the station shoreline not drawn. Active: when closed for threats.
- `usace-334-595-ccafs-anchors`, Atlantic Ocean off Cape Canaveral SFS restricted area (anchor points) (warn; zones-statewide). Citations: 33 C.F.R. § 334.595. Flag: Markers only; seaward edge 1.5 nm off the shoreline. Active: when closed for threats.
- `usace-334-600-tridentbasin`, Trident Basin danger zone, Port Canaveral (entrance line) (closed; zones-statewide). Citations: 33 C.F.R. § 334.600; 33 C.F.R. § 165.705. Flag: Entrance line only; the whole Trident Basin behind it is closed. Active: always.
- `usace-334-610-a1-trumanannex-south`, Key West Naval restricted Area 1, Truman Annex south shore (closed; zones-statewide). Citations: 33 C.F.R. § 334.610. Flag: Line only; the closed water is the 100-yard band between this line and the Truman Annex south shore. Active: always.
- `usace-334-610-a2-trumanannex-west`, Key West Naval restricted Area 2, Truman Annex west shore and harbor (closed; zones-statewide). Citations: 33 C.F.R. § 334.610. Flag: Line only; the closed water lies between this line and the Truman Annex west shore and harbor. Active: always (transit corridor allowed).
- `usace-334-610-a4-flemingkey-west`, Key West Naval restricted Area 4, Fleming Key (west legs) (closed; zones-statewide). Citations: 33 C.F.R. § 334.610. Flag: Explicit west legs only; the 100-yard band around the rest of Fleming Key is not drawn. Active: always.
- `usace-334-610-a4-flemingkey-east`, Key West Naval restricted Area 4, Fleming Key (southeast legs) (closed; zones-statewide). Citations: 33 C.F.R. § 334.610. Flag: shared text A. Active: always.
- `usace-334-680-a2-tyndall-smallarms2`, Tyndall small-arms range Area 2, Gulf and St. Andrew Sound (line) (warn; zones-statewide). Citations: 33 C.F.R. § 334.680. Flag: Line only; closure along the shore not drawn. Active: during firing, red flag.
- `usace-334-700-a1-choctaw-west`, Choctawhatchee Bay west aerial gunnery range (explicit legs) (warn; zones-statewide). Citations: 33 C.F.R. § 334.700. Flag: Explicit legs only; two shoreline legs not drawn. Active: during announced firing.
- `usace-334-700-a1-choctaw-west-b`, Choctawhatchee Bay west aerial gunnery range (southwest leg) (warn; zones-statewide). Citations: 33 C.F.R. § 334.700. Flag: shared text A. Active: during announced firing.
- `usace-334-700-a2-choctaw-northshore`, Choctawhatchee Bay north shore aerial gunnery range (line) (warn; zones-statewide). Citations: 33 C.F.R. § 334.700. Flag: Line only. The zone is all water between this line and the north shore of Choctawhatchee Bay. Active: when activated.
- `usace-334-730-a2ii-santarosa-north-anchors`, Eglin restricted Area 2, Santa Rosa Island north side (anchor points) (warn; zones-statewide). Citations: 33 C.F.R. § 334.730. Flag: shared text B. Active: during high security threats.
- `usace-334-730-a2iii-hurlburt-anchors`, Eglin restricted Area 3, Hurlburt Field shore (anchor points) (warn; zones-statewide). Citations: 33 C.F.R. § 334.730. Flag: shared text B. Active: during high security threats.
- `usace-334-740-choctaw-northshore-anchors`, Choctawhatchee Bay north shore, Eglin restricted area (anchor points) (warn; zones-statewide). Citations: 33 C.F.R. §§ 334.740 to 334.748. Flag: shared text B. Active: during high security threats.
- `usace-334-742-camppinchot-anchors`, Eglin Camp Pinchot restricted area (anchor points) (warn; zones-statewide). Citations: 33 C.F.R. §§ 334.740 to 334.748. Flag: shared text B. Active: during high security threats.
- `usace-334-744-poquito-anchors`, Eglin Poquito housing restricted area (anchor points) (warn; zones-statewide). Citations: 33 C.F.R. §§ 334.740 to 334.748. Flag: shared text B. Active: during high security threats.
- `usace-334-748-wynnhaven-anchors`, Wynnhaven Beach, Eglin restricted area (anchor points) (warn; zones-statewide). Citations: 33 C.F.R. §§ 334.740 to 334.748. Flag: shared text B. Active: during high security threats.
- `usace-334-760-nsapc-alligatorbayou-anchors`, Naval Support Activity Panama City shoreline restricted area (anchor points) (closed; zones-statewide). Citations: 33 C.F.R. § 334.760. Flag: shared text B. Active: always.
- `usace-334-775-a1-naspensacola`, NAS Pensacola naval restricted area (a)(1), Pensacola Bay (line) (warn; zones-statewide). Citations: 33 C.F.R. § 334.775. Flag: Line only; closure along the NAS shoreline not drawn. Active: during naval operations.
- `usace-334-778-nas-b`, NAS Pensacola restricted area, Points 5 to 18 (Pensacola Bay to Bayou Grande) (closed; zones-statewide). Citations: 33 C.F.R. § 334.778. Flag: Line only; the area is the water between this line and the NAS shoreline. Active: always.
- `usace-334-780-seaplane`, Pensacola Bay seaplane restricted area (NAS small-boat training area) (closed; zones-statewide). Citations: 33 C.F.R. § 334.780. Flag: Line only. The closed water is everything inside this line and west of it to the NAS Pensacola shore. Satellite check needed before any polygon is drawn. Active: always.
- `usace-334-665-tyndall-threat-anchors`, Tyndall enhanced threat restricted area (23 shoreline points) (warn; zones-statewide). Citations: 33 C.F.R. § 334.665. Flag: Markers only; the band is 500 ft waterward of mean high water. Active: only when activated for a threat.
- `usace-334-720-missile-legs`, Gulf south from Choctawhatchee Bay, Eglin missile test area (seaward legs) (warn; zones-statewide). Citations: 33 C.F.R. § 334.720. Flag: Seaward legs only; the 3 nm offshore north edge from Santa Rosa Island to south of Apalachicola Bay is not drawn. Active: during announced firing periods.

### 11. Army Corps areas where a chord or straight segment stands in for a shoreline (not satellite-checked) (5)

- `usace-334-560-patrick`, Banana River at Patrick SFB restricted area (closed; zones-statewide). Citations: 33 C.F.R. § 334.560. Flag: Chord across Patrick SFB land stands in for the shoreline; not satellite-checked. Active: always.
- `usace-334-610-a3-trumbopoint`, Key West Naval restricted Area 3, Coast Guard station and Trumbo Point (closed; zones-statewide). Citations: 33 C.F.R. § 334.610; 33 C.F.R. § 165.764. Flag: East side is a chord across Trumbo Point. The true boundary follows the shore and may include water in Key West Bight east of the chord that is not drawn. Active: always (transit channels allowed).
- `usace-334-610-a5-bocachica-sw`, Key West Naval restricted Area 5, Boca Chica Key southwest shore (closed; zones-statewide). Citations: 33 C.F.R. § 334.610. Flag: Explicit legs only; the 100-yard shoreline offset between them is drawn as a straight segment. Active: always (channel transit allowed).
- `usace-334-640-apalachee-rocketrange`, Gulf south of Apalachee Bay, Air Force rocket firing range (warn; zones-statewide). Citations: 33 C.F.R. § 334.640. Flag: Inshore edge drawn as a chord. The true edge (3 miles off the shore) is up to about 3 km closer to shore than drawn, mainly at the west end off St. George Island. Active: during announced firing.
- `usace-334-778-nas-a`, NAS Pensacola restricted area, Big Lagoon to Point 4 (explicit points) (closed; zones-statewide). Citations: 33 C.F.R. § 334.778. Flag: Straight segments stand in for 500-ft shoreline offsets between Points 2, 3 and 4; the segment from Point 4 to Point 5 is not drawn. Active: always.

### 12. Army Corps areas with derived geometry, a defective CFR description or no operative prohibition (6)

Shared text A, used by 2 features in this group: "No operative prohibition in the current text of 334.762(b)."

- `usace-334-650-stgeorge-fan`, Gulf south of St. George Island, Army helicopter test firing range (warn; zones-statewide). Citations: 33 C.F.R. § 334.650. Flag: Arc centre derived from the corners, not stated as coordinates. The enforcing unit (Army Aviation Test Board, Fort Rucker) may no longer exist; currency of use unknown. Active: weekday daylight when firing.
- `usace-334-710-narrows-lune`, The Narrows and Gulf adjacent to Santa Rosa Island, Eglin restricted area (warn; zones-statewide). Citations: 33 C.F.R. § 334.710. Flag: Undefined 'segment' drawn as the full lune (conservative). Active: intermittent daylight use.
- `usace-334-762-nb1`, NSA Panama City restricted area NB-1 (warn; zones-statewide). Citations: 33 C.F.R. §§ 334.761 to 334.763. Flag: No operative prohibition in the current text of 334.762(b). NB-1 lists its 'Southeast point' at the same longitude as its 'Northwest point'; drawn as printed. Active: during training events.
- `usace-334-762-nb2`, NSA Panama City restricted area NB-2 (warn; zones-statewide). Citations: 33 C.F.R. §§ 334.761 to 334.763. Flag: shared text A. Active: during training events.
- `usace-334-762-nb3`, NSA Panama City restricted area NB-3 (warn; zones-statewide). Citations: 33 C.F.R. §§ 334.761 to 334.763. Flag: shared text A. Active: during training events.
- `usace-334-763-gulf`, NSA Panama City restricted area, Gulf of Mexico (warn; zones-statewide). Citations: 33 C.F.R. §§ 334.761 to 334.763. Flag: No operative prohibition in the current text of 334.763(b). Active: during training events.
---

## Questions that need a human, ranked

Ranked by how much water, or how many dives, the answer moves. Resolved items from the 22 August list are kept below the open ones with how they were resolved.

### Open

1. **Key West and Great White Heron national wildlife refuges: open or closed?**
   50 C.F.R. § 27.21 bars taking any animal on a refuge unless part 32 opens it, and part 32 does not open either refuge. The Fish and Wildlife Service's own pages say refuge waters are open to fishing, snorkeling and diving under state law, the submerged land is state-owned, and it is co-managed under the 1992 Backcountry Management Agreement. Both are drawn `warn` with the conflict stated (`nwr-kew`, `nwr-gwh`). Ask the Florida Keys National Wildlife Refuges Complex which reading its officers enforce, and whether § 25.12 "waters administered by FWS" excludes the state-owned bottom.

2. **Volusia County: what are the "inland salt waters"?**
   R. 68B-3.008 never defines them and FWC publishes no boundary (`vol`). Ask FWC's Division of Law Enforcement how the line is enforced. Until then assume the whole Halifax River and Mosquito Lagoon system.

3. **Federal mackerel gear: may a recreational diver spear king mackerel or Atlantic Spanish mackerel in federal waters?**
   50 C.F.R. § 622.375(a)(1) lists "the only fishing gears that may be used" in directed fisheries for king and Spanish mackerel, and the spear is absent for Atlantic king, Gulf king and Atlantic Spanish mackerel. Paragraph (b)(3) makes a person aboard with unauthorized gear subject to the bag limits, and the List of Fisheries (§ 600.725(v), 2025 edition) lists spear as authorized recreational gear for coastal migratory pelagics. "Directed fisheries" is undefined. The species panel treats spearing them in the EEZ as not authorized. Ask NOAA Fisheries Southeast Regional Office, and read the current § 600.725(v) rows (version effective 6 Apr 2026).

4. **Is a dive charter a "vessel for hire" under r. 68B-14.009(4)?**
   The 1 September 2026 amendment added an Atlantic For-Hire Reef Fish Registry for 2026 to 2028: a vessel for hire "may not harvest, attempt to harvest, or possess" the 13 listed species in Atlantic waters unless its owner, operator or custodian has registered. The rule does not say whether a boat that carries paying spearfishers is covered. FWC, 850-487-0554.

5. **Venice § 46-114: how far is "near"?**
   "It shall be unlawful for any person to engage or attempt to engage in spear fishing within or near the territorial waters of the city." The whole city polygon is drawn (`loc-venice`) and Venice Inlet treated as closed. Ask the Venice city clerk or the police marine unit what distance they apply.

6. **Treasure Island: § 22-2 "designated as permissible", and the width of § 58-34.**
   § 22-2 bans discharging spring, gas or mechanically powered projectile weapons citywide except "to a person spear fishing in any area where such activity has been designated as permissible either by the city, the state or the federal government." Does the city treat water where state law allows spearfishing as "designated"? If not, the whole city is closed to spearguns (`loc-ti222`). Separately, § 58-34 gives a 1,500-ft distance out from two points and no lateral limit (`ti58`). Treasure Island city clerk.

7. **Sunny Isles Beach § 108-4: a standing rule or a dangerous-conditions rule?**
   "Except in designated areas, no person shall fish in the Atlantic Ocean by use of hook and line, seine, trap, spear gig or other device." The sentence sits in a section on swimming and dangerous conditions; the history note was not shown. Drawn as standing (`loc-sib`). City clerk.

8. **Lee County § 20-25: how far do "adjacent littoral waters" run?**
   County parks, defined to include beaches, piers and adjacent littoral waters, ban fishing with spears at all times. Only the Lynn Hall pier is drawn (`loc-lee-lynnhall`). Ask Lee County Parks and Recreation for the seaward extent, and for a list of the beach parks it applies to.

9. **Hallandale Beach § 16-23: does the "public beach" include the water?**
   Spearfishing and scuba are banned on the public beach, defined as land seaward of the erosion control line, "except within a designated area"; no designated area was found (`loc-hallandale`). City clerk.

10. **Twelve state parks with no mapped water: is the water beside them park water?**
    The MPA Inventory lists Yellow River Marsh Preserve, Estero Bay Preserve, Indian River Lagoon Preserve, Pumpkin Hill Creek Preserve, Amelia Island, Fred Gannon Rocky Bayou, Mound Key Archaeological, Navarre Beach, San Marcos de Apalache Historic, Dr. Julian G. Bruce St. George Island, The Barnacle Historic and Werner-Boyce Salt Springs, none of which has a polygon in `data/parkwaters.json`. FDEP's inventory figures record little or no submerged area for most of them. Spearfishing is banned in every park's waters (r. 62D-2.014(9)(d); r. 68B-20.003(2)(e)); the open point is how far the Division of Recreation and Parks' jurisdiction runs over adjoining sovereign submerged land, and whether the 400-ft reference in r. 62D-2.014(9)(b) (commercial food and bait fishing within 400 ft of mean high water inside a park's riparian lines) implies that the park's water reaches at least that far. Ask the FDEP Division of Recreation and Parks. Until answered, treat water beside these parks as closed.

11. **City of Marathon: what is the code section for the canal speargun ban?** RESOLVED 30 Sep 2026: § 18-27.
    The Monroe County State Attorney lists Marathon's manmade canals alongside unincorporated Monroe (`marathon-canal`, secondary). Municode's API could not resolve the client. Marathon City Clerk, or a browser search of library.municode.com/fl/marathon for "speargun", "spear gun", "canal" and "manmade".

12. **St. Pete Beach § 94-1: where is "Blind Pass south of the 75th Avenue centerline"?**
    Unchanged from August (`spb94`). Pull the plat or call the city clerk; also get the § 94-1(2) Pass-a-Grille description into coordinates.

13. **John Pennekamp 2026 lobster zones: are the seven-zone coordinates right?**
    R. 68B-24.0065 was amended effective 1 July 2026 to seven Coral Formation Protection Zones. Every web mirror still shows the 1995 ten-zone table, and the drawn zones (`penncpz-*`) come from the proposed-rule notice (FAR Vol. 51 No. 161), adopted without change. Check every corner against the flrules .doc, tid 30968625. Lobster only; the park is closed to spearfishing regardless.

14. **Indian River County manatee amendment: is the Vero Beach No Entry zone gone?**
    R. 68C-22.007 was amended effective 30 June 2026; the proposed rule converted (1)(e) from seasonal No Entry to Idle Speed all year, and the notice of change left (e) as proposed. FWC's layer (last edited 13 May 2025) still shows No Entry (`man-66`). Read the adopted text, flrules tid 31013148. Also confirm whether manatee zones bind before they are posted (rr. 68C-22.001, 68C-22.004 not read).

15. **FKNMS: which rulebook applies where, and will NOAA codify it?**
    The Restoration Blueprint governs federal sanctuary waters, the 1997 zoning governs state waters, and eCFR still shows the old text. NOAA said in March and June 2026 that it would publish a notice codifying the split; none has appeared. Two 1997 zones in the MPA Inventory (French Reef SPA; Looe Key Research Only Area) have no same-named zone in NOAA's post-Blueprint GIS. FKNMS, 305-809-4700.

16. **Executive Order 14430: what will agencies propose?**
    Signed 17 September 2026 (91 FR 60293); section 5 directs agencies to begin, within 30 days, action to suspend, revise or rescind regulations that burden anglers, boaters and outdoor businesses (secondary quotation). Watch the Federal Register from mid-October 2026 for proposals touching FKNMS zoning, NPS compendia, refuge fishing rules or federal fishery closures.

17. **National wildlife refuge water boundaries.**
    Nine refuges are flagged because the Fish and Wildlife Service boundary layer includes land and interest parcels, and it is not confirmed that the refuge boundary covers the water drawn (Egmont Key, Great White Heron, Island Bay, Key West, Matlacha Pass, Hobe Sound, Passage Key, Pine Island, Pinellas). Ask FWS Division of Realty or each refuge for the water boundary. Hobe Sound (rods and reels and poles and lines only), Pinellas (fishing only from vessels around Tarpon Key) and Egmont Key (two attended poles) exclude spearfishing on the conservative reading, so their water extent decides real closures.

18. **Oculina Bank HAPC coordinate table defects.**
    § 622.224(b)(1) prints point 21 as "79°54″" (read as 79°54′), its opening origin as 80°14′48.06″W and its closing origin as 80°14′55.27″W; the 2015 correction (80 FR 61486) prints only points 7 and 8. The HAPC ban reaches bottom gear and anchoring by fishing vessels, and the experimental closed area inside it (a clean box) is unaffected. Ask NOAA Fisheries Southeast Regional Office, or find the Council's source table.

19. **Gulf Islands National Seashore: was the 2021 projectile ban rescinded?** The current compendium does not contain it; the water boundary is now known (one mile off Perdido Key, Fort Pickens and Santa Rosa; 100 yards at Naval Live Oaks). Call 850-934-2600.
    The projectile ban is sourced from the 2021 compendium release and a 2022 NPS page; the current compendium (updated 1 Sep 2026) did not render, and the NPS fishing page's offshore boundary sentence was truncated. Read both in a browser: nps.gov/guis/learn/management/compendium.htm and nps.gov/guis/planyourvisit/fishing-in-florida.htm.

20. **Sarasota County § 130-33(j): which channels count as "marked"?**
    Unchanged from August (`sar130`). Only the federal project channel is drawn. City of Sarasota § 10-64 has the same marked-channel rule inside city limits.

21. **Palm Beach chs. 59-1699 and 59-1702: pull the session-law text.**
    Unchanged from August. The county code version has been read verbatim; the 1959 Laws of Florida have not (State Library scans block automated fetch).

22. **FWC Critical Wildlife Areas bind only where posted.**
    Unchanged from August. R. 68A-19.005 attaches to posting, not to the GIS; the 37 drawn areas are evidence, not the trigger.

23. **Monroe County ch. 26 art. IV: the 300-ft lobster-season diving ban.**
    A county flyer describes a ban on diving and snorkeling within 300 ft of improved shoreline, in canals and in marinas around the lobster seasons (`monroe-26-art4`, unverified). News reports also describe a proposed 300-ft bridge ban. Read Monroe County Code ch. 26 art. IV on Municode in a browser.

24. **Pompano Beach § 91.22 Hillsboro Inlet boundary.**
    Drawn from the charted inlet (`loc-pompano-hillsboro`); the ordinance's own boundary description was not read. codelibrary.amlegal.com/codes/pompanobeach/latest/pompanobeach_fl/0-0-0-81781.

25. **The 26 jurisdictions whose codes need a browser read.**
    Listed in `research/municipal-ordinance-sweep.md`. Highest priority: Town of Palm Beach ch. 74 art. III, Martin County ch. 83, Marathon, Pinellas County, St. Petersburg, Naples, Hollywood, Santa Rosa County and the Santa Rosa Island Authority (Pensacola Beach).

### Resolved since 22 August 2026

- **Madeira Beach ch. 78 (was question 4).** Read verbatim on 30 Sep 2026 through Municode's API. § 78-3(a) bans swimming, diving, floating, spearfishing and skin diving in John's Pass between the 128th Avenue extension lines at Boca Ciega Bay and the Gulf (`madeira-78-3`). Unlike Treasure Island § 58-34 it has no 1,500-ft extension into the Gulf or the bay. Drawn from the charted pass (`loc-madeira-johnspass`).
- **Legare Anchorage coordinates (was question 6).** The Biscayne Superintendent's Compendium (approved 17 Sep 2025) bounds it by latitude 25°29′ and 25°30′ N and longitude 80°07′ and 80°08′ W; r. 68B-7.008(4) matches. Drawn as `bnp-legare`. The compendium also closes diving within 100 ft of every marked channel, which is not drawn (see `npsbisc`).
- **Treasure Island § 58-34 wording (part of was question 5).** Now read verbatim; it confirms there is no lateral limit, so the width question stays open (question 6 above).
- **FKNMS (was question 7).** Partly resolved: no 2026 change to the sanctuary rules was found, and Florida's own rules (rr. 68B-6.002, 68B-6.003(1)(b)) now back the state-water zones. The codification question stays open (question 15).
- **Jacksonville ch. 388.** Whole-code search on 30 Sep 2026 found no spear, speargun, scuba or snorkel provision; the only diving rule bars diving from a City dock (§ 28.723). Recorded as `neg-jax-388`.
- **City of Miami § 61-35 (weapons).** Whole-code search on 30 Sep 2026 returned no hits for the search terms; the lead was not found. Recorded as `neg-miami-city`. Hialeah also returned zero hits.
- **Stuart ch. 30, Panama City Beach ch. 7, Islamorada, Pinellas Park § 16-110.** Resolved as negatives for spearfishing (`neg-stuart-panamacitybeach`): Stuart and Panama City Beach bar only diving from piers and docks; Islamorada's rule is a lobster-season diving and snorkeling ban; Pinellas Park § 16-110 is a nudity ordinance.
- **Miami Beach (August "probable negative").** Overturned: § 82-441 bans fishing by spear from bridges, in the 29th to 33rd Street jetty area and in lifeguard swim areas (`miamibeach-82-441`).
- **Gulf Islands National Seashore compendium (August flag).** Partly resolved: the 2021 compendium's projectile ban has been found and the Seashore is drawn `closed`; the current text is still unread (question 19).
- **Biscayne ch. 68B-7 "no spear prohibition".** Overturned: r. 68B-7.008(5) has closed a bonefish area to all fishing from 1 March to 31 May since 4 November 2025.

---

## Unsolved by design: the fresh/salt line

This is a gap in the law, not in the data, and it is not going to close.

Florida's test for salt water is a taste test: water that has become "unpalatable because of the saline content", Fla. Stat. § 379.101(33). There is no salinity threshold in fisheries law, no per-river list and no FWC GIS layer. Only the Steinhatchee River has a designated boundary. The one numeric salinity line in Florida law, 1,500 mg/L chloride in Fla. Admin. Code r. 62-302.200(30), belongs to DEP water-quality classification, not to FWC licensing, and FDEP's surface-water GIS carries only the specially classified named waters, not a statewide marine/fresh split. That was checked directly: the layer exists and does not contain what would be needed. R. 62-302.200 was amended on 25 November 2025 without changing (30), and § 379.101 was last amended in 2025 without changing (33).

**What the map does instead.** Every bridge, pier and ramp carries a coastal, tidal or inland classification inferred by nearest-neighbour vote from FWC's own labelled ramps (95.1 per cent leave-one-out agreement). The "Inland waters" toggle hides everything classified inland in one click (4,958 bridges and 239 piers), so the interior of the state can be dismissed wholesale. The classification is a planning heuristic with no legal force, and every popup says so.

**Why that is enough in practice.** The question only bites in brackish water, where visibility is usually too poor to hunt. Where it does bite, carry both licences and treat the stricter regime as controlling: the freshwater side is where the speargun ban lives.
