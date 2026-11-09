# -*- coding: utf-8 -*-
"""补齐旧版遗漏的分尺寸说明与变体名/说明（v0.6.4 仍在英文状态）。"""
import json, io, os, glob, time, shutil, collections

BASE = r"D:\001wyh\newrf\extract\assets"
CATALOG = os.path.join(BASE, "catalogs", "stock_parts.json")
BAK = r"D:\001wyh\newrf\backup\text_residual_bak_%s" % time.strftime("%Y%m%d_%H%M%S")

MAP = {
"A compact powered auger. While switched on and touching solid ground it slowly carves the terrain under the bit. Point it down for a shaft, mount it on a rover for a trench.":
"紧凑型动力螺旋钻。开启并接触坚实地面时，会慢慢在钻头下方刨开地层。朝下设成竖井，装在巡视车上则用来开沟。",
"A heavy mining rig with a 2.4 m bit. Chews through ground quickly and drinks power to match, so bring generation or a big battery bank.":
"钻头长 2.4 米的重型采矿装置。掘进飞快，耗电也与之相当，记得带上发电机或大容量电池组。",
"A broad sealed flotation block for modular rafts and recovery cradles. Displaces 500 liters when fully submerged: up to 460 kg of additional load in fresh water.":
"宽大的密封浮力块，用于模块化浮筏与回收托架。完全浸没时排水 500 升：在淡水中可额外承载 460 公斤。",
"Pressurized living quarters for up to 2 astronauts. Crew can exit through the hatch, and a small backup battery keeps life support running. No flight controls: pair it with a command pod or probe core.":
"加压居住舱，最多容纳 2 名宇航员。乘员可从舱门出舱，小型备用电池维持生命支持运转。没有飞行控制：需搭配指令舱或探针核心。",
"Pressurized living quarters for up to 4 astronauts. Crew can exit through the hatch, and a small backup battery keeps life support running. No flight controls: pair it with a command pod or probe core.":
"加压居住舱，最多容纳 4 名宇航员。乘员可从舱门出舱，小型备用电池维持生命支持运转。没有飞行控制：需搭配指令舱或探针核心。",
"Pressurized living quarters for up to 8 astronauts. Crew can exit through the hatch, and a small backup battery keeps life support running. No flight controls: pair it with a command pod or probe core.":
"加压居住舱，最多容纳 8 名宇航员。乘员可从舱门出舱，小型备用电池维持生命支持运转。没有飞行控制：需搭配指令舱或探针核心。",
"Pressurized living quarters for up to 16 astronauts. Crew can exit through the hatch, and a small backup battery keeps life support running. No flight controls: pair it with a command pod or probe core.":
"加压居住舱，最多容纳 16 名宇航员。乘员可从舱门出舱，小型备用电池维持生命支持运转。没有飞行控制：需搭配指令舱或探针核心。",
"Folding blade leg pushed open by a telescoping strut. Folds flat against the hull and opens to a wide, flat-footed stance.":
"由伸缩撑杆推开的折叠刀形着陆腿。收拢时平贴船体，展开后形成宽阔的平脚支撑。",
"Compact laser cannon for small craft. Each tap in flight fires one battery-powered glowing bolt. Bolts stop at the first thing they hit; turn on Damage in the builder to make them destroy vehicle parts.":
"用于小型飞船的紧凑激光炮。飞行中每点一次发射一发电池供能的发光弹。光束遇到第一个物体即止；在建造器中打开“伤害”后才会摧毁载具部件。",
"Heavy laser cannon for capital ships. Each tap in flight fires one battery-powered bolt with a long reach. Bolts stop at the first thing they hit; turn on Damage in the builder to make them destroy vehicle parts.":
"用于大型舰船的重型激光炮。飞行中每点一次发射一发射程很远的电池供能弹。光束遇到第一个物体即止；在建造器中打开“伤害”后才会摧毁载具部件。",
"Rare Element Bin": "稀有元素箱",
"An armored bin of rare elements to carry where they are needed. On top of the planet's budget, welding spends what nearby bins and the crates in a suit's bag hold, and a colony launch what bins near its pad hold. Bins launched from a colony leave empty unless their material is unlimited there. The smallest size is a crate that stacks in the bag.":
"装甲料箱，用来把稀有元素运到需要的地方。在星球配额之外，焊接会消耗附近料箱与宇航服背包中料盒里的存量，殖民地发射则消耗发射台附近料箱里的存量。从殖民地发射的料箱起飞时是空的，除非该处的这种材料无限。最小尺寸是可堆叠在背包里的料盒。",
"Exotic Matter Bin": "奇异物质箱",
"A shielded bin of exotic matter to carry where it is needed. On top of the planet's budget, welding spends what nearby bins and the crates in a suit's bag hold, and a colony launch what bins near its pad hold. Bins launched from a colony leave empty unless their material is unlimited there. The smallest size is a crate that stacks in the bag.":
"屏蔽料箱，用来把奇异物质运到需要的地方。在星球配额之外，焊接会消耗附近料箱与宇航服背包中料盒里的存量，殖民地发射则消耗发射台附近料箱里的存量。从殖民地发射的料箱起飞时是空的，除非该处的这种材料无限。最小尺寸是可堆叠在背包里的料盒。",
"Heavy 0.8 m recovery canister for Pallas-class capsules. Four times the drag area of the standard parachute.":
"用于智神星级座舱的重型 0.8 米回收伞筒。阻力面积是标准降落伞的四倍。",
"A heavy-duty sealed float for barges, floating cranes and recovery platforms. Displaces 4 cubic meters when fully submerged: up to 3740 kg of additional load in fresh water.":
"重型密封浮筒，用于驳船、浮吊与回收平台。完全浸没时排水 4 立方米：在淡水中可额外承载 3,740 公斤。",
"Radioisotope thermoelectric generator in the style of the MMRTG. The decay heat of 4.8 kg of plutonium-238 becomes 0.11 kW of steady power: no sunlight needed, it works sealed in a fairing and between the stars. Output halves every 88 years of the craft's own time.":
"MMRTG 风格的同位素温差发电机。4.8 公斤钚-238 的衰变热化为 0.11 kW 的稳定电力：无需阳光，封在整流罩里、身处星际之间都能工作。输出每 88 年（飞船自身时间）减半。",
"Two hinged panels of triple-junction cells fold out of a compact housing, sized for small probes. Makes 0.12 kW in full sunlight at 1 AU. Output falls off with the square of the distance from the star.":
"两组三结电池铰接板从紧凑壳体中展开，尺寸适合小型探针。在 1 AU 的满照阳光下出力 0.12 kW。输出随与恒星距离的平方衰减。",
"Four hinged panels of triple-junction cells swing out one after another from a hull-mounted stowage housing. Makes 0.4 kW in full sunlight at 1 AU. Output falls off with the square of the distance from the star.":
"四组三结电池铰接板从船体上的收纳壳中依次展开。在 1 AU 的满照阳光下出力 0.4 kW。输出随与恒星距离的平方衰减。",
"Six large hinged panels of triple-junction cells for heavy probes and ships bound for the outer planets, where sunlight fades. Makes 3 kW in full sunlight at 1 AU. Output falls off with the square of the distance from the star.":
"六组大型三结电池铰接板，适合重型探针和前往阳光昏暗的外行星的飞船。在 1 AU 的满照阳光下出力 3 kW。输出随与恒星距离的平方衰减。",
"Rare Element Warehouse": "稀有元素仓库",
"A prefab storage hall for rare elements on a colony world. Landed there, its storage lets the planet's rare-element mines raise the budget for what you build and launch there.":
"殖民地星球上的稀有元素预制仓储大厅。降落在那里后，其储量可提高该星球稀有元素矿为当地建造与发射提供的配额。",
"Exotic Matter Warehouse": "奇异物质仓库",
"A shielded storage hall for exotic matter on a colony world. Landed there, its storage lets the planet's exotic mines raise the budget for what you build and launch there.":
"殖民地星球上的奇异物质屏蔽仓储大厅。降落在那里后，其储量可提高该星球奇异物质矿为当地建造与发射提供的配额。",
"Battery-powered bow beam cannon. Tap it in flight to charge it for a few seconds, then it unleashes a wide energy beam that stops at the first thing in its path. Turn on Damage in the builder to let the beam burn through vehicle parts.":
"电池供能的舰首光束炮。飞行中点一下充能数秒，随后释放一道宽阔的能量束，遇到路径上的第一个物体即止。在建造器中打开“伤害”后，光束才能烧穿载具部件。",
"Colossal battery-powered bow cannon. Tap it in flight to charge it for a few seconds, then it unleashes a huge energy beam that stops at the first thing in its path. Turn on Damage in the builder to let the beam burn through vehicle parts.":
"巨型电池供能舰首炮。飞行中点一下充能数秒，随后释放一道巨大的能量束，遇到路径上的第一个物体即止。在建造器中打开“伤害”后，光束才能烧穿载具部件。",
"Hub Wheel": "轮毂轮",
"The rover wheel without its strut, for custom landing gear and rovers. It mounts at the top of the tire and keeps the same suspension, drive and brakes.":
"去掉支柱的巡视车轮，用于自制起落架和巡视车。它从轮胎顶部安装，悬挂、驱动与制动都与原款相同。",
}

