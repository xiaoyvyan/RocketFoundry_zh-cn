# -*- coding: utf-8 -*-
"""v0.6.4 新增/变更文本的汉化：零件名、说明、变体名与变体说明、各尺寸说明。
按英文原文精确匹配替换，作用范围：assets/parts/*/part.json 与 assets/catalogs/stock_parts.json
"""
import json, io, os, glob, time, collections

BASE = r"D:\001wyh\newrf\extract\assets"
CATALOG = os.path.join(BASE, "catalogs", "stock_parts.json")
BAK = r"D:\001wyh\newrf\backup\text064_bak_%s" % time.strftime("%Y%m%d_%H%M%S")

MAP = {
    # ---- 名称 ----
    "Balloon": "气球",
    "Fuel Cell": "燃料电池",
    "Exotic Fuel Cell": "特种燃料电池",
    "TNT": "TNT 炸药",
    "Dish Probe": "碟形探针",
    "Compact Propeller": "紧凑螺旋桨",
    "Nuclear Bomb": "核弹",
    # ---- 说明 ----
    "A sealed gas balloon like the giant envelopes that carry telescopes to the stratosphere. Set its helium or hydrogen in the builder: each cubic meter lifts about 1 kg at Earth sea level, and it climbs until the thinning air holds it. Lift follows the local air, so thick Venus and Titan carry far more, Mars barely any, and nothing floats in a vacuum or in a hydrogen giant. The gas never vents: drop the balloon with a decoupler to come down.":
        "密封气体气球，形如把望远镜送上平流层的巨型气囊。在建造器里设定它充氦气还是氢气：在地球海平面每立方米约可吊起 1 公斤，气球会一直上升，直到稀薄的大气托不住它。升力取决于当地大气，所以在浓密的金星与土卫六上能吊起得多得多，火星上几乎没有，真空中和氢巨星里则完全浮不起来。气体不会排出：要下降就用分离器把气球抛掉。",
    "Hydrogen-oxygen fuel cell stack like the ones that powered Apollo and the Space Shuttle. Turns the craft's liquid propellant into electricity at 0.4 kg per kWh, burning only what the batteries and systems need. Makes 2 kW at the smallest size and 16 kW at the largest. Mount it in the fuel stack, keep a battery on the craft, and tap it in flight to switch it on or off.":
        "氢氧燃料电池组，与当年驱动阿波罗和航天飞机的同类。以每千瓦时 0.4 公斤的速率把飞船的液体推进剂转为电力，只消耗电池和各系统实际需要的量。最小尺寸出力 2 kW，最大尺寸 16 kW。把它装在燃料堆里，船上保留一块电池，飞行中点一下即可开机或关机。",
    "Fuel cell stack that burns Exotic Fuel instead of propellant: an emergency supply for interstellar ships whose reactors fail. Makes 1.5 MW at the smallest size and 12 MW at the largest, twelve Reactors' worth. At 0.1 kg of Exotic Fuel per kWh, a 1.6 m tank of it lasts under 3 hours at full output and over a day at one Reactor's load. Burns only what the batteries and systems need. Mount it against a tank set to Exotic Fuel.":
        "燃烧特种燃料而非推进剂的燃料电池组：为反应堆失效的星际飞船准备的应急电源。最小尺寸出力 1.5 MW，最大尺寸 12 MW，相当于十二台反应堆。按每千瓦时 0.1 公斤特种燃料计算，1.6 米长的贮箱在满功率下用不到 3 小时，在单台反应堆的负载下可撑一天以上。只消耗电池和各系统实际需要的量。把它贴在一个设定为特种燃料的贮箱上。",
    "A small steel-cased high-explosive charge, made to drop from drones and light aircraft. It is set from 10 kg to 900 t of TNT (100 kg by default), enough to wreck whatever stands close by and leave a small crater.":
        "小型钢壳高爆装药，用来从无人机和轻型飞机上投放。装药量可在 10 公斤到 900 吨 TNT 之间设定（默认 100 公斤），足以摧毁近旁的一切并留下一个小坑。",
    "Probe flight computer built into a high-gain dish, with no battery of its own. It flies the craft only while a battery aboard has charge: mount it on a battery, or the craft stays dark from launch. Draws 10 W at this size.":
        "集成在高增益碟形天线里、自身不带电池的探针飞行计算机。只有在船上电池有电时才能操纵飞船：把它装在电池上，否则飞船从发射起就一片漆黑。此尺寸耗电 10 W。",
    "Probe flight computer built into a high-gain dish, with no battery of its own. It flies the craft only while a battery aboard has charge: mount it on a battery, or the craft stays dark from launch. Draws 2 W at this size.":
        "集成在高增益碟形天线里、自身不带电池的探针飞行计算机。只有在船上电池有电时才能操纵飞船：把它装在电池上，否则飞船从发射起就一片漆黑。此尺寸耗电 2 W。",
    "Probe flight computer built into a high-gain dish, with no battery of its own. It flies the craft only while a battery aboard has charge: mount it on a battery, or the craft stays dark from launch. Draws 5 W at this size.":
        "集成在高增益碟形天线里、自身不带电池的探针飞行计算机。只有在船上电池有电时才能操纵飞船：把它装在电池上，否则飞船从发射起就一片漆黑。此尺寸耗电 5 W。",
    "Electric motor pod turning a 1.5 m two-blade propeller, the kind that pulls light electric aircraft. Gives 12 kN at Earth sea level for 25 kW of battery power. Thrust follows the air: weaker in thin air, nothing in a vacuum.":
        "电动机吊舱带动 1.5 米双叶螺旋桨，与牵引轻型电动飞机的同类。在地球海平面以 25 kW 电池功率产生 12 kN 推力。推力随空气变化：稀薄大气中更弱，真空中为零。",
    "Compact electric propeller for drones: a 1 m two-blade rotor on a short motor pod, like the lift props of a heavy camera drone. Gives 2 kN at Earth sea level for only 2.5 kW. Four of them hover a probe core, a slim battery and a TNT charge for over 20 minutes, but they cannot lift heavy craft. Thrust follows the air: weaker in thin air, nothing in a vacuum.":
        "用于无人机的紧凑电动螺旋桨：短电机吊舱上装 1 米双叶旋翼，类似重型航拍无人机的升力桨。在地球海平面仅需 2.5 kW 就能产生 2 kN 推力。四台足以让探针核心、一块薄型电池和一枚 TNT 炸药悬停 20 分钟以上，但吊不起重型飞船。推力随空气变化：稀薄大气中更弱，真空中为零。",
    "Heavy sealed-core power supply for interstellar ships. Produces 1 MW without sunlight, enough for one Tern and support systems. Output halves over 100 years of ship time as its sealed core ages. Tap it in flight to shut it down: it then makes no power and its core ages a hundred times slower, halving over 10,000 years. Core refueling is not available.":
        "用于星际飞船的重型密封堆芯电源。无需阳光即可发出 1 MW，足够一台「燕鸥」及支持系统使用。随着密封堆芯老化，输出会在 100 年船载时间内减半。飞行中点一下可将其停堆：此时不发电，堆芯老化速度慢一百倍，要 10,000 年才减半。堆芯无法更换。",
}

