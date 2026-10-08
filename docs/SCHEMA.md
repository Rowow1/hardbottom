# Data schema

Every file in `data/`. Field by field, with the enumerations spelled out. If you are editing data,
read this first — several fields carry conventions that are load-bearing.

Coordinates are **`[lat, lon]`** everywhere (Leaflet order), rounded to **5 decimal places** (~1.1 m).
This is the opposite of GeoJSON's `[lon, lat]`. Every ArcGIS/GeoJSON import flips at the boundary.

---

## `law.json` — the citation registry

```json
{ "version": "2026-08-22", "entries": [ … ] }
```

Each entry:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable slug, referenced from every other file. Pattern: `<jurisdiction>-<section>` — `fac-68b-20-003-2`, `fs-379-2425`, `monroe-26-5`, `cfr-922-164-d`. **Never renumber an existing id** — the map joins on it. |
| `cite` | string | Full citation as it should be printed on the chip. Include the subsection: `Fla. Admin. Code r. 68B-3.008(3)(a)`. |
| `title` | string | Plain-English headline. Convention: where a rule is commonly *misunderstood*, say what it is **not** — e.g. "Lobster & stone crab sanctuary — NOT a spearfishing rule". |
| `juris` | enum | `federal` · `state` · `county` · `city`. Drives the grouping in the encyclopedia panel. |
| `kind` | enum | `statute` · `rule` · `cfr` · `ordinance` · `specialact` · `negative`. `negative` entries render in their own "rules that do not exist" section and get a green chip. |
| `url` | string | Deep link to the authoritative text. Prefer flsenate.gov, ecfr.gov, flrules, Municode. |
| `effect` | string | One sentence: the practical consequence. This is what shows before you expand. |
| `excerpt` | string | The operative text, **verbatim**. Never paraphrase into this field — put paraphrase in `effect`. |
| `full` | string \| null | Longer text, subsection detail, history. Renders behind a `<details>`. |
| `verified` | enum | `verbatim` (read from the primary source, word for word) · `secondary` (from a reliable third party, not confirmed word for word) · `unverified` (a lead, not a rule). Drives the chip colour: blue / amber / red. **Mandatory.** |
| `scope` | string \| null | Where it applies — geography, species list, coordinates. |
| `note` | string \| null | Caveats, corrections, cross-references, currency warnings. Date any correction: "CORRECTED 22 Aug 2026 — …". |
| `geom` | any \| null | Reserved. Unused today. |

Built by `tools/build-law.py`. **Edit that script, not the JSON** — the JSON is generated.

---

## `zones-local.json` — local, park and federal zones with geometry

```json
{ "version": "2026-08-22", "zones": [ … ] }
```

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Short slug: `spb54`, `ti58`, `mon26`, `npsbisc`, `pszcenter`. |
| `n` | string | Display name. The app prepends ⚠ automatically when `flag` is non-null — **do not type the ⚠ yourself**. |
| `law` | string[] | `law.json` ids. This is the join that produces the citation chips. |
| `cat` | enum | Which legend layer it lands in: `local` (municipal/county ordinances) · `fed` (federal parks and zones). `zones-statewide.json` adds `fedfish` · `mil` · `manatee` · `stateareas` · `nwr`. Must match a `CATS` id in `js/app.js`; an unknown value falls back to `local`. |
| `kind` | enum | Rendering intent: `closed` (red — a real prohibition) · `warn` (amber — restriction, seasonal, or not squarely a spearfishing rule) · `open` (green — a place people wrongly believe is closed) · `line` (drawn as polylines only). |
| `r` | array | Polygon rings: `[[[lat,lon],…], …]`. Each ring closed (first point repeated). May be `[]`. |
| `line` | array | Polylines: `[[[lat,lon],…], …]`. Used for canal centrelines and channel spines. May be `[]` or absent. |
| `s` | string | Popup HTML. `<b>` for the operative words. Keep it to what a diver needs. |
| `src` | string | **Provenance sentence.** Names the dataset and, where it matters, the date and method. Required — a zone with no stated source is not shippable. |
| `flag` | string \| null | The open-question text. Non-null means: ⚠ prefix on the name, dashed outline, a yellow pin in the "Open questions" layer, a `<details>` block in the popup, and an entry in `research/open-questions.md`. **Explain exactly why the drawn geometry is not the closure.** |

A zone may have `r` only, `line` only, or both. The app draws whatever is present and always adds a
centroid marker so a zone with no fill is still clickable.

Built by `tools/build-zones-local.py`.

### `zones-statewide.json`

Same shape as `zones-local.json` (208 zones, built by `tools/build-zones-statewide.py`), plus:

| Field | Type | Meaning |
|---|---|---|
| `pts` | array | Published vertices that cannot be closed into a ring (anchor points, a single named point). Drawn as small unconnected markers. |
| `active` | string \| null | When the rule applies, in the rule's own terms ("always", "NOV 15 - MAR 31", "during announced firing"). Shown as a "When it applies" line in the popup and in What's here. |

A zone with `r` is included in the What's here point query. A zone with only `line` or `pts` has no
drawn boundary and is listed under "Rules nearby with no drawn boundary" within 5 km.

---

## `fknms.json` — Florida Keys sanctuary zones

Flat array. 76 zones from NOAA's post-Blueprint GIS.

