# Data sources

Every file in `data/`, every remote map service the page loads, and the vendored code, with its
source, how it was derived, its size and its terms. Record counts were computed from the files on
6 October 2026. Licences for the project's own files are set out in `LICENSE-DATA.md`.

All agency data was pulled from the agencies' own public GIS services, mostly in August and
September 2026. Coordinates are `[lat, lon]` rounded to 5 decimal places (about 1 m). The raw pulls
are not in the repository because they total about 60 MB; `tools/src-2026-09-30/raw-manifest.json`
lists them with their service URLs, layer ids and SHA-256 hashes.

## Legal layers

| File | Contents | Source | Derivation | Records | Licence |
|---|---|---|---|---|---|
| `law.json` | Citation registry: citation, title, effect, verbatim excerpt, URL, verification status | Online Sunshine (statutes), FLRules (administrative code), eCFR (federal), Municode and county codes (local) | Built by `tools/build-law.py` plus the dated review passes in `tools/law-updates/` | 278 entries: 124 federal regulation, 66 state rule, 53 ordinance, 25 confirmed negative, 9 statute, 1 special act. 246 verbatim, 31 secondary, 1 unverified. | CC BY 4.0; quoted law is free |
| `zones-statewide.json` | Statewide legal zones: federal fishery closures, Coast Guard and military zones, manatee No Entry zones, state areas, wildlife refuges, local ordinances | Coordinate text in the CFR and the Florida Administrative Code; FWC State Manatee Protection Zones (MapServer/9); USFWS NWR boundaries; NOAA ENC named sea areas; Census TIGERweb places; `piers.json`, `bridges.json` | `tools/build-zones-statewide.py`. Structure buffers drawn at 125 per cent of the stated distance. Boundaries the law gives only in words are drawn from the nearest published geometry with a flag, or shown as a marker. | 208 zones: 94 military and Coast Guard, 33 local, 27 manatee, 21 federal fishery, 16 state areas, 15 refuges, 2 other federal | CC BY 4.0 |
| `zones-local.json` | Local, park and federal zones | TIGER 2025 places; OpenStreetMap (Keys canals, 127th Avenue, Blind Pass marker); USACE National Channel Framework; NPS land resources boundaries; 33 C.F.R. § 165.785 coordinates; two positions read from aerial imagery (see open questions) | `tools/build-zones-local.py` (August inputs not kept), then the text-only patches `tools/patch-zones-local-2026-09-30.py` and `-2026-10-06.py` | 18 zones; the Lower Keys canal zone holds 122 polylines | ODbL 1.0 |
| `zones-palmbeach.json` | Palm Beach County refuges and carve-outs, beach, jetty, groin, bridge and park buffers, inlet readings, COLREGS line, 3 nm line | OpenStreetMap coastline (596 points), OSM breakwater and bridge span; NOAA ENC jetty tips; PBC Code App. G latitudes; 33 C.F.R. § 80.727 | `tools/build-zones-palmbeach.py`. Beach buffer drawn at 125 yd for a 100 yd rule, jetties at 150 ft for a 100 ft rule. | 17 features | ODbL 1.0 |
| `closures.json` | Fla. Stat. § 379.2425 closures: Upper Keys and John Pennekamp | Hand-built Upper Keys box through Long Key; FDEP park boundary for Pennekamp | `tools/build-layers.py` | 2 polygons | CC BY 4.0 |
| `fknms.json` | Florida Keys National Marine Sanctuary zones with regulation text | NOAA ONMS, `FKNMS_Zone_Boundaries_With_Attributes_04282026/FeatureServer/1` | Passed through from the August pull | 76 zones; 50 prohibit fishing; 47 in state waters | US government work |
| `cwa.json` | FWC Critical Wildlife Areas | `gis.myfwc.com/.../Critical_Wildlife_Areas_in_Florida/MapServer/7` | Fields reduced | 37 | Florida public record |
| `parkwaters.json` | State parks with submerged acreage | FDEP `PARKS_BOUNDARIES/MapServer/0` | Vertex thinning at 0.0006 deg | 120 parks, 1,798 rings | Florida public record |
| `jurisdiction.json` | State and federal waters boundary: 3 nm Atlantic, 9 nm Gulf | BOEM Submerged Lands Act boundary | Passed through; 230 Gulf paths repeat Atlantic paths and are dropped at load | 270 Atlantic and 600 Gulf paths | US government work |
| `regs.json` | Sidebar reference text by topic and county | The project's own | Hand-maintained | 92 entries in 8 sections | CC BY 4.0 |
| `species.json` | Spear status and limits per species, with citations | The project's own research | `tools/build-layers-2026.py` from `tools/src-2026-09-30/species.json` | 91 species | CC BY 4.0 |
| `coverage.json` | Research coverage tiers shown on the map | The project's own | Hand-drawn outlines, deliberately coarse | 3 regions | CC BY 4.0 |

