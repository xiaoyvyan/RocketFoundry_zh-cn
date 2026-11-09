# -*- coding: utf-8 -*-
"""只读校验：#US 映射表里有没有把 Godot 类型名/场景节点名写进去。

用法：python check_us_map.py [map.json ...]
默认检查 us_map_hud2.json / us_map_hud3.json（当前生效的两张）。
命中即退出码 1 —— 这些键一旦写进 #US，会同时改掉代码里的类型查找和 GetNode()。
"""
import json, os, sys

TOOLS = r"D:\001wyh\newrf\tools"

TYPES = """Node Node2D Control Button Label RichTextLabel Panel PanelContainer PopupPanel Window
AcceptDialog ConfirmationDialog LineEdit TextEdit SpinBox Slider HSlider VSlider Range ProgressBar
TextureButton TextureProgressBar CheckBox CheckButton OptionButton MenuButton LinkButton ItemList Tree
PopupMenu Popup TabBar TabContainer ScrollContainer MarginContainer VBoxContainer HBoxContainer
GridContainer CenterContainer AspectRatioContainer FlowContainer SplitContainer HSplitContainer
VSplitContainer ColorRect TextureRect NinePatchRect BaseButton Container BoxContainer CanvasItem
Viewport Label3D Font FontFile SystemFont""".split()

LAYOUT = """Backdrop Background Border Bottom Body Card Cards Center Chrome Column Columns Content
Contents Context Deck Divider Edge Ends Footer Frame Frames Front Gap Grid Group Groups Handle Header
Heading Height Hidden Hide Icon Icons Inner Label Labels Layer Layers Left Line Lines Margin Marker
Middle Mount Outer Overlay Padding Panel Panels Pivot Placeholder Root Row Rows Rule Scroll Separator
Shadow Shell Spacer Spacing Stack Stroke Surface Tab Tabs Text Title Track Width Wrapper""".split()

RESERVED = set(TYPES) | {t.upper() for t in TYPES} | set(LAYOUT)

# 本作里被代码当节点名使用的自造词（HUD 就是 FlightScene 的节点名，译成「界面」会 Node not found）
GAME_NODES = ["HUD", "Backdrop", "BuilderScene", "FlightScene"]


def main():
    maps = sys.argv[1:] or [os.path.join(TOOLS, n) for n in ("us_map_hud2.json", "us_map_hud3.json")]
    bad_total = 0
    for m in maps:
        d = json.load(open(m, encoding="utf-8"))
        bad = sorted(k for k in d if k in RESERVED or k in GAME_NODES)
        bad_total += len(bad)
        print(("FAIL " if bad else "ok   ") + os.path.basename(m) + "  keys=" + str(len(d)))
        for k in bad:
            print("      reserved key:", repr(k), "->", repr(d[k]))
    if bad_total:
        print("命中保留词 %d 个，禁止写入 #US。" % bad_total)
        raise SystemExit(1)
    print("全部通过：生效映射表不含类型名/节点名。")


main()
