# -*- coding: utf-8 -*-
"""Build data/zones-local.json: real geometry for local / park / federal rules."""
import json, io, math, os
U=os.environ.get('ZONES_LOCAL_RAW', 'raw/2026-08-22/')  # August inputs, not kept in the repository
G=json.load(open(U+'spear-geo-batch1.json'))
O=json.load(open(U+'spear-osm-batch2.json'))
R=5   # decimal places ~1.1 m

def rings_from(geom):
    """GeoJSON geometry -> list of [[lat,lon],...] rings (outer rings only)."""
    t=geom['type']; c=geom['coordinates']
    out=[]
    if t=='Polygon': out.append(c[0])
    elif t=='MultiPolygon':
        for p in c: out.append(p[0])
    elif t=='LineString': out.append(c)
    elif t=='MultiLineString': out.extend(c)
    return [[[round(y,R),round(x,R)] for x,y in ring] for ring in out]

def dp(pts, tol):
    """Douglas-Peucker on [lat,lon]."""
    if len(pts)<3: return pts
    def d(p,a,b):
        (y0,x0),(y1,x1),(y2,x2)=p,a,b
        dx,dy=x2-x1,y2-y1
        if dx==0 and dy==0: return math.hypot(x0-x1,y0-y1)
        t=max(0,min(1,((x0-x1)*dx+(y0-y1)*dy)/(dx*dx+dy*dy)))
        return math.hypot(x0-(x1+t*dx), y0-(y1+t*dy))
    a,b=pts[0],pts[-1]; mi,md=0,0.0
    for i in range(1,len(pts)-1):
        dd=d(pts[i],a,b)
        if dd>md: mi,md=i,dd
    if md>tol:
        return dp(pts[:mi+1],tol)[:-1]+dp(pts[mi:],tol)
    return [a,b]

def simp(rings, tol=0.00008):
    out=[]
    for r in rings:
        s=dp(r,tol)
        if len(s)>=4 or (len(s)>=2 and len(r)<4): out.append(s)
    return out

# ---- lookups ----
places={f['properties']['BASENAME']: f['geometry'] for f in G['places']['features']}
counties={f['properties']['NAME']: f['geometry'] for f in G['counties']['features']}
nps={f['properties']['UNIT_CODE']: f['geometry'] for f in G['nps']['features']}
chans={f['properties']['sdsfeaturename']: f['geometry'] for f in G['channels']['features']}

Z=[]
def add(**k):
    k.setdefault('flag', None); k.setdefault('kind','closed')
    Z.append(k)

M_PER_DEG = 111320.0
def circ(lat,lon,r_m,a0=0,a1=360,n=48):
    pts=[]
    for i in range(n+1):
        a=math.radians(a0+(a1-a0)*i/n)
        dlat=(r_m*math.cos(a))/M_PER_DEG
        dlon=(r_m*math.sin(a))/(M_PER_DEG*math.cos(math.radians(lat)))
        pts.append([round(lat+dlat,R), round(lon+dlon,R)])
    return pts
def sector(lat,lon,r_m,a0,a1):
    return [[round(lat,R),round(lon,R)]]+circ(lat,lon,r_m,a0,a1)+[[round(lat,R),round(lon,R)]]

# ============ 1. St. Pete Beach — § 54-4, citywide ============
add(id='spb54', n='St. Pete Beach: speargun discharge banned citywide',
    law=['spb-54-4','fs-790-33'], cat='local',
    r=simp(rings_from(places['St. Pete Beach'])),
    s='Discharging any spear or harpoon from a spring gun, mechanic gun, power gun or any mechanic '
      'device is unlawful <b>anywhere in the corporate limits</b>: land or water. Pole spears and '
      'Hawaiian slings arguably fall outside "mechanic device"; that has never been tested.',
    src='Boundary: US Census TIGER 2025 Incorporated Places, layer 4.',
    flag='The city limits shown are the TIGER municipal boundary, which includes the water parcels '
         'the city claims. How far St. Pete Beach’s police power actually reaches into the Gulf '
         'is unresolved: Florida municipalities generally have jurisdiction only to their '
         'charter boundary, and sovereign submerged lands beyond it are state water. Treat the '
         'offshore edge of this polygon as soft.')