## Structure and access

| File | Contents | Source | Derivation | Records | Licence |
|---|---|---|---|---|---|
| `sites.json` | Artificial reefs and natural sites | FWC Artificial Reef Locations (MapServer/12, 4,548 records); Palm Beach County ERM reef sites (252) | `tools/fetch-statewide.py`: merged within 60 m; `ref` and `edge` computed against the OSM coastline; `closed` from `closures.json`; `iw` from the inland classifier | 3,609 (3,548 artificial, 61 natural) | Positions public record; file ODbL 1.0 because of `ref` and `edge` |
| `spots.json` | Curated dive spots with descriptions and media links | Positions from `sites.json`, FKNMS and FDEP buoy lists, `piers.json`, FPAN, NPS and other agency pages; text is the project's own | `tools/build-layers-2026.py` from `tools/src-2026-09-30/spots.json` | 283 spots, 481 links (352 pages, 66 photos, 61 videos, 2 galleries) | CC BY 4.0 for text and curation; media keep their own licences |
| `ramps.json` | Saltwater boat ramps | FWC Florida Boat Ramp Inventory (MapServer/4) | Filtered to saltwater ramps with lanes | 613 | Florida public record |
| `piers.json` | Fishing piers, jetties and fishing bridges | FWC Fishing Piers, Jetties and Bridges inventory | Inland/tidal/coastal tag added; buffer circles drawn by the page | 646 | Public record; tags CC BY 4.0 |
| `bridges.json` | Bridges with a three-way fishing-buffer status | FHWA National Bridge Inventory | `tools/build-layers.py`: limited-access classes excluded under § 316.130(18), FWC fishing structures confirmed, the rest presumed buffered; inland/tidal/coastal class from `tools/classify-inland.py` | 7,822: 211 confirmed, 6,041 presumed, 1,570 excluded; 2,561 coastal, 303 tidal, 4,958 inland | Positions public domain; classification CC BY 4.0 |
| `buoys.json` | FKNMS mooring, spar and boundary buoys | NOAA ONMS `PubFKNMSBuoy2025/FeatureServer/0` | Fields reduced | 807 | US government work |
| `stations.json` | Tide, current and NDBC buoy stations | NOAA CO-OPS metadata API; NDBC active stations | Current stations deduplicated | 913: 625 tide, 178 current, 110 buoy | US government work |

## Habitat, depth and bottom

| File | Contents | Source | Derivation | Records | Licence |
|---|---|---|---|---|---|
| `contours.json` | Depth contours at 12, 18, 30, 60, 100 and 120 ft | NOAA ENC Direct DEPCNT, coastal and approach bands | Converted to feet, simplified at 0.00005 deg | 6,415 lines | CC0 |
| `enc.json` | Wrecks, obstructions, fish-haven points, rocks | NOAA ENC Direct WRECKS, OBSTRN, UWTROC, all three usage bands | Duplicates merged, most detailed band kept | 10,770: 5,940 obstructions, 2,499 rocks, 2,219 wrecks, 112 fish havens | CC0 |
| `enc-areas.json` | Charted fish-haven and wreck areas | NOAA ENC Direct OBSTRN and WRECKS areas | Duplicates merged, simplified | 952: 918 fish havens, 34 wreck areas | CC0 |
| `seabed.json` | Charted bottom type (S-57 NATSUR) | NOAA ENC Direct SBDARE points and areas | Deduplicated across bands | 14,038 points, 266 areas, 87 classes | CC0 |
| `hardbottom.json` | Natural hardbottom, southeast Atlantic | FWRI Unified Reef Map v2.2 | Fields reduced | 2,913 polygons | FWRI; use constraints not located |
| `hardbottom-sw.json` | Hardbottom outside the Unified Reef Map, West Florida Shelf pavement, worm reef | FWC Coral and Hard Bottom Habitats Statewide (MapServer/18), West Florida Shelf Benthic Habitats (MapServer/13), Worm Reef Habitats (MapServer/14) | Filtered to sources outside the Unified Reef Map; pavement only; simplified | 6,122: 4,958 West Florida Shelf, 1,144 FWC statewide, 20 worm reef | FWC statewide part public domain; the other two not located |

