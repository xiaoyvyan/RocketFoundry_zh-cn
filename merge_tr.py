import json, os
T = r"D:\001wyh\newrf\translate"
hand = ["zh_test.json", "zh_ui_1.json", "zh_ui_2.json", "zh_ui_3.json"]
out = {}
for f in hand:
    p = os.path.join(T, f)
    if os.path.exists(p):
        for k, v in json.load(open(p, encoding="utf-8")).items():
            out.setdefault(k, v)
mtp = os.path.join(T, "zh_mt.json")
added = 0
if os.path.exists(mtp):
    for k, v in json.load(open(mtp, encoding="utf-8")).items():
        if k not in out and v:
            out[k] = v
            added += 1
json.dump(out, open(os.path.join(T, "zh_all.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("merged", len(out), "mt_new", added)
