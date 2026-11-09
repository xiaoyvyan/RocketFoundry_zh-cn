# -*- coding: utf-8 -*-
"""把 109 个零件的显示名汉化：写回 assets/parts/*/part.json 与 assets/catalogs/stock_parts.json。"""
import json, io, os, glob, shutil, time

BASE = r"D:\001wyh\newrf\extract\assets"
BAK = r"D:\001wyh\newrf\backup\parts_bak_%s" % time.strftime("%Y%m%d_%H%M%S")

NAME = {
 "alien": "异星乘员",
 "asteroid_cruithne": "克鲁特尼",
 "asteroid_leo_1": "小行星 001",
 "astronaut": "宇航员",
 "balloon": "气球",
 "battery_deep": "电池",
 "battery_slim": "薄型电池",
 "bomb": "核弹",
 "cable_eyelet": "钢索端头",
 "cargo_container": "货柜",
 "colony_launch_pad": "殖民地发射台",
 "command_cockpit": "驾驶舱",
 "command_pallas": "智神星",
 "command_probe": "指令探针",
 "command_vesta": "灶神星",
 "concrete_block": "混凝土块",
 "decoupler": "径向分离器",
 "deep_space_telescope": "深空望远镜",
 "docking_port": "对接口",
 "drill": "螺旋钻",
 "engine_albatross": "信天翁固体助推器",
 "engine_condor": "神鹰",
 "engine_harrier": "鹞式",
 "engine_hawk": "鹰",
 "engine_hawk_v": "鹰-V",
 "engine_heron": "苍鹭",
 "engine_ion": "离子发动机",
 "engine_kestrel": "红隼",
 "engine_kite": "鹞",
 "engine_osprey": "鱼鹰",
 "engine_peregrine": "游隼",
 "engine_phoenix": "凤凰",
 "engine_raptor": "猛禽",
 "engine_shrike": "伯劳",
 "engine_swift": "雨燕",
 "engine_tern": "燕鸥",
 "engine_vernier": "游标微调机",
 "exotic_fuel_tank": "特种燃料箱",
 "fairing_base": "整流罩底座",
 "fairing_body": "整流罩罩体",
 "fairing_nosecone": "整流罩头锥",
 "fin": "后掠尾翼",
 "fin_delta": "三角尾翼",
 "fin_delta_clip": "截角三角尾翼",
 "fin_delta_tall": "钝头三角尾翼",
 "fin_raked": "斜削尾翼",
 "fin_tail": "垂直尾翼",
 "flight_termination_system": "飞行终止系统",
 "flotation_block": "浮力块",
 "fuel_depot": "燃料库",
 "fuel_tank": "燃料箱",
 "fuel_cell": "燃料电池",
 "geo_scanner": "地质扫描仪",
 "grabber_4_4": "高级抓取单元",
 "grid_fin": "格栅舵",
 "ground_anchor": "地面锚",
 "habitat": "居住舱",
 "half_nosecone": "半锥头罩",
 "half_nosecone_pointed": "半尖头罩",
 "heatshield": "隔热盾",
 "helicopter_rotor": "直升机旋翼",
 "jet_tail": "喷气尾翼",
 "jet_wing": "喷气机翼",
 "joint_revolute": "转动关节",
 "ladder": "梯子",
 "landing_leg": "着陆腿",
 "landing_leg_mantis": "螳螂着陆腿",
 "laser_cannon": "激光炮",
 "launch_escape_apollo": "阿波罗逃逸塔",
 "material_bin": "金属料箱",
 "mining_rig": "采矿装置",
 "nav_light": "航行灯",
 "nav_light_round": "圆形航行灯",
 "nosecone": "头锥",
 "nosecone_pointed": "尖头锥",
 "parachute": "降落伞",
 "piston": "液压活塞",
 "pontoon": "浮筒",
 "probe_core": "探针核心",
 "probe_dish": "碟形探针",
 "probe_ishtar": "伊什塔尔探针",
 "propeller_2_3": "电动螺旋桨",
 "propeller_marine": "船用螺旋桨",
 "propeller_piston_2_3": "活塞螺旋桨",
 "rcs_2_3": "RCS 推进器",
 "rcs_4_4": "四向 RCS",
 "reaction_wheel": "反作用轮",
 "reactor": "反应堆",
 "rope": "绳索",
 "rope_anchor": "绳索锚点",
 "rover_seat": "巡视座椅",
 "rtg": "同位素电源",
 "separator": "级间分离器",
 "side_ladder": "侧梯",
 "solar_array_wing": "太阳能电池翼",
 "solar_panel": "太阳能板",
 "solar_sail": "太阳帆",
 "stabilizer": "尾部稳定翼",
 "station_airlock": "气闸舱",
 "station_cupola": "穹顶舱",
 "station_greenhouse": "温室",
 "tank_sphere": "球形贮箱",
 "tank_toroid": "环形贮箱",
 "truss": "金属桁架",
 "truss_corner": "桁架转角",
 "truss_separator": "桁架分离器",
 "warehouse": "金属仓库",
 "wave_motion_gun": "波动炮",
 "wheel_rover": "巡视车轮",
 "winch_4_4": "动力绞盘",
 "winch_cable": "绞盘钢索",
 "wing": "机翼",
}

def dump(path, obj):
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")

changed = 0
for p in glob.glob(os.path.join(BASE, "parts", "*", "part.json")):
    d = json.load(io.open(p, encoding="utf-8"))
    pid = d.get("id")
    if pid in NAME and d.get("name") != NAME[pid]:
        os.makedirs(BAK, exist_ok=True)
        shutil.copy2(p, os.path.join(BAK, os.path.basename(os.path.dirname(p)) + ".part.json"))
        d["name"] = NAME[pid]
        dump(p, d)
        changed += 1

cat = os.path.join(BASE, "catalogs", "stock_parts.json")
d = json.load(io.open(cat, encoding="utf-8"))
os.makedirs(BAK, exist_ok=True)
shutil.copy2(cat, os.path.join(BAK, "stock_parts.json"))
n = 0
for e in d.get("entries", []):
    df = e.get("definition") or {}
    pid = df.get("id")
    if pid in NAME and df.get("name") != NAME[pid]:
        df["name"] = NAME[pid]
        n += 1
dump(cat, d)
print("part.json updated", changed, "catalog updated", n, "map", len(NAME), "bak", BAK)