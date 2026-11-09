# -*- coding: utf-8 -*-
import json
d = json.load(open(r"D:\001wyh\newrf\tools\diff_files.json", encoding="utf-8"))
print("ADDED .cs/.json/.import:")
for x in d["added"]:
    if x.endswith((".cs", ".json", ".import")):
        print("  +", x)
print("\nADDED .ctex:")
for x in d["added"]:
    if x.endswith(".ctex"):
        print("  +", x)
print("\nREMOVED:")
for x in d["removed"]:
    print("  -", x)
print("\nCHANGED:")
for x in d["changed"]:
    print("  ~", x)
