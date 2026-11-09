# -*- coding: utf-8 -*-
"""Report #US map keys with zero hits in a DLL (strings that changed/disappeared)."""
import json, sys, os
sys.path.insert(0, r"D:\001wyh\newrf\tools")
import importlib.util

spec = importlib.util.spec_from_file_location("dpu", r"D:\001wyh\newrf\tools\dll_patch_us.py")
# dll_patch_us runs main() on import, so parse manually instead
import struct

def u16(b, o): return struct.unpack_from("<H", b, o)[0]
def u32(b, o): return struct.unpack_from("<I", b, o)[0]

def us_items(path):
    data = open(path, "rb").read()
    e = u32(data, 0x3C)
    nsec = u16(data, e + 6); optsz = u16(data, e + 20); opt = e + 24
    magic = u16(data, opt)
    dd = opt + (112 if magic == 0x20b else 96)
    cli_rva = u32(data, dd + 14 * 8)
    so = opt + optsz
    secs = []
    for i in range(nsec):
        vs, va, rs, rp = struct.unpack_from("<IIII", data, so + 40 * i + 8)
        secs.append((va, vs, rp, rs))
    def r2o(rva):
        for va, vs, rp, rs in secs:
            if va <= rva < va + max(vs, rs):
                return rp + (rva - va)
        raise ValueError(hex(rva))
    cli = r2o(cli_rva)
    md = r2o(u32(data, cli + 8))
    vl = u32(data, md + 12); p = md + 16 + vl + 2
    ns = u16(data, p); p += 2
    streams = {}
    for _ in range(ns):
        off, size = struct.unpack_from("<II", data, p); p += 8
        end = data.index(b"\0", p); name = data[p:end].decode(); p = end + 1
        p = (p + 3) & ~3
        streams[name] = (md + off, size)
    off, size = streams["#US"]
    out = []
    p = 1
    while p < size:
        n = data[off + p]
        if n & 0x80 == 0: ln = n; pre = 1
        elif n & 0xC0 == 0x80: ln = ((n & 0x3F) << 8) | data[off + p + 1]; pre = 2
        else: ln = ((n & 0x1F) << 24) | (data[off + p + 1] << 16) | (data[off + p + 2] << 8) | data[off + p + 3]; pre = 4
        if ln == 0 or p + pre + ln > size:
            break
        raw = data[off + p + pre:off + p + pre + ln]
        try:
            out.append(raw[:-1].decode("utf-16-le"))
        except Exception:
            pass
        p += pre + ln
    return out, data, off

dll = sys.argv[1] if len(sys.argv) > 1 else r"D:\001wyh\newrf\backup\RocketFoundry.dll.orig"
items, data, us_off = us_items(dll)
counts = {}
for t in items:
    counts[t] = counts.get(t, 0) + 1

maps = ["us_map_hud2.json", "us_map_hud3.json"]
for m in maps:
    d = json.load(open(os.path.join(r"D:\001wyh\newrf\tools", m), encoding="utf-8"))
    miss = [k for k in d if counts.get(k, 0) == 0]
    print("%s: keys=%d missing=%d" % (m, len(d), len(miss)))
    for k in miss:
        print("   MISSING", repr(k), "->", d[k])
