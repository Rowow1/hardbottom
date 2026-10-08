import json, math, collections, re, os
D="florida-spearfishing-map/data/"
FWC=json.load(open("fwc_reefs.json")); PBC=json.load(open("pbc_reefs.json"))
RA=json.load(open("fwc_ramps.json")); CUR={s["name"]:s for s in json.load(open("sites_merged.json"))}
KEEP={"NS","PB","PBC","FWC","SE","SW","NE","NW","USS","MV","SS","LW","PI","RBM","N","S","E","W","II","III","IV"}
def tc(n):
    out=[]
    for w in str(n).split():
        if w.upper() in KEEP or re.fullmatch(r"[A-Z]{1,3}-?\d+[A-Z]?", w):
            out.append(w.upper() if w.upper() in KEEP else w)
        else:
            out.append(re.sub(r"[A-Za-z']+", lambda m:m.group(0)[0].upper()+m.group(0)[1:].lower(), w.lower()))
    return " ".join(out).replace("'S","'s")
def hav(a,b):
    la1,lo1=map(math.radians,a); la2,lo2=map(math.radians,b)
    return 2*3440.065*math.asin(math.sqrt(math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
sites=[]
for r in FWC:
    if not r.get("Lat_DD"): continue
    sites.append(dict(n=tc(r.get("Name") or "Unnamed"), lat=round(r["Lat_DD"],5), lon=round(r["Long_DD"],5),
        d=r.get("Depth"), rel=r.get("Relief"), t="a", c=str(r.get("County") or "").title(),
        m=r.get("MatCat"), src="FWC",
        nt=" · ".join(str(x) for x in [r.get("MatDescrip"),r.get("Description")] if x)[:120]))
for r in PBC:
    try: lat=float(r["DEC_DEG_LAT"]); lon=float(r["DEC_DEG_LONG"])
    except: continue
    sites.append(dict(n=tc(r.get("FNAME") or "Unnamed"), lat=round(lat,5), lon=round(lon,5),
        d=None, rel=None, t="n" if "Natural" in str(r.get("REEF_TYPE")) else "a",
        c="Palm Beach", m=None, src="PBC",
        nt=" · ".join(str(x) for x in [r.get("REEF_TYPE"),r.get("NOTES"),
          None if r.get("REEF_STATUS")=="REEF IS ACTIVE" else r.get("REEF_STATUS")] if x)[:120]))
sites.sort(key=lambda s:(0 if s["src"]=="FWC" else 1))
kept=[]; grid=collections.defaultdict(list)
for s in sites:
    k=(round(s["lat"],3),round(s["lon"],3)); hit=None
    for dk in [(k[0]+i*0.001,k[1]+j*0.001) for i in(-1,0,1) for j in(-1,0,1)]:
        for o in grid[dk]:
            if hav((s["lat"],s["lon"]),(o["lat"],o["lon"]))*1852<60: hit=o; break
        if hit: break
    if hit:
        if s["t"]=="n": hit["t"]="n"
        for f in ("d","rel","m"):
            if hit.get(f) in (None,"") and s.get(f) not in (None,""): hit[f]=s[f]
        if s["src"] not in hit["src"]: hit["src"]+="+"+s["src"]
    else: kept.append(s); grid[k].append(s)
for s in kept:
    for cn,c in CUR.items():
        if abs(s["lat"]-c["lat"])<0.002 and abs(s["lon"]-c["lon"])<0.002 and hav((s["lat"],s["lon"]),(c["lat"],c["lon"]))*1852<150:
            s["n"]=c["name"]
            if not s.get("d") and c.get("depth"): s["d"]=c["depth"]
            break
def dms(d,m,sec): return d+m/60+sec/3600
REF={1:(dms(26,44,51),dms(26,45,48)),2:(dms(26,46,38),dms(26,47,38))}
shore=json.load(open("shoreline_used.json"))
def shore_lon(lat):
    if lat<=shore[0][0] or lat>=shore[-1][0]: return None
    lo,hi=0,len(shore)-1
    while hi-lo>1:
        mm=(lo+hi)//2
        if shore[mm][0]<=lat: lo=mm
        else: hi=mm
    a,b=shore[lo],shore[hi]; t=0 if b[0]==a[0] else (lat-a[0])/(b[0]-a[0])
    return a[1]+t*(b[1]-a[1])
YD=3/6076.115
MON=json.load(open("monroe_closure.json")); PENN=json.load(open("pennekamp.json"))
def inpoly(pt,ring):
    x,y=pt[1],pt[0]; ins=False; n=len(ring)
    for i in range(n):
        y1,x1=ring[i]; y2,x2=ring[(i+1)%n]
        if (y1>y)!=(y2>y):
            xi=(x2-x1)*(y-y1)/(y2-y1)+x1
            if x<xi: ins=not ins
    return ins
for s in kept:
    s["ref"]=None; s["edge"]=False; s["closed"]=None
    sl=shore_lon(s["lat"])
    if sl is not None and 26.5<s["lat"]<27.0:
        off=(s["lon"]-sl)/(1/(60*math.cos(math.radians(s["lat"]))))
        for n,(a,b) in REF.items():
            if a<=s["lat"]<=b and off>=750*YD: s["ref"]=n
        s["edge"]= min(abs(s["lat"]-e)*60 for a,b in REF.values() for e in (a,b))<=0.05
    if 24.4<s["lat"]<25.5:
        if any(inpoly((s["lat"],s["lon"]),r) for r in PENN): s["closed"]="penn"
        elif any(inpoly((s["lat"],s["lon"]),r) for r in MON): s["closed"]="keys"
    s["d"]= s["d"] if isinstance(s["d"],str) else (int(s["d"]) if s["d"] else None)
kept.sort(key=lambda s:(s["c"],s["n"]))
json.dump(kept, open(D+"sites.json","w"), separators=(',',':'))
ramps=[]
for r in RA:
    if not (r.get("TotalLanes") or 0)>0 or "Salt" not in str(r.get("WaterType")): continue
    if not r.get("Latitude"): continue
    ramps.append(dict(n=str(r.get("RampName") or "").replace(" Boat Ramp",""),
      lat=round(float(r["Latitude"]),5), lon=round(float(r["Longitude"]),5),
      c=str(r.get("County") or "").title(), ln=r.get("TotalLanes"), tr=r.get("Trailer"),
      h=str(r.get("Hours") or "?"), fee=str(r.get("isFeeRequired") or "?"),
      rate=str(r.get("Rate") or r.get("FeeAmount") or "")[:40], st=str(r.get("Status") or ""),
      ad=str(r.get("PrimaryAdminEntity") or "")[:50], ph=str(r.get("ContactPhone") or "")))
ramps.sort(key=lambda r:(r["c"],-(r["tr"] or 0)))
json.dump(ramps, open(D+"ramps.json","w"), separators=(',',':'))
# statewide closures layer
clos=[{"id":"keys","name":"Upper Keys: spearfishing PROHIBITED",
       "rule":"Fla. Stat. § 379.2425(2)(a): spearfishing is prohibited in all salt waters under FWC jurisdiction "
              "beginning at the Miami-Dade/Monroe county line and running south, including all of the keys down to "
              "and including Long Key. Possession of a spear in the water in a prohibited area is prima facie "
              "evidence of a violation. The southern edge drawn here is a construction through Long Key: the "
              "statute names the island, not a coordinate.","rings":MON},
      {"id":"penn","name":"John Pennekamp Coral Reef State Park: PROHIBITED",
       "rule":"Fla. Stat. § 379.2425(2)(a) prohibits spearfishing within the park boundary. The statute gives no "
              "coordinates; this polygon is the FDEP published park boundary. Also a DEP Division of Recreation and "
              "Parks water under R. 68B-20.003(2)(e).","rings":PENN}]
json.dump(clos, open(D+"closures.json","w"), separators=(',',':'))
PK=json.load(open("fl_park_waters.json"))
def thin(r,tol=0.0006):
    out=[r[0]]; a=r[0]
    for p in r[1:-1]:
        if abs(p[0]-a[0])>tol or abs(p[1]-a[1])>tol: out.append(p); a=p
    out.append(r[-1]); return out
parks=[]
for p in PK:
    rings=[thin(r) for r in p["r"] if len(r)>4]
    rings=[r for r in rings if len(r)>3]
    if rings: parks.append({"n":p["n"],"c":p["c"],"r":rings})
json.dump(parks, open(D+"parkwaters.json","w"), separators=(',',':'))
E=json.load(open("enc_statewide.json"))
json.dump(E, open(D+"enc.json","w"), separators=(',',':'))
print("sites",len(kept),"| natural",sum(1 for s in kept if s["t"]=="n"),
      "| keys-closed",sum(1 for s in kept if s["closed"]))
print("ramps",len(ramps),"| counties",len(set(s['c'] for s in kept)))
print("parks",len(parks),"verts",sum(len(r) for p in parks for r in p["r"]))
print("enc",len(E))
for f in sorted(os.listdir(D)): print(" ",f,round(os.path.getsize(D+f)/1024),"KB")
