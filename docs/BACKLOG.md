# Application backlog

Distinct from `OPEN-QUESTIONS.md`, which is the legal research queue. This is what to build. Ranked.
Last reviewed 7 October 2026.

## Done at launch (7 October 2026)

- Site public at bottomtruth.com; repository public; search engines admitted with a sitemap.
- Phone layout checked at 360, 390 and 820 px wide (headless Chromium) and fixed: compact header,
  wrapping notice bar, smaller attribution.
- OpenStreetMap-derived geometry rebuilt from NOAA ENC, USGS NHD and TIGER; the three files are now
  CC BY 4.0. The `ti58` and `3sis` positions re-read from USGS NAIP.

## Next

5. **A reporting channel that does not need GitHub.** The About page sends error reports to GitHub
   issues, which only works once the repository is public and needs a GitHub account. A contact
   email would widen it.
6. **Season dates expire.** `regs.json`, `species.json` and several `law.json` lines carry 2026
   dates. The re-check calendar from the 7 Oct 2026 pass: 9, 12, 14, 15, 23 and 28 Oct 2026; 1 Nov
   and 1 Dec 2026; 1 and 5 Jan 2027 (the main sweep, when the 2026 executive orders and temporary
   rules lapse); then each FWC and NMFS season announcement through 2027.

## High value

5. **The two ERDDAP overlays.** Sea temperature and Kd490 water clarity failed or took more than 20 s
   on 30 Sep. Try the CoastWatch central node (`coastwatch.noaa.gov/erddap`) or NOAA Coral Reef Watch,
   or drop them.
6. **Wikimedia Commons photos for the spots.** 229 of 283 spots have no media; Commons was unreachable
   from the research tools. `tools/src-2026-09-30/commons-candidates.json` holds 10 files to check.
7. **The 100 ft Biscayne channel dive closure** needs a channel or aids-to-navigation layer for the park.
8. **Buffers statewide.** The R. 68B-20.003(2) beach, pier, bridge and jetty buffers are drawn only in
   Palm Beach County. Pier and confirmed-bridge circles exist statewide; beaches and jetties do not.
9. **Madeira Beach and Treasure Island lines** at 127th and 128th Avenues need street geometry; St. Pete
   Beach § 94-1 now has a charted "Blind Pass" polygon in ENC named sea areas worth checking against
   the ordinance.
10. **Printable boat sheet, statewide**, regenerated from `regs.json` and `species.json`.

## Worth doing

11. **Offline tiles** for the boat: a low-zoom coastal pack of the NOAA chart.
12. **Sweep app prose against `law.json` automatically.** `tools/test-data.py` now checks law ids; it
    does not yet diff citation text in `regs.json` and popups against the registry.
13. **Split the full offline build** further or lazy-load per region; 15 MB is heavy on LTE.
14. **Trip mode** (launch, date, species → closures that apply). Read the UPL section of the
    publishing plan first.
15. **Bridge ground-truth loop** for the 6,041 presumed-buffered bridges.

## Known debt

- `jurisdiction.json`: the `gom` array repeats all 230 `atl` paths. The app drops the repeats at load;
  fix the file at the source.
- `piers.json`: Fort Pickens pier filed under Santa Rosa (it is Escambia); "Ft. Pierce Jetty Park"
  operator reads "City of Fort Worth".
- `sites.json`: "Ft. Lauderdale, C-1 Reef (Sheridan Express)" depth of 25 ft looks wrong.
- `zones-palmbeach.json` predates the zones schema; migrate it.
- `zones-local.json` cannot be rebuilt from source because its August raw pulls are not kept.
- Existing popup strings still contain em dashes; new strings do not.

## Added 8 Oct 2026 (second review)

- Rebuild `jetties.json` and the `dk`/`sp` bridge fields from NOAA ENC shoreline construction and
  BRIDGE areas instead of OpenStreetMap ways, as was done for the zone files on 7 Oct 2026, so those
  files can leave the ODbL group (LICENSE-DATA.md section 2a). The structure-by-structure review notes in
  `tools/jetties-2026-10-07/review.py` say which records are OSM and which are ENC or traced.
- Draw the canal gear rules (Pinellas County, Cape Coral, Sanibel, Naples, Collier, Brevard, Satellite
  Beach) from USGS NHD canal flowlines, as `mon26` is drawn.
- Read Melbourne Beach § 40-33 and Cocoa Beach § 5-56 verbatim, the Naples ch. 90-469 canal table and
  Collier § 210-67 Exhibit A in full, and r. 68B-35.004(5).
