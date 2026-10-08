"""Build data/zones-palmbeach.json: Palm Beach County refuges, buffers and boundary lines.

Two sources for the shoreline and the structures, chosen with the first argument (default "enc"):

  enc  NOAA ENC harbour-band geometry, tools/geometry/2026-10-07/enc-palmbeach.json (CC0), made by
       tools/extract-enc-2026-10-07.py. Coastline (COALNE), jetty rip rap and groin (SLCONS), Blue Heron
       Bridge spans (BRIDGE areas), Peanut Island east shore. Writes data/zones-palmbeach.json and
       tools/geometry/2026-10-07/shoreline-used-palmbeach.json (read by tools/recompute-sites-ref-2026-10-07.py).
  osm  The August 2026 build: OpenStreetMap coastline from shoreline_atlantic.json in the current
       directory (not kept in the repository), OSM breakwater and bridge points. Writes zones.json and
       shoreline_used.json in the current directory, with the same content the ODbL file held before 7 Oct 2026
       (it was saved compact, without ASCII escapes).

    python3 tools/build-zones-palmbeach.py            # enc
    python3 tools/build-zones-palmbeach.py osm        # the old OpenStreetMap build, for comparison
"""
import json, math, os, sys
FT=1/6076.115; YD=3*FT
def lpn(lat): return 1.0/(60.0*math.cos(math.radians(lat)))

SRC=(sys.argv[1] if len(sys.argv)>1 else "enc").lower()
assert SRC in ("enc","osm"), "source must be enc or osm"
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
GEO=os.path.join(ROOT,"tools","geometry","2026-10-07")

# Bridge the inlet gap: between the chart-verified jetty roots the extraction wanders inside the inlet.
GAP=(26.7706,26.7742)
ROOT_S=(26.771415,-80.034414); ROOT_N=(26.773489,-80.031564)
if SRC=="osm":
    RAW=json.load(open("shoreline_atlantic.json"))
    shore=[p for p in RAW if not (GAP[0] <= p[0] <= GAP[1])]
    shore += [[26.7706,-80.03330],[ROOT_S[0],ROOT_S[1]],[ROOT_N[0],ROOT_N[1]],[26.7742,-80.03120]]
else:
    ENC=json.load(open(os.path.join(GEO,"enc-palmbeach.json")))
    RAW=ENC["shoreline"]["pts"]
    # Only the two chart-verified jetty roots bridge the gap. The OSM build also added two hand points
    # (26.7706 N and 26.7742 N); on NAIP imagery the first sits in the water off the south jetty root.
    shore=[p for p in RAW if not (GAP[0] <= p[0] <= GAP[1])]
    shore += [[ROOT_S[0],ROOT_S[1]],[ROOT_N[0],ROOT_N[1]]]
shore.sort()
print("shoreline pts:", len(shore), "range", shore[0][0], shore[-1][0])

def shore_lon(lat):
    if lat<=shore[0][0]: return shore[0][1]
    if lat>=shore[-1][0]: return shore[-1][1]
    lo,hi=0,len(shore)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if shore[m][0]<=lat: lo=m
        else: hi=m
    a,b=shore[lo],shore[hi]
    t=0 if b[0]==a[0] else (lat-a[0])/(b[0]-a[0])
    return a[1]+t*(b[1]-a[1])

def band(s,n,inner_nm,outer_nm,step=0.0004):
    lats=[s+i*step for i in range(int((n-s)/step)+1)]
    if lats[-1]<n: lats.append(n)
    west=[[la, shore_lon(la)+inner_nm*lpn(la)] for la in lats]
    east=[[la, shore_lon(la)+outer_nm*lpn(la)] for la in lats]
    return west+east[::-1]+[west[0]]

