# -*- coding: utf-8 -*-
"""Dump all #US strings of a .NET assembly, diff two assemblies."""
import struct, sys, json, io, os

def u16(b, o): return struct.unpack_from("<H", b, o)[0]
def u32(b, o): return struct.unpack_from("<I", b, o)[0]

def parse(data):
    e = u32(data, 0x3C)
    assert data[e:e+4] == b"PE\0\0"
    nsec = u16(data, e+6); optsz = u16(data, e+20); opt = e+24
    magic = u16(data, opt)
    dd = opt + (112 if magic == 0x20b else 96)
    cli_rva = u32(data, dd + 14*8)
    so = opt + optsz
    secs = []
    for i in range(nsec):
        vs, va, rs, rp = struct.unpack_from("<IIII", data, so + 40*i + 8)
        secs.append((va, vs, rp, rs))
    def r2o(rva):
        for va, vs, rp, rs in secs:
            if va <= rva < va + max(vs, rs):
                return rp + (rva - va)
        raise ValueError(hex(rva))
    cli = r2o(cli_rva)
    md = r2o(u32(data, cli + 8))
    assert data[md:md+4] == b"BSJB"
    vl = u32(data, md + 12); p = md + 16 + vl + 2
    ns = u16(data, p); p += 2
    streams = {}
    for _ in range(ns):
        off, size = struct.unpack_from("<II", data, p); p += 8
        end = data.index(b"\0", p); name = data[p:end].decode(); p = end + 1
        p = (p + 3) & ~3
        streams[name] = (md + off, size)
    return streams

def entries(data, off, size):
    out = []
    p = 1
    while p < size:
        start = p; n = data[off + p]
        if n & 0x80 == 0: ln = n; pre = 1
        elif n & 0xC0 == 0x80: ln = ((n & 0x3F) << 8) | data[off+p+1]; pre = 2
        else: ln = ((n & 0x1F) << 24) | (data[off+p+1] << 16) | (data[off+p+2] << 8) | data[off+p+3]; pre = 4
        if ln == 0 or p + pre + ln > size:
            break
        raw = data[off+p+pre:off+p+pre+ln]
        try:
            txt = raw[:-1].decode("utf-16-le")
        except Exception:
            txt = ""
        out.append((txt, ln))
        p += pre + ln
    return out

def us_strings(path):
    data = open(path, "rb").read()
    st = parse(data)
    off, size = st["#US"]
    return entries(data, off, size)

old = r"D:\001wyh\newrf\_orig_extract\.godot\mono\publish\x86_64\RocketFoundry.dll"
new = r"D:\001wyh\newrf\extract\.godot\mono\publish\x86_64\RocketFoundry.dll"
o = us_strings(old)
n = us_strings(new)
oset = set(t for t, _ in o if t)
nset = set(t for t, _ in n if t)
print("old #US entries", len(o), "unique", len(oset), "bytes", os.path.getsize(old))
print("new #US entries", len(n), "unique", len(nset), "bytes", os.path.getsize(new))
added = nset - oset
removed = oset - nset
print("added", len(added), "removed", len(removed))
json.dump(dict(added=sorted(added), removed=sorted(removed)),
          open(r"D:\001wyh\newrf\tools\dll_us_diff.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("\n== added samples (>=2 chars, printable-ish) ==")
cnt = 0
for s in sorted(added, key=len):
    if len(s) < 2 or len(s) > 200:
        continue
    if not any(c.isalpha() for c in s):
        continue
    print("  +", repr(s))
    cnt += 1
    if cnt >= 120:
        break
