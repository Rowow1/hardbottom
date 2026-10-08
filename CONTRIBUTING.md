# Contributing

Corrections and new rules are welcome. Because people plan dives from this map, a change to the
legal layer has to meet the evidence standard below before it is merged. A change that cannot meet
it is still useful as an issue, where it stays visible as an open question.

## Reporting an error

Open an issue using the "Wrong or missing rule" or "Posted sign" template. The most useful reports
include:

- the location (coordinates, or a dropped pin from the map's What's here? popup),
- what the map shows there,
- what the posted sign or the law says, with a photo of the sign or a link to the official text,
- the date you saw it.

Issues are public. Do not post personal information.

Reports are not promoted into the map as they stand. A maintainer checks each one against the
primary source first, and the map keeps user reports separate from verified geometry.

## The evidence standard for legal changes

1. **Primary sources only.** Statutes from Online Sunshine (leg.state.fl.us), administrative rules
   from FLRules, federal regulations from eCFR, and local ordinances from Municode or the county or
   city's own code site. A blog, a dive shop page, a forum post or an AI summary is not authority.
2. **Verbatim or flagged.** An excerpt in `data/law.json` is either word for word from the primary
   source, with `verified` set to `verbatim`, or it is marked `secondary` with a note on where it
   came from.
3. **Four checks before a citation goes in:** the citation number is in force; the cited
   subsection actually contains the quoted text; the quote is word for word; and the URL resolves
   to the authoritative text.
4. **Confirmed negatives count.** "No such ordinance exists" is recorded and cited with the same
   care as a rule that does exist (`kind: negative`).
5. **No invented geometry.** If the law defines a boundary that no public dataset carries, draw it
   from the nearest published geometry that contains it and say how the drawing differs in the
   zone's `flag`, or drop a marker. Never trace a plausible-looking line.
6. **Conservative margin.** Where a rule is ambiguous, draw the reading that closes more water and
   say which reading was drawn.
7. **Closures only.** Text on the map states what the law closes or restricts. It never says that
   water is open or that spearfishing is legal at a place.
8. **Sweep for stale copies.** When a rule changes, search `data/regs.json`, the zone text and the
   README for the old wording.

## How to make a change

- Do not edit `data/law.json` by hand. Add a dated pass under `tools/law-updates/<date>/` or an entry
  in the manual block of `tools/law_updates.py`, then run `python3 tools/build-law.py`.
- Zone procedure, including the satellite check, is in `docs/ADDING-A-ZONE.md`. Field formats are
  in `docs/SCHEMA.md`. Coordinates are `[lat, lon]` with 5 decimal places.
- Run `python3 tools/test-data.py` and the smoke test (see the README) before opening a pull request.
- Add a line to `CHANGELOG.md` for any change to what the map says about the law.

## Writing style

Plain, precise prose. State the rule and its source. No marketing language, no em dashes, and
ranges written with "to" (10 to 20 ft).

## Licensing of contributions

Code contributions are accepted under the MIT licence in `LICENSE`. Data contributions are accepted
under the licence of the file they go into, as listed in `LICENSE-DATA.md`.