def buf_line(pts, nm, n=20):
    dense=[]
    for a,b in zip(pts,pts[1:]):
        for i in range(25): t=i/24; dense.append((a[0]+t*(b[0]-a[0]), a[1]+t*(b[1]-a[1])))
    dense.append(tuple(pts[-1]))
    cand=[]
    for (lat,lon) in dense:
        for k in range(n):
            th=2*math.pi*k/n
            cand.append((lat+nm*math.cos(th)/60.0, lon+nm*math.sin(th)*lpn(lat)))
    lat0=sum(p[0] for p in dense)/len(dense)
    proj=[(p[1]/lpn(lat0), p[0]*60) for p in cand]
    idx=sorted(range(len(proj)), key=lambda i:(proj[i][0],proj[i][1]))
    def cr(o,a,b): return (proj[a][0]-proj[o][0])*(proj[b][1]-proj[o][1])-(proj[a][1]-proj[o][1])*(proj[b][0]-proj[o][0])
    lo=[]
    for i in idx:
        while len(lo)>=2 and cr(lo[-2],lo[-1],i)<=0: lo.pop()
        lo.append(i)
    up=[]
    for i in reversed(idx):
        while len(up)>=2 and cr(up[-2],up[-1],i)<=0: up.pop()
        up.append(i)
    ring=[[cand[i][0],cand[i][1]] for i in lo[:-1]+up[:-1]]
    ring.append(ring[0]); return ring

def circle(lat,lon,nm,n=40):
    return [[lat+nm*math.cos(2*math.pi*k/n)/60.0, lon+nm*math.sin(2*math.pi*k/n)*lpn(lat)] for k in range(n)]+[[lat+nm/60.0,lon]]

def dms(d,m,s): return d+m/60+s/3600
REFUGE={1:{"s":dms(26,44,51),"n":dms(26,45,48)},2:{"s":dms(26,46,38),"n":dms(26,47,38)}}

# chart-verified jetty tips; extended west along documented length
TIPN=(26.773512,-80.030989); TIPS=(26.771312,-80.031752)
NJ_WEST=TIPN[1]-2000*FT*lpn(26.7735); SJ_WEST=TIPS[1]-1900*FT*lpn(26.7713)
GROIN=[[26.773918,-80.031635],[26.773901,-80.030786],[26.773900,-80.030743],[26.774088,-80.030669]]
def clip_west(pts, lon_min):
    """Keep the parts of a polyline east of lon_min, cutting segments at lon_min. Pieces are concatenated:
    buf_line takes the convex hull, so the joins add nothing outside the hull."""
    out=[]
    for a,b in zip(pts,pts[1:]):
        ina, inb = a[1]>=lon_min, b[1]>=lon_min
        if ina: out.append(list(a))
        if ina!=inb:
            t=(lon_min-a[1])/(b[1]-a[1]); out.append([a[0]+t*(b[0]-a[0]), lon_min])
    if pts[-1][1]>=lon_min: out.append(list(pts[-1]))
    return out
if SRC=="osm":
    NJ=[[TIPN[0],TIPN[1]],[26.7736,-80.03366],[26.77365, NJ_WEST]]
    SJ=[[TIPS[0],TIPS[1]],[ROOT_S[0],ROOT_S[1]],[26.77145, SJ_WEST]]
    BRIDGE=[[26.78330,-80.04820],[26.78345,-80.04400],[26.78355,-80.03970]]   # OSM, real span
    PEANUT=None
else:
    # ENC rip rap lines (always dry) cut at the same documented lengths the OSM build used.
    NJ=clip_west(ENC["north_jetty"]["pts"], NJ_WEST)
    SJ=clip_west(ENC["south_jetty"]["pts"], SJ_WEST)
    BRIDGE=[p for ring in ENC["blue_heron_bridge"]["areas"] for p in ring]   # both charted spans
    PEANUT=ENC["peanut_east_shore"]["pts"]+ENC["peanut_east_shore"]["sw_corner"]
BEACH_YD = 125 if SRC=="osm" else 150
# Refuge inner edge. The rule says 750 yd from mean high water. On NAIP imagery the ENC line runs at the
# waterline in places (Palm Beach, 26.76 N), so it can sit seaward of mean high water; drawing the edge
# 25 yd closer to shore keeps the refuge (a closure) from shrinking below the rule there.
REFUGE_YD = 750 if SRC=="osm" else 725
SHORE_NAME = "OpenStreetMap coastline data" if SRC=="osm" else "the NOAA ENC chart coastline (harbour band)"

Z=[]
def add(i,c,nm,rule,g,kind="poly"): Z.append(dict(id=i,cls=c,name=nm,rule=rule,kind=kind,geom=g))

