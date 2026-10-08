import json, math, re, collections
FWC=json.load(open("fwc_reefs.json")); PBC=json.load(open("pbc_reefs.json"))
OLD={s["name"]:s for s in json.load(open("stage1.json"))["sites"]}
TIP=(26.773512,-80.030989); R=3440.065
def d2r(x): return math.radians(x)
def lpn(lat): return 1.0/(60.0*math.cos(d2r(lat)))
def geo(a,b):
    la1,lo1=d2r(a[0]),d2r(a[1]); la2,lo2=d2r(b[0]),d2r(b[1]); dlo=lo2-lo1
    dist=2*R*math.asin(math.sqrt(math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin(dlo/2)**2))
    y=math.sin(dlo)*math.cos(la2); x=math.cos(la1)*math.sin(la2)-math.sin(la1)*math.cos(la2)*math.cos(dlo)
    return dist,(math.degrees(math.atan2(y,x))+360)%360
shore=json.load(open("shoreline_used.json"))
def shore_lon(lat):
    if lat<=shore[0][0]: return shore[0][1]
    if lat>=shore[-1][0]: return shore[-1][1]
    lo,hi=0,len(shore)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if shore[m][0]<=lat: lo=m
        else: hi=m
    a,b=shore[lo],shore[hi]; t=0 if b[0]==a[0] else (lat-a[0])/(b[0]-a[0])
    return a[1]+t*(b[1]-a[1])
def dms(dd,m,s): return dd+m/60+s/3600
REF={1:(dms(26,44,51),dms(26,45,48)),2:(dms(26,46,38),dms(26,47,38))}
YD=3/6076.115

sites=[]
def push(name,lat,lon,depth,relief,typ,mat,src,note):
    if lat is None or lon is None: return
    dist,brg=geo(TIP,(lat,lon))
    if dist>18: return
    sites.append(dict(name=str(name).strip(),lat=round(lat,6),lon=round(lon,6),
        depth=depth,relief=relief,typ=typ,mat=mat,src=src,note=note,
        nm=round(dist,2),brg=round(brg)))

for r in FWC:
    if not r.get("Lat_DD"): continue
    push(r.get("Name") or "(unnamed)", r["Lat_DD"], r["Long_DD"], r.get("Depth"), r.get("Relief"),
         "artificial", r.get("MatCat"), "FWC",
         " · ".join(str(x) for x in [r.get("MatDescrip"),r.get("Description")] if x)[:150])
for r in PBC:
    try: lat=float(r["DEC_DEG_LAT"]); lon=float(r["DEC_DEG_LONG"])
    except: continue
    t="natural" if "Natural" in str(r.get("REEF_TYPE")) else "artificial"
    push(r.get("FNAME") or "(unnamed)", lat, lon, None, None, t, None, "PBC",
         " · ".join(str(x) for x in [r.get("REEF_TYPE"),r.get("NOTES"),
           None if r.get("REEF_STATUS")=="REEF IS ACTIVE" else r.get("REEF_STATUS")] if x)[:150])

# dedupe: same point within 60 m -> merge, preferring the record with more attributes
def key(s): return (round(s["lat"],3), round(s["lon"],3))
sites.sort(key=lambda s:(0 if s["src"]=="FWC" else 1))
kept=[]
for s in sites:
    hit=None
    for k in kept:
        dd,_=geo((s["lat"],s["lon"]),(k["lat"],k["lon"]))
        if dd*1852 < 60: hit=k; break
    if hit:
        if s["typ"]=="natural": hit["typ"]="natural"
        for f in ("depth","relief","mat"):
            if hit.get(f) in (None,"") and s.get(f) not in (None,""): hit[f]=s[f]
        if s["name"].lower() not in hit["name"].lower() and len(hit.get("alt",""))<40:
            hit["alt"]=s["name"]
        hit["src"]=hit["src"]+"+"+s["src"] if s["src"] not in hit["src"] else hit["src"]
    else: kept.append(s)

# carry across the curated depth/notes from the original 40-site research set
for k in kept:
    for on,o in OLD.items():
        dd,_=geo((k["lat"],k["lon"]),(o["lat"],o["lon"]))
        if dd*1852<150:
            k["curated"]=on
            if not k.get("depth") and o.get("depth"): k["depth"]=o["depth"]
            if o.get("note"): k["note"]=(o["note"]+" · "+k["note"])[:200]
            k["kind_old"]=o["kind"]
            break

for s in kept:
    lat=s["lat"]; off=(s["lon"]-shore_lon(lat))/lpn(lat)
    s["offshore_nm"]=round(off,2); s["federal"]= off>3.0
    s["refuge"]=None
    for n,(a,b) in REF.items():
        if a<=lat<=b and off>=750*YD: s["refuge"]=n
    s["refuge_margin_nm"]=round(min(abs(lat-a)*60 for a,b in REF.values() for a in (a,b)),2)


KEEP={"NS","PB","PBC","FWC","SE","SW","NE","NW","USS","MV","SS","LW","PI","RBM","N","S","E","W","II","III","IV"}
def tc(n):
    out=[]
    for w in str(n).split():
        if w.upper() in KEEP or re.fullmatch(r"[A-Z]{1,3}-?\d+[A-Z]?", w) or re.fullmatch(r"[A-Z]?\d+", w):
            out.append(w.upper() if w.upper() in KEEP else w)
        else:
            out.append(re.sub(r"[A-Za-z']+", lambda m: m.group(0)[0].upper()+m.group(0)[1:].lower(), w.lower()))
    return " ".join(out).replace("'S","'s")
for k in kept:
    if k["name"].isupper(): k["name"]=tc(k["name"])
    if k.get("alt","").isupper(): k["alt"]=tc(k["alt"])
    if k.get("curated"): k["name"]=k["curated"]
kept.sort(key=lambda s:s["nm"])
json.dump(kept, open("sites_merged.json","w"))
print(f"merged sites within 18 nm: {len(kept)}")
print(" sources:", collections.Counter(s["src"] for s in kept))
print(" types:", collections.Counter(s["typ"] for s in kept))
print(" in refuge:", sum(1 for s in kept if s["refuge"]))
print(f" natural sites: {sum(1 for s in kept if s['typ']=='natural')}")
print("\nnatural reefs, nearest 16:")
for s in [x for x in kept if x["typ"]=="natural"][:16]:
    print(f"  {s['nm']:5.2f} nm @{s['brg']:03d}  {s['name'][:30]:32} {str(s.get('depth') or '?'):>5} ft  "
          f"{'REFUGE '+str(s['refuge']) if s['refuge'] else 'open':9} {s.get('curated','')}")