# ============ 2. St. Pete Beach — § 94-1 Blind Pass ============
# AUDITED 22 Aug 2026 against Esri satellite imagery. An earlier rectangle drawn from the
# OpenStreetMap 75th Avenue bearing landed in the open Gulf, nowhere near Blind Pass. Removed.
# What is certain: the 75th Avenue / Blind Pass Road intersection at 27.743229 N, 82.749825 W
# (OpenStreetMap). Everything else about this zone's geometry is unresolved.
add(id='spb94', n='St. Pete Beach: Blind Pass, no swimming or skin diving',
    law=['spb-94-1'], cat='local', kind='warn',
    r=[circ(27.743229,-82.749825,150)],
    s='No person shall swim, skin dive or wade in the waters of Blind Pass within the city limits '
      '<b>lying south of an extension of the centerline of 75th Avenue</b>. § 94-1(2) separately '
      'closes Gulf and Boca Ciega waters off Pass-a-Grille between two points 150 ft north of the '
      'south boundary of First Avenue. § 94-2 bans diving or jumping from any public bridge.',
    src='Marker only: the 75th Avenue / Blind Pass Road intersection, from OpenStreetMap.',
    flag='GEOMETRY NOT MAPPED: this is a 150 m marker circle on a street intersection, NOT the '
         'closure. Three separate problems. (1) The ordinance\u2019s northern edge is "an extension '
         'of the centerline of 75th Avenue", a line the city never surveyed and no dataset carries. '
         '(2) OpenStreetMap has no water feature named Blind Pass anywhere near here: only Blind '
         'Pass ROAD: so the extent of "the waters of Blind Pass" is itself unresolved; the named '
         'inlet sits about 1.3 km NORTH of 75th Avenue, which makes "south of 75th Avenue" read as '
         'the back-bay channel rather than the inlet. (3) The § 94-1(2) Pass-a-Grille zone is not '
         'drawn at all. Resolving this needs the city plat or a call to St. Pete Beach.')

# ============ 3. Treasure Island — § 58-34 John's Pass ============
tipts=[]
for e in O['ti127']['elements']:
    if e.get('geometry'): tipts += [(p['lat'],p['lon']) for p in e['geometry']]
tw=min(tipts,key=lambda p:p[1]); te=max(tipts,key=lambda p:p[1])
FT=0.3048; D=1500*FT
# John's Pass corridor — HAND-DIGITISED from Esri satellite imagery 22 Aug 2026 and visually
# verified to sit on the channel. The OpenStreetMap "river" ways for John's Pass chain together
# into a line that runs across the Madeira Beach spit and a kilometre out into the Gulf; a corridor
# built on them landed on dry land. These vertices were read off the imagery instead.
jp_poly=[[[27.78016,-82.78741],[27.78126,-82.78598],[27.78236,-82.78439],[27.78349,-82.78288],
          [27.78465,-82.78157],[27.78603,-82.7803],[27.78739,-82.77921],[27.78605,-82.77705],
          [27.78461,-82.7782],[27.78309,-82.77961],[27.78177,-82.7811],[27.78054,-82.78273],
          [27.77946,-82.7843],[27.7784,-82.78567],[27.78016,-82.78741]]]

add(id='ti58', n="Treasure Island: John's Pass spearfishing ban",
    law=['ti-58-34'], cat='local',
    r=[sector(tw[0],tw[1],D,180,360), sector(te[0],te[1],D,0,180)] + jp_poly,
    line=[],
    s='Unlawful to swim, dive, jump in, bathe, float or engage in <b>spearfishing or skin diving</b> '
      'in the waters commonly known as John’s Pass, and in the Gulf <b>1,500 ft west</b> of the '
      'mean high water mark at the western termination of 127th Avenue, and in Boca Ciega Bay '
      '<b>1,500 ft east</b> of the eastern termination. § 58-34(b) also bans jumping, diving or '
      'swimming from any bridge or catwalk citywide.',
    src='127th Avenue termini from OpenStreetMap, verified against Esri satellite imagery: the western '
        'end sits on the Gulf beach and the eastern end at the bridge approach, both inside the '
        'Treasure Island city limits (checked by point-in-polygon against TIGER). 1,500 ft = 457.2 m, '
        'drawn as half-discs. John’s Pass drawn as a 260 m corridor on the OpenStreetMap channel '
        'centreline, clipped to the inlet throat.',
    flag='THE ORDINANCE HAS NO LATERAL LIMIT. It gives a distance out from two points but never says '
         'how wide the zone is. Half-discs of 1,500 ft radius are drawn here as the conservative '
         'reading: they cover every interpretation. A narrow reading would be a corridor only '
         'as wide as 127th Avenue. Also: OpenStreetMap’s 127th Avenue does not reach the Gulf '
         'beach, so the western terminus used here is the end of the mapped street, not the mean '
         'high water mark. Both need a plat or a site visit.')

