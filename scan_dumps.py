# -*- coding: utf-8 -*-
"""Scan zh_dump captures for leftover English-looking values that are not in the table."""
import os, glob, re, json, io

DUMPS = r"D:\001wyh\newrf\tools\dumps"
TABLE = json.load(io.open(r"D:\001wyh\newrf\translate\zh_all.json", encoding="utf-8"))

def norm(s):
    s = s.replace("\u200b", "").replace("\u200c", "").replace("\u200d", "").replace("\ufeff", "")
    return s.strip().lower()

lower = {}
for k, v in TABLE.items():
    lower.setdefault(norm(k), v)

WORD = re.compile(r"[A-Za-z]{2,}")
CJK = re.compile(r"[\u4e00-\u9fff]")

def englishish(s):
    if not WORD.search(s):
        return False
    # proportion of ascii letters vs length
    letters = sum(1 for c in s if c.isalpha())
    cjk = len(CJK.findall(s))
    return letters >= 4 and cjk == 0

rows = []
for p in sorted(glob.glob(os.path.join(DUMPS, "*.txt"))):
    for line in io.open(p, encoding="utf-8"):
        line = line.rstrip("\n")
        if "|" not in line:
            continue
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        cls, prop, val = parts
        if not englishish(val):
            continue
        if norm(val) in lower:
            continue
        rows.append((os.path.basename(p), cls, prop, val))

seen = set()
for f, cls, prop, val in rows:
    key = (cls, prop, val)
    if key in seen:
        continue
    seen.add(key)
    print("%-16s %-14s %-14s %r" % (f[:16], cls[:14], prop[:14], val[:150]))
print("\ntotal unique", len(seen))