hits = collections.Counter()

def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, str) and v in MAP:
                o[k] = MAP[v]
                hits[v] += 1
            else:
                walk(v)
    elif isinstance(o, list):
        for v in o:
            if isinstance(v, str) and v in MAP:
                hits[v] += 1
            else:
                walk(v)

os.makedirs(BAK, exist_ok=True)
files = sorted(glob.glob(os.path.join(BASE, "parts", "*", "part.json")))
changed = 0
for p in files:
    d = json.load(io.open(p, encoding="utf-8"))
    before = json.dumps(d, ensure_ascii=False, sort_keys=True)
    walk(d)
    after = json.dumps(d, ensure_ascii=False, sort_keys=True)
    if before != after:
        import shutil
        rel = os.path.relpath(p, BASE).replace("\\", "_")
        shutil.copyfile(p, os.path.join(BAK, rel))
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            json.dumps(d, ensure_ascii=False, indent=2))
        changed += 1
        print("changed part.json:", os.path.basename(os.path.dirname(p)))

d = json.load(io.open(CATALOG, encoding="utf-8"))
before = json.dumps(d, ensure_ascii=False, sort_keys=True)
walk(d)
if before != json.dumps(d, ensure_ascii=False, sort_keys=True):
    import shutil
    shutil.copyfile(CATALOG, os.path.join(BAK, "stock_parts.json"))
    io.open(CATALOG, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
    print("changed catalog: stock_parts.json")

print("\nhits per string:")
for k, v in hits.items():
    print("  %3d  %s" % (v, k[:70]))
missed = [k for k in MAP if hits[k] == 0]
print("\nUNMATCHED (%d):" % len(missed))
for k in missed:
    print("   ?", k[:100])
