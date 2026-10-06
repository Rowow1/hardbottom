/* Bottom Truth: header search.
   Load AFTER js/app.js. Reads SEARCH_ITEMS (filled by the build functions in app.js), the law
   registry (window.FLLaw) and the species list (window.FLSpecies), and parses typed coordinates.
   Adds window.FLSpearMap.search(q). */
(function () {
  'use strict';
  if (typeof SEARCH_ITEMS === 'undefined') {
    console.error('[search] app.js has not loaded; put this script tag after js/app.js');
    return;
  }

  /* sources whose features are searchable by name; loaded (not shown) on first use */
  var SEARCH_SRC = ['spots', 'enc', 'enc-areas', 'piers', 'buoys', 'fknms', 'parkwaters', 'cwa',
                    'zones-local', 'zones-statewide'];
  var GROUPS = [
    ['coord', 'Coordinates'], ['spot', 'Dive spots'], ['site', 'Reef sites'],
    ['enc', 'Charted wrecks & fish havens'], ['ramp', 'Boat ramps'], ['pier', 'Piers & jetties'],
    ['buoy', 'Keys sanctuary buoys'], ['zone', 'Legal zones'], ['law', 'Law'], ['species', 'Species']
  ];
  var MAX = 40;

  var norm = function (s) {
    return String(s == null ? '' : s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[’'`]/g, '').replace(/[^a-z0-9.]+/g, ' ').trim();
  };
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  };

  /* ---------------------------------------------------------------- coordinates */
  /* Accepts decimal degrees ("26.78, -80.04", "26.78N 80.04W"), degrees and decimal minutes
     ("26 46.9 N 80 02.7 W", "26°46.9'N 80°02.7'W") and degrees, minutes, seconds. A positive
     longitude with no hemisphere letter, between 79 and 88.5, is read as west (Florida). */
  function partToDeg(p) {
    var n = p.trim().split(/\s+/).filter(Boolean);
    if (!n.length || n.length > 3) return NaN;
    if (!n.every(function (x) { return /^[-+]?\d+(\.\d+)?$/.test(x); })) return NaN;
    var neg = /^-/.test(n[0]);
    var d = Math.abs(parseFloat(n[0])), m = n[1] != null ? parseFloat(n[1]) : 0, s = n[2] != null ? parseFloat(n[2]) : 0;
    if (m >= 60 || s >= 60) return NaN;
    if (n.length > 1 && /\./.test(n[0])) return NaN;
    var v = d + m / 60 + s / 3600;
    return neg ? -v : v;
  }
  function parseCoord(q) {
    var s = String(q || '').toUpperCase()
      .replace(/[°º˚'′’"″”]/g, ' ')
      .replace(/[,;\/]/g, ' ').replace(/\s+/g, ' ').trim();
    if (!s || !/\d/.test(s) || /[A-DF-MO-RT-VX-Z]/.test(s)) return null;
    var lat, lon, guessed = false, m;
    if ((m = /^([-+\d.\s]+?)\s*([NS])\s*([-+\d.\s]+?)\s*([EW])$/.exec(s))) {
      lat = partToDeg(m[1]); lon = partToDeg(m[3]);
      if (m[2] === 'S') lat = -Math.abs(lat);
      if (m[4] === 'W') lon = -Math.abs(lon);
    } else if ((m = /^([NS])\s*([-+\d.\s]+?)\s+([EW])\s*([-+\d.\s]+)$/.exec(s))) {
      lat = partToDeg(m[2]); lon = partToDeg(m[4]);
      if (m[1] === 'S') lat = -Math.abs(lat);
      if (m[3] === 'W') lon = -Math.abs(lon);
    } else if (!/[NSEW]/.test(s)) {
      var n = s.split(' ');
      if (n.length % 2 || n.length < 2 || n.length > 6) return null;
      var h = n.length / 2;
      lat = partToDeg(n.slice(0, h).join(' '));
      lon = partToDeg(n.slice(h).join(' '));
      if (lon > 79 && lon < 88.5 && lat > 24 && lat < 31.5) { lon = -lon; guessed = true; }
    } else return null;
    if (!isFinite(lat) || !isFinite(lon) || Math.abs(lat) > 90 || Math.abs(lon) > 180) return null;
    return { lat: lat, lon: lon, guessed: guessed };
  }

  /* ---------------------------------------------------------------- scoring */
  function score(qn, words, name, extra) {
    var n = norm(name);
    if (!n) return 0;
    if (n === qn) return 100;
    if (n.indexOf(qn) === 0) return 85;
    var nw = ' ' + n;
    if (nw.indexOf(' ' + qn) >= 0) return 70;
    var all = words.every(function (w) { return nw.indexOf(' ' + w) >= 0; });
    if (all) return 60;
    if (n.indexOf(qn) >= 0) return 45;
    if (extra) {
      var e = ' ' + norm(extra);
      if (e.indexOf(' ' + qn) >= 0) return 40;
      if (words.every(function (w) { return (nw + e).indexOf(' ' + w) >= 0; })) return 30;
    }
    return 0;
  }

  var PREP = null;
  function prepare() {
    if (PREP) return PREP;
    /* sites and ramps register at coreReady; the named sources register as they load */
    var core = coreReady;
    var list = [SEARCH_SRC.map(ensure)];
    if (window.FLSpecies && window.FLSpecies.load) list.push(window.FLSpecies.load());
    list.push(core);
    PREP = Promise.all(list.map(function (x) { return Array.isArray(x) ? Promise.all(x) : x; }))
      .then(function () { return true; }, function () { return true; });
    return PREP;
  }

  function lawItems() {
    if (!window.FLLaw || !window.FLLaw.all) return [];
    return window.FLLaw.all().map(function (e) {
      return { g: 'law', id: e.id, n: e.cite, a: e.title, sub: e.title, neg: e.kind === 'negative' };
    });
  }
  function speciesItems() {
    if (!window.FLSpecies || !window.FLSpecies.list) return [];
    var SP = { prohibited: 'Spear prohibited', restricted: 'Spear restricted', allowed: 'Spear is legal gear; limits apply' };
    return window.FLSpecies.list().map(function (s) {
      return { g: 'species', id: s.id, n: s.name, a: (s.aka || []).join(' ') + ' ' + (s.sci || ''),
               sub: (s.sci ? s.sci + ' · ' : '') + (SP[s.spear] || s.spear) };
    });
  }

  function find(q) {
    var out = [];
    var c = parseCoord(q);
    if (c) {
      out.push({ g: 'coord', n: c.lat.toFixed(5) + ', ' + c.lon.toFixed(5),
        sub: (c.guessed ? 'Longitude read as west. ' : '') + 'Go here and check the legal layers at this point',
        ll: [c.lat, c.lon], coord: c, s: 100 });
    }
    var qn = norm(q);
    if (qn.length < 2 && !c) return out;
    var words = qn.split(' ').filter(Boolean);
    var pool = SEARCH_ITEMS.filter(function (it) { return !it.inland || showInland; })
      .concat(lawItems(), speciesItems());
    var byG = {};
    pool.forEach(function (it) {
      var sc = score(qn, words, it.n, it.a);
      if (!sc) return;
      (byG[it.g] = byG[it.g] || []).push({ it: it, s: sc });
    });
    var groupsHit = GROUPS.filter(function (g) { return byG[g[0]]; }).length || 1;
    var cap = Math.max(6, Math.floor(MAX / groupsHit));
    GROUPS.forEach(function (g) {
      var arr = byG[g[0]];
      if (!arr) return;
      var seen = {};
      arr.sort(function (a, b) { return b.s - a.s || String(a.it.n).length - String(b.it.n).length; });
      arr.filter(function (x) {
        var k = norm(x.it.n) + '|' + (x.it.ll ? x.it.ll.map(function (v) { return v.toFixed(3); }).join(',') : x.it.id);
        if (seen[k]) return false; seen[k] = 1; return true;
      }).slice(0, cap).forEach(function (x) { out.push(Object.assign({}, x.it, { s: x.s })); });
    });
    return out.slice(0, MAX);
  }

  function select(it) {
    if (!it) return;
    if (it.g === 'coord') {
      map.setView(it.ll, Math.max(map.getZoom(), 13), { animate: false });
      whatsHere(it.ll[0], it.ll[1]);
    } else if (it.g === 'law') {
      if (window.FLLaw) window.FLLaw.open(it.id);
    } else if (it.g === 'species') {
      if (window.FLSpecies) window.FLSpecies.open(it.id);
    } else {
      focusFeature(it);
    }
  }

  function publicResult(it) {
    var r = { type: it.g, name: it.n, sub: it.sub || '', id: it.id || null,
              lat: it.ll ? it.ll[0] : null, lon: it.ll ? it.ll[1] : null };
    r.select = function () { select(it); };
    return r;
  }

  /* ---------------------------------------------------------------- UI */
  var inp, box, res = [], act = -1, timer = null;

  function renderList(items) {
    res = items; act = items.length ? 0 : -1;
    if (!inp.value.trim()) { close(); return; }
    if (!items.length) {
      box.innerHTML = '<div class="q-empty">No match. Try a reef or wreck name, a county rule, a species, ' +
        'or coordinates such as 26 46.9 N 80 02.7 W.</div>';
      open(); return;
    }
    var html = '', last = null, i = 0;
    items.forEach(function (it) {
      if (it.g !== last) {
        last = it.g;
        var lab = GROUPS.filter(function (g) { return g[0] === it.g; })[0];
        html += '<div class="q-g">' + esc(lab ? lab[1] : it.g) + '</div>';
      }
      html += '<div class="q-i" role="option" id="q-o' + i + '" data-i="' + i + '"' +
        (i === act ? ' aria-selected="true"' : '') + '><b>' + esc(it.n) + '</b>' +
        (it.sub ? '<span>' + esc(it.sub) + '</span>' : '') + '</div>';
      i++;
    });
    box.innerHTML = html;
    open();
    mark();
  }
  function mark() {
    Array.prototype.forEach.call(box.querySelectorAll('.q-i'), function (el) {
      var on = +el.dataset.i === act;
      el.classList.toggle('act', on);
      if (on) { el.setAttribute('aria-selected', 'true'); inp.setAttribute('aria-activedescendant', el.id);
                if (el.scrollIntoView) el.scrollIntoView({ block: 'nearest' }); }
      else el.removeAttribute('aria-selected');
    });
  }
  function open() { box.hidden = false; inp.setAttribute('aria-expanded', 'true'); }
  function close() { box.hidden = true; inp.setAttribute('aria-expanded', 'false'); inp.removeAttribute('aria-activedescendant'); }
  function run() {
    var q = inp.value;
    if (!q.trim()) { close(); return; }
    prepare().then(function () { if (inp.value === q) renderList(find(q)); });
    if (res.length === 0) { box.innerHTML = '<div class="q-empty">Searching…</div>'; open(); }
  }
  function choose(i) {
    var it = res[i];
    if (!it) return;
    close();
    inp.blur();
    select(it);
  }

  function install() {
    inp = document.getElementById('q');
    box = document.getElementById('q-res');
    if (!inp || !box) return;
    inp.addEventListener('focus', function () { prepare(); if (inp.value.trim()) run(); });
    inp.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, 110); });
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); if (box.hidden) run(); else if (res.length) { act = (act + 1) % res.length; mark(); } }
      else if (e.key === 'ArrowUp') { e.preventDefault(); if (res.length) { act = (act - 1 + res.length) % res.length; mark(); } }
      else if (e.key === 'Enter') {
        e.preventDefault();
        var q = inp.value;
        prepare().then(function () {
          if (inp.value !== q) return;
          if (!res.length || box.hidden) res = find(q);
          choose(act >= 0 ? act : 0);
        });
      } else if (e.key === 'Escape') { if (!box.hidden) { e.stopPropagation(); close(); } else inp.blur(); }
    });
    box.addEventListener('mousedown', function (e) { e.preventDefault(); });
    box.addEventListener('click', function (e) {
      var el = e.target.closest && e.target.closest('.q-i');
      if (el) choose(+el.dataset.i);
    });
    document.addEventListener('click', function (e) {
      if (!box.hidden && !(e.target.closest && e.target.closest('#srch'))) close();
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install);
  else install();

  /* ---------------------------------------------------------------- API */
  var api = window.FLSpearMap;
  if (api) {
    /* search(q) resolves with up to 40 results [{type, name, sub, id, lat, lon, select()}].
       type is one of coord, spot, site, enc, ramp, pier, buoy, zone, law, species. */
    api.search = function (q) {
      return coreReady.then(prepare).then(function () { return find(q).map(publicResult); });
    };
    api.parseCoord = parseCoord;
  }
  window.FLSearch = { parseCoord: parseCoord, find: function (q) { return prepare().then(function () { return find(q); }); } };
})();
