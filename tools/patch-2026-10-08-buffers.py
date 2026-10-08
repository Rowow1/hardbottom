# -*- coding: utf-8 -*-
"""Sidebar text for the statewide buffer layers rebuilt or added on 8 Oct 2026 (jetties and bridge
decks from the NOAA chart and Census roads, beaches from FDEP range monuments). Idempotent: each edit
is applied only where the old text is still present, and the script fails if neither the old nor the
new text is found."""
import io, json, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
P = os.path.join(ROOT, 'data', 'regs.json')
d = json.load(io.open(P, encoding='utf-8'))
EDITS = [
    (0, 'All four are drawn only in Palm Beach County; elsewhere only FWC-inventoried piers and the classified bridges carry a buffer. Outside Palm Beach County, assume all four apply wherever there is a beach, pier, fishing bridge or jetty.',
        'On this map the jetty buffer is drawn at 75 structures statewide, the bridge buffer along each deck that the NOAA chart or the Census road map shows, the pier buffer around every FWC-listed pier, and the beach buffer along the open-coast sandy beaches that FDEP\'s range monuments mark. Beaches on bays and lagoons, and piers and bridges missing from the inventories, are not drawn: assume all four apply wherever there is a beach, pier, fishing bridge or jetty.'),
    (1, 'On this map each coastal and tidal bridge buffer is drawn along the deck as traced on imagery, not only around the inventory point.',
        'On this map each coastal and tidal bridge buffer is drawn along the deck where the NOAA chart or the Census road map shows one, not only around the inventory point; where neither shows a deck, only the circle is drawn and a long bridge is under-drawn.'),
]
for i, old, new in EDITS:
    item = d['statewide'][i]
    if old in item[1]:
        item[1] = item[1].replace(old, new)
    elif new not in item[1]:
        sys.exit('statewide[%d]: neither the old nor the new text found' % i)
io.open(P, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))
print('regs.json statewide buffer text updated')