| Field | Meaning |
|---|---|
| `n` | Zone name |
| `t` | Zone type: `Sanctuary Preservation Area` · `Wildlife Management Area` · `Ecological Reserve` · `Conservation Area` · `Management Area` · `Restoration Area-Habitat` · `Restoration Area-Nursery` · `Special Use Area` · `Area to be Avoided` · `No Anchor Zone` |
| `reg` | NOAA's simplified regulation string |
| `full` | NOAA's full regulation text |
| `fish` | `Yes` / `No` — **the app draws only `No`** (50 of 76) |
| `sw` | `Yes` / `No` — inside Florida state waters. **This decides which rulebook applies**: `Yes` → 1997 zoning (the Governor blocked the Blueprint in state waters); `No` → 2025 Restoration Blueprint |
| `nwr` | Inside a National Wildlife Refuge |
| `ac` | Acres |
| `r` | Polygon rings, `[lat,lon]` |

---

## `cwa.json` — FWC Critical Wildlife Areas

Flat array: `n` name · `no` CWA number · `d` description · `cd` closure dates · `sp` focal species ·
`c` county · `ac` acres · `r` rings.

**The rule binds only where the area is POSTED on site** (r. 68A-19.005(1)(b)). The GIS is evidence,
not the trigger. Say so in any popup that uses this.

---

## `regs.json` — sidebar reference content

Object of section → array of `[heading, htmlBody]` pairs. Sections: `licences`, `statewide`,
`prohibited`, `seasons`, `safety`, `ramps`, `counties`, `freshwater`. Hand-maintained.

**When `law.json` is corrected, sweep this file too** — it carries prose restatements of the same
rules and has drifted before.

---

## `closures.json` — statutory closure polygons

Flat array: `name` · `rule` (popup HTML) · `rings` (array of rings). Currently the Upper Keys
§ 379.2425 corridor and John Pennekamp.

---

## The bulk geodata

Not in the project knowledge base — coordinate volume with no retrieval value. All in git.

| File | Records | Key fields |
|---|---|---|
| `sites.json` | 3,609 reef/wreck sites | `n,lat,lon,d,rel,t,c,m,src,nt,ref,edge,closed,czone,ctype,iw,iwr` — `t` = `n`atural/`a`rtificial, `c` = county, `closed` = `keys`/`penn`/`fknms`, `ref` = PBC refuge 1\|2, `iw` = water class |
| `bridges.json` | 7,822 | `n,o,lat,lon,fc,st,cf,iw,iwr` — `st` = `confirmed`(211) / `presumed`(6041) / `excluded`(1570) |
| `piers.json` | 646 | FWC fishing structures |
| `ramps.json` | 613 | saltwater ramps with lanes, hours, fees |
| `parkwaters.json` | 120 | FDEP park water polygons |
| `hardbottom.json` | 2,913 | FWRI Unified Reef Map, SE Atlantic only |
| `jurisdiction.json` | — | BOEM state/federal line, 3 nm Atlantic / 9 nm Gulf |
| `zones-palmbeach.json` | — | PBC refuges, buffers, boundary lines |

### Added 30 Sep 2026

| File | Records | Key fields |
|---|---|---|
| `enc.json` (replaced) | 10,770 | `k` = `wreck` · `obstruction` · `fishhaven` · `rock`; `lat,lon`; `n` name; `cat`; `d` VALSOU metres; `wl` WATLEV code (1 partly submerged at high water, 2 always dry, 3 always under water, 4 covers and uncovers, 5 awash, 6 subject to flooding, 7 floating); `inf` |
| `enc-areas.json` | 952 | `k` = `fishhaven` · `wreckarea`; `n,d,cat,inf`; `r` rings |
| `seabed.json` | 14,038 points, 266 areas | `classes` (charted NATSUR strings); `pts` = `[lat, lon, classIndex]`; `areas` = `{c, r}`. The app colours by the first token. |
| `contours.json` (replaced) | 6,415 lines | `ft` = 12 · 18 · 30 · 60 · 100 · 120; `p` paths. Florida ENC cells carry no 10 or 20 ft contours. |
| `hardbottom-sw.json` | 6,122 | `c` class; `s` source; `y` year; `b` cover; `r` rings. Outside the SE tract that `hardbottom.json` covers. |
| `buoys.json` | 807 | FKNMS buoys: `n,no,t,d` (ft), `reg,res,lat,lon` |
| `stations.json` | 913 | `k` = `tide` · `current` · `buoy`; `id,n,lat,lon`; tide `ref`; current `bin`; buoy `o,t` |
| `enc-restricted.json` | 532 | Charted restricted and military areas. **Reference only, not the law.** |
| `mpa.json` | 219 | NOAA MPA Inventory. **Reference only**: NOAA says these are not legal documents. |
| `spots.json` | 283 | Curated dive spots: `id,n,aka,lat,lon,coord_src,coord_url,kind,depth_ft,county,region,access,desc,tags,links,note`. Descriptive only; no record states or implies that spearfishing is legal at a spot. |
| `species.json` | 91 | Per-species spear status (`prohibited` · `restricted` · `allowed`), region limits, `law` ids, `sources`. |
| `coverage.json` | 3 regions | Research-coverage tiers for `js/coverage.js`. Not a legal layer. |

`iw` on any feature is `coastal` · `tidal` · `inland`, with `iwr` the human-readable reason.
Produced by `tools/classify-inland.py`. **It is a planning heuristic with no legal force.**
