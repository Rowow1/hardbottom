import json, math, collections
RA=json.load(open("fwc_ramps.json"))
LAB=[]
for r in RA:
    if not r.get("Latitude"): continue
    wt=str(r.get("WaterType") or "")
    k = "salt" if "Salt" in wt else ("fresh" if "Fresh" in wt else None)
    if k: LAB.append((float(r["Latitude"]), float(r["Longitude"]), k))

MARINE = ["GULF","ATLANTIC","OCEAN","BAY ","BAYS","SOUND","INLET"," PASS","PASS ","HARBOR","HARBOUR",
          "LAGOON","INTRACOASTAL","ICW","ESTUARY","STRAIT","BIGHT","ANCHORAGE","SEA ","CHANNEL"]
FRESH  = ["LAKE","POND","SLOUGH","MARSH","SWAMP","PRAIRIE","BRANCH","DITCH","RESERVOIR","SPRING",
          "IMPOUNDMENT","WCA","CONSERVATION AREA","RESERVE","BORROW","RETENTION","DRAIN","OUTFALL"]
# named tidal rivers/waterbodies that are genuinely marine well inland
TIDAL_NAMED = ["LAKE WORTH","INDIAN RIVER","BANANA RIVER","HALIFAX","MATANZAS","BISCAYNE","TAMPA",
               "SARASOTA","CHOCTAWHATCHEE","PENSACOLA","ST ANDREW","ST. ANDREW","APALACHICOLA BAY",
               "ESTERO","LEMON BAY","CHARLOTTE HARBOR","FLORIDA BAY","BOCA CIEGA","OLD TAMPA",
               "HILLSBOROUGH BAY","ST JOSEPH","ST. JOSEPH","PERDIDO BAY","ESCAMBIA BAY","SANTA ROSA"]

def hav(a,b):
    la1,lo1=map(math.radians,a); la2,lo2=map(math.radians,b)
    return 2*6371.0*math.asin(math.sqrt(math.sin((la2-la1)/2)**2+
        math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))

# spatial index on labelled ramps
GRID=collections.defaultdict(list)
def cell(lat,lon): return (round(lat,1), round(lon,1))
for la,lo,k in LAB: GRID[cell(la,lo)].append((la,lo,k))
def knn(lat,lon,k=7,maxkm=12.0):
    cand=[]
    for i in (-1,0,1):
        for j in (-1,0,1):
            cand += GRID[(round(lat,1)+i*0.1, round(lon,1)+j*0.1)]
    if not cand: return None,None
    d=sorted(((hav((lat,lon),(a,b)),lab) for a,b,lab in cand))[:k]
    d=[x for x in d if x[0]<=maxkm]
    if not d: return None,None
    w=collections.defaultdict(float)
    for dist,lab in d: w[lab]+= 1.0/max(dist,0.15)
    best=max(w,key=w.get); tot=sum(w.values())
    return best, w[best]/tot

def classify(name, lat, lon, exclude=None):
    up=str(name).upper()
    if any(t in up for t in TIDAL_NAMED): return "coastal","named tidal water body"
    if any(t in up for t in MARINE):      return "coastal","marine water-body name"
    if any(t in up for t in FRESH):       return "inland","freshwater water-body name"
    lab,conf = knn(lat,lon)
    if lab is None: return "inland","no labelled ramp within 12 km"
    if lab=="salt" and conf>=0.6: return "coastal","%.0f%% of nearby FWC ramps are salt/brackish"%(conf*100)
    if lab=="fresh" and conf>=0.6: return "inland","%.0f%% of nearby FWC ramps are freshwater"%(conf*100)
    return "tidal","mixed fresh and salt ramps nearby: transitional"

# ---- leave-one-out validation on the labelled ramps ----
ok=tot=0; conf=collections.Counter()
for la,lo,truth in LAB:
    GRID[cell(la,lo)].remove((la,lo,truth))
    pred,_=knn(la,lo)
    GRID[cell(la,lo)].append((la,lo,truth))
    if pred is None: continue
    tot+=1; ok+= (pred==truth); conf[(truth,pred)]+=1
print(f"leave-one-out on {tot} FWC ramps: {ok/tot*100:.1f}% agreement")
for k,v in sorted(conf.items()): print(f"   truth={k[0]:6} pred={k[1]:6} {v}")

D="florida-spearfishing-map/data/"
def tag(rows, namekey, out=None):
    c=collections.Counter()
    for r in rows:
        k,why = classify(r.get(namekey,""), r["lat"], r["lon"])
        r["iw"]=k; r["iwr"]=why; c[k]+=1
    return c

BR=json.load(open(D+"bridges.json"))
print("\nbridges:", tag(BR,"o"))
json.dump(BR, open(D+"bridges.json","w"), separators=(',',':'))

RM=json.load(open(D+"ramps.json"))
# ramps already carry FWC's own WaterType via the salt filter, but tag for consistency
for r in RM: r["iw"]="coastal"; r["iwr"]="FWC classifies this ramp as salt or brackish water"
json.dump(RM, open(D+"ramps.json","w"), separators=(',',':'))

PI=json.load(open(D+"piers.json"))
print("piers:", tag(PI,"w"))
json.dump(PI, open(D+"piers.json","w"), separators=(',',':'))

ST=json.load(open(D+"sites.json"))
print("sites:", tag(ST,"nt"))
json.dump(ST, open(D+"sites.json","w"), separators=(',',':'))

print("\nbridge classes x fishing status:")
x=collections.Counter((b["iw"],b["st"]) for b in BR)
for k,v in sorted(x.items()): print(f"   {k[0]:8} {k[1]:10} {v}")
print("\nsample inland bridges:", [(b['n'][:18],b['o'][:20]) for b in BR if b['iw']=='inland'][:5])
print("sample coastal bridges:", [(b['n'][:18],b['o'][:20]) for b in BR if b['iw']=='coastal'][:5])
