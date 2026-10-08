# How to add a rule to the map

The project's most repeated operation. Follow it in order; step 1 is not optional.

## 0. Before you write anything — read the rule

Get the **primary source**. Municode, flrules.org, ecfr.gov, flsenate.gov. Not a summary, not a
forum post, not a news article. If you cannot get the primary text, the entry's `verified` field is
`secondary` and the popup must say so.

Municode is a JavaScript app — server-side fetching fails. It renders only in a real browser. This
container has no outbound network except package registries, so use the user's Chrome:
navigate → run `fetch` in page context → read `document.querySelector('#codesContent').innerText`.
Node ids look like `CH26WA_ARTIINGE`; guessing them usually fails, so find the real link in the
table-of-contents DOM (`a[href*="nodeId"]`).

## 1. Add the citation — `tools/build-law.py`

Append an `E(...)` call. Never edit `data/law.json` directly; it is generated.

```python
L.append(E("city-12-34", "City of Somewhere Code § 12-34",
  "Named Bay — spearfishing prohibited", "city", "ordinance",
  "https://library.municode.com/...",
  "One sentence on what it actually does to a diver.",
  "The operative sentence, verbatim, exactly as printed.",
  full="Longer text, definitions, penalty, history.",
  verified="verbatim",
  scope="Where it applies, in words.",
  note="Caveats. Date any correction: 'CORRECTED 3 Sep 2026 — …'"))
```

Then `python3 tools/build-law.py`.

**Conventions that are load-bearing:**
- `excerpt` is **verbatim or it is not an excerpt**. Paraphrase belongs in `effect`.
- `verified` is mandatory and honest. `secondary` is not a failure — an uncited-but-real rule is
  worth mapping *as* uncited.
- If the rule is commonly misdescribed, say what it is **not** in the `title`.
- A confirmed *absence* of a rule is an entry too, with `kind="negative"`.

## 2. Add the geometry — `tools/build-zones-local.py`

```python
add(id='city1234', n='Somewhere — Named Bay spearfishing ban',
    law=['city-12-34'], cat='local', kind='closed',
    r=simp(rings_from(places['Somewhere'])),
    s='Popup HTML. <b>Bold the operative words.</b>',
    src='Boundary: US Census TIGER 2025 Incorporated Places, layer 4.',
    flag=None)
```

Then `python3 tools/build-zones-local.py`. See `docs/SCHEMA.md` for every field and its enumeration.

### Where geometry comes from

Prefer, in this order: the rule's own coordinates → an authoritative GIS layer → hand-digitising
from satellite imagery → nothing. Endpoints and their traps are in `docs/BUILD.md`.

### If there is no geometry — this is the important part

**Do not draw a plausible polygon.** Draw a marker or a small circle at a defensible landmark, set
`flag` to an explanation, and say in `src` exactly what the drawn shape is.

A polygon that looks authoritative and is wrong is worse than an honest gap. This has already bitten
this project three times — a John's Pass corridor that ran across dry land, a Blind Pass rectangle
that sat in the open Gulf, and a Three Sisters Springs circle 350 m inland over a housing estate.
All three came from trusting a data source without looking at it.

### Verify it visually. Every time.

Satellite tiles do not load in this container. Use the user's Chrome:

1. Navigate to a page with Leaflet and no restrictive CSP — `https://leafletjs.com/examples/quick-start/example.html` works; `tigerweb.geo.census.gov` does **not** (`script-src 'self'`, no eval).
2. Grab the page's map object, resize its container to the viewport, swap in Esri World Imagery:
   `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`
3. Draw your rings, `fitBounds`, screenshot, **look at it**.
4. To digitise: read vertices off the screenshot in pixels, scale by `mapSize.x / screenshotWidth`,
   and convert with `map.containerPointToLatLng([x*K, y*K])`.

Check the bounding box before you even render — a stray ring 120 km away shows up as a suspicious
min/max longitude.

## 3. Wire the county — `js/app.js`

If the rule applies to a whole county, add it to `COUNTY_LAW` so every reef site in that county
cites it automatically:

```js
const COUNTY_LAW = { 'Somewhere County': ['city-12-34'], … };
```

If you need a whole new legend row, add to `CATS` and give it a colour in `COL`.

## 4. Rebuild and check

```sh
python3 build-standalone.py
```

Then open `bottom-truth-offline.html` and confirm: the zone renders, the popup shows the citation chips, clicking
a chip opens the encyclopedia at the right entry, and a flagged zone shows the ⚠ pin.

A quick headless smoke test (tiles will be blank; that is expected):

```sh
node -e "new Function(require('fs').readFileSync('js/app.js','utf8'))"   # parses?
```

## 5. Regenerate the open-questions register

If the new zone carries a `flag`, regenerate `OPEN-QUESTIONS.md` so it stays in sync — it is
generated from `data/zones-local.json`, not hand-written.

## 6. Sweep for drift

If you *corrected* an existing rule rather than adding one, grep the prose for the old version:

```sh
grep -rn "379.101(17)" js/ data/regs.json README.md
```

`data/regs.json` and `README.md` carry prose restatements of the same rules and have drifted from
`law.json` before. That is how a citation the verification pass had already fixed survived in the
shipped README.

## 7. Commit with the reasoning, not just the change

Commit messages in this repo record *why* — which defect, which source, which visual check. They are
the only audit trail the legal layer has.