# ============ 4. Sarasota County — marked navigable channels ============
add(id='sar130', n='Sarasota County: no diving or spearfishing in marked channels',
    law=['sarasota-130-33'], cat='local',
    r=simp(rings_from(chans['GIWW CAL TO ANC (SARASOTA COUNTY)']),0.00004),
    s='Unlawful to skin dive, scuba dive or spearfish <b>within the bounds of any marked navigable '
      'channel</b> in Sarasota County without permission from a law-enforcement agency, obtained by '
      'showing some necessity for diving in the channel. Amended by Ord. 2025-043, effective '
      '1 Jan 2026.',
    src='Geometry: USACE National Channel Framework, ChannelArea polygons, GIWW Caloosahatchee to '
        'Anclote (Sarasota County reach).',
    flag='UNDER-INCLUSIVE. The polygon drawn is the FEDERAL project channel only. The ordinance says '
         '"any marked navigable channel", which also catches locally marked channels: New Pass, '
         'Big Pass, Venice Inlet approaches, and marked residential and marina channels that USACE '
         'does not maintain and no single dataset publishes. Assume more channel is closed than is '
         'drawn here.')

# ============ 5. Monroe canals — real OSM canal geometry ============
canal_lines=[]
for e in O['canals']['elements']:
    g=e.get('geometry')
    if not g or len(g)<2: continue
    pts=[[round(p['lat'],R),round(p['lon'],R)] for p in g]
    mla=sum(q[0] for q in pts)/len(pts); mlo=sum(q[1] for q in pts)/len(pts)
    if not (24.53 <= mla <= 24.80 and -81.85 <= mlo <= -80.90): continue
    if len(pts)>=2 and max(abs(pts[0][0]-pts[-1][0]),abs(pts[0][1]-pts[-1][1]))>0.05: continue
    canal_lines.append(dp(pts,0.00004))
add(id='mon26', n='Lower Keys: speargun discharge banned in manmade canals',
    law=['monroe-26-5','marathon-canal','fs-379-2425'], cat='local', kind='line',
    r=[], line=canal_lines,
    s='Unlawful to use, fire or discharge a speargun <b>on or below the surface of any manmade '
      'canal</b> in unincorporated Monroe County. The § 26-1 definition catches any device that '
      'can propel a projectile more than <b>24 inches</b>: pole spears and Hawaiian slings '
      'included: regardless of power source. Conviction forfeits the gun to the Sheriff for '
      'destruction.',
    src='Canal centrelines from OpenStreetMap (waterway=canal / water=canal), Lower Keys only '
        '(24.53–24.80 N, 81.85–80.85 W).',
    flag='PARTIAL COVERAGE, and drawn as centrelines rather than water polygons. OpenStreetMap canal '
         'coverage in the Keys is good but not complete, and this pull covers the LOWER Keys only: '
         'the stretch that matters, because everything above Long Key is already closed by '
         'Fla. Stat. § 379.2425. Canals inside the City of Marathon are also covered by the ban '
         'per the Monroe State Attorney, but Marathon’s own code section has not been located. '
         'Absence of a line here does NOT mean a canal is open.')

# ============ 6. Layton ============
add(id='lay50', n='Layton: lobster and stone crab sanctuary (all city waters)',
    law=['layton-50-1','fs-379-2425'], cat='local', kind='warn',
    r=simp(rings_from(places['Layton'])),
    s='No person shall remove <b>by any means: trap, diving, spearing or otherwise: </b> any '
      'Florida spiny lobster or stone crab from any waters within the Layton city limits. '
      '$25–$250 per offence, per day. <b>Finfish spearfishing is not addressed by this '
      'ordinance</b>, but all of Layton sits inside the § 379.2425 Upper Keys closure, where '
      'spearfishing is prohibited outright.',
    src='Boundary: US Census TIGER 2025 Incorporated Places.')

