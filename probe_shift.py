# -*- coding: utf-8 -*-
import struct, hashlib

pck = r"D:\001wyh\newrf\RocketFoundry.pck"
d = open(pck, "rb").read()
dir_off = struct.unpack_from("<Q", d, 32)[0]
count = struct.unpack_from("<I", d, dir_off)[0]
o = dir_off + 4
rows = []
for i in range(count):
    ln = struct.unpack_from("<I", d, o)[0]
    path = d[o + 4:o + 4 + ln].rstrip(b"\x00").decode("utf-8", "replace")
    o += 4 + ln
    off, sz = struct.unpack_from("<QQ", d, o); o += 16
    md5 = d[o:o + 16]; o += 16
    fl = struct.unpack_from("<I", d, o)[0]; o += 4
    rows.append((path, off, sz, md5, fl))

# pick a mismatching entry
target = None
for r in rows:
    if r[0].endswith("engine_lab_slider_row.scn"):
        target = r
        break
path, off, sz, md5, fl = target
print("target", path, off, sz, md5.hex())

found = []
for delta in range(-4096, 4097, 4):
    s = off + delta
    if s < 0 or s + sz > len(d):
        continue
    if hashlib.md5(d[s:s + sz]).digest() == md5:
        found.append(delta)
print("delta matches:", found[:10], "count", len(found))

# also check whether data at 'off' equals some other entry's whole data
if not found:
    # look for RSRC magic near off
    idx = d.rfind(b"RSRC", off - 4096, off + 64)
    print("nearest RSRC before:", idx, "delta", idx - off if idx > 0 else None)
    print("bytes around off:", d[off-8:off+8])