hits = collections.Counter()

def walk(o):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if isinstance(v, str) and v in MAP:
                o[k] = MAP[v]
                hits[v] += 1
            else:
                walk(v)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, str) and v in MAP:
                o[i] = MAP[v]
                hits[v] += 1
            else:
                walk(v)

os.makedirs(BAK, exist_ok=True)
for p in sorted(glob.glob(os.path.join(BASE, "parts", "*", "part.json"))):
    d = json.load(io.open(p, encoding="utf-8"))
    b = json.dumps(d, sort_keys=True, ensure_ascii=False)
    walk(d)
    if b != json.dumps(d, sort_keys=True, ensure_ascii=False):
        shutil.copyfile(p, os.path.join(BAK, os.path.basename(os.path.dirname(p)) + "_part.json"))
        io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
        print("changed", os.path.basename(os.path.dirname(p)))

d = json.load(io.open(CATALOG, encoding="utf-8"))
b = json.dumps(d, sort_keys=True, ensure_ascii=False)
walk(d)
if b != json.dumps(d, sort_keys=True, ensure_ascii=False):
    shutil.copyfile(CATALOG, os.path.join(BAK, "stock_parts.json"))
    io.open(CATALOG, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
    print("changed catalog")

print("hits", dict((k[:40], v) for k, v in hits.items()))
print("unmatched:", [k[:60] for k in MAP if hits[k] == 0])
