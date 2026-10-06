/* Bottom Truth: species panel.
   Same pattern as the legal encyclopedia in law.js: a fixed side panel, a filter box, one
   collapsible card per species. Data: data/species.json (window.__DATA.species in the standalone
   build). Citation chips come from window.FLLaw.cite and open the encyclopedia.
   Wording rule: "allowed" is never shown as a green light. It reads "Spear is legal gear; limits
   apply", in neutral styling, because place closures apply regardless of species. */
(function () {
  'use strict';
  var DATA = null, LIST = [], BYID = {}, loading = null, filt = { q: '', spear: '' };
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  };
  var norm = function (s) { return String(s == null ? '' : s).toLowerCase(); };

  var SPEAR = {
    prohibited: { cls: 'sp-no',   txt: 'Spear prohibited' },
    restricted: { cls: 'sp-warn', txt: 'Spear restricted: read the region rows' },
    allowed:    { cls: 'sp-neu',  txt: 'Spear is legal gear; limits apply' }
  };
  var REGIONS = [['atlantic', 'Atlantic state waters'], ['gulf', 'Gulf state waters'], ['keys', 'Keys (Monroe)'],
                 ['eez_sa', 'South Atlantic federal waters'], ['eez_gulf', 'Gulf federal waters']];
  var COLS = [['size', 'Size'], ['bag', 'Bag'], ['vessel', 'Vessel'], ['season', 'Season'],
              ['closed', 'Closed'], ['notes', 'Notes']];

  function fetchData() {
    if (window.__DATA) {
      return window.__DATA.species ? Promise.resolve(window.__DATA.species)
        : Promise.reject(new Error('species.json is not included in this offline build'));
    }
    return fetch('data/species.json').then(function (r) {
      if (!r.ok) throw new Error('data/species.json: ' + r.status);
      return r.json();
    });
  }
  function load() {
    if (loading) return loading;
    loading = fetchData().then(function (d) {
      DATA = d; LIST = d.species || [];
      BYID = {}; LIST.forEach(function (s) { BYID[s.id] = s; });
      return LIST;
    }, function (e) { DATA = { error: e.message }; LIST = []; return LIST; });
    return loading;
  }

  function cell(v) { return v == null || v === '' ? '<span class="sp-nil" title="Not listed">\u00b7</span>' : esc(v); }
  function table(s) {
    var rows = REGIONS.filter(function (r) { return s.regions && s.regions[r[0]]; });
    if (!rows.length) return '';
    return '<div class="sp-tw"><table class="sp-t"><thead><tr><th>Waters</th>' +
      COLS.map(function (c) { return '<th>' + c[1] + '</th>'; }).join('') + '</tr></thead><tbody>' +
      rows.map(function (r) {
        var v = s.regions[r[0]];
        return '<tr><th scope="row">' + esc(r[1]) + '</th>' +
          COLS.map(function (c) { return '<td data-h="' + c[1] + '">' + cell(v[c[0]]) + '</td>'; }).join('') + '</tr>';
      }).join('') + '</tbody></table></div>';
  }
  function badge(s) {
    var b = SPEAR[s.spear] || { cls: 'sp-neu', txt: s.spear };
    return '<span class="sp-b ' + b.cls + '">' + esc(b.txt) + '</span>';
  }
  function card(s, open) {
    var aka = (s.aka || []).filter(Boolean);
    var src = (s.sources || []).map(function (u) {
      return '<li><a href="' + esc(u) + '" target="_blank" rel="noopener">' +
        esc(String(u).replace(/^https?:\/\/(www\.)?/, '').slice(0, 70)) + '</a></li>';
    }).join('');
    var v = s.verified === 'verbatim' ? '<span class="v-ok">Checked against the primary text</span>'
      : s.verified === 'secondary' ? '<span class="v-warn">From a secondary reading, not confirmed word for word</span>'
      : '<span class="v-no">Not verified</span>';
    var body =
      (s.spear_note ? '<div class="sp-note">' + esc(s.spear_note) + '</div>' : '') +
      table(s) +
      (s.srfs ? '<div class="sp-srfs">State Reef Fish Survey species: a State Reef Fish Angler designation is ' +
        'required to harvest it from a vessel in Florida waters (r. 68B-14.009).</div>' : '') +
      (window.FLLaw && s.law && s.law.length ? window.FLLaw.cite(s.law) : '') +
      (src ? '<div class="sp-srcs"><b>Sources</b><ul>' + src + '</ul></div>' : '') +
      '<div class="lw-meta">' + v + (s.checked ? ' &middot; checked ' + esc(s.checked) : '') + '</div>';
    return '<details class="lw sp-c" id="sp-' + esc(s.id) + '"' + (open ? ' open' : '') + '>' +
      '<summary><span class="lw-title">' + esc(s.name) + '</span>' +
      '<span class="lw-cite">' + (s.sci ? '<i>' + esc(s.sci) + '</i>' : '') +
      (aka.length ? (s.sci ? ' &middot; ' : '') + esc(aka.join(', ')) : '') + '</span>' +
      badge(s) + (s.srfs ? '<span class="sp-b sp-srfs-b">Reef Fish Survey</span>' : '') +
      '</summary><div class="lw-body">' + body + '</div></details>';
  }
  function match(s) {
    if (filt.spear && s.spear !== filt.spear) return false;
    if (!filt.q) return true;
    var q = norm(filt.q);
    return norm(s.name + ' ' + (s.aka || []).join(' ') + ' ' + (s.sci || '') + ' ' + (s.group || '') + ' ' +
      (s.spear_note || '')).indexOf(q) >= 0;
  }
  function renderList(openId) {
    var el = document.getElementById('sp-list');
    if (!el) return;
    if (DATA && DATA.error) { el.innerHTML = '<p class="lw-intro">' + esc(DATA.error) + '</p>'; return; }
    if (!DATA) { el.innerHTML = '<p class="lw-intro">Loading species…</p>'; return; }
    var hits = LIST.filter(match);
    var counts = { prohibited: 0, restricted: 0, allowed: 0 };
    LIST.forEach(function (s) { if (counts[s.spear] != null) counts[s.spear]++; });
    document.querySelectorAll('#spanel [data-sp]').forEach(function (b) {
      var k = b.dataset.sp;
      b.classList.toggle('on', filt.spear === k);
      b.setAttribute('aria-pressed', String(filt.spear === k));
      var em = b.querySelector('em'); if (em) em.textContent = counts[k];
    });
    el.innerHTML = hits.length ? hits.map(function (s) { return card(s, s.id === openId); }).join('')
      : '<p class="lw-intro">Nothing matches.</p>';
  }
  function head() {
    var d = DATA || {};
    var notes = (d.general_notes || []).map(function (n) { return '<li>' + esc(n) + '</li>'; }).join('');
    var defs = d.spear_def ? '<dl class="sp-defs">' + ['prohibited', 'restricted', 'allowed'].map(function (k) {
      return d.spear_def[k] ? '<dt>' + badge({ spear: k }) + '</dt><dd>' + esc(d.spear_def[k]) + '</dd>' : '';
    }).join('') + '</dl>' : '';
    var regs = d.regions_def ? '<dl class="sp-defs">' + REGIONS.map(function (r) {
      return d.regions_def[r[0]] ? '<dt>' + esc(r[1]) + '</dt><dd>' + esc(d.regions_def[r[0]]) + '</dd>' : '';
    }).join('') + '</dl>' : '';
    return '<div class="sp-disc">' + esc(d.disclaimer || 'Not legal advice.') +
      (d.version ? ' <span class="sp-ver">Compiled ' + esc(d.version) + '.</span>' : '') + '</div>' +
      '<details class="sp-more"><summary>What the labels and regions mean</summary><div>' + defs + regs +
      (notes ? '<b>Rules that apply to every species</b><ul>' + notes + '</ul>' : '') + '</div></details>';
  }

  function mount() {
    if (document.getElementById('spanel')) return;
    var el = document.createElement('div');
    el.id = 'spanel';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', 'Species rules');
    el.innerHTML =
      '<div class="lw-head"><b>Species and spear rules</b>' +
      '<button id="sp-x" title="Close" aria-label="Close">&times;</button></div>' +
      '<div id="sp-head"></div>' +
      '<input id="sp-q" type="search" placeholder="Filter by name, other name or scientific name" autocomplete="off">' +
      '<div class="sp-chips">' +
      '<button class="sp-chip" data-sp="prohibited" aria-pressed="false">Prohibited <em></em></button>' +
      '<button class="sp-chip" data-sp="restricted" aria-pressed="false">Restricted <em></em></button>' +
      '<button class="sp-chip" data-sp="allowed" aria-pressed="false">Legal gear <em></em></button></div>' +
      '<div id="sp-list"></div>';
    document.body.appendChild(el);
    el.querySelector('#sp-x').onclick = close;
    var inp = el.querySelector('#sp-q'), t = null;
    inp.oninput = function () {
      clearTimeout(t);
      t = setTimeout(function () { filt.q = inp.value.trim(); renderList(); }, 120);
    };
    el.querySelector('.sp-chips').onclick = function (e) {
      var b = e.target.closest && e.target.closest('[data-sp]');
      if (!b) return;
      filt.spear = filt.spear === b.dataset.sp ? '' : b.dataset.sp;
      renderList();
    };
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') close(); });
  }
  function open(id) {
    mount();
    var el = document.getElementById('spanel');
    if (window.FLLaw && window.FLLaw.close) window.FLLaw.close();
    el.classList.add('on');
    var btn = document.getElementById('spbtn'); if (btn) btn.classList.add('on');
    renderList(id);
    return load().then(function () {
      document.getElementById('sp-head').innerHTML = head();
      if (id) { filt.q = ''; filt.spear = ''; var inp = document.getElementById('sp-q'); if (inp) inp.value = ''; }
      renderList(id);
      if (id) {
        var c = document.getElementById('sp-' + id);
        if (c) { c.open = true; if (c.scrollIntoView) c.scrollIntoView({ block: 'center' }); c.classList.add('lw-flash');
                 setTimeout(function () { c.classList.remove('lw-flash'); }, 1400); }
      }
      return !!(id ? BYID[id] : true);
    });
  }
  function close() {
    var el = document.getElementById('spanel'); if (el) el.classList.remove('on');
    var btn = document.getElementById('spbtn'); if (btn) btn.classList.remove('on');
  }
  /* opening any citation chip brings the encyclopedia forward over this panel */
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('.cite[data-law]');
    if (b) close();
  }, true);

  function install() {
    /* the encyclopedia and this panel share the right edge: opening one closes the other */
    if (window.FLLaw && window.FLLaw.open && !window.FLLaw._spWrapped) {
      var lawOpen = window.FLLaw.open;
      window.FLLaw.open = function (id) { close(); return lawOpen(id); };
      window.FLLaw._spWrapped = true;
    }
    var b = document.getElementById('spbtn');
    if (b) b.onclick = function () {
      var el = document.getElementById('spanel');
      if (el && el.classList.contains('on')) close(); else open();
    };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install);
  else install();

  window.FLSpecies = { load: load, open: open, close: close,
    list: function () { return LIST; }, get: function (id) { return BYID[id]; } };
})();
