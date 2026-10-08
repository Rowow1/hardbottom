# Bottom Truth (Florida spearfishing legal and structure map): project index

**Start here.** This is the map of the project itself: what exists, what state it is in, and the
order to read it in.

> **Before writing anything for this project, read `research/00-WRITING-STYLE.md`.** It is a
> standing instruction, not a suggestion: it governs every document, README, popup string, and
> long-form chat answer produced here.

**Status as of 8 October 2026.** The project is ready for public release as **Bottom Truth**
(bottomtruth.com) and is not live yet. The full repository is on GitHub at
`github.com/Rowow1/hardbottom` (private), which is the primary copy. GitHub Actions run the checks
and build the website into a `site` branch on every push; both were green on commit 3bb9b91. The
domain is registered at Hostinger; connecting Git deployment, the password lock and the launch-day
steps remain. The release plan and its open items are in **`research/public-release-2026-10-06.md`**.

The legal layer was reviewed twice in October. The 7 October currency pass and the second review of
7 and 8 October took the registry from 278 to **326 citations** (302 verbatim, 24 secondary), shown on
the map as "Rules current as of 8 Oct 2026". The map now draws:

- **Jetties:** 75 structures traced one at a time on imagery, with the 100 ft buffer drawn at 150 ft
  (55 closed, 20 amber where the structure may not count as a jetty).
- **Bridges:** 1,441 of the 2,509 coastal and tidal fishable bridges carry the 125 yd buffer along the
  traced deck instead of a circle at the inventory point.
- **Zones:** 212 statewide and 21 local zones, including Clearwater citywide, Ponce Inlet, the
  Steinhatchee River and Crystal River NWR closed.

The fresh/salt boundary stays closed as **unsolvable**.

**Open decision for the author:** `jetties.json` and the bridge deck fields (`dk`, `sp`) start from
OpenStreetMap ways, so they are ODbL 1.0 while every zone file has been OSM-free (CC BY 4.0) since
7 October. Rebuilding them from NOAA ENC shoreline construction and bridge areas is in the backlog.
Whether to do that before launch is open.

**What this is for:** planning the author's own dives, built to open-source standards so it can
become a public tool. Risk posture is *conservative with margin* throughout. **Nothing here is legal
advice, and nothing here substitutes for reading the posted signage on site.**

---

## 1. Read these first

| Doc | Why |
|---|---|
| **`research/00-WRITING-STYLE.md`** | How everything in this project is written. |
| **`research/current-legal-review.md`** | The standing state of the legal layer as of 8 Oct 2026: settled traps, currency watch, where the geometry is soft, the local-ordinance posture. **If you read one legal thing, read this.** |
| **`research/legal-review-2026-10-08.md`** | The second review: the jetty tracing, the bridge spans, every registry change of 7 and 8 Oct, ten dive-planning tips, and what the independent check corrected. |
| **`research/open-questions.md`** | The flagged map features and the ranked questions that need a phone call or a clerk (27 to 33 added 8 Oct). |
| **`research/public-release-2026-10-06.md`** | Release status, where everything is, launch steps, open items. |
| **`maps/BUILD.md`** | Where the repo copies are, the repository layout, how to rebuild and check, and every endpoint. |

## 2. The legal corpus

| Doc | Scope |
|---|---|
| `research/legal-review-2026-10-08.md` | Second statewide review of 7 and 8 Oct 2026, run in parallel with the currency pass. |
| `research/currency-2026-10-07-federal.md`, `-state.md`, `-local.md` | The 7 Oct legal currency pass: what changed in federal, state and local law since 30 Sep. |
| `research/review-2026-10-07/reads.md` | Every passage read in the browser for the second review, with the page it came from. |
| `research/review-2026-10-07/federal-leads.md`, `state-leads.md`, `local-leads.md`, `practical-leads.md`, `jetties-inventory.md` | The research leads behind the second review and the jetty inventory. |
| `research/legal-review-2026-09-30.md` | Statewide review of 30 Sep 2026 (federal fisheries, Coast Guard and military, NPS and refuges, manatee, state rules, local sweep, species). |
| `research/florida-spearfishing-legal-compendium.md` | The August master reference. Still correct on the core rules; superseded where the 30 Sep and October reviews say so. |
| `research/municipal-ordinance-sweep.md` | Every coastal city and county checked as of 30 Sep 2026. The October local reads are in `reads.md` and not yet folded in. |
| `research/citation-verification-2026-08.md` | The August four-axis pass (53 citations, 16 defects fixed). |
| `research/refuge-findings.md`, `research/se-atlantic-legal-findings.md`, `research/statewide-closures-and-bridges.md` | Palm Beach refuges, the SE Atlantic, statewide closures and bridges. |
| `research/fresh-vs-salt-water-legal-line.md`, `research/salinity-numbers-and-the-taste-test.md` | The fresh/salt question, closed as unsolvable. |

