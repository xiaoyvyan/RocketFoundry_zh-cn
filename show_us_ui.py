# -*- coding: utf-8 -*-
import json, re

d = json.load(open(r"D:\001wyh\newrf\tools\dll_us_diff.json", encoding="utf-8"))
added = d["added"]
removed = d["removed"]

def ui_like(s):
    if len(s) < 3:
        return False
    if not re.search(r"[A-Za-z]", s):
        return False
    # must look like a phrase: contains a space and a lowercase word, or ends with punctuation
    words = s.split()
    has_lower = any(w[:1].islower() for w in words)
    return (len(words) >= 2 and has_lower) or s.endswith((".", "?", "!", "…"))

print("== ADDED ui-like (%d/%d) ==" % (sum(1 for x in added if ui_like(x)), len(added)))
for x in added:
    if ui_like(x):
        print("+", repr(x))
print("\n== REMOVED ui-like (%d/%d) ==" % (sum(1 for x in removed if ui_like(x)), len(removed)))
for x in removed:
    if ui_like(x):
        print("-", repr(x))
