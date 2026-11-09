# -*- coding: utf-8 -*-
"""Diff two extracted pck trees: added / removed / changed files."""
import os, hashlib, sys, json, collections

A = r"D:\001wyh\newrf\_orig_extract"   # old v0.6.1 pristine
B = r"D:\001wyh\newrf\extract"          # new

def walk(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root).replace("\\", "/")
            if rel.startswith("_manifest"):
                continue
            out[rel] = os.path.getsize(p)
    return out

a, b = walk(A), walk(B)
added = sorted(set(b) - set(a))
removed = sorted(set(a) - set(b))
common = sorted(set(a) & set(b))
print("old files", len(a), "new files", len(b))
print("added", len(added), "removed", len(removed), "common", len(common))

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        while True:
            c = f.read(1 << 20)
            if not c:
                break
            h.update(c)
    return h.digest()

changed = []
same = 0
for rel in common:
    pa = os.path.join(A, rel.replace("/", os.sep))
    pb = os.path.join(B, rel.replace("/", os.sep))
    if os.path.getsize(pa) == os.path.getsize(pb) and md5(pa) == md5(pb):
        same += 1
    else:
        changed.append(rel)
print("changed", len(changed), "identical", same)

def ext(x):
    return os.path.splitext(x)[1].lower()
print("\n== added by ext ==")
for k, v in collections.Counter(ext(x) for x in added).most_common():
    print("  %-10s %d" % (k, v))
print("\n== changed by ext ==")
for k, v in collections.Counter(ext(x) for x in changed).most_common():
    print("  %-10s %d" % (k, v))
print("\n== removed by ext ==")
for k, v in collections.Counter(ext(x) for x in removed).most_common():
    print("  %-10s %d" % (k, v))

json.dump(dict(added=added, removed=removed, changed=changed),
          open(r"D:\001wyh\newrf\tools\diff_files.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nadded list (first 40):")
for x in added[:40]:
    print("  +", x)
print("changed list (non-imported/exported, first 60):")
n = 0
for x in changed:
    if x.startswith(".godot/"):
        continue
    print("  ~", x, a[x], "->", b[x])
    n += 1
    if n >= 60:
        break
