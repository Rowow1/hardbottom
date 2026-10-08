#!/usr/bin/env python3
"""Build self-contained HTML files: no web server needed, just open one.

Writes two files, next to this script or into the directory given with --out DIR:
  bottom-truth-offline.html       every data file except the two reference-only layers
                                  (enc-restricted, mpa)
  bottom-truth-offline-lite.html  also without the bulk habitat and depth files (contours,
                                  hardbottom, hardbottom-sw, seabed, enc-areas)

The built files are not committed. The GitHub deploy workflow builds them for the website and
attaches them to each release.

Every <script src="js/..."> in index.html is inlined in document order, so a new script only has to
be added to index.html. A layer whose data file is left out shows "not included in this offline
build" in its legend row. Remote tiles (base maps and overlays) still need a network connection.
"""
import json, os, re, sys

here = os.path.dirname(os.path.abspath(__file__))
out_dir = here
if '--out' in sys.argv:
    out_dir = os.path.abspath(sys.argv[sys.argv.index('--out') + 1])
    os.makedirs(out_dir, exist_ok=True)


def r(*p):
    return open(os.path.join(here, *p), encoding='utf-8').read()


def d(n):
    return json.load(open(os.path.join(here, 'data', n + '.json'), encoding='utf-8'))


def js_safe(text):
    """Keep inlined code and JSON from closing the <script> element early."""
    return re.sub(r'</(script)', r'<\\/\1', text, flags=re.I)


ALL = ['sites', 'ramps', 'zones-palmbeach', 'regs', 'closures', 'law', 'enc', 'enc-areas', 'parkwaters',
       'contours', 'hardbottom', 'hardbottom-sw', 'seabed', 'fknms', 'jurisdiction', 'piers', 'bridges', 'jetties', 'beaches',
       'zones-local', 'zones-statewide', 'cwa', 'buoys', 'stations', 'spots', 'species', 'coverage',
       'enc-restricted', 'mpa']
REFERENCE_ONLY = {'enc-restricted', 'mpa'}
LITE_DROP = REFERENCE_ONLY | {'contours', 'hardbottom-sw', 'seabed', 'enc-areas', 'hardbottom'}

missing = [n for n in ALL if not os.path.exists(os.path.join(here, 'data', n + '.json'))]
if missing:
    sys.exit('missing data files: ' + ', '.join(missing))

leaflet_css = re.sub(r'url\([^)]*\)', 'none', r('vendor', 'leaflet', 'leaflet.css'))
index = r('index.html')
scripts = re.findall(r'<script src="(js/[^"]+)"></script>', index)
if 'js/app.js' not in scripts:
    sys.exit('index.html does not load js/app.js')


def build(names, out_name, label):
    data = {k: d(k) for k in names}
    html = index
    html = html.replace('<link rel="stylesheet" href="vendor/leaflet/leaflet.css">',
                        '<style>' + leaflet_css + '</style>')
    html = html.replace('<link rel="stylesheet" href="css/app.css">',
                        '<style>' + r('css', 'app.css') + '</style>')
    html = html.replace('<script src="vendor/leaflet/leaflet.js"></script>',
                        '<script>' + js_safe(r('vendor', 'leaflet', 'leaflet.js')) + '</script>')
    for i, src in enumerate(scripts):
        tag = '<script src="%s"></script>' % src
        body = '<script>' + js_safe(r(*src.split('/'))) + '</script>'
        if i == 0:
            body = ('<script>window.__DATA=' + js_safe(json.dumps(data, separators=(',', ':'), ensure_ascii=False)) +
                    ';window.__BUILD=' + json.dumps(label) + ';</script>\n' + body)
        html = html.replace(tag, body)
    # The offline copy has no about.html beside it; link to the live page instead.
    html = html.replace('href="about.html"', 'href="https://bottomtruth.com/about.html"')
    html = html.replace('href="favicon.svg"', 'href="https://bottomtruth.com/favicon.svg"')
    left = re.findall(r'<script src="[^"]+"></script>', html)
    if left:
        sys.exit('not inlined: ' + ', '.join(left))
    out = os.path.join(out_dir, out_name)
    open(out, 'w', encoding='utf-8').write(html)
    size = os.path.getsize(out)
    print('wrote %-46s %6.1f MB  (%d data files; left out: %s)' % (
        out_name, size / 1048576, len(names), ', '.join(sorted(set(ALL) - set(names))) or 'none'))
    return size


build([n for n in ALL if n not in REFERENCE_ONLY], 'bottom-truth-offline.html', 'full')
build([n for n in ALL if n not in LITE_DROP], 'bottom-truth-offline-lite.html', 'lite')
