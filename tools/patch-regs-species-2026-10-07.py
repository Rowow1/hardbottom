# -*- coding: utf-8 -*-
"""Legal review of 7 and 8 Oct 2026: bring data/regs.json and data/species.json in line with the
registry pass in tools/law-updates/2026-10-07/r1-review.json.

Every change below is a literal replacement or an append, keyed by item title or species id, and
names the registry entry it rests on. The script is idempotent: a change whose new text is already
present is skipped, and a replacement whose old text is missing stops the run, so silent drift is
impossible. Never touches law ids that are not in data/law.json (tools/test-data.py checks).
"""
import io, json, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RP = os.path.join(ROOT, "data", "regs.json")
SP = os.path.join(ROOT, "data", "species.json")
R = json.load(io.open(RP, encoding="utf-8"))
S = json.load(io.open(SP, encoding="utf-8"))
done = []


def sub(text, old, new, where):
    if new in text:
        return text
    if old not in text:
        sys.exit("%s: expected text not found: %r" % (where, old[:80]))
    done.append(where)
    return text.replace(old, new)


def app(text, new, where):
    if new.strip() in text:
        return text
    done.append(where)
    return text.rstrip() + " " + new


def item(sec, title):
    for it in R[sec]:
        if it[0] == title:
            return it
    sys.exit("regs.json: no item %r in %s" % (title, sec))


def upd(sec, title, fn):
    it = item(sec, title)
    it[1] = fn(it[1], "regs %s/%s" % (sec, title))


def add_item(sec, title, text, after=None):
    if any(it[0] == title for it in R[sec]):
        return
    pos = len(R[sec])
    if after:
        pos = [i for i, it in enumerate(R[sec]) if it[0] == after][0] + 1
    R[sec].insert(pos, [title, text])
    done.append("regs %s/+%s" % (sec, title))


def county(name, fn):
    c = R["counties"][name]
    c["txt"] = fn(c["txt"], "county " + name)

# ------------------------------------------------------------------ licences
upd("licences", "Florida recreational saltwater fishing licence", lambda t, w: app(t,
    "Carry it in personal possession while taking or possessing fish, § 379.354(3). Scuba divers aboard a dive "
    "boat that carries them for a fee and holds the right vessel licence are not required to hold individual "
    "licences, § 379.354(7)(f). Spiny lobster needs the separate annual lobster permit, § 379.354(8)(d).", w))
upd("licences", "Diver-down device", lambda t, w: sub(t,
    "A divers-down buoy may not be displayed on board a vessel.",
    "The flag is at least <b>12 by 12 in</b> shown from the water and <b>20 by 24 in</b> shown from a boat, "
    "§ 327.331(1)(c)1. Other boats inside those distances must slow to headway speed, § 327.331(6). The flag "
    "must come down once every diver is aboard or ashore, and a boat may not run with it up unless divers are "
    "in the water, § 327.331(7).", w))

# ------------------------------------------------------------------ statewide
it = [x for x in R["statewide"] if x[0].startswith("Bridges:")][0]
if it[0] == "Bridges: fishing from a bridge is lawful by default, so the buffer applies":
    it[0] = "Bridges: unless FDOT has investigated and posted a ban, the buffer applies"
    it[1] = it[1].replace("So an unposted bridge is one where fishing is legally permitted, and the 100 yd spearfishing buffer attaches.",
                          "So an unposted bridge falls within the rule's words 'where public fishing is legally permitted', and the 100 yd spearfishing buffer attaches.")
    done.append("regs statewide/Bridges retitled")
upd("statewide", "Bridges: unless FDOT has investigated and posted a ban, the buffer applies", lambda t, w: app(t,
    "Separately, <b>jumping or diving from any publicly owned bridge is prohibited</b>, posted or not, "
    "Fla. Stat. § 316.130(17). On this map each coastal and tidal bridge buffer is drawn along the deck as "
    "traced on imagery, not only around the inventory point.", w))
upd("statewide", "Fresh water", lambda t, w: app(t,
    "R. 68A-23.002(7): the use <b>or possession</b> of spear guns <i>\"in or upon the fresh waters of the "
    "state\"</i> is prohibited, so a speargun aboard a boat on a freshwater river is a violation. The "
    "Steinhatchee River is fresh water by statute from source to mouth, § 379.101(17).", w))
upd("statewide", "Local ordinances", lambda t, w: app(t,
    "<b>Added 8 Oct 2026:</b> Clearwater bans firing any spring, air or gas projectile weapon citywide, "
    "spearfishing excepted only where designated (§ 21.06), drawn closed like Treasure Island. Canal gear rules "
    "like Pinellas County's also cover Cape Coral and Sanibel (special acts), listed Naples and Collier canals, "
    "unincorporated Brevard and named Satellite Beach canals: hook and line, cast nets or crab traps only. "
    "<b>Preemption:</b> Fla. Stat. § 379.2412 reserves saltwater fishing regulation to the state except for "
    "fishing from property a local government owns; § 790.33 covers firearms, not spearguns. Until a court "
    "says otherwise, obey the local rule.", w))