**Headline legal changes found on 7 and 8 Oct 2026** (details and citations in the two reviews):

- **Fresh water:** possessing a speargun in or upon fresh water is itself prohibited (r. 68A-23.002(7));
  the earlier note that FWC overstated this is withdrawn. The Steinhatchee River is fresh water to its
  mouth by statute and is drawn.
- **National parks:** a loaded speargun is prohibited in any vessel, anchored or under way (36 C.F.R.
  § 2.4(c)).
- **Refuges:** spears may not be used or possessed on a national wildlife refuge unless a refuge rule
  allows it (50 C.F.R. § 27.43); Crystal River NWR is drawn closed.
- **Preemption:** the fishing preemption statute is § 379.2412, which reserves saltwater fish
  regulation to the state but lets a local government close fishing from property it owns. § 790.33
  reaches firearms only.
- **Grouper:** gag and black grouper become 2 per private vessel combined in South Atlantic federal
  waters from 28 Oct 2026 (SA Reg. Am. 36), with a matching state rule proposed (r. 68B-14.0036,
  comments to 26 Oct 2026).
- **Handling and gear:** reef fish must be landed whole; a descending device or venting tool is
  required aboard when harvesting reef fish from a vessel; snook may not be kept aboard with spear
  gear.
- **Local:** new local reads cover Clearwater § 21.06 (citywide projectile ban), the canal gear acts of
  Cape Coral, Sanibel, Naples, Collier, Brevard and Satellite Beach, St. Petersburg § 7-5, Volusia
  § 20-121, Mexico Beach § 95.03 and Broward § 13-5 (status open).

**Headline legal changes found on 30 Sep 2026:** Biscayne National Park has a seasonal bonefish
closure to all fishing and a 100 ft dive closure along every marked channel; the Mar-a-Lago East
security zone became no-entry in Sept 2025; Old Tampa Bay north of the Gandy Bridge and Turkey and
Crane Creeks are closed to spears by gear lists; state manatee No Entry zones bar swimmers and divers;
Western Dry Rocks is closed to all fishing 1 Apr to 31 Jul; two federal artificial-reef SMZs (Ft. Pierce
Inshore, Key Biscayne AR-H) ban spearfishing gear; the Oculina experimental closed area bans
snapper-grouper by spear; Venice, Cedar Key, Bal Harbour, Lauderdale-by-the-Sea, Treasure Island
(§ 22-2), Dania Beach and Sunny Isles Beach have area-wide speargun or spearfishing bans; Marathon's
canal ban is § 18-27. The Gulf Islands National Seashore projectile ban of 2021 is **not** in the
current compendium; its status is unresolved and drawn amber.

## 3. Data provenance

| Doc | Scope |
|---|---|
| `research/data-sources-2026-09-30.md` | Every dataset and tile service added on 30 Sep: endpoints, layer ids, counts, licences, the Chrome pull method, and the traps. |
| `maps/app/DATA-SOURCES.md` | The public version: every data file, service and vendored code with terms, including the jetty and bridge-span rows. |
| `maps/app/LICENSE-DATA.md` | Licence per data file. Zone files are CC BY 4.0; section 2a lists the ODbL 1.0 files (`jetties.json`, the bridge `dk` and `sp` fields). |
| `research/florida-reef-data-sources.md` | The August reef and structure sources. |
| `research/florida-boat-ramp-data-and-pbc-ground-truth.md` | Ramps and the Palm Beach ground truth. |

## 4. The application

Source is mirrored flat at `maps/app/`; the repository on GitHub is authoritative. Builds and
coordinate bulk (`bridges.json`, `jetties.json`, `zones-statewide.json` and the base layers) do not
live here. See `maps/BUILD.md`.

