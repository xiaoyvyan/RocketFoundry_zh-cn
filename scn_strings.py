# -*- coding: utf-8 -*-
"""Extract text candidates from Godot .scn (binary resource): UTF-8 runs + UTF-32LE runs."""
import re, sys, json, os

PRINT = re.compile(rb"[\x20-\x7e]{4,}")

def utf32_runs(data):
    out = []
    i = 0
    n = len(data)
    cur = []
    while i + 4 <= n:
        lo = data[i]; mid = data[i+1]; hi = data[i+2]; top = data[i+3]
        if top == 0 and (mid in (0, )) and lo >= 0x20:
            ch = lo
        elif top == 0 and mid != 0 and 0x4e00 <= ((mid << 8) | lo) <= 0x9fff or (top == 0 and mid >= 0x30 and lo):
            ch = (mid << 8) | lo
        else:
            ch = None
        if ch is not None and (ch >= 0x20):
            cur.append(chr(ch))
            i += 4
        else:
            if len(cur) >= 4:
                out.append("".join(cur))
            cur = []
            i += 1
    if len(cur) >= 4:
        out.append("".join(cur))
    return out

def strings(path):
    d = open(path, "rb").read()
    s = set()
    for m in PRINT.finditer(d):
        s.add(m.group().decode("ascii"))
    s |= set(utf32_runs(d))
    return s

if __name__ == "__main__":
    a_dir = r"D:\001wyh\newrf\_orig_extract\.godot\exported\133200997"
    b_dir = r"D:\001wyh\newrf\extract\.godot\exported\133200997"
    same_name = []
    for f in sorted(os.listdir(a_dir)):
        if not f.endswith(".scn"):
            continue
        a = strings(os.path.join(a_dir, f))
        b = strings(os.path.join(b_dir, f)) if os.path.exists(os.path.join(b_dir, f)) else set()
        added = b - a
        # only human-looking: has lowercase words or spaces, no weird symbols
        cand = sorted([x for x in added if len(x) < 120 and any(c.isalpha() for c in x)])
        if cand:
            print("==", f.split("-")[-1], "added", len(cand))
            for x in cand[:80]:
                print("   +", repr(x))
