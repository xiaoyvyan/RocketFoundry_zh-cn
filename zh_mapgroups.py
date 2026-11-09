# -*- coding: utf-8 -*-
"""Translate mapGroup titles in structure JSON files (display-only grouping on maps/lists)."""
import glob, io, os, shutil, time

MAP = {
 "Baikonur Cosmodrome": "拜科努尔航天中心",
 "Michigan Spaceport": "密歇根航天港",
 "Michigan Crawler Annex": "密歇根履带区",
 "Plesetsk Cosmodrome": "普列谢茨克航天中心",
 "Starbase Texas": "德克萨斯星舰基地",
}

root = r"D:\001wyh\newrf\extract\assets"
bak = r"D:\001wyh\newrf\backup\mgroup_bak_" + time.strftime("%Y%m%d_%H%M%S")
files = glob.glob(os.path.join(root, "structures") + r"\**\*.json", recursive=True)
changed = 0
for f in files:
    raw = io.open(f, encoding="utf-8", newline="").read()
    new = raw
    for en, zh in MAP.items():
        new = new.replace('"mapGroup": "%s"' % en, '"mapGroup": "%s"' % zh)
    if new != raw:
        if not os.path.isdir(bak):
            os.makedirs(bak)
        shutil.copy2(f, os.path.join(bak, os.path.relpath(f, root).replace("\\", "_")))
        io.open(f, "w", encoding="utf-8", newline="").write(new)
        changed += 1
print("changed", changed, "of", len(files), "bak", bak)
