# Data licences

The files in `data/` are licensed per file. The code licence in `LICENSE` (MIT) does not cover them.
Every file falls into one of three groups, depending on where its content came from. The full
record of sources, record counts and derivations is in `DATA-SOURCES.md`.

## 1. The project's own research: CC BY 4.0

These files hold the project's legal research, curation and classification:

`law.json`, `regs.json`, `species.json`, `coverage.json`, `closures.json`, `zones-statewide.json`,
`spots.json` (descriptions and curation), and the classification fields added to `bridges.json`
(`st`, `iw`, `iwr`) and `piers.json` (`iw`, `iwr`).

They are licensed under the Creative Commons Attribution 4.0 International licence,
<https://creativecommons.org/licenses/by/4.0/>. Attribution: **"Bottom Truth (Robert Karas),
bottomtruth.com"**, with a link to this repository where practical, and a note of any changes made.

The licence covers the selection, arrangement, summaries and classifications. It does not cover the
law itself. Statutes, rules, regulations and ordinances quoted in `law.json` are government edicts
and are free for anyone to use whatever this licence says (*Georgia v. Public.Resource.Org*, 590
U.S. 255 (2020)).

## 2. Files derived from OpenStreetMap: ODbL 1.0

These files contain geometry or fields computed from OpenStreetMap data, which makes them derivative
databases under the Open Database License:

| File | OpenStreetMap input |
|---|---|
| `zones-palmbeach.json` | Refuge edges at 750 yd and the 3 nm line offset from the OSM coastline; beach buffer; north jetty breakwater; Blue Heron bridge span |
| `zones-local.json` | Lower Keys canal centrelines (`mon26`); 127th Avenue termini (`ti58`); the Blind Pass marker position (`spb94`) |
| `sites.json` | The `ref` and `edge` fields, computed against the OSM coastline. Site positions themselves are FWC and Palm Beach County public records. |

They are made available under the Open Database License 1.0, <https://opendatacommons.org/licenses/odbl/1-0/>.
Any rights in individual contents of the database are licensed under the Database Contents License,
<https://opendatacommons.org/licenses/dbcl/1-0/>. Map data © OpenStreetMap contributors,
<https://www.openstreetmap.org/copyright>. Anyone who publicly uses an adapted version of these
files must offer that version under ODbL as well.

Recomputing the Palm Beach offsets and the `sites.json` fields from the NOAA ENC coastline (CC0)
would move these files into group 1. That work is listed in `docs/BACKLOG.md`.

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
