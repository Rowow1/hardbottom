# -*- coding: utf-8 -*-
"""Release text pass of 6 Oct 2026 for data/zones-local.json. Run after patch-zones-local-2026-09-30.py.

Applies the prose fields (n, s, src, flag) and kind recorded in tools/release-2026-10-06/zones-local-text.json:
closure-only wording, no em or en dashes, and Biscayne NP drawn amber ("warn") instead of green, so no zone
reads as open water. Never touches coordinates or law ids. Idempotent.
"""
import io, json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = os.path.join(ROOT, "data", "zones-local.json")
T = json.load(io.open(os.path.join(ROOT, "tools", "release-2026-10-06", "zones-local-text.json"), encoding="utf-8"))
d = json.load(io.open(P, encoding="utf-8"))
for z in d["zones"]:
    for k, v in T.get(z["id"], {}).items():
        z[k] = v
io.open(P, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
print("zones-local.json: release text applied to", sum(1 for z in d["zones"] if z["id"] in T), "zones")
