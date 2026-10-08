# Data licences

The files in `data/` are licensed per file. The code licence in `LICENSE` (MIT) does not cover them.
Every current file falls into one of two groups, depending on where its content came from: the
project's own work (group 1) or redistributed public data (group 3). Group 2 records earlier versions
of five files that were derived from OpenStreetMap; no current file carries OpenStreetMap geometry.
The full record of sources, record counts and derivations is in `DATA-SOURCES.md`.

## 1. The project's own research: CC BY 4.0

These files hold the project's legal research, curation and classification:

`law.json`, `regs.json`, `species.json`, `coverage.json`, `closures.json`, `zones-statewide.json`,
`zones-local.json`, `zones-palmbeach.json`, `jetties.json`, `beaches.json`, `spots.json` (descriptions
and curation), and the fields added to `bridges.json` (`st`, `iw`, `iwr`, `rv`, `ds`, `dk`, `sp`),
`piers.json` (`iw`, `iwr`) and `sites.json` (`ref`, `edge`, `closed`, `iw`, `iwr`). The site positions
and descriptions in `sites.json` are FWC and Palm Beach County public records.

`jetties.json` is drawn from NOAA ENC shoreline construction and from lines traced on USGS NAIP imagery;
the bridge decks in `bridges.json` (`dk`, `sp`) from NOAA ENC bridges and from US Census TIGER/Line
roads over TIGER and USGS NHD water areas; `beaches.json` from FDEP's Coastal Range Monuments (a Florida
public record) and the NOAA ENC coastline. One input to `jetties.json` came from OpenStreetMap and is
kept on purpose: 39 stand-in points (`tools/jetties-2026-10-08/standins.txt`) mark stretches of 18
structures that the chart does not carry, each the midpoint of a stretch of a way the 7 October review
had checked on imagery, with a circle radius taken from the stretch length. Fewer than 100 positions
taken once from fewer than 100 features is an insubstantial extract under the OpenStreetMap Foundation's
community guideline on substantial extracts, so no ODbL terms attach to them; the source is credited
here and in each popup that uses one (Map data © OpenStreetMap contributors).

`zones-local.json` and `zones-palmbeach.json` are drawn from public-domain inputs: NOAA Electronic
Navigational Charts (CC0), USGS National Hydrography Dataset and NAIP imagery, US Census TIGER, USACE
and NPS boundaries, and coordinates printed in regulations. The Palm Beach Phil Foster Park circle
(`pfp`) is centred on a point whose source was not recorded in August 2026; it lies within 40 m of the
FWC and Palm Beach County reef-site positions for the same park, and a single position is not a
substantial part of any database.

They are licensed under the Creative Commons Attribution 4.0 International licence,
<https://creativecommons.org/licenses/by/4.0/>. Attribution: **"Bottom Truth (Robert Karas),
bottomtruth.com"**, with a link to this repository where practical, and a note of any changes made.

The licence covers the selection, arrangement, summaries and classifications. It does not cover the
law itself. Statutes, rules, regulations and ordinances quoted in `law.json` are government edicts
and are free for anyone to use whatever this licence says (*Georgia v. Public.Resource.Org*, 590
U.S. 255 (2020)).

## 2. Earlier versions derived from OpenStreetMap: ODbL 1.0

Up to 7 October 2026 three files contained geometry or fields computed from OpenStreetMap data, which
made them derivative databases under the Open Database License (the two files of 8 October 2026 are in
section 2a):

| File | OpenStreetMap input in those versions |
|---|---|
| `zones-palmbeach.json` | Refuge edges at 750 yd and the 3 nm line offset from the OSM coastline; beach buffer; north jetty breakwater; Blue Heron bridge span; Peanut Island beach |
| `zones-local.json` | Lower Keys canal centrelines (`mon26`); 127th Avenue termini (`ti58`); the Blind Pass marker position (`spb94`) |
| `sites.json` | The `ref` and `edge` fields, computed against the OSM coastline |

