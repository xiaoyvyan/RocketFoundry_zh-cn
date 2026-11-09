# -*- coding: utf-8 -*-
"""打包汉化工程（脚本 + 译文 + 生成物），方便下个版本直接复用。"""
import os, zipfile, time

GAME = r"D:\001wyh\newrf"
OUT = os.path.join(GAME, "dist", "汉化工程-脚本与译文.zip")

include = [
    (r"tools", lambda n: n.endswith((".py", ".ps1", ".json"))),
    (r"translate", lambda n: n.endswith(".json")),
    (os.path.join("extract", "zh"), lambda n: n.endswith((".json", ".gd"))),
    ("build", lambda n: n.endswith((".txt",))),
    ("build\\fonts", lambda n: n.endswith(".ttf")),
]
extra_files = [r"override.cfg", r"汉化说明.md", r"使用说明.txt"]

t0 = time.time()
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for sub, keep in include:
        root = os.path.join(GAME, sub)
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d.lower() not in ("dumps", "__pycache__", "logs")]
            for f in filenames:
                if not keep(f):
                    continue
                p = os.path.join(dirpath, f)
                arc = os.path.relpath(p, GAME)
                z.write(p, arcname=arc)
                print("  +", arc, os.path.getsize(p))
    for f in extra_files:
        p = os.path.join(GAME, f)
        if os.path.exists(p):
            z.write(p, arcname=f)
            print("  +", f)
print("zip ->", OUT, os.path.getsize(OUT), "bytes", "%.1fs" % (time.time() - t0))
with zipfile.ZipFile(OUT) as z:
    print("entries:", len(z.infolist()), "testzip:", z.testzip() or "ok")
