import json, math
FT=1/6076.115; YD=3*FT
def lpn(lat): return 1.0/(60.0*math.cos(math.radians(lat)))

RAW=json.load(open("shoreline_atlantic.json"))
# Bridge the inlet gap: between the chart-verified jetty roots the extraction wanders inside the inlet.
GAP=(26.7706,26.7742)
ROOT_S=(26.771415,-80.034414); ROOT_N=(26.773489,-80.031564)
shore=[p for p in RAW if not (GAP[0] <= p[0] <= GAP[1])]
shore += [[26.7706,-80.03330],[ROOT_S[0],ROOT_S[1]],[ROOT_N[0],ROOT_N[1]],[26.7742,-80.03120]]
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
NJ=[[TIPN[0],TIPN[1]],[26.7736,-80.03366],[26.77365, TIPN[1]-2000*FT*lpn(26.7735)]]
SJ=[[TIPS[0],TIPS[1]],[ROOT_S[0],ROOT_S[1]],[26.77145, TIPS[1]-1900*FT*lpn(26.7713)]]
GROIN=[[26.773918,-80.031635],[26.773901,-80.030786],[26.773900,-80.030743],[26.774088,-80.030669]]
BRIDGE=[[26.78330,-80.04820],[26.78345,-80.04400],[26.78355,-80.03970]]   # OSM, real span

Z=[]
def add(i,c,nm,rule,g,kind="poly"): Z.append(dict(id=i,cls=c,name=nm,rule=rule,kind=kind,geom=g))

for n,b in REFUGE.items():
    add(f"refuge{n}","refuge",f"Refuge Area No. {n}",
      "PBC Code App. G §§ 13-55, 13-56: no spearfishing on underwater breathing apparatus. Freediving is NOT restricted. Latitudes are exact; the 750 yd inner edge is measured from OpenStreetMap coastline data.",
      band(b["s"],b["n"],750*YD,3.0))
    add(f"refuge{n}near","refnear",f"Area No. {n}: inner carve-out",
      "§ 13-55 excludes water inside 750 yd of MHW, and water shallower than 30 ft at MLW, from the refuge. The depth condition is NOT drawn: only the 750 yd distance.",
      band(b["s"],b["n"],0,750*YD))

# seaward-only beach buffer along the whole Atlantic front
add("beach","hard","Atlantic beach buffer: 125 yd seaward",
 "R. 68B-20.003(2)(a): 100 yd from ALL public bathing beaches: FWC's rule says 'all', not 'designated'. Drawn at 125 yd, seaward only, along the entire developed beachfront. Named public beaches here: Palm Beach (to 26.771), Riviera Beach / Singer Island (26.774 to 26.800), Ocean Reef / MacArthur (26.800 to 26.814).",
 band(26.70,26.86,0,125*YD))

add("jettyN","hard","North jetty: 150 ft buffer","Rule is 100 ft from the unsubmerged portion (R. 68B-20.003(2)(d)). Drawn at 150 ft for submerged toe stone and tide swing. Tip is chart-accurate (NOAA ENC); the landward run follows OSM breakwater geometry.",buf_line(NJ,150*FT))
add("jettyS","hard","South jetty: 150 ft buffer","Same rule and margin. Tip and root are chart-accurate.",buf_line(SJ,150*FT))
add("groin","hard","Ruined L-groin: 150 ft buffer","Charted as a GROIN, not a jetty, and it covers and uncovers: so the buffer arguably blinks with the tide. Treated as always-on.",buf_line(GROIN,150*FT))
add("bhb","hard","Blue Heron Bridge: 125 yd","Public fishing IS legally permitted here: Fla. Stat. § 316.1305 allows bridge fishing by default, and FDOT's Feb 2021 no-fishing signs were removed within days as installed in error. So the 100 yd bridge buffer attaches. Span geometry from OpenStreetMap. Drawn at 125 yd.",buf_line(BRIDGE,125*YD))
add("pfp","hard","Phil Foster Park: 125 yd","Guarded swim area, a public fishing pier (the old bridge remnant) and two fishing platforms: each an independent 100 yd buffer. Plus the R. 68B-42.0036 no-take SMLA.",circle(26.78330,-80.04350,125*YD))
add("peanut","hard","Peanut Island swim area: 125 yd","County beach and snorkel trail on the island's east side. Beach polygon from OpenStreetMap.",circle(26.77204,-80.04485,125*YD))

add("inletN","county","Inlet: narrow reading",
 "§ 13-33: no underwater spear fishing within any inlet, ever. Narrow reading = water between the jetties, seaward limit at the COLREGS line across the tips.",
 [[TIPN[0],TIPN[1]],[TIPS[0],TIPS[1]],[26.77145,-80.03760],[26.77365,-80.03713],[TIPN[0],TIPN[1]]])
add("inletB","county","Inlet: broad reading",
 "The throat west of the jetty roots, toward the Port turning basin. 'Inlet' is UNDEFINED in § 13-31 (confirmed by reading it). This western limit is one plausible construction, not a boundary anyone has adopted.",
 [[26.77365,-80.03713],[26.77145,-80.03760],[26.77020,-80.04380],[26.77560,-80.04380],[26.77365,-80.03713]])
add("demarc","line","COLREGS demarcation line","33 CFR 80.727: a line across the seaward extremity of the Lake Worth Inlet jetties. The only official line drawn at this inlet.",
 [[TIPN[0],TIPN[1]],[TIPS[0],TIPS[1]]],kind="line")
add("flag200","flag","Diver-flag zone: 200 yd of the jetties","§ 13-37: flag required in Atlantic waters within 200 yd of any portion of the jetties. Does not apply inside 150 yd of the MHW line. § 13-38 requires one anywhere more than 150 yd offshore anyway.",buf_line(NJ+SJ[::-1],200*YD))
add("sw3","line","3 nm state waters line","Atlantic state waters end at 3 nm. East of this line federal snapper-grouper rules apply. Measured from the OSM coastline: approximate, and the legal baseline is not identical to the visible shoreline.",
 [[la,shore_lon(la)+3.0*lpn(la)] for la in [26.66+i*0.01 for i in range(25)]],kind="line")
add("idle","speed","Idle / slow speed zone: approximate","R. 68C-22.009 and R. 68D-24.017(1)(c): year-round idle speed both sides of Lake Worth from the Port turning basin to one mile south of Peanut Island, plus a shoreline-to-shoreline slow zone across Peanut Island / Blue Heron. THIS OUTLINE IS INDICATIVE ONLY: the real zone follows the lagoon shoreline and posted markers.",
 [[26.7900,-80.0530],[26.7900,-80.0380],[26.7580,-80.0430],[26.7580,-80.0530],[26.7900,-80.0530]])

json.dump(Z, open("zones.json","w"))
json.dump(shore, open("shoreline_used.json","w"))
print(f"{len(Z)} zones")
for z in Z: print(f"  {z['id']:12} {z['cls']:8} {len(z['geom']):5} pts  {z['name']}")
print("\nshore_lon spot checks (real vs my old guesses):")
for la,old in [(26.700,-80.0350),(26.780,-80.0322),(26.8248,-80.0360),(26.7500,-80.0340)]:
    r=shore_lon(la); print(f"  {la}: real {r:.5f}  old {old:.4f}  error {abs(r-old)*111320*math.cos(math.radians(la)):.0f} m")