# ============ 7. Key Colony Beach ============
add(id='kcb5', n='Key Colony Beach: seasonal diving and snorkeling closure',
    law=['kcb-5-11','fs-379-2425'], cat='local', kind='warn',
    r=simp(rings_from(places['Key Colony Beach'])),
    s='During the lobster window: 4 days before mini-season through 10 days after the commercial '
      'season opens: diving or snorkeling in any navigable canal, marina, or <b>within 300 ft of '
      'an improved residential or commercial shoreline</b> is a public nuisance. $250 per violation. '
      'Diving incidental to vessel or dock maintenance is exempt with a diver-down flag displayed. '
      '<b>This is not a spearfishing rule</b>: and Key Colony Beach is inside the § 379.2425 '
      'Upper Keys closure regardless.',
    src='Boundary: US Census TIGER 2025 Incorporated Places.',
    flag='The 300 ft "improved shoreline" buffer is NOT drawn: no dataset distinguishes improved '
         'from unimproved shoreline. The whole city polygon is shown instead, which over-states the '
         'closure inland and under-states nothing.')

# ============ 8. Presidential Security Zone — 33 CFR 165.785 ============
dms=lambda d,m,s: d+m/60+s/3600
PSZ={
 'Center':[(dms(26,41,21),-dms(80,2,39)),(dms(26,41,21),-dms(80,2,13)),
           (dms(26,39,58),-dms(80,2,20)),(dms(26,39,58),-dms(80,2,38))],
 'West':  [(dms(26,41,21),-dms(80,2,39)),(dms(26,41,21),-dms(80,3,0)),
           (dms(26,39,58),-dms(80,2,55)),(dms(26,39,58),-dms(80,2,38))],
 'East':  [(dms(26,41,21),-dms(80,2,1)),(dms(26,39,57),-dms(80,2,9)),
           (dms(26,39,57),-dms(80,1,36)),(dms(26,41,22),-dms(80,1,29))]}
notes={'Center':'Entry prohibited without Captain of the Port Miami authorization.',
       'West':'Transit permitted with escort, at steady speed. No stopping.',
       'East':'Transit at steady speed; notification required if you stop.'}
for k,v in PSZ.items():
    ring=[[round(a,R),round(b,R)] for a,b in v]; ring.append(ring[0])
    add(id='psz'+k.lower(), n='Presidential Security Zone: %s Zone, Palm Beach' % k,
        law=['cfr-33-165-785','cfr-33-165-760'], cat='fed', r=[ring],
        s=notes[k]+' Enforced when the President, First Family or other Secret Service protectees '
          'are present or expected. COTP Miami (305) 535-4472, VHF 16.',
        src='Coordinates verbatim from 33 C.F.R. § 165.785.')

# ============ 9. National parks ============
PARKS={'DRTO':('Dry Tortugas National Park', ['cfr-36-7-27','cfr-922-164-d'],
        'Spearfishing prohibited by every gear name: pole spear, Hawaiian sling, rubber, '
        'pneumatic and spring guns, air rifles, bows, powerheads. <b>Hook-and-line only.</b> '
        '36 C.F.R. § 7.27(b)(4)(ii). Park-wide recreational vessel permit required.', 'closed'),
 'EVER':('Everglades National Park', ['cfr-36-7-45'],
        'Effectively a spearfishing ban: 36 C.F.R. § 7.45(d)(6) allows <b>only a closely attended '
        'hook and line</b>, and a spear is not on the permitted-gear list. Waters near Royal Palm '
        'and Shark Valley are closed to fishing entirely.', 'closed'),
 'BISC':('Biscayne National Park: closures inside the park', ['bnp-status','cfr-36-2-3'],
        'Contrary to common belief there is no federal spearfishing ban here. No 36 C.F.R. part 7 '
        'section exists for this park, so § 2.3(e) sends you to state law. The 2015 General '
        'Management Plan marine reserve zone was <b>never implemented</b> as a spearfishing closure. '
        'Six small named harbours and basins are closed to all fishing, and <b>Legare Anchorage is '
        'closed to scuba, snorkeling and swimming</b>.', 'open'),
 'CANA':('Canaveral National Seashore', ['fac-68b-3-008','fac-68b-20-003-1'],
        'No federal spearfishing rule. NPS defers to Florida law. On the Mosquito Lagoon side the '
        'binding constraint is the <b>Volusia County inland-salt-waters rule</b>: flounder and '
        'sheepshead only, barbed spear of three prongs or fewer.', 'warn'),
 'BICY':('Big Cypress National Preserve', ['cfr-36-2-3'],
        'Fresh water. Spearing marine species while diving in fresh water is prohibited by '
        'r. 68B-4.012 regardless.', 'warn'),
 'GUIS':('Gulf Islands National Seashore', ['cfr-36-2-3'],
        'No fishing provisions in 36 C.F.R. § 7.12, so § 2.3(e) sends you to state law. The '
        'Superintendent’s Compendium has not been read.', 'warn')}
