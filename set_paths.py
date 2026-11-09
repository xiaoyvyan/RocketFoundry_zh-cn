# -*- coding: utf-8 -*-
"""Rewrite legacy root path D:\\001wyh\\rf -> D:\\001wyh\\newrf inside copied scripts."""
import os, glob, io

OLD = r"D:\001wyh\rf"
NEW = r"D:\001wyh\newrf"
for p in glob.glob(r"D:\001wyh\newrf\tools\*.py") + glob.glob(r"D:\001wyh\newrf\tools\*.ps1"):
    if os.path.basename(p) in ("pck_unpack.py", "diff_pck.py", "probe_pck.py", "probe_hash.py",
                               "probe_shift.py", "show_diff.py", "dll_us_diff.py", "show_us_ui.py",
                               "scn_strings.py", "set_paths.py"):
        continue
    s = io.open(p, encoding="utf-8").read()
    if OLD in s:
        s = s.replace(OLD, NEW)
        io.open(p, "w", encoding="utf-8", newline="").write(s)
        print("rewrote", os.path.basename(p))