Those versions, which remain in this repository's history and in the offline copies attached to
earlier releases, stay available under the Open Database License 1.0,
<https://opendatacommons.org/licenses/odbl/1-0/>, with any rights in individual contents under the
Database Contents License, <https://opendatacommons.org/licenses/dbcl/1-0/>. Map data © OpenStreetMap
contributors, <https://www.openstreetmap.org/copyright>.

On 7 October 2026 all three were rebuilt without OpenStreetMap data: the coastline, jetties, bridge and
Peanut Island shore from the NOAA ENC harbour-band charts, the Keys canals from the USGS National
Hydrography Dataset, 127th Avenue and the Blind Pass intersection from US Census TIGER/Line roads, and
the imagery readings from USGS NAIP. The scripts are `tools/extract-enc-2026-10-07.py`,
`tools/build-zones-palmbeach.py`, `tools/recompute-sites-ref-2026-10-07.py` and
`tools/patch-zones-local-geometry-2026-10-07.py`. The current files are in group 1. OpenStreetMap was
used only to compare old and new geometry.

## 2a. The versions of 8 October 2026 derived from OpenStreetMap: ODbL 1.0

The jetty and bridge reviews of 7 and 8 October 2026 first used OpenStreetMap ways as the starting
geometry, checked structure by structure on USGS NAIP imagery. Those versions, committed on 8 October
2026 before the rebuild described below, are derivative databases:

| File | OpenStreetMap input in those versions |
|---|---|
| `jetties.json` | Breakwater and groyne ways for 46 of the 75 structures, and the buffer rings drawn from them |
| `bridges.json` | The `dk` deck lines and the `sp` span buffers drawn from OSM bridge ways (1,441 records) |

They remain in this repository's history and stay available under the Open Database License 1.0,
<https://opendatacommons.org/licenses/odbl/1-0/>, with any rights in individual contents under the
Database Contents License, <https://opendatacommons.org/licenses/dbcl/1-0/>. Map data © OpenStreetMap
contributors, <https://www.openstreetmap.org/copyright>.

Later on 8 October 2026 both were rebuilt without OpenStreetMap geometry: the jetties from NOAA ENC
shoreline construction (`tools/jetties-2026-10-08/`, `tools/build-jetties.py`) with the stand-in points
described in section 1, and the bridge decks from NOAA ENC bridges and US Census TIGER/Line roads over
mapped water (`tools/bridges-2026-10-08/decks.txt`, `tools/build-bridge-spans.py`). The current files
are in group 1. OpenStreetMap was used only to find which charted features belong to a reviewed
structure, to measure how much of each reviewed structure the chart covers, to compare the old and
new closures, and to pick the 40 stretches of mapped water where a third road pass looked again for a
deck (the geometry that pass added is TIGER roads over TIGERweb water; see `tools/build-bridge-spans.py`).

## 3. Redistributed public data: upstream terms, no added restriction

These files are reduced copies of public data. The project claims no rights in them and adds no
restriction:

| Files | Upstream status |
|---|---|
| `contours.json`, `enc.json`, `enc-areas.json`, `enc-restricted.json`, `seabed.json` | NOAA Electronic Navigational Charts, CC0 1.0 |
| `buoys.json`, `fknms.json`, `stations.json`, `mpa.json`, `jurisdiction.json` | United States government works (17 U.S.C. § 105) |
| `bridges.json` (positions) | FHWA National Bridge Inventory, United States government work |
| `cwa.json`, `parkwaters.json`, `piers.json` (records), `ramps.json` | Florida agency public records |
| `hardbottom-sw.json` (FWC statewide part) | Public domain, per the FWC layer metadata |
| `hardbottom.json`, `hardbottom-sw.json` (West Florida Shelf and worm reef parts) | FWC FWRI and partners; use constraints not located (see `DATA-SOURCES.md`) |

## Linked media

Photographs and videos referenced in `spots.json` are links to third-party pages and files. They are
not part of this repository's data and are not covered by any licence above. Each photo record
carries its own `licence` and `credit` fields, and the map shows them under the image.

## Not legal advice

Nothing in these files is legal advice, official, or a substitute for the posted signage on site.
The licences above grant permission to reuse the files. They do not warrant that the files are
correct, current or complete.
