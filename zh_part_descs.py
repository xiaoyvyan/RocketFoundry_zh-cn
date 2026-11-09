# -*- coding: utf-8 -*-
"""Translate part descriptions in assets/parts/*/part.json (+ stock_parts.json). Idempotent."""
import glob, json, io, os, shutil, time

MAP = {
"A compact sealed flotation block for capsule recovery, small rafts and amphibious rovers. Displaces 250 liters when fully submerged: up to 230 kg of additional load in fresh water.":
 "紧凑的密封浮力块，用于回收返回舱、小型浮筏和两栖巡视车。完全浸没时排水 250 升，在淡水中可额外承载 230 千克。",
"A drilling derrick that mines an ore region for good. Land it inside a region you have found, then deploy it: the mine raises the planet's budget of that resource for everything you build or launch there, up to what your warehouses or fuel depots there can store. Several rigs can work one region up to its mine cap (shown as 3/15): the first third yield in full, each one after less. A region mined to its cap makes the resource unlimited once storage holds all it yields.":
 "能长期开采矿区的钻井架。把它降落在你已发现的矿区里再展开：这座矿井会提高该天体上此种资源的预算上限，你在此建造或发射的东西都能用，上限受当地仓库或燃料库的存储量限制。同一矿区可架设多台钻机，直到达到矿井上限（显示为 3/15）：第一台按全额产出，之后每台依次递减。矿区采到上限后，只要仓储能装下全部产出，该资源即为无限。",
"A flexible two-end tether. Attach only the two short ends to separate craft, or connect one end to a powered winch. Resizing along the cable changes its length.":
 "两端可连接的柔性绳索。只把两端短接头分别接到不同飞船上，或把一端接到动力绞盘上。沿缆绳调整长度即可改变绳长。",
"A gray-green visitor in a glowing bio-suit. Walks, flies a jetpack, boards cabins and fires the sidearm exactly like an astronaut.":
 "穿着发光生物服、灰绿色的异星访客。行走、用喷气背包飞行、进出舱室和发射侧臂的方式与宇航员完全一样。",
"A heavy auger that screws into the ground. Deployed on a landed craft, it pins the craft in place: it can no longer slide, tip or be pushed, and its engines cannot lift it. Retract it to take off.":
 "重型螺旋地锚，可拧入地面。在已着陆的飞船上展开后能把飞船钉在原地：不再滑动、倾倒或被推动，发动机也无法把它抬起。收起即可起飞。",
"A launch deck for a colony. Landed on a world, it lets you build rockets in the builder and launch them from it, paid from the planet's budget. A launch carries at most as many crew as there are seats parked on that world.":
 "殖民地的发射台。降落在某个天体上后，你可以在建造器里造火箭并从它发射，费用由该天体的预算支付。每次发射搭载的乘员不能超过停在该天体上的座位数。",
"A navigation lamp. In the builder set its blink type (steady, pulse or strobe), the blink period, its color (any color from the picker) and whether it starts lit. Tap it in flight to toggle the lamp.":
 "航行灯。在建造器里可设置闪烁方式（常亮、脉冲或频闪）、闪烁周期、颜色（取色器里的任意颜色）以及初始是否点亮。飞行中点一下即可开关此灯。",
"A prefab storage hall for metal on a colony world. Landed there, its storage lets the planet's metal mines raise the budget for what you build and launch there.":
 "殖民地天体上的预制金属仓库。降落之后，它能为天体的金属矿提高预算，供你在此建造与发射使用。",
"A propellant storage sphere for a colony world. Landed there, it lets the planet's fuel mines raise the fuel budget: the most fuel a rocket launched or refueled there may carry.":
 "殖民地天体的推进剂储罐球。降落之后，它能让天体的燃料矿提高燃料预算，即在此发射或加注的火箭最多可携带的燃料量。",
"A reflective sail on four roll-out booms, packed in a deployer drum. Open it in vacuum, then use SAS Sail Faster or Sail Slower to steer. Sunlight gives a tiny continuous push without fuel or electricity. Larger sizes carry wider sails. Thrust fades with distance but still works in the outer system. It stops in shadow; coast between star systems. Moving air tears an open sail away. Only the drum is solid.":
 "四面展开臂撑起的反射帆，收纳在释放筒里。在真空中展开，再用 SAS「帆加速 / 帆减速」操纵。阳光提供无需燃料和电力的持续微小推力。尺寸越大帆面越宽。推力随距离衰减，但在外太阳系仍然有效；进入阴影即停止，跨恒星系之间只能滑行。流动的空气会把展开的帆撕走。只有筒体是实体的。",
"A round navigation lamp seen from the front, with the same blink type, period, color and lamp settings as the Nav Light. May be placed over other parts without enabling part clipping. Tap it in flight to toggle the lamp.":
 "正面看为圆形的航行灯，闪烁方式、周期、颜色与灯光设置都与航行灯相同。无需开启部件穿透即可叠放在其他部件上。飞行中点一下即可开关。",
"A sealed boat float with a rounded hull and deck mounts. Displaces 1 cubic meter when fully submerged: up to 920 kg of additional load in fresh water. Use spaced pontoons for a stable platform.":
 "密封船用浮筒，圆润船体带甲板安装位。完全浸没时排水 1 立方米，在淡水中可额外承载 920 千克。间隔布置多个浮筒可获得稳定平台。",
"A solid block of cast concrete that adds dead weight wherever a craft needs it. Set its mass in Part Settings, up to a million metric tons to pin a structure in place.":
 "实心混凝土块，可在需要配重的地方增加死重。在「部件设置」里设定其质量，最高可达一百万吨，用来把结构压稳在原地。",
"A station-class array in the style of the International Space Station's wings. A truss mast pushes two pleated blankets of silicon cells 24 m out of a compact containment box, and power builds as they open. Makes 24 kW in full sunlight at 1 AU. Fly wings in pairs to keep a station balanced. Output falls off with the square of the distance from the star.":
 "国际空间站翼式风格的空间站级电池阵。桁架桅杆把两块褶皱的硅电池毯从紧凑收纳箱推出 24 米，展开过程中功率随之上升。1 AU 满日照下发电 24 kW。成对安装可让空间站保持平衡。输出随距恒星距离的平方衰减。",
"A steel box for spare parts. Pack it in the builder or stow parts in it on EVA, then take them out and fit them where they are needed. It has no seats, so it suits uncrewed supply runs.":
 "装零件的钢箱。可在建造器里装箱，或在舱外活动时把零件收进去，需要时再取出安装。没有座位，适合无人补给。",
"A straight-sided booster nose cone with a compact rounded tip.":
 "直边助推器头罩，顶端为紧凑圆头。",
"A survey instrument for low orbit. Below half a body's radius up it scans each area it passes over, finding the ore regions visible from orbit. It draws power while it scans, so give it a solar panel or generator. Some regions only show up in samples from a drill or a rock.":
 "用于低轨道的勘测仪器。升到天体半径的一半以下时，它扫过每个区域，找出从轨道上可见的矿区。扫描耗电，请配太阳能板或发电机。有些矿区只能用钻机取样或岩石样本发现。",
"A telescoping piston for arms, lifts and launch tower umbilicals. Parts attach to its base (bottom) and head (top). Part Settings sets its length at launch, the length it moves to, its speeds, and whether the head lets go of what it touches. Stage it or tap it in flight to move it.":
 "可伸缩活塞，用于机械臂、升降装置和发射塔脐带。部件接在其底座（下端）与头部（上端）。「部件设置」可设定发射时的长度、移动目标长度、速度，以及头部是否松开接触物。分级或飞行中点按即可动作。",
"A two-blade electric main rotor on a slim mast. Bolt its small base to the top of a craft with the mast upright and it lifts straight up. It runs on battery power and needs air to bite into, so it gives no thrust in vacuum.":
 "细桅杆上的双叶电动主旋翼。把其小底座以桅杆竖直的方式固定在飞行器顶部，即可垂直升空。它靠电池驱动，且需要空气产生拉力，因此在真空中没有推力。",
"Aerospike. Its plume adapts to the outside air, so it stays efficient from the launch pad all the way to orbit.":
 "气动塞式发动机。尾焰随外界空气自适应，从发射台到轨道都保持高效率。",
"Afterburning jet engine. It breathes air, so it burns far less fuel than a rocket, but it loses thrust as the air thins and does nothing in space. Pair it with wings and a cockpit.":
 "加力喷气发动机。它吸空气，耗油远低于火箭，但空气稀薄时推力下降，太空中完全无效。请搭配机翼与驾驶舱。",
"Always-open lattice fin. Switch steering on or off by tapping it or through staging. Twists with your rotation input to steer in thick air, keeps working at steep angles, and does nothing in vacuum.":
 "常开格栅舵。点按或通过分级可开关转向。随你的转向输入偏转，在稠密大气中操控，大迎角下仍有效，真空中无效。",
"An armored bin of metal to carry where it is needed. On top of the planet's budget, welding spends what nearby bins and the crates in a suit's bag hold, and a colony launch what bins near its pad hold. Bins launched from a colony leave empty unless their material is unlimited there. The smallest size is a crate that stacks in the bag.":
 "装甲金属料箱，可运到需要的地方。除天体预算外，焊接还会消耗附近料箱与宇航服背包中板条箱的存量；殖民地发射则消耗发射台附近料箱的存量。从殖民地发射的料箱默认是空的，除非当地该材料为无限。最小尺寸即为可叠放在背包里的板条箱。",
"An observatory for prospecting from afar. Powered and off the ground (in flight, in orbit or in deep space), it learns how rich every body in its star system is and how rich other star systems within 60 light years are. Over a few days it also spots the ore regions visible from space, mostly rich ones, on worlds near it: a moon from its planet's orbit, a planet only on approach. A geo scanner in low orbit finds more, and rock samples or a drill find every region of their area. Resting on the ground it observes nothing. It draws power while it observes, so give it a solar panel or generator.":
 "用于远距勘探的天文台。通电且离地（飞行中、轨道上或深空）时，它能测出本恒星系每个天体的富集程度，以及 60 光年内其他恒星系的富集程度。几天之后，它还能发现附近天体上从太空可见的矿区（多为富矿）：卫星要在其行星轨道上观测，行星只在接近时才能看到。低轨道的地质扫描仪能发现更多，岩石样本或钻机则能找出所在区域的全部矿区。停在地面上时它什么也观测不到。观测耗电，请配太阳能板或发电机。",
"An open seat for one suited astronaut, with a hand controller. The craft answers the controls only while someone sits in it, so it turns a rover into a crewed buggy. Walk up to it to climb in; tap the seat to get out.":
 "供一名穿宇航服的宇航员乘坐的开放式座椅，带手动控制器。只有有人坐上去时飞船才响应操控，因此可把巡视车变成载人小车。走近即可坐上去；点一下座椅即可下车。",
"Bronze screw on a faired stern bossing. Bolt it to the back of a hull with the blades trailing: it pushes the boat away from them, and only underwater.":
 "青铜螺旋桨，装在流线型艉轴毂上。把桨叶朝后固定在船体尾部：它会把船推离桨叶方向，且只能在水下工作。",
"Compact battery-powered bow cannon. Tap it in flight to charge it for a moment, then it fires an energy beam that stops at the first thing in its path. Turn on Damage in the builder to let the beam burn through vehicle parts.":
 "紧凑的电池驱动舰首炮。飞行中点按充能片刻，随后射出一道能量束，遇到路径上第一个物体即停止。在建造器里开启「伤害」后，光束可烧穿载具部件。",
"Compact steering and landing thruster for fine control.":
 "用于精细控制的紧凑转向与着陆微调发动机。",
"Crew airlock with an oversized hatch for spacewalks. Holds 2 astronauts.":
 "带加大舱门的乘员气闸舱，用于舱外活动。可容纳 2 名宇航员。",
"Dependable starter engine. Modest thrust, forgiving handling, works everywhere.":
 "可靠的入门发动机。推力适中、操纵宽容，到处都能用。",
"Emergency solid-motor tower for Pallas. Place it directly above a nose parachute. Tap in flight to pull the capsule and heat shield away from the booster; tap again after burnout to jettison the tower. Staging never aborts: stage the unused tower to discard it on a nominal ascent.":
 "为 Pallas 准备的应急固体逃逸塔。直接装在头部降落伞上方。飞行中点按可把返回舱与隔热罩从助推器上拉走；燃尽后再点按可抛掉逃逸塔。分级不会触发逃逸：正常上升时把未使用的逃逸塔分级抛掉即可。",
"Fighter-style laser cannon. Each tap in flight fires one battery-powered glowing bolt. Bolts stop at the first thing they hit; turn on Damage in the builder to make them destroy vehicle parts.":
 "战机式激光炮。飞行中每次点按发射一发电池驱动的发光弹丸。弹丸遇到第一个物体即停止；在建造器里开启「伤害」后，弹丸可摧毁载具部件。",
"Five hinged panels of triple-junction cells swing out one after another from a hull-mounted stowage housing. Makes 1.2 kW in full sunlight at 1 AU. Output falls off with the square of the distance from the star.":
 "五块铰接三结电池板，从船体上的收纳箱依次展开。1 AU 满日照下发电 1.2 kW。输出随距恒星距离的平方衰减。",
"Folding blade leg pushed open by a telescoping strut. It lies flat against the hull and opens to a wide, flat-footed stance.":
 "折叠刀式着陆腿，由伸缩撑杆撑开。贴伏在船体上，展开后形成宽大、平足的站姿。",
"Four-direction RCS block. May be placed over other parts without enabling part clipping.":
 "四向 RCS 组块。无需开启部件穿透即可叠放在其他部件上。",
"Half of a rounded ogive nose cone, cut down its axis. Pairs with its mirror or caps a stack side.":
 "沿轴线剖开的圆润卵形头罩的一半。可与镜像件配对，或封住堆叠的一侧。",
"Half of a straight-sided booster nose cone, cut down its axis. Pairs with its mirror.":
 "沿轴线剖开的直边助推器头罩的一半。可与镜像件配对。",
"Heavy booster for wider stacks. One turbopump, one job: lift.":
 "用于更宽堆叠的重型助推器。一台涡轮泵，只干一件事：起吊。",
"Heavy sealed-core power supply for interstellar ships. Produces 1 MW without sunlight, enough for one Tern and support systems. Output halves over 100 years of ship time as its sealed core ages. Core refuelling is not available.":
 "星际飞船用的重型密封堆芯电源。无日照时输出 1 MW，足以带动一台 Tern 及保障系统。随密封堆芯老化，飞船时间每过 100 年输出减半。不支持堆芯换料。",
"Heavy-lift steerable solid motor nozzle for 3.60 m boosters. Its grain throttles itself back through maximum dynamic pressure. Once lit it cannot be throttled or shut down.":
 "用于 3.60 米助推器的重型可转向固体发动机喷管。药柱在最大动压段自动节流。点燃后无法节流或关机。",
"High-thrust vacuum engine for heavy upper stages and departure burns.":
 "用于重型上面级与离轨点火的高推力真空发动机。",
"Hydrogen upper-stage engine sized for Hawk stacks. The extended radiative skirt boosts efficiency in space but is dead weight in atmosphere.":
 "为 Hawk 堆叠尺寸设计的氢上面级发动机。加长辐射裙在太空提升效率，在大气中却是死重。",
"Includes a cable and end fitting. Mount the housing on its top or sides, then place cargo or a grabbing unit against the bottom of the end fitting. Select any piece to move the whole winch. Part Settings sets the start length, cable limit up to 200 m, gearing and motor power. Tap in flight to reel in, pay out, hold or detach. Pulls 20 kN at 1 m/s using 25 kW. Higher gearing pulls up to 2,000 kN, reeling slower; more motor power reels faster and uses more electricity. The brake holds without power.":
 "含缆绳与端接头。把壳体装在其顶部或侧面，再把货物或抓取单元贴到端接头底部。选中任意部件即可整体移动绞盘。「部件设置」可设初始长度、最长 200 米的缆绳上限、传动比与电机功率。飞行中点按可收绳、放绳、保持或脱开。1 m/s 时拉力 20 kN，耗电 25 kW。更高传动比可拉到 2,000 kN，但收绳更慢；电机功率越大收绳越快、耗电越多。制动器断电仍可保持。",
"Independent range-safety destruct module. Tap it in flight or assign it to a stage to deliberately break up the complete carrier. Does not damage nearby vessels or terrain.":
 "独立的靶场安全自毁模块。飞行中点按或指派到某个分级，即可故意把整枚运载器解体。不会损伤附近飞船或地形。",
"Jet wing seen from the side. Place it straight over the fuselage: it may overlap other parts without enabling part clipping.":
 "侧视的喷气机翼。竖直安装在机身正上方：无需开启部件穿透即可与其他部件重叠。",
"Legacy Exotic Fuel tank, retained for existing designs. For new designs, use a Fuel Tank and choose Exotic Fuel under Propellant / Other fuel.":
 "旧版特种燃料箱，为兼容既有设计而保留。新设计请使用燃料箱，并在「推进剂 / 其他燃料」中选择特种燃料。",
"Nuclear thermal rocket. Its reactor heats propellant to twice the exhaust speed of any chemical engine, but it is heavy and weak at sea level. Light it in space.":
 "核热火箭。反应堆把推进剂加热到任何化学发动机两倍的排速，但自身沉重、海平面推力弱。请在太空点火。",
"Observation module ringed with large windows. Seats 1 astronaut and has an EVA hatch.":
 "环绕大舷窗的观察舱。可坐 1 名宇航员，并带舱外活动舱门。",
"Pressure-fed lander engine. Gentle thrust for touchdowns and orbital tweaks.":
 "挤压式着陆发动机。推力柔和，适合触地与轨道微调。",
"Pressurized garden module with grow lights. Holds 2 astronauts.":
 "带植物生长灯的可增压温室舱。可容纳 2 名宇航员。",
"Pressurized living quarters for 1 astronaut. Crew can exit through the hatch, and a small backup battery keeps life support running. No flight controls: pair it with a command pod or probe core.":
 "供 1 名宇航员居住的可增压生活舱。乘员可从舱门出入，小型备用电池维持生命保障。没有飞行控制：请搭配指令舱或探针核心。",
"Pulsed fusion drive for crossing between stars. Burns Exotic Fuel from a tank set to Exotic Fuel and draws 600 kW from the ship. Any positive throttle runs at full output; zero stops it. Strong plasma flashes once per second accompany 1 MN of sustained thrust. Fires only in vacuum.":
 "用于恒星际航行的脉冲聚变推进器。燃烧设为特种燃料的储箱中的特种燃料，并从飞船取用 600 kW 电力。任何正油门都以全功率运行，归零即停止。持续 1 MN 推力伴随每秒一次的强等离子闪光。只能在真空中点火。",
"Radioisotope thermoelectric generator in the style of the GPHS-RTG that powers Voyager-class probes. The decay heat of 7.8 kg of plutonium-238 becomes 0.3 kW of steady power: no sunlight needed, it works sealed in a fairing and between the stars. Output halves every 88 years of the craft's own time.":
 "为旅行者级探测器供电的 GPHS-RTG 风格同位素温差电源。7.8 千克钚-238 的衰变热转为 0.3 kW 稳定功率：无需日照，可在整流罩内密封工作，也能在星际之间工作。输出按飞船自身时间每 88 年减半。",
"Ring-shaped tank that packs a lot of propellant into a short, wide stage. Ideal under landers and service modules.":
 "环形贮箱，把大量推进剂装进矮而宽的级段。适合放在着陆器与服务舱下方。",
"Round tank that carries propellant with the least structure. It keeps its round shape instead of tapering to fit its neighbors.":
 "球形贮箱，以最少的结构承载推进剂。它保持球形，不会为贴合相邻部件而收窄。",
"Rung ladder for astronauts. Mount it on the side of a hull to climb between the ground and a hatch: walk up to it and press up or down to grab on.":
 "供宇航员使用的横档梯。装在船体侧面，可在地面与舱门之间攀爬：走近后按上/下即可抓住。",
"Side-on ladder rail for astronauts and aliens. Mount it on the outside of a hull, walk up beside it and press up to grab on, then climb in profile. It is solid like the hull: use a clippable ladder to climb in front of a craft.":
 "供宇航员与异星乘员使用的侧向梯轨。装在船体外侧，走到旁边按上即可抓住，然后以侧面姿态攀爬。它与船体一样是实体的：若要在飞船前方攀爬，请使用可穿透的梯子。",
"Solar-powered ion drive. Whisper-quiet thrust and extraordinary efficiency: it sips liquid fuel from its tanks and needs charged batteries to fire.":
 "太阳能离子推进器。推力轻不可闻、效率极高：从储箱吸取液体燃料，并需要带电的电池才能点火。",
"Solid motor nozzle for 1.60 m boosters. Fit it under tanks loaded with solid grain: a longer stack burns harder for about the same time. Once lit it cannot be throttled or shut down.":
 "用于 1.60 米助推器的固体发动机喷管。装在填满固体药柱的贮箱下方：堆叠越长，燃烧越猛、时间大致相同。点燃后无法节流或关机。",
"Staged-combustion heavy booster for serious launch vehicles.":
 "用于重型运载器的分级燃烧重型助推器。",
"Steerable solid motor nozzle for 2.40 m boosters. Fit it under tanks loaded with solid grain: a longer stack burns harder for about the same time. Once lit it cannot be throttled or shut down.":
 "用于 2.40 米助推器的可转向固体发动机喷管。装在填满固体药柱的贮箱下方：堆叠越长，燃烧越猛、时间大致相同。点燃后无法节流或关机。",
"Streamlined one-seat cockpit for aircraft and spaceplanes, with a bubble canopy.":
 "用于飞机与航天飞机的流线型单座驾驶舱，带气泡座舱盖。",
"Super-heavy first-stage engine. Twin turbopumps feed one huge bell.":
 "超重型一级发动机。双涡轮泵共喂一台巨大喷管。",
"Swept jet tail with an all-moving horizontal stabilizer. Mount it by its root on top of the fuselage; the stabilizer pitches the plane.":
 "后掠喷气尾翼，配全动平尾。以翼根装在机身顶部；平尾负责俯仰。",
"The captive cable of a compound winch, centered beneath its housing.":
 "复合绞盘的承力缆绳，居中位于其壳体下方。",
"The captive end fitting of a compound winch. Its bottom edge attaches to cargo.":
 "复合绞盘的承力端接头，其底边用于连接货物。",
"The workhorse excavation drill: a 1.2 m bit that cuts open pits and trenches while powered. Digging drains the battery group it is wired into.":
 "主力挖掘钻：1.2 米钻头，通电时掘开坑与沟槽。挖掘会消耗其接入的电池组。",
"Workhorse first-stage booster with class-leading thrust for its weight.":
 "主力一级助推器，同重量下推力同级领先。",
}

root = r"D:\001wyh\newrf\extract\assets"
bak = r"D:\001wyh\newrf\backup\partsdesc_bak_" + time.strftime("%Y%m%d_%H%M%S")
files = glob.glob(root + r"\parts\**\part.json", recursive=True)
cat = root + r"\catalogs\stock_parts.json"
targets = files + ([cat] if os.path.isfile(cat) else [])

changed = 0
for f in targets:
    raw = io.open(f, encoding="utf-8", newline="").read()
    hit = False
    for en, zh in MAP.items():
        if en in raw:
            hit = True
            raw = raw.replace(en, zh)
    if hit:
        if not os.path.isdir(bak):
            os.makedirs(bak)
        rel = os.path.relpath(f, root).replace("\\", "_")
        shutil.copy2(f, os.path.join(bak, rel))
        io.open(f, "w", encoding="utf-8", newline="").write(raw)
        changed += 1

print("files changed", changed, "of", len(targets), "backup", bak)
