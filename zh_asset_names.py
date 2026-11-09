# -*- coding: utf-8 -*-
"""Translate body / launch-site / skin / appearance names in data files (name fields only)."""
import glob, io, os, shutil, time

MAP = {
 # 天体
 "Sun":"太阳","Mercury":"水星","Venus":"金星","Earth":"地球","Moon":"月球","Mars":"火星",
 "Phobos":"火卫一","Deimos":"火卫二","Ceres":"谷神星","Jupiter":"木星","Saturn":"土星",
 "Uranus":"天王星","Neptune":"海王星","Pluto":"冥王星","Charon":"卡戎","Eris":"阋神星",
 "Makemake":"鸟神星","Haumea":"妊神星","Quaoar":"创神星","Sedna":"塞德娜","Orcus":"奥库斯",
 "Vanth":"万斯","Pallas":"智神星","Vesta":"灶神星","Hygiea":"健神星","Psyche":"灵神星",
 "Eros":"爱神星","Itokawa":"系川","Bennu":"贝努","Ryugu":"龙宫","Arrokoth":"天涯海角",
 "Halley":"哈雷","Didymos":"迪迪莫斯","Dimorphos":"迪莫弗斯","Cruithne":"克鲁特尼",
 "Amalthea":"阿马尔忒亚","Thebe":"忒拜","Io":"木卫一","Europa":"欧罗巴","Ganymede":"盖尼米德",
 "Callisto":"卡利斯托","Pan":"潘","Prometheus":"普罗米修斯","Pandora":"潘多拉",
 "Epimetheus":"厄庇墨透斯","Janus":"雅努斯","Mimas":"弥玛斯","Enceladus":"恩克拉多斯",
 "Tethys":"忒堤斯","Dione":"狄俄涅","Rhea":"瑞亚","Titan":"泰坦","Hyperion":"许珀里翁",
 "Iapetus":"伊阿珀托斯","Phoebe":"福柏","Puck":"帕克","Miranda":"米兰达","Ariel":"阿里尔",
 "Umbriel":"乌姆柏里厄尔","Titania":"泰坦妮亚","Oberon":"奥伯龙","Naiad":"涅瑞伊得",
 "Larissa":"拉里萨","Galatea":"伽拉忒亚","Despina":"德斯皮娜","Proteus":"普罗透斯",
 "Triton":"特里同","Nereid":"涅瑞伊得斯","Nix":"尼克斯","Hydra":"许德拉","Kerberos":"刻耳柏洛斯",
 "Styx":"斯堤克斯","Dysnomia":"迪丝诺美亚","Hi'iaka":"希亚卡","Namaka":"纳玛卡",
 "Gonggong":"共工星","Xiangliu":"相柳","Weywot":"威沃特","Salacia":"萨拉西亚","Actaea":"阿克泰亚",
 "Chariklo":"女凯龙","Chiron":"凯龙","Pluto-Charon":"冥王星-卡戎","Orcus-Vanth":"奥库斯-万斯",
 # 发射场 / 站点
 "Launch Pad":"发射台","Runway":"跑道","Landing Boat":"着陆船","Space Droneship":"海上无人回收船",
 "Open Water (Water Launch)":"开阔水域（水上发射）","Crawler Launch Pad":"履带发射台",
 "Michigan Crawler Pad":"密歇根履带发射台","Michigan Pad":"密歇根发射台","Michigan Runway":"密歇根跑道",
 "Mexico":"墨西哥","Greenland":"格陵兰","Sonmiani Spaceport":"索尼阿尼航天港",
 "Baikonur Pad 1":"拜科努尔 1 号发射台","Baikonur Pad 2":"拜科努尔 2 号发射台","Baikonur Pad 3":"拜科努尔 3 号发射台",
 "Plesetsk Pad 1":"普列谢茨克 1 号发射台","Plesetsk Pad 2":"普列谢茨克 2 号发射台",
 "Starbase Pad 1":"星舰基地 1 号发射台","Starbase Pad 2":"星舰基地 2 号发射台","Starbase Pad 3":"星舰基地 3 号发射台",
 "Starbase Pad 4":"星舰基地 4 号发射台","Starbase Pad 5":"星舰基地 5 号发射台","Starbase Pad 6":"星舰基地 6 号发射台",
 "Shackleton Outpost":"沙克尔顿前哨站",
 # 地貌
 "Acidalia Planitia":"阿西达利亚平原","Aeneas Crater":"埃涅阿斯环形山","Aphrodite Terra":"阿佛洛狄忒高地",
 "Arabia Terra":"阿拉伯高地","Arden Corona":"阿尔登冕状地形","Asgard Basin":"阿斯加德盆地",
 "Beta Regio":"贝塔区","Borealis Planitia":"北方平原","Caloris Basin":"卡洛里斯盆地",
 "Cantaloupe Terrain":"哈密瓜地形","Cassini Regio":"卡西尼区","Cthulhu Macula":"克苏鲁斑",
 "Equatorial Ridge":"赤道山脊","Galileo Regio":"伽利略区","Guinevere Planitia":"桂妮薇儿平原",
 "Hellas Basin":"希腊盆地","Herschel Crater":"赫歇尔环形山","Ithaca Chasma":"伊萨卡峡谷",
 "Kraken Mare":"克拉肯海","Ligeia Mare":"利吉亚海","Lineae Network":"线状地形网","Loki Patera":"洛基火山口",
 "Mare Crisium":"危海","Mare Frigoris":"冷海","Marius Hills Hole":"马里乌斯丘陵竖井","Marius Regio":"马里乌斯区",
 "Occator Bright Spots":"奥卡托亮斑","Oceanus Procellarum":"风暴洋","Pele Deposit":"佩蕾沉积",
 "Rembrandt Basin":"伦勃朗盆地","Rheasilvia Basin":"瑞亚西尔维亚盆地","Roncevaux Terra":"龙塞斯瓦列斯高地",
 "Samarkand Sulci":"撒马尔罕沟槽","Serenity Chasma":"静海峡谷","Snowman Craters":"雪人环形山",
 "South Polar Cap":"南极冰盖","Stickney Crater":"史蒂克尼环形山","Tiger Stripes":"虎纹",
 "Tombaugh Regio":"汤博区","Tros Crater":"特罗斯环形山","Tycho Crater":"第谷环形山",
 "Valhalla Basin":"瓦尔哈拉盆地","Verona Rupes":"维罗纳断崖","Vulcan Planitia":"伏尔甘平原",
 "Wispy Terrain":"絮状地形",
 # 涂装颜色
 "Red":"红色","Orange":"橙色","Yellow":"黄色","Olive":"橄榄色","Teal":"青绿色","Blue":"蓝色",
 "Purple":"紫色","White":"白色","Charcoal":"炭黑色","Chrome":"铬色","Champagne":"香槟色",
 # 外观样式
 "Fine Checkerboard":"细棋盘格","Large Checkerboard":"大棋盘格","Fine Corrugation":"细波纹",
 "Wide Corrugation":"宽波纹","Four Stripes":"四条纹",
}

root = r"D:\001wyh\newrf\extract\assets"
dirs = ["bodies", "asteroids", "structures", "parts\\skins", "parts\\appearance"]
bak = r"D:\001wyh\newrf\backup\names_bak_" + time.strftime("%Y%m%d_%H%M%S")
files = []
for d in dirs:
    files += glob.glob(os.path.join(root, d) + r"\**\*.json", recursive=True)

changed = 0
for f in files:
    raw = io.open(f, encoding="utf-8", newline="").read()
    new = raw
    for en, zh in MAP.items():
        new = new.replace('"name": "%s"' % en, '"name": "%s"' % zh)
    if new != raw:
        if not os.path.isdir(bak):
            os.makedirs(bak)
        shutil.copy2(f, os.path.join(bak, os.path.relpath(f, root).replace("\\", "_")))
        io.open(f, "w", encoding="utf-8", newline="").write(new)
        changed += 1
print("changed", changed, "of", len(files), "bak", bak)
