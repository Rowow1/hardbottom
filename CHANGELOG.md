# Changelog

Changes to what the map says about the law are listed here with the date they were made, so anyone
who relied on an earlier version can see what changed. Code-only changes are summarised.

## 7 October 2026

- Offshore, where the USGS imagery stops, the satellite base now shows the 2016 Sentinel-2 mosaic
  beneath it instead of blank water.
- Phone layout: a compact header and shorter side panel give the map most of the screen, and the
  notice bar wraps instead of running off the edge.
- Search engines may now index the site; a sitemap lists the map and the About page.
- The map opens on satellite imagery (USGS NAIP) instead of the NOAA nautical chart. The chart is
  one click away in the base map control, or open the map with `?base=chart`. No legal content changed.

## 6 October 2026: first public release as Bottom Truth

- Renamed from "Florida Spearfishing Map" to Bottom Truth.
- Map text reworded so that it only states what the law closes or restricts, never that water or
  gear is lawful. Examples:
  - The Biscayne National Park zone, previously named "spearfishing IS legal" and drawn green, is
    now "Biscayne National Park: closures inside the park" and drawn amber. Its citation entry now
    lists the channel, harbor, Legare Anchorage and bonefish-area closures.
  - The Ft. Pierce Offshore Reef zone, previously named "(spearfishing allowed)", now names the
    gear the rule restricts.
  - Species and citation entries that read "spearing allowed" or "spearing is lawful" now say the
    rule "does not exclude spear as gear". The species panel's "Legal gear" label is now "Not
    excluded".
- Pier, jetty and bridge buffers are now shown when the map first loads.
- Em and en dashes removed from the map's own text; quoted law is unchanged.
- Removed stale claims that local ordinances outside Palm Beach County had not been read, and
  marked the City of Marathon canal rule (§ 18-27) as read.
- Licences set per file (MIT for code, CC BY 4.0 for the project's research, ODbL 1.0 for the three
  files derived from OpenStreetMap), with a full source list in `DATA-SOURCES.md`.
- Offline builds renamed `bottom-truth-offline.html` and `bottom-truth-offline-lite.html` and moved
  out of the repository into releases.

## 30 September 2026: statewide legal review

The full review, with every citation and the browser check of each excerpt, is in the project's
research notes and in `tools/law-updates/2026-09-30/`.

- Citation registry grew from 53 to 278 entries. A browser check compared 230 excerpts word for word
  with the primary source: 208 matched, 16 had trivial differences, 6 were corrected. After the review
  the registry held 246 entries verified word for word, 31 marked secondary (taken from a source other
  than the primary text, or not yet matched to it) and 1 unverified.
- Added 208 statewide zones: federal fishery closures and special management zones, Coast Guard and
  military zones, manatee No Entry zones, wildlife refuges and local ordinances.
- New closures found, among others: Biscayne National Park's seasonal bonefish closure and its 100 ft
  dive closure along marked channels; Mar-a-Lago east security zone changed to no entry (September
  2025); Old Tampa Bay north of the Gandy Bridge and Turkey and Crane Creeks closed to spears by gear
  rules; manatee No Entry zones closed to swimmers and divers; Western Dry Rocks closed to all
  fishing 1 April to 31 July; spearfishing gear banned in the Ft. Pierce Inshore and Key Biscayne
  AR-H special management zones; area-wide speargun or spearfishing bans in Venice, Cedar Key, Bal
  Harbour, Lauderdale-by-the-Sea, Treasure Island, Dania Beach and Sunny Isles Beach.
- Gulf Islands National Seashore: the 2021 projectile-gear ban is not in the compendium updated
  1 September 2026. Its status is unresolved and the Seashore is drawn amber.

## August 2026: first versions

- 22 August: first map, for the southeast Atlantic coast, expanded statewide the same day, with the Palm Beach County refuge areas and the state rule buffers.
- Late August: first citation verification pass (53 citations, 16 defects fixed).
