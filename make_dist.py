# -*- coding: utf-8 -*-
"""把汉化成品打成一个可直接解压游玩的压缩包。"""
import os, sys, zipfile, time

GAME = r"D:\001wyh\newrf"
OUT_DIR = os.path.join(GAME, "dist")
ZIP_NAME = "火箭铸造厂-v0.6.4-汉化版.zip"
FILES = ["RocketFoundry.exe", "RocketFoundry.pck", "datachannel.dll",
         "override.cfg", "webrtc-native.json", "使用说明.txt", "汉化说明.md"]

os.makedirs(OUT_DIR, exist_ok=True)
zp = os.path.join(OUT_DIR, ZIP_NAME)
t0 = time.time()
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in FILES:
        src = os.path.join(GAME, name)
        if not os.path.exists(src):
            print("MISS", name)
            continue
        z.write(src, arcname=name)
        print("added %-28s %12d bytes  %6.1fs" % (name, os.path.getsize(src), time.time() - t0))
print("zip ->", zp, os.path.getsize(zp), "bytes")
with zipfile.ZipFile(zp) as z:
    bad = z.testzip()
    print("testzip:", bad if bad else "ok")
    for i in z.infolist():
        print("  %-28s %12d  crc=%08x" % (i.filename, i.file_size, i.CRC))
