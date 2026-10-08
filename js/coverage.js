/* Bottom Truth: research-coverage layer ("what have we actually looked at?")
   Drop-in. Load AFTER js/app.js in index.html:
       <script src="js/coverage.js"></script>

   Why this exists
   ---------------
   The map's most important limitation is that legal coverage is not uniform: Palm Beach County
   is fully mapped, the Keys are partly mapped, and everywhere else carries statewide layers only.
   Stated in the README and in the sidebar, that limitation is invisible at the one moment it
   matters — when someone zooms to a county that has never been researched and sees clean water.
   Clean water reads as permission whatever the sidebar says.

   This layer makes coverage a thing you can SEE. Un-inventoried water gets a grey wash; the two
   researched regions get an outline. It is a fog-of-war layer, not a legal layer, and every
   string in it says so.

   Implementation notes
   --------------------
   * The wash is `interactive:false` — a state-sized polygon that swallowed clicks would break
     every popup underneath it. The explanation lives in the legend footnote and the sidebar.
   * Region OUTLINES are polylines, not polygons, for the same reason.
   * Rows are pushed into the existing `legal` legend group so no edit to buildLegend() is needed.
   * CATS/layers/shown/buildLegend/applyVisibility are top-level bindings in app.js. Classic
     scripts share the global lexical environment, so they are reachable here by bare name.
   * CATS.push happens synchronously at parse time — before boot()'s first await resolves — so the
     rows exist by the time boot() builds the layer groups. Layer drawing waits for `map`.
*/
(function () {
  'use strict';

  var CAT_ROWS = [
    { id: 'covNone', tier: 'none' },
    { id: 'covPart', tier: 'partial' },
    { id: 'covFull', tier: 'full' }
  ];

  /* Fallback styling, overridden by whatever data/coverage.json declares. */
  var FALLBACK = {
    none:    { label: 'Not inventoried',    col: '#94a3b8', fill: 0.22, on: true },
    partial: { label: 'Partly inventoried', col: '#facc15', fill: 0.0,  on: true },
    full:    { label: 'Fully inventoried',  col: '#30a46c', fill: 0.0,  on: true }
  };

  /* ---- 1. register legend rows synchronously ---- */
  if (typeof CATS === 'undefined') {
    console.error('[coverage] app.js has not loaded; put this script tag AFTER js/app.js');
    return;
  }
  CAT_ROWS.forEach(function (r) {
    var f = FALLBACK[r.tier];
    CATS.push({ id: r.id, grp: 'legal', label: 'Coverage: ' + f.label, col: f.col, on: f.on });
  });

  /* ---- 2. load the data, then draw once the map exists ---- */
  var COV = null;

  function fetchData() {
    if (window.__DATA && window.__DATA.coverage) return Promise.resolve(window.__DATA.coverage);
    return fetch('data/coverage.json').then(function (r) {
      if (!r.ok) throw new Error('data/coverage.json: ' + r.status);
      return r.json();
    });
  }

  function ready() {
    return typeof map !== 'undefined' && map &&
           typeof layers !== 'undefined' && layers && layers.covNone;
  }

  function whenReady(fn) {
    if (ready()) { fn(); return; }
    var tries = 0;
    (function poll() {
      if (ready()) { fn(); return; }
      if (++tries > 600) { console.warn('[coverage] map never became ready'); return; }
      requestAnimationFrame(poll);
    })();
  }

  fetchData().then(function (d) {
    COV = d;
    /* adopt the file's own labels/colours if present */
    CAT_ROWS.forEach(function (r) {
      var t = COV.tiers && COV.tiers[r.tier];
      if (!t) return;
      var row = CATS.filter(function (c) { return c.id === r.id; })[0];
      if (!row) return;
      if (t.label) row.label = 'Coverage: ' + t.label;
      if (t.col) row.col = t.col;
      if (typeof t.on === 'boolean') { row.on = t.on; shown[r.id] = t.on; }
    });
    whenReady(draw);
  }).catch(function (e) {
    console.warn('[coverage] not drawn:', e.message);
  });

  /* ---- 3. drawing ---- */
  function rowIdFor(tier) { return CAT_ROWS.filter(function (r) { return r.tier === tier; })[0].id; }
  function cfg(tier) {
    return (COV.tiers && COV.tiers[tier]) || FALLBACK[tier];
  }

  function popupHtml(reg) {
    var t = cfg(reg.tier);
    var cls = reg.tier === 'none' ? 'pv-warn' : (reg.tier === 'full' ? 'pv-ok' : 'pv-warn');
    var h = '<h3>' + reg.n + '</h3>' +
      '<div class="pv ' + cls + '"><b>' + t.head + '</b><br><br>' + t.body + '</div>';
    if (reg.detail) h += '<div style="margin-top:8px">' + reg.detail + '</div>';
    h += '<span class="m"><b>This is a research-coverage layer, not a legal boundary.</b> ' +
         'It describes how much of the law has been read and drawn in this region. It makes no ' +
         'statement about whether any particular water is open or closed. Outlines are coarse and, ' +
         'where uncertain, drawn smaller than the true extent.' +
         (COV.generated ? '<br>Coverage assessed ' + COV.generated : '') + '</span>';
    return h;
  }

  function draw() {
    COV.regions.forEach(function (reg) {
      var t = cfg(reg.tier);
      var grp = layers[rowIdFor(reg.tier)];
      if (!grp) return;

      /* fill (non-interactive so it never eats a click on the data underneath) */
      if (t.fill > 0) {
        var rings = [reg.outer].concat(reg.holes || []);
        L.polygon(rings, {
          color: t.col, weight: 0, opacity: 0,
          fillColor: t.col, fillOpacity: t.fill,
          interactive: false
        }).addTo(grp);
      }

      /* outline — a polyline, clickable, carries the explanation */
      var ring = reg.outer.concat([reg.outer[0]]);
      L.polyline(ring, {
        color: t.col,
        weight: reg.tier === 'none' ? 1 : 2,
        opacity: reg.tier === 'none' ? 0.45 : 0.9,
        dashArray: reg.tier === 'full' ? null : '7,5'
      }).bindPopup(function () { return popupHtml(reg); }).addTo(grp);

      /* hole edges get an outline too, so the covered regions read as cut-outs */
      (reg.holes || []).forEach(function (h) {
        L.polyline(h.concat([h[0]]), {
          color: t.col, weight: 1, opacity: 0.35, dashArray: '3,4', interactive: false
        }).addTo(grp);
      });
    });

    /* keep the wash beneath every data layer */
    ['covNone', 'covPart', 'covFull'].forEach(function (id) {
      if (layers[id] && map.hasLayer(layers[id])) layers[id].eachLayer(function (l) {
        if (l.bringToBack) l.bringToBack();
      });
    });

    if (typeof applyVisibility === 'function') applyVisibility();
    if (typeof buildLegend === 'function') buildLegend();
    addLegendNote();
    hookSidebar();
  }

  /* ---- 4. legend footnote ---- */
  function addLegendNote() {
    var el = document.getElementById('legend');
    if (!el) return;
    var body = el.querySelector('#lg-body');
    if (!body || body.querySelector('.lg-note-cov')) return;
    var d = document.createElement('div');
    d.className = 'lg-note lg-note-cov';
    d.innerHTML = '<b>Coverage is not the law.</b> The grey wash marks water where local rules and the ' +
      'buffers of r. 68B-20.003(2) around bay and lagoon beaches and unlisted piers have not been inventoried; ' +
      'assume they apply. ' +
      'Federal, state and many local closures are still drawn there. ' +
      'Un-shaded water is <b>not</b> shown as open.';
    body.appendChild(d);
  }
  /* buildLegend() rebuilds innerHTML, so re-attach after every rebuild */
  if (typeof buildLegend === 'function') {
    var _bl = buildLegend;
    window.buildLegend = buildLegend = function () { _bl.apply(null, arguments); addLegendNote(); };
  }

  /* ---- 5. sidebar verdict for the selected launch ---- */
  var COUNTY_TIER = { 'Palm Beach': 'full', 'Monroe': 'partial' };

  function sidebarBlock(county) {
    var tier = COUNTY_TIER[county] || 'none';
    var t = cfg(tier);
    var cls = tier === 'full' ? 'info' : 'note';
    return '<div class="' + cls + '"><b>Research coverage: ' + t.label.toLowerCase() +
      '.</b><br><br>' + t.head + ' ' + t.body +
      '<br><br><span style="opacity:.75">Switch the <b>Coverage</b> rows in the legend to see the ' +
      'same thing on the map.</span></div>';
  }

  function hookSidebar() {
    if (typeof render !== 'function') return;
    var _r = render;
    window.render = render = function () {
      _r.apply(null, arguments);
      var side = document.getElementById('side');
      if (!side || typeof origin === 'undefined' || !origin) return;
      if (side.querySelector('.cov-block')) return;
      var wrap = document.createElement('div');
      wrap.className = 'cov-block';
      wrap.innerHTML = sidebarBlock(origin.c);
      var h2 = side.querySelector('h2');
      if (h2) side.insertBefore(wrap, h2); else side.appendChild(wrap);
    };
    render();
  }

  /* ---- 6. public API ---- */
  window.FLCoverage = {
    get data() { return COV; },
    tierForCounty: function (c) { return COUNTY_TIER[c] || 'none'; },
    show: function (on) {
      ['covNone', 'covPart', 'covFull'].forEach(function (id) { shown[id] = !!on; });
      applyVisibility(); buildLegend(); render();
    }
  };
})();