for n,b in REFUGE.items():
    add(f"refuge{n}","refuge",f"Refuge Area No. {n}",
      "PBC Code App. G §§ 13-55, 13-56: no spearfishing on underwater breathing apparatus. Freediving is NOT restricted. Latitudes are exact; the 750 yd inner edge is measured from "+SHORE_NAME+("." if SRC=="osm" else ", and drawn at 725 yd so that a chart line lying seaward of mean high water cannot shrink the refuge."),
      band(b["s"],b["n"],REFUGE_YD*YD,3.0))
    add(f"refuge{n}near","refnear",f"Area No. {n}: inner carve-out",
      "§ 13-55 excludes water inside 750 yd of MHW, and water shallower than 30 ft at MLW, from the refuge. The depth condition is NOT drawn: only the 750 yd distance"+("." if SRC=="osm" else ", drawn at 725 yd from the chart coastline (see the refuge note).")+"",
      band(b["s"],b["n"],0,REFUGE_YD*YD))

# seaward-only beach buffer along the whole Atlantic front
BEACH_RULE=("R. 68B-20.003(2)(a): 100 yd from ALL public bathing beaches: FWC's rule says 'all', not 'designated'. Drawn at 125 yd, seaward only, along the entire developed beachfront. Named public beaches here: Palm Beach (to 26.771), Riviera Beach / Singer Island (26.774 to 26.800), Ocean Reef / MacArthur (26.800 to 26.814)."
 if SRC=="osm" else
 "R. 68B-20.003(2)(a): 100 yd from ALL public bathing beaches: FWC's rule says 'all', not 'designated'. Drawn at 150 yd, seaward only, along the entire developed beachfront, measured from the NOAA chart coastline. On USGS NAIP imagery (service refreshed June 2024) the chart line runs along the upper beach, up to about 30 m landward of the waterline, so the extra 50 yd keeps the drawn edge more than 100 yd from the water's edge. Named public beaches here: Palm Beach (to 26.771), Riviera Beach / Singer Island (26.774 to 26.800), Ocean Reef / MacArthur (26.800 to 26.814).")
add("beach","hard","Atlantic beach buffer: %d yd seaward" % BEACH_YD, BEACH_RULE,
 band(26.70,26.86,0,BEACH_YD*YD))

add("jettyN","hard","North jetty: 150 ft buffer","Rule is 100 ft from the unsubmerged portion (R. 68B-20.003(2)(d)). Drawn at 150 ft for submerged toe stone and tide swing. "+("Tip is chart-accurate (NOAA ENC); the landward run follows OSM breakwater geometry." if SRC=="osm" else "Tip and landward run are the charted rip rap (NOAA ENC, always dry), 2,000 ft west from the tip."),buf_line(NJ,150*FT))
add("jettyS","hard","South jetty: 150 ft buffer","Same rule and margin. Tip and root are chart-accurate."+("" if SRC=="osm" else " Drawn on the charted rip rap (NOAA ENC, always dry), 1,900 ft west from the exposed tip; the charted always-submerged extension beyond the tip is not 'unsubmerged' and carries no buffer."),buf_line(SJ,150*FT))
add("groin","hard","Ruined L-groin: 150 ft buffer","Charted as a GROIN, not a jetty, and it covers and uncovers: so the buffer arguably blinks with the tide. Treated as always-on.",buf_line(GROIN,150*FT))
add("bhb","hard","Blue Heron Bridge: 125 yd","Public fishing IS legally permitted here: Fla. Stat. § 316.1305 allows bridge fishing by default, and FDOT's Feb 2021 no-fishing signs were removed within days as installed in error. So the 100 yd bridge buffer attaches. "+("Span geometry from OpenStreetMap." if SRC=="osm" else "Span geometry: the two charted bridge areas (NOAA ENC), joined across Phil Foster Park island.")+" Drawn at 125 yd.",buf_line(BRIDGE,125*YD))
add("pfp","hard","Phil Foster Park: 125 yd","Guarded swim area, a public fishing pier (the old bridge remnant) and two fishing platforms: each an independent 100 yd buffer. Plus the R. 68B-42.0036 no-take SMLA.",circle(26.78330,-80.04350,125*YD))
if SRC=="osm":
    add("peanut","hard","Peanut Island swim area: 125 yd","County beach and snorkel trail on the island's east side. Beach polygon from OpenStreetMap.",circle(26.77204,-80.04485,125*YD))