for code,(name,law,txt,kind) in PARKS.items():
    if code not in nps: continue
    _r=[x for x in simp(rings_from(nps[code]),0.0002) if len(x)>=5]
    if code=='GUIS':
        _r=[x for x in _r if min(p[1] for p in x) > -87.65]     # Florida units only
    if code=='DRTO':
        _r=[x for x in _r if min(p[1] for p in x) < -82.0]      # drop a stray outlying tract
    add(id='nps'+code.lower(), n=name, law=law, cat='fed', kind=kind,
        r=_r, s=txt,
        src='Boundary: NPS Land Resources Division Boundary service, UNIT_CODE=%s.'%code,
        flag=('Legare Anchorage: closed to scuba, snorkeling, swimming and underwater viewing '
              'devices by the Superintendent’s Compendium approved 17 Sep 2025: is NOT '
              'drawn. Its coordinates have not been obtained. It sits offshore of the park’s '
              'northeast reef tract.') if code=='BISC' else
             ('The Superintendent’s Compendium for this unit has not been read. There may be '
              'closures not shown.') if code=='GUIS' else None)

# ============ 10. Volusia inland salt waters ============
add(id='vol', n='Volusia County: inland salt waters, spearing restricted',
    law=['fac-68b-3-008'], cat='local', kind='warn',
    r=[], line=[dp(r,0.00006) for r in rings_from(chans['IWW JAX TO MIA (VOLUSIA COUNTY)'])],
    s='Spearing is prohibited in Volusia County’s inland salt waters <b>except legal-size '
      'flounder and sheepshead</b>, and only with a barbed spear of <b>three prongs or fewer</b>. '
      'Fla. Admin. Code r. 68B-3.008(3)(a). This covers the Halifax River and Mosquito Lagoon '
      'systems: including the lagoon side of Canaveral National Seashore.',
    src='Drawn as the Intracoastal Waterway channel through Volusia County (USACE National Channel '
        'Framework) as a positional spine only.',
    flag='THE BOUNDARY IS UNDEFINED IN LAW. Rule 68B-3.008 never defines "inland salt waters" of '
         'Volusia County, and FWC publishes no boundary. What is drawn is the ICW channel as a '
         'landmark, NOT the extent of the rule. Treat the ENTIRE Halifax River / Mosquito Lagoon '
         'system, and every connected tidal creek, as covered. This is one of the two worst '
         'unmapped-boundary problems in the dataset.')

# ============ 11. Three Sisters / Kings Bay ============
add(id='3sis', n='Three Sisters Springs: scuba and spearfishing prohibited (seasonal)',
    law=['cfr-50-17-108'], cat='fed',
    r=[circ(28.89098,-82.58931,200)],
    s='Within the Kings Bay Manatee Refuge, <b>scuba diving and fishing including by spear are '
      'prohibited 15 November – 31 March</b>, and all waterborne activity is barred sunset to '
      'sunrise over the same dates. 50 C.F.R. § 17.108(c)(14)(ii)(A). Year-round: no chasing, '
      'no touching a resting or feeding manatee, no diving from the surface onto one.',
    src='200 m circle centred on the Three Sisters Springs pool at 28.89098 N, 82.58931 W: position '
        'read off Esri satellite imagery 22 Aug 2026.',
    flag='CORRECTED 22 Aug 2026: the previous centre was 350 m south of the springs, over a residential street. APPROXIMATE CIRCLE. USFWS publishes no GIS layer for the Kings Bay Manatee Refuge or the '
         'Three Sisters area: the boundary exists only as Federal Register text (77 FR 15617). '
         'The wider refuge is "all waters of Kings Bay, including all tributaries and adjoining '
         'waterbodies, upstream of the confluence of Kings Bay and Crystal River", which is far '
         'larger than the circle drawn.')

data={'version':'2026-08-22','zones':Z}
io.open('data/zones-local.json','w',encoding='utf-8').write(json.dumps(data,ensure_ascii=False,separators=(',',':')))
print('zones:',len(Z),'bytes:',os.path.getsize('data/zones-local.json'))
for z in Z:
    nr=sum(len(r) for r in z.get('r',[])); nl=sum(len(l) for l in z.get('line',[]))
    print('  %-10s %-58s rings=%d/%dpts lines=%d/%dpts %s'%(z['id'],z['n'][:58],len(z.get('r',[])),nr,len(z.get('line',[])),nl,'FLAG' if z['flag'] else ''))
