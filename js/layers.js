/* Bottom Truth: base maps and raster overlays.
   Load AFTER js/app.js. Owns the #base control on the map and the Layers panel.

   Sources were chosen for terms that allow a public site to load them without a key. Details,
   probe results and the rejected candidates are in the d1-layers research notes (layers.json).

     Base, one at a time      Nautical chart (NOAA NCDS), Satellite (USGS NAIP, default),
                              Satellite (Sentinel-2 2016, EOX, CC BY 4.0), Topographic (USGS),
                              Street (OpenStreetMap, ODbL).
     Keyed, hidden by default Esri World Imagery and CARTO dark need a key each. Fill KEYS below
                              to make them appear. Unkeyed hotlinking of either is not licensed.
     Overlays, off by default relief shading, bottom habitat, sea temperature, water clarity,
                              marine forecast zones, charted danger zones.

   Two service quirks carried here:
   * The NOAA Chart Display Service cache is numbered two levels below web-mercator zoom, so the
     chart base uses zoomOffset -2 (cache level 8 = map zoom 10). maxNativeZoom 16 requests level 14
     at most; deeper zoom upsamples.
   * CoastWatch ERDDAP WMS serves EPSG:4326 only. The two ERDDAP overlays pass crs L.CRS.EPSG4326 to
     L.tileLayer.wms; Leaflet then writes the 1.3.0 bbox in lat,lon order.

   A layer whose server stops returning tiles marks itself unavailable in the panel instead of
   leaving a broken map. Remote tiles never load in the offline standalone file without a network. */
