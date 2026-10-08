#!/usr/bin/env python3
"""Data integrity checks for the map. Run from the repo root or anywhere:

    python3 tools/test-data.py

Checks
  1. Every law id referenced by zones-local.json, zones-statewide.json, species.json, and by string
     literals in js/app.js and js/coverage.js exists in data/law.json.
  2. Every coordinate in the geodata files lies within 24 to 31.5 N and 79 to 88.5 W.
  3. Every polygon ring is closed (first point equals last point) and has at least 4 points.
Exit status 1 if any check fails. Warnings (outside-box points in files that legitimately reach
past Florida, such as tide stations in Georgia) are listed but do not fail the run.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
LAT = (24.0, 31.5)
LON = (-88.5, -79.0)

fails, warns, known = [], [], []

# Reviewed exceptions to the coordinate box. Each is real geometry that lies outside it on purpose.
# A point is excused only when its location string starts with one of these keys.
KNOWN_OUTSIDE = {
    'zones-statewide.json#usace-334-620-a1-kw-training':
        '33 C.F.R. 334.620(a)(1) NAS Key West training area; its arc runs south of 24 N',
    'jurisdiction.json atl path 18':
        'BOEM SLA line ends at the Georgia boundary, 31.507 N',
    'jurisdiction.json gom path 384':
        'same Georgia-end segment; the gom array repeats the atl paths (see app.js buildJuris)',
}


def load(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as f:
        return json.load(f)


def fail(msg):
    fails.append(msg)


# ------------------------------------------------------------------ 1. law ids
law = load('law.json')
entries = law['entries'] if isinstance(law, dict) else law
LAW_IDS = {e['id'] for e in entries}
dupes = {i for i in LAW_IDS if sum(1 for e in entries if e['id'] == i) > 1}
if dupes:
    fail('law.json: duplicate ids: ' + ', '.join(sorted(dupes)))


def check_ids(where, ids):
    for i in ids or []:
        if i not in LAW_IDS:
            fail('%s: law id "%s" not in law.json' % (where, i))


zl = load('zones-local.json')
for z in zl.get('zones', zl):
    check_ids('zones-local.json#' + z['id'], z.get('law'))
zs = load('zones-statewide.json')
for z in zs.get('zones', zs):
    check_ids('zones-statewide.json#' + z['id'], z.get('law'))
jt = load('jetties.json')
for z in jt['zones']:
    check_ids('jetties.json#' + z['id'], z.get('law'))
bc = load('beaches.json')
for z in bc['zones']:
    check_ids('beaches.json#' + z['id'], z.get('law'))
sp = load('species.json')
for s in sp['species']:
    check_ids('species.json#' + s['id'], s.get('law'))

# string literals in the app code that look like law ids. The patterns cover every id prefix in
# use; a literal that matches the pattern but is not a law id must be listed in NOT_LAW.
PREFIX = sorted({e['id'].split('-')[0] for e in entries})
LIT = re.compile(r"""['"]((?:%s)-[a-z0-9-]+)['"]""" % '|'.join(map(re.escape, PREFIX)))
NOT_LAW = {'fed', 'local'}
lit_n = 0
for js in ('js/app.js', 'js/coverage.js'):
    src = open(os.path.join(ROOT, js), encoding='utf-8').read()
    for m in LIT.finditer(src):
        i = m.group(1)
        if i in NOT_LAW:
            continue
        lit_n += 1
        if i not in LAW_IDS:
            line = src.count('\n', 0, m.start()) + 1
            fail('%s:%d: law id "%s" not in law.json' % (js, line, i))

# ------------------------------------------------------------------ 2 and 3. coordinates, rings
counts = {'points': 0, 'rings': 0}


def pt(where, p, soft=False):
    counts['points'] += 1
    if not (isinstance(p, (list, tuple)) and len(p) >= 2 and all(isinstance(v, (int, float)) for v in p[:2])):
        fail('%s: not a [lat, lon] pair: %r' % (where, p))
        return
    lat, lon = p[0], p[1]
    if not (LAT[0] <= lat <= LAT[1] and LON[0] <= lon <= LON[1]):
        msg = '%s: %.5f, %.5f outside 24 to 31.5 N, 79 to 88.5 W' % (where, lat, lon)
        k = next((k for k in KNOWN_OUTSIDE if where.startswith(k)), None)
        if k:
            known.append(k)
        else:
            (warns if soft else fails).append(msg)


def ring(where, r, soft=False):
    counts['rings'] += 1
    if len(r) < 4:
        fail('%s: ring has %d points (need 4 or more, closed)' % (where, len(r)))
    elif r[0] != r[-1]:
        fail('%s: ring not closed (first %r, last %r)' % (where, r[0], r[-1]))
    for p in r:
        pt(where, p, soft)


def rings(where, rs, soft=False):
    for k, r in enumerate(rs or []):
        ring('%s ring %d' % (where, k), r, soft)


def paths(where, ps, soft=False):
    for k, path in enumerate(ps or []):
        for p in path:
            pt('%s path %d' % (where, k), p, soft)


def points(name, rows, soft=False, key='n'):
    for i, x in enumerate(rows):
        pt('%s[%d] %s' % (name, i, x.get(key) or x.get('id') or ''), [x['lat'], x['lon']], soft)


for z in zl.get('zones', zl):
    w = 'zones-local.json#' + z['id']
    rings(w, z.get('r')); paths(w, z.get('line'))
for z in zs.get('zones', zs):
    w = 'zones-statewide.json#' + z['id']
    rings(w, z.get('r')); paths(w, z.get('line'))
    for p in z.get('pts') or []:
        pt(w + ' pts', p)

