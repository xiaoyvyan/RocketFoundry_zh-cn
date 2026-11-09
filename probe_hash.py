# -*- coding: utf-8 -*-
import struct, hashlib, json, os, sys

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

ok = bad = 0
samples = []
for path, off, sz, md5, fl in rows:
    data = d[off:off + sz]
    if hashlib.md5(data).digest() == md5:
        ok += 1
    else:
        bad += 1
        if len(samples) < 4 and sz < 3_000_000:
            samples.append((path, off, sz, md5, data))
print("md5 ok", ok, "bad", bad)

for path, off, sz, md5, data in samples:
    print("=" * 60)
    print(path, "off", off, "size", sz)
    print("head", data[:16])
    print("stored   ", md5.hex())
    cands = {
        "md5": hashlib.md5(data).hexdigest(),
        "md5[:16]path": hashlib.md5(path.encode()).hexdigest(),
        "sha1[:16]": hashlib.sha1(data).hexdigest()[:32],
        "sha256[:16]": hashlib.sha256(data).hexdigest()[:32],
        "blake2b16": hashlib.blake2b(data, digest_size=16).hexdigest(),
        "blake2s16": hashlib.blake2s(data, digest_size=16).hexdigest(),
    }
    for k, v in cands.items():
        print("  %-14s %s %s" % (k, v, "<== MATCH" if v == md5.hex() else ""))
