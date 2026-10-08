import json, math, collections
D="florida-spearfishing-map/data/"
P=json.load(open("piers_fknms.json")); BR=json.load(open("fl_bridges.json")); S=json.load(open("sla_contours.json"))
FT=1/6076.115; YD=3*FT
def lpn(lat): return 1.0/(60.0*math.cos(math.radians(lat)))
def circle(lat,lon,nm,n=24):
    return [[round(lat+nm*math.cos(2*math.pi*k/n)/60.0,5),
             round(lon+nm*math.sin(2*math.pi*k/n)*lpn(lat),5)] for k in range(n)]

# ---- 1. confirmed public fishing structures: 100 yd rule, drawn at 125 yd ----
piers=[]
for x in P["piers"]:
    if x["lat"] is None: continue
    piers.append({"n":x["n"],"c":x["c"],"t":x["t"],"w":x["w"],"e":x["e"],
                  "lat":x["lat"],"lon":x["lon"],"r":circle(x["lat"],x["lon"],125*YD)})
json.dump(piers, open(D+"piers.json","w"), separators=(',',':'))

# ---- 2. bridges: three-valued per the 316.1305 analysis ----
LIM={'01','11','02','12'}
def near_pier(b):
    for p in P["piers"]:
        if p["lat"] is None: continue
        if abs(p["lat"]-b["lat"])<0.004 and abs(p["lon"]-b["lon"])<0.004: return p["n"]
    return None
bridges=[]
for b in BR:
    lim = b["fc"] in LIM
    conf = near_pier(b)
    st = "excluded" if lim else ("confirmed" if conf else "presumed")
    bridges.append({"n":b["f"] or "Bridge","o":b["o"],"lat":b["lat"],"lon":b["lon"],
                    "st":st,"fc":b["fc"],"cf":conf})
json.dump(bridges, open(D+"bridges.json","w"), separators=(',',':'))

# ---- 3. FKNMS zones ----
fk=[z for z in P["fknms"]]
json.dump(fk, open(D+"fknms.json","w"), separators=(',',':'))

# ---- 4. jurisdiction lines + statewide 30 ft contour ----
json.dump({"atl":S["sla"]["atl"],"gom":S["sla"]["gom"]}, open(D+"jurisdiction.json","w"), separators=(',',':'))
json.dump([{"v":9.1,"p":[p]} for p in S["contours"]], open(D+"contours.json","w"), separators=(',',':'))

print("piers", len(piers))
print("bridges", len(bridges), collections.Counter(b["st"] for b in bridges))
print("fknms", len(fk), "| no-fishing", sum(1 for z in fk if z["fish"]!="Yes"))
print("contours", len(S["contours"]))
import os
for f in sorted(os.listdir(D)): print("  ",f, round(os.path.getsize(D+f)/1024),"KB")
