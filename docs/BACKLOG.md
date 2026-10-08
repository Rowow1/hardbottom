# Application backlog

Distinct from `OPEN-QUESTIONS.md`, which is the legal research queue. This is what to build. Ranked.
Last reviewed 6 October 2026.

## Blocking (before the site is unlocked)

1. **Look at the map in a real browser** on a desktop and a phone, on the password-protected
   Hostinger deployment: layout, the legend, the What's here popup and the About page.
2. **Make the repository public** at launch, so the About page links (issues, changelog, sources)
   resolve. Until then they return 404 for visitors.
3. **Recompute the OpenStreetMap-derived offsets** (`zones-palmbeach.json` refuge edges and 3 nm line,
   `sites.json` `ref` and `edge`) from the NOAA ENC coastline, which would move those files from ODbL
   to CC BY 4.0. Optional: ODbL is a valid licence for them as they stand.
4. **Re-read the two imagery positions** in `zones-local.json` (`ti58` John's Pass corridor, `3sis`)
   from USGS NAIP instead of Esri imagery, and correct the `ti58` source text.

5. **A reporting channel that does not need GitHub.** The About page sends error reports to GitHub
   issues, which only works once the repository is public and needs a GitHub account. A contact
   email would widen it.
6. **Season dates expire.** `regs.json` and several `law.json` effect lines carry 2026 season dates
   (red snapper, gag, amberjack, hogfish) that lapse from October 2026. Set a review date after each
   FWC and Gulf or South Atlantic council season announcement.

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