| Path | What |
|---|---|
| `maps/app/index.html`, `about.html`, `app.css` | Page shell (search, What's here, Species, Law, persistent notice), the About page, styles |
| `maps/app/app.js` | The map: legend groups, lazy-loaded layers, popups, zones, traced jetties, bridge spans, dive spots, point query, exports |
| `maps/app/layers.js` | Base layers and the overlay panel |
| `maps/app/search.js`, `species.js`, `law.js`, `coverage.js` | Search, the species panel, the legal encyclopedia, the research-coverage layer |
| `maps/app/build-standalone.py` | Builds the full and lite offline copies (`--out DIR`) |
| `maps/app/README.md`, `SCHEMA.md`, `CONTRIBUTING.md`, `CHANGELOG.md` | Public docs; every data file field by field; the evidence standard; every correction |
| `maps/app/ADDING-A-ZONE.md`, `BACKLOG.md` | Procedure for adding a rule; what to build next |
| `maps/app/tools/` | Derivation scripts, including `law_updates.py` (dated passes and release wording), `build-jetties.py`, `build-bridge-spans.py`, `check-text.py`, `test-data.py` |

`maps/app/basemaps.js` is **superseded** by `layers.js` and kept for history.

**Legal and regulatory data carried here as knowledge:**

| Path | What |
|---|---|
| `data/law.json` | **The citation registry**: 326 entries with excerpt, scope, caveats, verification status and URL |
| `data/species.json` | 91 species: spear status and state and federal limits, with citations |
| `data/regs.json` | Sidebar prose with 36 county notes |
| `data/zones-local.json` | 21 local, park and federal zones |
| `data/fknms.json`, `data/cwa.json`, `data/closures.json`, `data/coverage.json` | Keys zones, Critical Wildlife Areas, statutory closures, research coverage |

Registry changes are made as dated passes in `tools/law-updates/<date>/` and applied by
`tools/law_updates.py`; `data/law.json` is never edited by hand.

## 5. Superseded, kept for history

The first-pass Lake Worth artifacts of 21 August (`maps/lake-worth-*`, `maps/dive-sites-from-phil-foster.html`),
`research/spearfishing-handoff.md`, `research/project-review-2026-08.md`, `research/florida-statewide-scoping.md`,
`maps/app/basemaps.js`, and the repo-location and tarball notes in `research/publishing-runbook-github-hostinger.md`.
Do not plan from them.

## 6. Name and positioning

| Doc | What |
|---|---|
| `research/name-clearance-bottomtruth-2026-10-05.md` | **The chosen name, Bottom Truth**: registers, domains, handles and search, clean as of 5 Oct 2026 |
| `research/name-clearance-hardbottom-2026-10-05.md` | Why Hardbottom was dropped (StrikeLines' HardbottomHD) |
| `research/name-clearance-truebottom-2026-10-05.md` | Why True Bottom was dropped (slang meaning) |
| `research/naming-alternatives-2026-10-05.md` | The candidate list and domain prices |
| `research/prior-art-and-positioning.md`, `research/website-naming.md`, `research/ads-and-monetization.md` | Positioning, the earlier naming note, and why the project stays non-commercial |
| `gear/speargun-jbl-6w45.md` | JBL Woody Florida Special 6W45 |

## 7. Publishing

| Doc | What |
|---|---|
| **`research/public-release-2026-10-06.md`** | **Current.** Status, launch steps, open items. |
| `research/outreach-channels-2026-10-07.md` | Where to share the map: ranked spearfishing communities, clubs, shops, events, media and technical audiences, with preconditions and open questions. Spearboard is parked. |
| `research/outreach/discord-servers-2026-10-07.md` | Fifteen Discord servers joined and evaluated (keep, keep later, leave), the steps waiting on the author, and a draft post per server for approval. |
| `research/publishing-and-legal-plan.md` | Legal posture for going public: closure-only framing, liability, UPL, disclaimers, licensing. |
| `research/publishing-runbook-github-hostinger.md` | The 29 Sep runbook. Its launch gate is closed and its repo, domain and deploy-key details are superseded by the release plan. |

## Conventions this project follows

0. **The writing style guide is binding.**
1. **Verbatim or flagged.** Every citation carries a verification status; excerpts are matched word for
   word at the source.
2. **No invented geometry.** Words-only boundaries are drawn from the nearest published geometry that
   contains them with a flag saying how the drawing differs, or as a marker.
3. **Negatives are findings.**
4. **Conservative with margin.**
5. **Everything traces back.** Every zone carries its citation, clickable to the encyclopedia and out to
   the official text.
6. **Closure-only.** The map states what the law closes or restricts, never that water or gear is
   open or legal. `tools/check-text.py` enforces it.
