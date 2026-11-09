# -*- coding: utf-8 -*-
"""Godot 4 pck unpacker with offset-mode auto-detection (pack v4 observed in Rocket Foundry).

usage: python pck_unpack.py <pck> <outdir> [manifest.json]
"""
import struct, sys, os, hashlib, json, collections

pck = sys.argv[1]
out = sys.argv[2]
manifest = sys.argv[3] if len(sys.argv) > 3 else os.path.join(out, "_manifest.json")

d = open(pck, "rb").read()
assert d[:4] == b"GDPC"
ver = struct.unpack_from("<I", d, 4)[0]
major, minor, patch = struct.unpack_from("<III", d, 8)
flags = struct.unpack_from("<I", d, 20)[0]
file_base = struct.unpack_from("<Q", d, 24)[0]
dir_off = struct.unpack_from("<Q", d, 32)[0]
print("pack v%d engine %d.%d.%d flags %d file_base %d dir_off %d" % (ver, major, minor, patch, flags, file_base, dir_off))

count = struct.unpack_from("<I", d, dir_off)[0]
o = dir_off + 4
raw_entries = []
for i in range(count):
    ln = struct.unpack_from("<I", d, o)[0]
    path = d[o + 4:o + 4 + ln].rstrip(b"\x00").decode("utf-8", "replace")
    o += 4 + ln
    off, sz = struct.unpack_from("<QQ", d, o); o += 16
    md5 = d[o:o + 16]; o += 16
    fl = struct.unpack_from("<I", d, o)[0]; o += 4
    raw_entries.append((path, off, sz, md5, fl))
print("entries", count, "dir_end", o, "file_size", len(d))

mode_abs = mode_rel = mode_none = 0
entries = []
bad = []
for path, off, sz, md5, fl in raw_entries:
    data = None
    mode = None
    for name, ao in (("abs", off), ("rel", off + file_base)):
        if 0 <= ao and ao + sz <= len(d):
            chunk = d[ao:ao + sz]
            if sz and hashlib.md5(chunk).digest() == md5:
                data, mode = chunk, name
                break
    if data is None:
        # fall back: try abs even if hash differs
        ao = off + file_base if (off + sz <= len(d) and off + file_base + sz <= len(d)) else off
        if ao + sz > len(d):
            bad.append((path, "OOR"))
            continue
        data, mode = d[ao:ao + sz], "guess"
        mode_none += 1
        bad.append((path, "HASH"))
    if mode == "abs":
        mode_abs += 1
    elif mode == "rel":
        mode_rel += 1
    entries.append(dict(path=path, off=off, size=sz, flags=fl, index=len(entries), offset_mode=mode))
    dst = os.path.join(out, path.replace("/", os.sep))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)

print("offset modes: abs=%d rel=%d unresolved=%d" % (mode_abs, mode_rel, mode_none))
print("bad", len(bad), bad[:5])
json.dump(dict(pack_version=ver, engine=[major, minor, patch], flags=flags,
               file_base=file_base, offset_mode_default="rel",
               entries=entries), open(manifest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("extracted", len(entries), "->", out)
