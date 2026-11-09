# -*- coding: utf-8 -*-
"""Repack a Godot 4 pck from an extracted tree, mirroring the original header layout.

usage: python pack_pck.py <out.pck>
Reads <extract>/_manifest.json (entry order, engine version, file_base) and
writes entries with offsets relative to file_base (global flag PACK_REL_FILEBASE).
"""
import struct, os, hashlib, sys, json

ROOT = r"D:\001wyh\newrf"
SRC = os.path.join(ROOT, "extract")
MAN = os.path.join(SRC, "_manifest.json")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "build", "RocketFoundry.zh.pck")
ALIGN = 16

man = json.load(open(MAN, encoding="utf-8"))
engine = man.get("engine", [4, 7, 2])
paths = [e["path"] for e in man["entries"]]
have = set(paths)
for extra in ("zh/ui_zh.gd", "zh/zh_ui.json"):
    if extra not in have and os.path.exists(os.path.join(SRC, extra.replace("/", os.sep))):
        paths.append(extra)
        have.add(extra)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
missing = []
with open(OUT, "wb") as f:
    f.write(b"\0" * 104)
    pad = (-f.tell()) % ALIGN
    f.write(b"\0" * pad)
    fb = f.tell()

    entries = []
    for p in paths:
        src = os.path.join(SRC, p.replace("/", os.sep))
        if not os.path.isfile(src):
            missing.append(p)
            continue
        data = open(src, "rb").read()
        ofs = f.tell()
        f.write(data)
        pad = (-f.tell()) % ALIGN
        f.write(b"\0" * pad)
        entries.append((p, ofs, len(data), hashlib.md5(data).digest()))

    pad = (-f.tell()) % ALIGN
    f.write(b"\0" * pad)
    dir_off = f.tell()

    f.write(struct.pack("<I", len(entries)))
    for p, ofs, sz, md5 in entries:
        raw = p.encode()
        pad = (-len(raw)) % 4
        f.write(struct.pack("<I", len(raw) + pad))
        f.write(raw)
        f.write(b"\0" * pad)
        f.write(struct.pack("<QQ", ofs - fb, sz))
        f.write(md5)
        f.write(struct.pack("<I", 0))

    f.seek(0)
    f.write(struct.pack("<I", 0x43504447))          # GDPC
    f.write(struct.pack("<I", man.get("pack_version", 4)))
    f.write(struct.pack("<III", *engine))
    f.write(struct.pack("<I", 2))                    # PACK_REL_FILEBASE
    f.write(struct.pack("<Q", fb))
    f.write(struct.pack("<Q", dir_off))
    f.write(b"\0" * 64)

print("files", len(entries), "file_base", fb, "dir_off", hex(dir_off),
      "size", os.path.getsize(OUT), "missing", missing[:5], "->", OUT)