else:
    add("peanut","hard","Peanut Island swim area: 125 yd","County beach and snorkel trail on the island's east side. Drawn 125 yd around the island's east shore and south-west corner (NOAA ENC coastline), which covers the swim beach wherever along that shore it is marked.",buf_line(PEANUT,125*YD))

add("inletN","county","Inlet: narrow reading",
 "§ 13-33: no underwater spear fishing within any inlet, ever. Narrow reading = water between the jetties, seaward limit at the COLREGS line across the tips.",
 [[TIPN[0],TIPN[1]],[TIPS[0],TIPS[1]],[26.77145,-80.03760],[26.77365,-80.03713],[TIPN[0],TIPN[1]]])
add("inletB","county","Inlet: broad reading",
 "The throat west of the jetty roots, toward the Port turning basin. 'Inlet' is UNDEFINED in § 13-31 (confirmed by reading it). This western limit is one plausible construction, not a boundary anyone has adopted.",
 [[26.77365,-80.03713],[26.77145,-80.03760],[26.77020,-80.04380],[26.77560,-80.04380],[26.77365,-80.03713]])
add("demarc","line","COLREGS demarcation line","33 CFR 80.727: a line across the seaward extremity of the Lake Worth Inlet jetties. The only official line drawn at this inlet.",
 [[TIPN[0],TIPN[1]],[TIPS[0],TIPS[1]]],kind="line")
add("flag200","flag","Diver-flag zone: 200 yd of the jetties","§ 13-37: flag required in Atlantic waters within 200 yd of any portion of the jetties. Does not apply inside 150 yd of the MHW line. § 13-38 requires one anywhere more than 150 yd offshore anyway.",buf_line(NJ+SJ[::-1],200*YD))
add("sw3","line","3 nm state waters line","Atlantic state waters end at 3 nm. East of this line federal snapper-grouper rules apply. Measured from "+("the OSM coastline" if SRC=="osm" else "the NOAA ENC coastline")+": approximate, and the legal baseline is not identical to the visible shoreline.",
 [[la,shore_lon(la)+3.0*lpn(la)] for la in [26.66+i*0.01 for i in range(25)]],kind="line")
add("idle","speed","Idle / slow speed zone: approximate","R. 68C-22.009 and R. 68D-24.017(1)(c): year-round idle speed both sides of Lake Worth from the Port turning basin to one mile south of Peanut Island, plus a shoreline-to-shoreline slow zone across Peanut Island / Blue Heron. THIS OUTLINE IS INDICATIVE ONLY: the real zone follows the lagoon shoreline and posted markers.",
 [[26.7900,-80.0530],[26.7900,-80.0380],[26.7580,-80.0430],[26.7580,-80.0530],[26.7900,-80.0530]])

if SRC=="osm":
    json.dump(Z, open("zones.json","w"))
    json.dump(shore, open("shoreline_used.json","w"))
else:
    def rnd(g): return [[round(a,6),round(b,6)] for a,b in g]
    for z in Z: z["geom"]=rnd(z["geom"])
    with open(os.path.join(ROOT,"data","zones-palmbeach.json"),"w",encoding="utf-8") as f:
        json.dump(Z, f, ensure_ascii=False, separators=(",",":"))
    json.dump(shore, open(os.path.join(GEO,"shoreline-used-palmbeach.json"),"w"))
print(f"{len(Z)} zones")
for z in Z: print(f"  {z['id']:12} {z['cls']:8} {len(z['geom']):5} pts  {z['name']}")
print("\nshore_lon spot checks (real vs my old guesses):")
for la,old in [(26.700,-80.0350),(26.780,-80.0322),(26.8248,-80.0360),(26.7500,-80.0340)]:
    r=shore_lon(la); print(f"  {la}: real {r:.5f}  old {old:.4f}  error {abs(r-old)*111320*math.cos(math.radians(la)):.0f} m")