upd("statewide", "National parks", lambda t, w: app(t,
    "<b>In every park unit a speargun is a weapon</b> (36 C.F.R. § 1.4), and a <b>loaded</b> weapon is "
    "prohibited in any vessel, anchored or under way, § 2.4(c): unload before you climb back aboard. Park fresh waters are hook and "
    "line only, § 2.3(d)(1). Gear and catch that are illegal in Everglades NP may cross it only by Indian Key, "
    "Sand Fly, Rabbit Key or Chokoloskee pass, § 7.45(d)(9).", w))
upd("statewide", "National wildlife refuges", lambda t, w: app(t,
    "50 C.F.R. § 27.43 also prohibits using or possessing spears and gigs on any refuge unless a refuge rule "
    "authorizes it. <b>Crystal River NWR: no fishing in refuge waters</b> (FWS), drawn closed.", w))
add_item("statewide", "Keep the fish whole",
    "Reef fish must be <b>landed whole</b>: no fillets, heads off or skin off on the water, a pier, a fishing "
    "bridge or a jetty; gutting and removing the gills are not prohibited, r. 68B-14.006(4). In federal waters every Gulf finfish "
    "and every South Atlantic snapper-grouper keeps head and fins, 50 C.F.R. §§ 622.10(a), 622.186(a). A boat "
    "harvesting reef fish in state waters, spearfishing included, must carry a venting tool or rigged descending "
    "device, r. 68B-14.005(3).", after="Powerheads, bangsticks, rebreathers")

# ------------------------------------------------------------------ seasons
upd("seasons", "Gag", lambda t, w: app(t,
    "<b>From 28 Oct 2026</b> the South Atlantic federal private vessel limit is <b>2 gag and black grouper "
    "combined</b> per day (91 FR 61160, Regulatory Amendment 36); FWC proposed the same change for Atlantic "
    "state waters on 5 Oct 2026 (not in force).", w))
upd("seasons", "Shallow-water grouper", lambda t, w: app(t,
    "South Atlantic federal waters: no more than <b>1 scamp or yellowmouth</b> within the 3 grouper, "
    "50 C.F.R. § 622.187(b)(2)(v).", w))
upd("seasons", "Snapper", lambda t, w: app(t,
    "South Atlantic federal waters: of the 20 other snapper-grouper, <b>no more than 10 of any one species</b>, "
    "§ 622.187(b)(8).", w))
upd("seasons", "Prohibited outright", lambda t, w: app(t,
    "<b>Snook:</b> hook and line only, and a snook may not be aboard with spear gear, r. 68B-21.006(3). "
    "<b>Tarpon:</b> no spearing in or out of state waters, r. 68B-32.006(2).", w))

# ------------------------------------------------------------------ fresh water
upd("freshwater", "Spearfishing in fresh water: two separate bans", lambda t, w: sub(t,
    "<b>R. 68A-23.002(5):</b> freshwater fish may not be taken by underwater swimming or diving, or by use of <b>spear guns</b>.",
    "<b>R. 68A-23.002(7)</b> (in force since 7 Jun 2022): the use <b>or possession</b> of spear guns <i>\"in or "
    "upon the fresh waters of the state\"</i> is prohibited unless a rule or permit allows it.", w))
it = [x for x in R["freshwater"] if x[0] in ("The possession claim is weaker than FWC states",
                                             "Possession of a speargun on fresh water is itself prohibited")][0]
if "68A-23.002(9)" in it[1]:
    it[0] = "Possession of a speargun on fresh water is itself prohibited"
    it[1] = ("CORRECTED 8 Oct 2026. This item used to say FWC overstated the rule. It did not: r. 68A-23.002(7), "
             "read verbatim on 7 Oct 2026, prohibits the <i>\"use or possession\"</i> of spear guns <i>\"in or upon "
             "the fresh waters of the state\"</i>. A speargun aboard a boat on a freshwater river or lake is a "
             "violation even if nobody dives. The earlier text relied on an older numbering of the rule.")
    done.append("regs freshwater/possession corrected")

# ------------------------------------------------------------------ counties
county("Palm Beach", lambda t, w: app(t,
    "<b>Boynton (South Lake Worth) Inlet</b> also bans swimming in the inlet and entering it from the jetties, "
    "bulkheads or bridge, and closes the ocean within 75 ft of the sand transfer plant, or its area of influence "
    "if larger (§ 18-1). Town of Palm Beach § 74-162(b) also bars fishing from town bridges and docks and the "
    "town areas under them.", w))