## Reference only (off by default, not in the offline builds)

| File | Contents | Source | Records | Licence |
|---|---|---|---|---|
| `enc-restricted.json` | Charted restricted and military practice areas | NOAA ENC Direct RESARE and MIPARE, deduplicated across bands | 532 | CC0 |
| `mpa.json` | NOAA MPA Inventory, Florida sites | NOAA MPA Inventory 2023 | 219 | Public domain; "not legal documents" |

The ENC restricted-area layer does not say what is restricted, because ENC Direct does not expose
the S-57 RESTRN attribute. The law comes from the CFR entries and the drawn zones.

## Remote map services

These load in the browser at run time. None needs a key except the two marked as optional.

| Service | Used for | Terms | Attribution shown |
|---|---|---|---|
| NOAA Chart Display Service | Default base map (nautical chart) | US government work | NOAA Office of Coast Survey. Not for navigation. |
| USGS The National Map, imagery | Satellite base map | Public domain | USGS The National Map, USDA NAIP |
| EOX Sentinel-2 cloudless 2016 | Satellite base map, 2016 | CC BY 4.0 (later years are non-commercial only) | Sentinel-2 cloudless by EOX IT Services GmbH, modified Copernicus Sentinel data 2016 and 2017 |
| USGS The National Map, topographic | Topographic base map | Public domain | USGS The National Map |
| OpenStreetMap tiles | Street base map | ODbL data; OSMF tile usage policy (light use) | © OpenStreetMap contributors, ODbL |
| Esri World Imagery (optional) | Imagery, only with an owner-supplied key | Esri terms | © Esri, Maxar, Earthstar Geographics |
| CARTO Dark Matter (optional) | Dark base map, only with an owner-supplied key | CARTO terms | © OpenStreetMap contributors, © CARTO |
| NOAA NCEI Coastal Relief Model and CUDEM hillshade | Seafloor relief overlays | US government work | NOAA NCEI. Not for navigation. |
| NOAA NCEI DEM Global Mosaic | Colour relief overlay | US government work | NOAA NCEI. Not for navigation. |
| GEBCO WMS | Ocean relief overlay | Public domain; not for navigation | GEBCO Compilation Group. Not for navigation. |
| FWC seagrass, coral and hardbottom, Unified Reef Tract, West Florida Shelf exports | Habitat overlays | FWC; the reef tract and shelf constraints not located | FWC Fish and Wildlife Research Institute and partners |
| NOAA CoastWatch ERDDAP (MUR SST, VIIRS Kd490) | Water temperature and clarity overlays | Free to use; not intended for legal use | NASA JPL and NOAA CoastWatch |
| NOAA NWS reference map | Marine forecast zones | US government work | NOAA National Weather Service |
| MarineCadastre danger zones | 33 C.F.R. part 334 areas as of July 2022 | Federal data | MarineCadastre.gov (NOAA and BOEM). Not for navigation. |
| Wikimedia Commons | Spot photo thumbnails | Per file | Each photo's credit and licence, shown under it |

## Vendored code

| Path | Version | Licence |
|---|---|---|
| `vendor/leaflet/` | Leaflet 1.9.4 | BSD 2-Clause, `vendor/leaflet/LICENSE` |

## Open questions about sources

- **Aerial-imagery positions.** Two positions in `zones-local.json` were read from Esri World
  Imagery in August 2026: the John's Pass corridor in `ti58` and the Three Sisters circle in `3sis`.
  Whether Esri's terms allow publishing positions read this way has not been checked. Re-reading
  both from USGS NAIP imagery (public domain) would settle it. The `ti58` source text also still
  credits the OpenStreetMap channel centreline, which disagrees with the build script.
- **Use constraints not located** for the FWRI Unified Reef Map v2.2, the West Florida Shelf benthic
  layer (Nova Southeastern University and FWRI) and the worm reef layer (TNC and FWRI).
- **August service URLs not kept** for the bridge inventory, the FWC pier inventory, the BOEM
  boundary, the FDEP parks pull and the FKNMS zones. Source names come from the build notes.
