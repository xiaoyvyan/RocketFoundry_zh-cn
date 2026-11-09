# -*- coding: utf-8 -*-
import json, io, os, glob, re

def is_cjk(s):
    return bool(re.search(r"[\u4e00-\u9fff]", s))

for root, tag in ((r"D:\001wyh\rf\extract\assets", "OLD-LOCALIZED"), (r"D:\001wyh\newrf\extract\assets", "NEW")):
    p = os.path.join(root, "catalogs", "stock_bodies.json")
    d = json.load(io.open(p, encoding="utf-8"))
    e = d.get("entries") or d.get("bodies") or []
    names = [(x.get("definition") or x).get("name") for x in e[:8]]
    print(tag, "stock_bodies entries", len(e), "first names", names)

print("\n=== residual English in NEW part.json ===")
for p in sorted(glob.glob(r"D:\001wyh\newrf\extract\assets\parts\*\part.json")):
    d = json.load(io.open(p, encoding="utf-8"))
    pid = d.get("id")
    for v in (d.get("variants") or []):
        if v.get("name") and not is_cjk(v["name"]):
            print("[VARNAME] %s.%s\t%s" % (pid, v.get("key"), v["name"]))
        if v.get("description") and not is_cjk(v["description"]):
            print("[VARDESC] %s.%s\t%s" % (pid, v.get("key"), v["description"]))
    for i, s in enumerate(d.get("sizes") or []):
        if s.get("description") and not is_cjk(s["description"]):
            print("[SIZEDESC] %s[%d]\t%s" % (pid, i, s["description"]))
