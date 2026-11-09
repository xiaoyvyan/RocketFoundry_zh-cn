# -*- coding: utf-8 -*-
"""v0.6.4 显示层构建：合并译文 -> 打回原版 DLL 并注入 #US 补丁 -> 算字集 -> 换中文字体
   -> 写译文表 -> 打包 pck -> 覆盖游戏 pck -> 写 override.cfg
用法: python build_layer.py [out.pck]
"""
import json, os, shutil, subprocess, sys, glob, re

RF = r"D:\001wyh\newrf"
PY = sys.executable
TR = os.path.join(RF, "translate")
EXTRACT = os.path.join(RF, "extract")
TOOLS = os.path.join(RF, "tools")
BUILD = os.path.join(RF, "build")
DLL_EXTRACT = os.path.join(EXTRACT, ".godot", "mono", "publish", "x86_64", "RocketFoundry.dll")
DLL_ORIG = os.path.join(RF, "backup", "RocketFoundry.dll.orig")
DLL_RUNTIME = os.path.join(os.environ["LOCALAPPDATA"], "data_RocketFoundry_windows_x86_64", "RocketFoundry.dll")


def run(args, log=None):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if log:
        open(log, "w", encoding="utf-8").write(r.stdout + "\n" + r.stderr)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise SystemExit("step failed: %s" % args)
    return r.stdout


def main(out_pck):
    os.makedirs(BUILD, exist_ok=True)

    # 1. 合并译文
    print(run([PY, "-u", os.path.join(TOOLS, "merge_tr.py")]))

    # 2. DLL 回到原版，把 #US 补丁打进 pck 里的程序集
    shutil.copyfile(DLL_ORIG, DLL_EXTRACT)
    for m in ("us_map_hud2.json", "us_map_hud3.json", "us_map_hud4.json", "us_map_hud5.json", "us_map_hud6.json"):
        print(run([PY, "-u", os.path.join(TOOLS, "dll_patch_us.py"),
                   "patch", DLL_EXTRACT, os.path.join(TOOLS, m)]))
    os.makedirs(os.path.dirname(DLL_RUNTIME), exist_ok=True)
    shutil.copyfile(DLL_EXTRACT, DLL_RUNTIME)
    print("DLL patched + synced ->", DLL_RUNTIME)

    # 3. 字集：译文表 + 所有 assets JSON 里的中文（零件说明、天体名、站点名等都会被绘制）
    tr = json.load(open(os.path.join(TR, "zh_all.json"), encoding="utf-8"))
    chars = set(chr(c) for c in range(0x20, 0x7F))
    chars |= set("\u200b\u3000，。、；：？！…—·《》「」『』（）【】％０１２３４５６７８９“”‘’～／·＋－±×÷≤≥°′″")
    for k, v in tr.items():
        chars |= set(v)
        chars |= set(k)
    cjk = re.compile(r"[\u2e80-\u9fff\uff00-\uffef\u3000-\u303f]")
    for p in glob.glob(os.path.join(EXTRACT, "assets", "**", "*.json"), recursive=True):
        try:
            txt = open(p, encoding="utf-8").read()
        except Exception:
            continue
        chars |= set(cjk.findall(txt))
    cs = "".join(sorted(chars))
    open(os.path.join(BUILD, "charset.txt"), "w", encoding="utf-8", newline="\n").write(cs)
    print("charset chars:", len(cs))

    # 4. 字体换成含中文字形的子集
    print(run([PY, "-u", os.path.join(TOOLS, "font_patch.py"), EXTRACT],
              os.path.join(TOOLS, "fontpatch.log")))

    # 5. 译文表写进 pck
    zh_dir = os.path.join(EXTRACT, "zh")
    os.makedirs(zh_dir, exist_ok=True)
    table_path = os.path.join(zh_dir, "zh_ui.json")
    clean = {}
    zw = {"\u200b": "", "\u200c": "", "\u200d": "", "\ufeff": "", "\u00a0": " "}
    for k, v in tr.items():
        ck = k
        for z in zw:
            ck = ck.replace(z, zw[z])
        ck = ck.strip()
        if ck and ck not in clean:
            clean[ck] = v
    json.dump(clean, open(table_path, "w", encoding="utf-8"), ensure_ascii=False)
    print("table written:", table_path, len(clean))

    # 6. 打包
    print(run([PY, "-u", os.path.join(TOOLS, "pack_pck.py"), out_pck]))

    # 7. 覆盖游戏 pck
    shutil.copyfile(out_pck, os.path.join(RF, "RocketFoundry.pck"))
    print("pck installed ->", os.path.join(RF, "RocketFoundry.pck"))

    # 8. override.cfg 注册 autoload
    cfg = os.path.join(RF, "override.cfg")
    open(cfg, "w", encoding="utf-8", newline="\n").write('[autoload]\n\nZhUi="*res://zh/ui_zh.gd"\n')
    print("override.cfg ->", cfg)
    print("done.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(BUILD, "RocketFoundry.zh.pck"))