(function () {
  'use strict';

  /* ------------------------------------------------------------------ keys (optional) */
  var KEYS = {
    /* ArcGIS Location Platform key: https://location.arcgis.com/ */
    arcgis: '',
    /* CARTO API key: https://carto.com/ */
    carto: ''
  };

  var NFN = 'Not for navigation.';
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  };

  /* ArcGIS dynamic export as Leaflet tiles: MapServer /export and ImageServer /exportImage.
     Fills {bbox}, {width}, {height} in the template, the way L.TileLayer.WMS builds its bbox. */
  if (!L.TileLayer.ArcGISExport) {
    L.TileLayer.ArcGISExport = L.TileLayer.extend({
      getTileUrl: function (coords) {
        var nwse = this._tileCoordsToNwSe(coords), crs = L.CRS.EPSG3857,
            nw = crs.project(nwse[0]), se = crs.project(nwse[1]), ts = this.getTileSize();
        var bbox = [nw.x, se.y, se.x, nw.y].map(function (v) { return v.toFixed(2); }).join(',');
        return this._url.replace('{bbox}', bbox).replace('{width}', ts.x).replace('{height}', ts.y);
      }
    });
    L.tileLayer.arcgisExport = function (url, opts) { return new L.TileLayer.ArcGISExport(url, opts); };
  }

  var EXPORT_Q = '?bbox={bbox}&bboxSR=3857&imageSR=3857&size={width},{height}&format=png32&transparent=true';
  var FWC = 'https://gis.myfwc.com/hosting/rest/services/Open_Data/';
  var NCEI_T = 'https://tiles.arcgis.com/tiles/C8EMgrsFcRFL6LrL/arcgis/rest/services/';
  var USGS_T = 'https://basemap.nationalmap.gov/arcgis/rest/services/';
  var ERDDAP = 'https://coastwatch.pfeg.noaa.gov/erddap/';
  var OSM_ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ODbL';
  var PD = 'US Government work, public domain (17 U.S.C. 105).';

  /* ------------------------------------------------------------------ base maps */
  var BASES = [
    { id: 'chart', label: 'Nautical chart', short: 'Chart', type: 'xyz',
      url: 'https://gis.charttools.noaa.gov/arcgis/rest/services/MarineChart_Services/NOAACharts/MapServer/tile/{z}/{y}/{x}',
      opts: { zoomOffset: -2, minZoom: 2, maxNativeZoom: 16, maxZoom: 19,
              attribution: 'NOAA Office of Coast Survey, Chart Display Service. ' + NFN },
      desc: 'NOAA raster charts with paper-chart symbols.', lic: PD },
    { id: 'sat', label: 'Satellite', short: 'Satellite', type: 'xyz',
      url: USGS_T + 'USGSImageryOnly/MapServer/tile/{z}/{y}/{x}',
      opts: { maxNativeZoom: 16, maxZoom: 19, attribution: 'Imagery: USGS The National Map, USDA NAIP' },
      desc: 'NAIP aerial imagery, about 1 m, near shore. Offshore extent varies.', lic: 'Public domain (USGS).' },
    { id: 's2', label: 'Satellite (Sentinel-2 2016)', short: 'Sentinel-2', type: 'xyz',
      url: 'https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{z}/{y}/{x}.jpg',
      opts: { maxNativeZoom: 15, maxZoom: 19,
              attribution: 'Sentinel-2 cloudless - <a href="https://s2maps.eu">https://s2maps.eu</a> by EOX IT ' +
                'Services GmbH (Contains modified Copernicus Sentinel data 2016 &amp; 2017)' },
      desc: 'Cloud-free 10 m mosaic from 2016. Shows the shelf where NAIP stops.', lic: 'CC BY 4.0.' },
    { id: 'topo', label: 'Topographic', short: 'Topo', type: 'xyz',
      url: USGS_T + 'USGSTopo/MapServer/tile/{z}/{y}/{x}',
      opts: { maxNativeZoom: 16, maxZoom: 19, attribution: 'USGS The National Map' },
      desc: 'US Topo map. Water is flat colour with no depth.', lic: 'Public domain (USGS).' },
    { id: 'street', label: 'Street', short: 'Street', type: 'xyz',
      url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      opts: { maxZoom: 19, attribution: OSM_ATTR },
      desc: 'OpenStreetMap standard tiles. Light use only under the OSM tile policy.',
      lic: 'Data ODbL; tiles under the OSM tile usage policy.' }
  ];
  if (KEYS.arcgis) BASES.push({ id: 'esri', label: 'Satellite (Esri)', short: 'Esri', type: 'xyz',
    url: 'https://basemaps-api.arcgis.com/arcgis/rest/services/styles/ArcGIS:Imagery/tiles/{z}/{y}/{x}?token=' +
      encodeURIComponent(KEYS.arcgis),
    opts: { maxZoom: 19, attribution: 'Imagery &copy; Esri, Maxar, Earthstar Geographics' },
    desc: 'Esri World Imagery through your ArcGIS key.', lic: 'Esri terms, keyed.' });
  if (KEYS.carto) BASES.push({ id: 'dark', label: 'Dark (CARTO)', short: 'Dark', type: 'xyz',
    url: 'https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?api_key=' + encodeURIComponent(KEYS.carto),
    opts: { maxZoom: 19, attribution: OSM_ATTR + ' &copy; CARTO' },
    desc: 'CARTO Dark Matter through your CARTO key.', lic: 'CARTO terms, keyed; data ODbL.' });

  /* ------------------------------------------------------------------ overlays */
  var OVERLAYS = [
    { id: 'relief', grp: 'Depth and relief', label: 'Seafloor relief hillshade', type: 'xyz',
      url: NCEI_T + 'CRM_hillshade/MapServer/tile/{z}/{y}/{x}',
      opts: { maxNativeZoom: 14, maxZoom: 19, opacity: 0.55,
              attribution: 'NOAA NCEI, Coastal Relief Model. ' + NFN },
      desc: 'Shaded depth to the shelf edge from the NCEI Coastal Relief Model, about 30 m detail.', lic: PD },
    { id: 'cudem', grp: 'Depth and relief', label: 'Nearshore relief', type: 'xyz',
      url: NCEI_T + 'CUDEM_hillshade/MapServer/tile/{z}/{y}/{x}',
      opts: { maxNativeZoom: 15, maxZoom: 19, opacity: 0.6,
              attribution: 'NOAA NCEI, Continuously Updated DEM (CUDEM). ' + NFN },
      desc: 'Finer shading for reef tracts and inlets where CUDEM exists; stops well short of the shelf edge.', lic: PD },
    { id: 'demcolor', grp: 'Depth and relief', label: 'Colour relief, deep zoom', type: 'export',
      url: 'https://gis.ngdc.noaa.gov/arcgis/rest/services/DEM_mosaics/DEM_global_mosaic_hillshade/ImageServer/exportImage' +
        '?bbox={bbox}&bboxSR=3857&imageSR=3857&size={width},{height}&format=jpgpng' +
        '&renderingRule=%7B%22rasterFunction%22%3A%22ColorHillshade%22%7D&f=image',
      opts: { minZoom: 6, maxNativeZoom: 17, maxZoom: 19, opacity: 0.6,
              attribution: 'NOAA NCEI, DEM Global Mosaic. ' + NFN },
      desc: 'Colour-shaded depth from the best available NCEI grid at each place. Drawn on request, so slower.', lic: PD },
    { id: 'gebco', grp: 'Depth and relief', label: 'GEBCO ocean relief', type: 'wms',
      url: 'https://wms.gebco.net/mapserv?',
      opts: { layers: 'GEBCO_LATEST', format: 'image/png', transparent: false, version: '1.3.0',
              minZoom: 3, maxNativeZoom: 12, maxZoom: 19, opacity: 0.6,
              attribution: 'Imagery reproduced from the GEBCO_2026 Grid, GEBCO Compilation Group (2026). ' + NFN },
      desc: 'Global 15 arc-second grid (about 450 m). Coarse; useful for the Straits and the shelf edge.',
      lic: 'Public domain. GEBCO: not for navigation or any purpose relating to safety at sea.' },
    { id: 'seagrass', grp: 'Bottom habitat', label: 'Seagrass', type: 'export',
      url: FWC + 'Seagrass_Statewide/MapServer/export' + EXPORT_Q + '&layers=show:15&f=image',
      opts: { minZoom: 9, maxZoom: 19, opacity: 0.6,
              attribution: 'FWC Fish and Wildlife Research Institute, Seagrass statewide' },
      desc: 'Statewide seagrass compilation, sources 1987 to 2025.', lic: 'FWC: available without restriction.' },
    { id: 'coral', grp: 'Bottom habitat', label: 'Coral and hardbottom, statewide', type: 'export',
      url: FWC + 'Coral_and_Hard_Bottom_Habitats_Statewide/MapServer/export' + EXPORT_Q + '&layers=show:18&f=image',
      opts: { minZoom: 8, maxZoom: 19, opacity: 0.7,
              attribution: 'FWC Fish and Wildlife Research Institute, Coral and Hard Bottom Habitats' },
      desc: 'FWC statewide compilation as of 2013. FWC notes it is not a comprehensive survey.',
      lic: 'Public domain (FWC); credit FWC as the source.' },
    { id: 'urt', grp: 'Bottom habitat', label: 'Unified Reef Tract benthic map', type: 'export',
      url: FWC + 'Unified_Florida_Reef_Tract_Benthic_Habitat/MapServer/export' + EXPORT_Q + '&layers=show:16&f=image',
      opts: { minZoom: 9, maxZoom: 19, opacity: 0.7,
              attribution: 'FWC Fish and Wildlife Research Institute and partners, Unified Florida Reef Tract Map' },
      desc: 'Benthic habitat classes from Martin County through the Keys to the Dry Tortugas.',
      lic: 'Use constraints not located in the service metadata; FWC credit given.' },
    { id: 'wfs', grp: 'Bottom habitat', label: 'West Florida Shelf benthic', type: 'export',
      url: FWC + 'West_Florida_Shelf_Benthic_Habitats/MapServer/export' + EXPORT_Q + '&layers=show:13&f=image',
      opts: { minZoom: 9, maxZoom: 19, opacity: 0.7,
              attribution: 'Brian Walker, Nova Southeastern University; FWC Fish and Wildlife Research Institute' },
      desc: 'Satellite-mapped bottom habitat on the Gulf shelf, Pinellas to Sarasota.',
      lic: 'Use constraints not checked; source credited.' },
    { id: 'sst', grp: 'Conditions', label: 'Sea surface temperature', type: 'wms', dated: 'jplMURSST41',
      url: ERDDAP + 'wms/jplMURSST41/request?',
      opts: { layers: 'jplMURSST41:analysed_sst', version: '1.3.0', crs: L.CRS.EPSG4326, format: 'image/png',
              transparent: true, bgcolor: '0x808080', styles: '', time: 'current',
              minZoom: 5, maxNativeZoom: 11, maxZoom: 19, opacity: 0.7,
              attribution: 'MUR SST: data provided by JPL under support by NASA MEaSUREs; served by NOAA CoastWatch ERDDAP' },
      desc: 'Daily 1 km analysis, one to two days behind. Colour scale is the server default.',
      lic: 'JPL PO.DAAC policy: free to use and redistribute, not intended for legal use.' },
    { id: 'kd490', grp: 'Conditions', label: 'Water clarity (Kd490)', type: 'wms', dated: 'nesdisVHNkd490Daily',
      url: ERDDAP + 'wms/nesdisVHNkd490Daily/request?',
      opts: { layers: 'nesdisVHNkd490Daily:kd_490', version: '1.3.0', crs: L.CRS.EPSG4326, format: 'image/png',
              transparent: true, bgcolor: '0x808080', styles: '', time: 'current', elevation: '0',
              minZoom: 5, maxNativeZoom: 9, maxZoom: 19, opacity: 0.7,
              attribution: 'NOAA CoastWatch, S-NPP VIIRS Kd490' },
      desc: 'Higher Kd490 means murkier water. Daily 4 km satellite pass; clouds leave gaps.',
      lic: 'Free to use and redistribute, not intended for legal use (dataset licence).' },
    { id: 'nwszones', grp: 'Conditions', label: 'NWS marine forecast zones', type: 'export',
      url: 'https://mapservices.weather.noaa.gov/static/rest/services/nws_reference_maps/nws_reference_map/MapServer/export' +
        EXPORT_Q + '&layers=show:5,6&f=image',
      opts: { minZoom: 5, maxZoom: 19, opacity: 0.8, attribution: 'NOAA National Weather Service' },
      desc: 'Coastal and offshore zone outlines, for finding the right marine forecast.', lic: PD },
    { id: 'danger', grp: 'Reference', label: 'Charted danger zones and restricted areas', type: 'xyz',
      url: 'https://coast.noaa.gov/arcgis/rest/services/OceanReports/DangerZonesAndRestrictedAreas/MapServer/tile/{z}/{y}/{x}',
      opts: { maxNativeZoom: 15, maxZoom: 19, opacity: 0.7,
              attribution: 'MarineCadastre.gov (NOAA and BOEM), 33 CFR 334 as of July 2022. ' + NFN },
      desc: 'Reference, current as of 2022. The legal layers on this map are drawn from the regulation text.',
      lic: 'Federal data, for coastal and ocean planning.' }
  ];

  function make(def) {
    var o = L.extend({}, def.opts);
    if (def.type === 'wms') return L.tileLayer.wms(def.url, o);
    if (def.type === 'export') return L.tileLayer.arcgisExport(def.url, o);
    return L.tileLayer(def.url, o);
  }

  /* ------------------------------------------------------------------ tile health */
  function watch(def, onBad) {
    def.ok = 0; def.err = 0; def.bad = false;
    def.layer.on('tileload', function () { def.ok++; });
    def.layer.on('tileerror', function () {
      def.err++;
      if (def.bad) return;
      /* An <img> error carries no status code, so a server that is down and a tile outside the
         layer's coverage look the same. Trip only on a full first screen of failures, or on a
         sustained failure rate; the panel offers Retry either way. */
      if ((def.ok === 0 && def.err >= 16) || (def.err >= 60 && def.err > def.ok * 6)) {
        def.bad = true;
        console.warn('[layers] ' + def.label + ': tiles are failing (' + def.err + ' errors, ' + def.ok + ' loaded)');
        onBad(def);
      }
    });
  }
  function resetHealth(def) { def.ok = 0; def.err = 0; def.bad = false; }

  /* ------------------------------------------------------------------ install */
  var cur = null, panel = null, ctl = null;

  function fmtDay(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || '');
    if (!m) return '';
    var mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][+m[2] - 1];
    return (+m[3]) + ' ' + mon + ' ' + m[1];
  }
  /* ask ERDDAP for the last time step, then pin the WMS request to it so the label matches */
  function fetchDate(def) {
    if (def.dateAsked) return;
    def.dateAsked = true;
    def.dateText = 'checking date…';
    renderPanel();
    fetch(ERDDAP + 'griddap/' + def.dated + '.json?time%5B(last)%5D').then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (j) {
      var t = j && j.table && j.table.rows && j.table.rows[0] && j.table.rows[0][0];
      if (!t) throw new Error('no time');
      def.dateText = 'Showing ' + fmtDay(t) + ' (latest available)';
      if (def.layer.setParams) def.layer.setParams({ time: t });
    }).catch(function () {
      def.dateText = 'Showing the latest available day; the server did not report the date';
    }).then(renderPanel);
  }

  function setBase(id) {
    var b = BASES.filter(function (x) { return x.id === id; })[0];
    if (!b) return false;
    if (cur && cur !== b && map.hasLayer(cur.layer)) map.removeLayer(cur.layer);
    cur = b;
    if (b.bad) resetHealth(b);
    if (!map.hasLayer(b.layer)) b.layer.addTo(map);
    b.layer.bringToBack();
    Array.prototype.forEach.call(ctl.querySelectorAll('[data-b]'), function (x) {
      x.classList.toggle('on', x.dataset.b === id);
    });
    renderPanel();
    return true;
  }
  function setOverlay(id, on) {
    var d = OVERLAYS.filter(function (x) { return x.id === id; })[0];
    if (!d) return false;
    d.on = !!on;
    if (d.on) {
      if (d.bad) resetHealth(d);
      if (!map.hasLayer(d.layer)) d.layer.addTo(map);
      if (d.dated) fetchDate(d);
    } else if (map.hasLayer(d.layer)) map.removeLayer(d.layer);
    renderPanel();
    return true;
  }

  function baseRow(b) {
    return '<label class="lp-row lp-base' + (cur === b ? ' on' : '') + '">' +
      '<input type="radio" name="lp-base" value="' + b.id + '"' + (cur === b ? ' checked' : '') + '>' +
      '<span class="lp-t"><b>' + esc(b.label) + '</b>' +
      '<span class="lp-d">' + esc(b.desc) + '</span>' +
      '<span class="lp-l">Licence: ' + esc(b.lic) + '</span>' +
      (b.bad ? '<span class="lp-bad">Unavailable: no tiles loaded from this server. Pick another base.</span>' : '') +
      '</span></label>';
  }
  function ovRow(d) {
    var z = map.getZoom(), minZ = d.opts.minZoom;
    var note = '';
    if (d.bad) note = '<span class="lp-bad">Unavailable: no tiles loaded. The server may be down, or it ' +
      'has no data for this area. ' +
      '<button class="lp-retry" data-retry="' + d.id + '">Retry</button></span>';
    else if (d.on && minZ != null && z < minZ) note = '<span class="lp-z">Zoom in to level ' + minZ + ' to see this layer.</span>';
    return '<div class="lp-row lp-ov' + (d.on ? ' on' : '') + (d.bad ? ' bad' : '') + '">' +
      '<label class="lp-ck"><input type="checkbox" data-ov="' + d.id + '"' + (d.on ? ' checked' : '') + '>' +
      '<b>' + esc(d.label) + '</b></label>' +
      '<span class="lp-d">' + esc(d.desc) + '</span>' +
      (d.on && d.dateText ? '<span class="lp-date">' + esc(d.dateText) + '</span>' : '') +
      (d.on ? '<span class="lp-op"><span>Opacity</span><input type="range" min="0.1" max="1" step="0.05" value="' +
        d.layer.options.opacity + '" data-op="' + d.id + '" aria-label="Opacity of ' + esc(d.label) + '"></span>' : '') +
      '<span class="lp-l">Licence: ' + esc(d.lic) + '</span>' +
      '<span class="lp-a">Source: ' + d.opts.attribution + '</span>' + note + '</div>';
  }
  function renderPanel() {
    if (!panel) return;
    var st = panel.querySelector('.lp-body');
    var top = st ? st.scrollTop : 0;
    var groups = [];
    OVERLAYS.forEach(function (d) { if (groups.indexOf(d.grp) < 0) groups.push(d.grp); });
    panel.innerHTML =
      '<div class="lp-head"><b>Map layers</b><button class="lp-x" title="Close" aria-label="Close">&times;</button></div>' +
      '<div class="lp-body">' +
      '<div class="lp-grp">Base map</div>' + BASES.map(baseRow).join('') +
      groups.map(function (g) {
        return '<div class="lp-grp">' + esc(g) + '</div>' +
          OVERLAYS.filter(function (d) { return d.grp === g; }).map(ovRow).join('');
      }).join('') +
      '<div class="lp-foot">Charts, relief and habitat layers are reference pictures from their publishers. ' +
      'None of them is a legal boundary. ' + NFN + '</div></div>';
    var body = panel.querySelector('.lp-body');
    if (body) body.scrollTop = top;
  }
  function togglePanel(force) {
    var on = force == null ? !panel.classList.contains('on') : !!force;
    panel.classList.toggle('on', on);
    var b = ctl.querySelector('[data-lp]');
    if (b) { b.classList.toggle('on', on); b.setAttribute('aria-expanded', String(on)); }
    if (on) renderPanel();
  }

  function install() {
    ctl = document.getElementById('base');
    BASES.forEach(function (b) {
      b.layer = make(b);
      watch(b, function () { renderPanel(); var x = ctl.querySelector('[data-b="' + b.id + '"]'); if (x) x.classList.add('bad'); });
    });
    OVERLAYS.forEach(function (d) {
      d.layer = make(d); d.on = false;
      watch(d, function () { if (map.hasLayer(d.layer)) map.removeLayer(d.layer); d.on = false; renderPanel(); });
    });

    ctl.innerHTML = BASES.map(function (b) {
      return '<button class="b-btn" data-b="' + b.id + '" title="' + esc(b.label + '. ' + b.desc) + '">' + esc(b.short) + '</button>';
    }).join('') + '<button class="b-lp" data-lp="1" aria-expanded="false" title="Base maps and overlays">Layers</button>';
    ctl.onclick = function (e) {
      var t = e.target.closest ? e.target.closest('button') : e.target;
      if (!t) return;
      if (t.dataset.lp) { togglePanel(); return; }
      if (t.dataset.b) setBase(t.dataset.b);
    };

    panel = document.createElement('div');
    panel.id = 'layerpanel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Map layers');
    ctl.parentNode.insertBefore(panel, ctl.nextSibling);
    [ctl, panel].forEach(function (el) {
      L.DomEvent.disableClickPropagation(el);
      L.DomEvent.disableScrollPropagation(el);
    });
    panel.addEventListener('change', function (e) {
      var t = e.target;
      if (t.name === 'lp-base') setBase(t.value);
      else if (t.dataset.ov) setOverlay(t.dataset.ov, t.checked);
    });
    panel.addEventListener('input', function (e) {
      var t = e.target;
      if (!t.dataset.op) return;
      var d = OVERLAYS.filter(function (x) { return x.id === t.dataset.op; })[0];
      if (d) d.layer.setOpacity(+t.value);
    });
    panel.addEventListener('click', function (e) {
      var t = e.target;
      if (t.classList.contains('lp-x')) { togglePanel(false); return; }
      if (t.dataset.retry) {
        var d = OVERLAYS.filter(function (x) { return x.id === t.dataset.retry; })[0];
        if (d) { resetHealth(d); setOverlay(d.id, true); d.layer.redraw(); }
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('on')) togglePanel(false);
    });
    map.on('zoomend', function () { if (panel.classList.contains('on')) renderPanel(); });

    var q = new URLSearchParams(location.search);
    var want = q.get('base');
    if (!want || !setBase(want)) setBase('sat');
    renderPanel();

    window.FLLayers = {
      bases: function () { return BASES.map(function (b) { return { id: b.id, label: b.label, on: cur === b, unavailable: !!b.bad }; }); },
      overlays: function () { return OVERLAYS.map(function (d) { return { id: d.id, label: d.label, on: !!d.on, unavailable: !!d.bad }; }); },
      setBase: setBase,
      setOverlay: setOverlay,
      /* the Leaflet layer behind a base or overlay id, for scripting and tests */
      layer: function (id) {
        var d = BASES.concat(OVERLAYS).filter(function (x) { return x.id === id; })[0];
        return d ? d.layer : null;
      },
      open: function () { togglePanel(true); },
      close: function () { togglePanel(false); }
    };
  }

  function ready() { return typeof map !== 'undefined' && map && document.getElementById('base'); }
  function start() {
    if (ready()) { install(); return; }
    document.addEventListener('flmap:ready', function once() {
      document.removeEventListener('flmap:ready', once);
      install();
    });
  }
  start();
})();
