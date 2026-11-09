# -*- coding: utf-8 -*-
import json, os, io

NEW = r"D:\001wyh\newrf\extract\assets"
OLD = r"D:\001wyh\newrf\_orig_extract\assets"

def load(p):
    return json.load(io.open(p, encoding="utf-8"))

out = []
ids = ["balloon", "fuel_cell", "mini_bomb", "probe_dish", "propeller_2_3", "reactor", "bomb"]
for pid in ids:
    pn = os.path.join(NEW, "parts", pid, "part.json")
    po = os.path.join(OLD, "parts", pid, "part.json")
    n = load(pn) if os.path.exists(pn) else {}
    o = load(po) if os.path.exists(po) else {}
    out.append("=" * 70)
    out.append("PART %s" % pid)
    out.append("name: %r" % n.get("name"))
    out.append("OLDname: %r" % o.get("name"))
    out.append("description: %r" % n.get("description"))
    out.append("OLDdescription: %r" % o.get("description"))
    for v in (n.get("variants") or []):
        out.append("  variant %s name=%r" % (v.get("key"), v.get("name")))
        out.append("  variant desc=%r" % v.get("description"))
    for i, s in enumerate(n.get("sizes") or []):
        if s.get("description"):
            out.append("  size[%d] desc=%r" % (i, s["description"]))
    tags = n.get("tags")
    out.append("tags: %r" % tags)
    for key in ("bomb", "fuelCell", "balloon", "command", "radioisotope"):
        if key in n:
            out.append("%s: %r" % (key, n[key]))

io.open(r"D:\001wyh\newrf\tools\parts_text.txt", "w", encoding="utf-8", newline="").write("\n".join(out))
print("written", len(out), "lines")
