# Bridge span review, 8 October 2026: working notes

Panels show each NBI bridge point (yellow) on USGS NAIP, the OpenStreetMap bridge decks matched to
it (green), the 125 yd buffer along those decks (red band), other OSM bridge ways within 250 m
(cyan dashes), and the old 125 yd circle where nothing matched (red ring). n = panel number in the
review order (coastal and tidal bridges, presumed or confirmed, in bridges.json order).

Policy fixed after panels 0 to 389:
- A deck counts only if it is within 60 m of the NBI point ("tight"). A loose match (nearest deck
  60 to 250 m away) is not used: it is often a different bridge. Those records keep the circle and
  get a note.
- Motorways and motorway links are never matched: they are limited-access and their own NBI records
  are already classed excluded. A presumed record whose only nearby deck is a motorway keeps its
  circle.
- For a road-named record, footways and paths more than 15 m away are not matched.
- The drawn buffer is the union of the old circle and the span band, so no record covers less
  water than before.

Panels needing a note or a fix (beyond the policy above):
- 2, 416 (no imagery tile returned): geometry from OSM only.
- 7, 28: SR-776 over the Myakka; NBI point at the south abutment, span band runs the full bridge. Correct.
- 156: Golden Gate Pkwy, nearest OSM way was a park footpath (removed by the footway rule).
- 262, 286, 297: Courtney Campbell and Gandy causeways: only the bridge decks are buffered, not the
  causeway fill, which follows the rule's "that portion of any bridge".
- 1408, 1409 (SR-A1A / SR-105 "Ferry", St. Johns River): the matched line is the Mayport ferry
  crossing, not a bridge deck. Span not used; the circle at the NBI point is kept.
- 1170 to 1260 (Okaloosa, Walton): NAIP tiles blank for part of the area; panels read on the
  Sentinel-2 2020 mosaic (marked S2) or the NAIP image service. Matches checked against the road line.
- Policy added after panel 750: a "loose" match is accepted only when the OSM way's name or ref
  shares a route number or a distinctive word with the NBI record ("named" matches, 43 records,
  all inspected).
