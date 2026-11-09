# -*- coding: utf-8 -*-
"""Audit data-layer localization: leftover English names/descriptions in parts & assets."""
import json, io, os, glob, re

BASE = r"D:\001wyh\newrf\extract\assets"

def is_cjk(s):
    return bool(re.search(r"[\u4e00-\u9fff]", s))

print("== part dirs ==")
dirs = sorted(os.listdir(os.path.join(BASE, "parts")))
print("count", len(dirs))
print("\n== part.json name/description with no CJK ==")
bad = 0
for p in sorted(glob.glob(os.path.join(BASE, "parts", "*", "part.json"))):
    d = json.load(io.open(p, encoding="utf-8"))
    nm = d.get("name", "")
    if nm and not is_cjk(nm):
        print("  NAME", os.path.basename(os.path.dirname(p)), "->", nm)
        bad += 1
    ds = d.get("description")
    if ds and not is_cjk(ds):
        print("  DESC", os.path.basename(os.path.dirname(p)), "->", ds[:80])
        bad += 1
    for v in (d.get("variants") or []):
        if v.get("name") and not is_cjk(v["name"]):
            print("  VAR", d.get("id"), v.get("key"), "->", v["name"])
            bad += 1
        if v.get("description") and not is_cjk(v["description"]):
            print("  VARDESC", d.get("id"), v.get("key"), "->", v["description"][:60])
            bad += 1
    for s in (d.get("sizes") or []):
        if s.get("description") and not is_cjk(s["description"]):
            print("  SIZEDESC", d.get("id"), "->", s["description"][:60])
            bad += 1
print("total bad", bad)

print("\n== catalog entries: name not CJK ==")
c = json.load(io.open(os.path.join(BASE, "catalogs", "stock_parts.json"), encoding="utf-8"))
for e in c["entries"]:
    nm = (e.get("definition") or {}).get("name", "")
    if nm and not is_cjk(nm):
        print("  ", e.get("source"), "->", nm)

print("\n== bodies/other jsons: English name fields sample ==")
for p in sorted(glob.glob(os.path.join(BASE, "bodies", "*", "*.json"))) + sorted(glob.glob(os.path.join(BASE, "catalogs", "*.json"))):
    try:
        d = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    txt = json.dumps(d, ensure_ascii=False)
    if '"name"' in txt:
        m = re.findall(r'"name":\s*"([^"]+)"', txt)
        cjk = sum(1 for x in m if is_cjk(x))
        print("  %-50s names=%3d cjk=%3d" % (os.path.relpath(p, BASE), len(m), cjk))