county("Broward", lambda t, w: sub(t,
    "Fort Lauderdale, Hillsboro Beach and county codes negative;",
    "Fort Lauderdale and Hillsboro Beach codes negative. <b>Possible county special act:</b> County Code § 13-5 "
    "(Sp. Acts 1921, ch. 8636) limits food fish in the county's \"rivers, creeks, canals and inside waters\" to "
    "hook and line or cast net; whether it is still in force, and whether it was aimed at fresh water, is open, so "
    "treat the Intracoastal and canals as closed to spearing until resolved;", w))
county("Pinellas", lambda t, w: sub(t,
    "Not yet read: Tarpon Springs, the Redingtons.",
    "<b>Clearwater bans firing spring, air or gas projectile weapons citywide</b>, spearfishing excepted only "
    "where designated (§ 21.06); drawn closed like Treasure Island. St. Petersburg also bars fishing at seven "
    "listed bridges, causeways and rights-of-way and in the pier district unless authorized (§ 7-5). County parks "
    "and their managed lands allow fishing only where designated (§ 90-7(e)). Not yet read: Tarpon Springs, "
    "Redington Beach and North Redington Beach.", w))
county("Lee", lambda t, w: sub(t,
    "Sanibel, Cape Coral, Fort Myers and Estero codes negative.",
    "<b>Cape Coral and Sanibel: manmade saltwater canals are hook and line (Sanibel also hand cast net) or "
    "crab traps only</b>, by special act (Laws of Fla. chs. 78-483 and 85-440), so no spearing in the canals. "
    "Fort Myers and Estero codes negative.", w))
county("Collier", lambda t, w: sub(t,
    "County code negative; Everglades City not checked.",
    "<b>Canals:</b> listed residential canals in unincorporated Collier (Isles of Capri first, § 210-67) and in "
    "Naples (Port Royal and others, Laws of Fla. ch. 90-469) are hook and line, cast net or crab traps only. "
    "Everglades City not checked.", w))
county("Brevard", lambda t, w: sub(t,
    "Coastal city codes negative; Melbourne Beach not yet read.",
    "<b>Residential manmade canals in unincorporated Brevard are hook and line or hand cast net only</b> "
    "(§ 122-3, Laws of Fla. ch. 93-376), and so are the named canals of Satellite Beach (§ 66-1, the Grand Canal "
    "included). Melbourne Beach § 40-33 and Cocoa Beach § 5-56 are reported to do the same; not yet read.", w))
county("Volusia", lambda t, w: app(t,
    "<b>Beach code § 20-121:</b> no swimming within 300 ft of any pier or jetty; the Ponce Inlet jetties are "
    "drawn at 350 ft.", w))
county("Monroe", lambda t, w: sub(t,
    "from three days before the mini-season through the first five days of the commercial season,",
    "from three days before the mini-season to its end, and again for the first five days of the commercial "
    "season,", w))
county("Bay", lambda t, w: sub(t,
    "Mexico Beach not yet read.",
    "<b>Mexico Beach:</b> no swimming in the canal boat channel or within 100 ft of either side of the "
    "entrance jetties (§ 95.03).", w))
county("Citrus", lambda t, w: app(t,
    "<b>Crystal River NWR waters are closed to all fishing</b> (FWS; 50 C.F.R. § 27.21), drawn closed from "
    "8 Oct 2026. In Kings Bay the federal rule bars all waterborne activity, spear fishing included, next to the "
    "sanctuaries and the four springs year-round (§ 17.108(c)(14)(iv)).", w))
county("Manatee", lambda t, w: sub(t,
    "Holmes Beach, Bradenton Beach, Bradenton and Palmetto negative.",
    "<b>Bradenton Beach</b> parks: no fishing from a boat within 300 ft of a public beach, pier or fishing groin "
    "(§ 46-46). Holmes Beach, Bradenton and Palmetto negative.", w))
for c in ("Dixie", "Taylor"):
    county(c, lambda t, w: app(t, "The river is drawn closed along its mapped centreline; a speargun may not even "
                                  "be carried on it, r. 68A-23.002(7).", w))

# ------------------------------------------------------------------ species
SPd = {s["id"]: s for s in S["species"]}


def law_add(sid, *ids):
    s = SPd[sid]
    for i in ids:
        if i not in s["law"]:
            s["law"].append(i)
            done.append("species %s law +%s" % (sid, i))


def reg_set(sid, region, field, fn):
    r = SPd[sid]["regions"].get(region)
    if r is None:
        return
    r[field] = fn(r.get(field) or "", "species %s/%s/%s" % (sid, region, field))