jids = set()
for z in jt['zones']:
    w = 'jetties.json#' + z['id']
    if z['id'] in jids:
        fail(w + ': duplicate id')
    jids.add(z['id'])
    if z['kind'] not in ('closed', 'warn'):
        fail(w + ': kind must be closed or warn')
    if not (z.get('r') or z.get('pts')):
        fail(w + ': no buffer ring and no marker')
    rings(w, z.get('r')); paths(w, z.get('line'))
    for p in z.get('pts') or []:
        pt(w + ' pts', p)
    if z.get('exempt'):
        rings(w + ' exempt', z['exempt']['r']); paths(w + ' exempt line', [z['exempt']['line']])


bids = set()
for z in bc['zones']:
    w = 'beaches.json#' + z['id']
    if z['id'] in bids:
        fail(w + ': duplicate id')
    bids.add(z['id'])
    if z['kind'] not in ('closed', 'warn'):
        fail(w + ': kind must be closed or warn')
    if not z.get('ri') or not z.get('li'):
        fail(w + ': no buffer ring or no shore line')


def dec_i(a):
    out, la, lo = [], 0, 0
    for k in range(0, len(a), 2):
        la, lo = (a[k], a[k + 1]) if k == 0 else (la + a[k], lo + a[k + 1])
        out.append([la / 1e5, lo / 1e5])
    return out


for i, b in enumerate(load('bridges.json')):
    w = 'bridges.json[%d] %s' % (i, b.get('n'))
    if b.get('rv') not in (None, 'span', 'short', 'none', 'ferry'):
        fail(w + ': unknown rv %r' % b.get('rv'))
    if (b.get('rv') == 'span') != bool(b.get('sp')) or bool(b.get('sp')) != bool(b.get('dk')):
        fail(w + ': rv span needs both sp and dk, and only span has them')
    if (b.get('rv') in ('span', 'short')) != (b.get('ds') in ('chart', 'roads', 'both', 'wide')):
        fail(w + ': rv span or short needs ds chart, roads, both or wide, and only they have it')
    if b.get('sp'):
        if b['st'] == 'excluded':
            fail(w + ': excluded bridge carries a span buffer')
        rings(w + ' span', [dec_i(r) for r in b['sp']]); paths(w + ' deck', [dec_i(d) for d in b['dk']])

for z in bc['zones']:
    w = 'beaches.json#' + z['id']
    rings(w, [dec_i(r) for r in z['ri']]); paths(w + ' shore', [dec_i(z['li'])])

for i, z in enumerate(load('zones-palmbeach.json')):
    w = 'zones-palmbeach.json#' + z['id']
    if z.get('kind') == 'line':
        paths(w, [z['geom']])
    else:
        ring(w, z['geom'])
for c in load('closures.json'):
    rings('closures.json#' + c.get('id', c.get('name', '')), c['rings'])
for name in ('fknms.json', 'parkwaters.json', 'cwa.json', 'enc-areas.json', 'hardbottom.json',
             'hardbottom-sw.json'):
    for i, x in enumerate(load(name)):
        rings('%s[%d] %s' % (name, i, x.get('n') or x.get('c') or ''), x['r'])
# reference-only layers: a charted area or inventory site can reach past the box; warn only
for name in ('enc-restricted.json', 'mpa.json'):
    for i, x in enumerate(load(name)):
        rings('%s[%d] %s' % (name, i, x.get('n') or ''), x['r'], soft=True)
sb = load('seabed.json')
for i, a in enumerate(sb.get('areas', [])):
    rings('seabed.json areas[%d]' % i, a['r'])
for i, p in enumerate(sb.get('pts', [])):
    pt('seabed.json pts[%d]' % i, p)
    if not (0 <= p[2] < len(sb['classes'])):
        fail('seabed.json pts[%d]: class index %r out of range' % (i, p[2]))
for i, c in enumerate(load('contours.json')):
    paths('contours.json[%d] %s ft' % (i, c.get('ft')), c['p'])
j = load('jurisdiction.json')
for k in ('atl', 'gom'):
    paths('jurisdiction.json ' + k, j[k])
cov = load('coverage.json')
for g in cov['regions']:
    for p in g['outer']:
        pt('coverage.json#' + g['id'], p)
for name in ('enc.json', 'buoys.json', 'piers.json', 'ramps.json', 'sites.json', 'bridges.json'):
    points(name, load(name))
# tide and current stations include a few in Georgia and Alabama on purpose
points('stations.json', load('stations.json'), soft=True)
spots = load('spots.json')
points('spots.json', spots['spots'], key='id')
ids = [s['id'] for s in spots['spots']]
if len(ids) != len(set(ids)):
    fail('spots.json: duplicate ids')

# ------------------------------------------------------------------ report
print('law.json: %d entries (version %s)' % (len(entries), law.get('version') if isinstance(law, dict) else '?'))
print('checked %d law-id literals in js/app.js and js/coverage.js' % lit_n)
print('checked %d coordinates and %d rings' % (counts['points'], counts['rings']))
if known:
    print('\nreviewed exceptions outside the box (not failures):')
    for k in sorted(set(known)):
        print('  KNOWN %s: %d point(s). %s' % (k, known.count(k), KNOWN_OUTSIDE[k]))
if warns:
    print('\n%d warning(s), not failures:' % len(warns))
    for w in warns[:25]:
        print('  WARN ' + w)
    if len(warns) > 25:
        print('  ... %d more' % (len(warns) - 25))
if fails:
    print('\n%d FAILURE(S):' % len(fails))
    for f in fails[:80]:
        print('  FAIL ' + f)
    if len(fails) > 80:
        print('  ... %d more' % (len(fails) - 80))
    sys.exit(1)
print('\nall checks passed')
