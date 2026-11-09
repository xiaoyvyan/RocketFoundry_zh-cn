# -*- coding: utf-8 -*-
"""Verify a packed pck against the extract tree (all entries, md5 + byte comparison)."""
import struct, hashlib, os, sys, json

pck = sys.argv[1] if len(sys.argv) > 1 else r"D:\001wyh\newrf\RocketFoundry.pck"
src = r"D:\001wyh\newrf\extract"
d = open(pck, "rb").read()
assert d[:4] == b"GDPC"
ver, = struct.unpack_from("<I", d, 4)
flags, = struct.unpack_from("<I", d, 20)
fb, = struct.unpack_from("<Q", d, 24)
dir_off, = struct.unpack_from("<Q", d, 32)
cnt, = struct.unpack_from("<I", d, dir_off)
o = dir_off + 4
bad = missing = 0
last_dir_end = 0
for i in range(cnt):
    ln, = struct.unpack_from("<I", d, o)
    path = d[o + 4:o + 4 + ln].rstrip(b"\0").decode()
    o += 4 + ln
    off, sz = struct.unpack_from("<QQ", d, o); o += 16
    md5 = d[o:o + 16]; o += 16
    o += 4
    ao = off + fb
    data = d[ao:ao + sz]
    if hashlib.md5(data).digest() != md5 or len(data) != sz:
        bad += 1
        print("BAD", path)
    p = os.path.join(src, path.replace("/", os.sep))
    if not os.path.isfile(p):
        missing += 1
        print("NO_SRC", path)
print("pack v%d flags=%d file_base=%d dir_off=%d entries=%d dir_end=%d size=%d" % (ver, flags, fb, dir_off, cnt, o, len(d)))
print("bad=%d missing_src=%d" % (bad, missing))