for sid in ("gag", "black-grouper"):
    reg_set(sid, "eez_sa", "vessel", lambda t, w: app(t,
        "From 28 Oct 2026: 2 gag and black grouper combined per private vessel per day (91 FR 61160).", w))
    for region in ("atlantic", "keys"):
        reg_set(sid, region, "vessel", lambda t, w: app(t or "No vessel limit found in the sources read.",
            "The state rule text was not read; FWC proposed matching the federal combined limit on 5 Oct 2026 "
            "(notice 31448290, not in force).", w))
    law_add(sid, "fr-91-61160", "fac-68b-14-006-4", "fac-68b-14-005-3")
for sid in ("scamp", "yellowmouth-grouper"):
    reg_set(sid, "eez_sa", "bag", lambda t, w: app(t,
        "No more than 1 scamp or yellowmouth combined (622.187(b)(2)(v)).", w))
    law_add(sid, "fr-91-63502")

# the Gulf 20-fathom closure, wherever a species card still carries it
OLD20 = "Recurring: closed Feb 1 to Mar 31 seaward of the 20-fathom line (622.34(d)). Amendment 62 proposes removing this closure (91 FR 41611, proposed Jul 2026; final status not checked)."
NEW20 = "The Feb 1 to Mar 31 closure seaward of 20 fathoms (former 622.34(d)) was removed on 2 Oct 2026 by Amendment 62 (91 FR 63502)."
for s in S["species"]:
    r = s["regions"].get("eez_gulf")
    if r and r.get("closed") and "622.34(d)" in r["closed"] and "removed on 2 Oct 2026" not in r["closed"]:
        if OLD20 in r["closed"]:
            r["closed"] = r["closed"].replace(OLD20, NEW20)
        else:
            sys.exit("species %s eez_gulf: unrecognised 622.34(d) wording: %r" % (s["id"], r["closed"]))
        done.append("species %s eez_gulf 20-fathom" % s["id"])
        if "fr-91-63502" not in s["law"]:
            s["law"].append("fr-91-63502")

ga = SPd["greater-amberjack"]["regions"].get("eez_gulf")
if ga and "91 FR 32360" not in (ga.get("closed") or ""):
    ga["closed"] = (ga.get("closed") or "").rstrip() + " 2026: closed 14 Oct 2026 through 31 Jul 2027 (91 FR 32360)."
    done.append("species greater-amberjack eez_gulf")

s = SPd["snook"]
s["spear_note"] = app(s["spear_note"], "R. 68B-21.006 also makes snook hook-and-line only, inside or outside Florida "
                      "waters, and prohibits possessing a snook while also possessing spear gear (r. 68B-21.006(3)).",
                      "species snook note")
law_add("snook", "fac-68b-21-006")
s = SPd["tarpon"]
s["spear_note"] = app(s["spear_note"], "R. 68B-32.006(2) repeats the ban for tarpon inside or outside Florida waters.",
                      "species tarpon note")
law_add("tarpon", "fac-68b-32-006-2")
for sid, gear in (("permit", "hook and line and spearing gear"), ("african-pompano", "hook and line gear or spearing")):
    for region in ("eez_sa", "eez_gulf"):
        reg_set(sid, region, "notes", lambda t, w: (
            "R. 68B-35.004 prohibits recreational harvest in adjacent federal waters by any gear other than " + gear +
            ", so that rule does not itself close the EEZ to spearing this species. The map keeps the conservative "
            "reading of r. 68B-20.005 until paragraph (5)(a) and the Special Permit Zone are read."
            if "68B-35.004" not in t else t))
    law_add(sid, "fac-68b-35-004")

gn = S["general_notes"]
for note in (
        "Reef fish must be landed whole: no fillets on the water, a pier, a fishing bridge or a jetty (r. 68B-14.006(4)); "
        "federal waters require head and fins intact (50 C.F.R. §§ 622.10(a), 622.186(a)).",
        "A boat harvesting reef fish in state waters, spearfishing included, must carry a venting tool or rigged "
        "descending device (r. 68B-14.005(3)).",
        "A speargun may not be used or possessed in or upon fresh water (r. 68A-23.002(7)); in national parks a "
        "loaded speargun in any vessel is prohibited (36 C.F.R. § 2.4(c))."):
    if note not in gn:
        gn.append(note)
        done.append("species general note")

R_V, S_V = "2026-10-08", "2026-10-08"
if done:
    S["version"] = S_V
io.open(RP, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1))
io.open(SP, "w", encoding="utf-8").write(json.dumps(S, ensure_ascii=False, separators=(",", ":")))
print(len(done), "changes")
for d in done:
    print(" ", d)
