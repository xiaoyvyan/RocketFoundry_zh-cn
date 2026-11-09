extends Node
## Rocket Foundry 汉化显示层
## 只在显示时把界面上的英文文本替换成中文：原始字符串、节点名、类型名一个字节都不改。

const TABLE_PATH := "res://zh/zh_ui.json"
const PROPS := ["text", "placeholder_text", "dialog_text", "title", "Caption", "_caption", "Value", "_value", "tooltip_text"]
const SCAN_MS := 500

var table: Dictionary = {}
var lower: Dictionary = {}
var watched: Array = []      # 命中过译文的控件，每帧重放（游戏会每帧把英文写回去）
var hidden: Array = []       # 需要永久隐藏的控件（更新提示）
var scanning: bool = false
var last_scan: int = 0

func _ready() -> void:
	process_priority = 1000   # 尽量在一帧里最后跑，覆盖游戏自己刚写进去的英文
	_load_table()
	get_tree().node_added.connect(_on_node_added)
	RenderingServer.frame_pre_draw.connect(_on_pre_draw)   # 渲染前最后一道：保证英文被换掉
	_scan(get_tree().root)
	print("ZH_LAYER_READY entries=", table.size(), " watched=", watched.size())

func _on_pre_draw() -> void:
	for n in watched:
		if is_instance_valid(n):
			_apply(n)

func _load_table() -> void:
	var f := FileAccess.open(TABLE_PATH, FileAccess.READ)
	if f == null:
		push_error("ZH_LAYER: 打不开 " + TABLE_PATH)
		return
	var parsed = JSON.parse_string(f.get_as_text())
	if parsed is Dictionary:
		table = parsed
		lower.clear()
		for k in table.keys():
			var nk := _norm(str(k))
			if not lower.has(nk):
				lower[nk] = table[k]
	else:
		push_error("ZH_LAYER: 译文表不是字典")

func _on_node_added(n: Node) -> void:
	if _apply(n):
		_watch(n)
	for c in n.get_children():
		if _apply(c):
			_watch(c)

func _watch(n: Node) -> void:
	if not watched.has(n):
		watched.append(n)

func _scan(n: Node) -> void:
	if _apply(n):
		_watch(n)
	for c in n.get_children():
		_scan(c)

var last_dump: int = 0
var dbg: int = 0

func _process(_delta: float) -> void:
	var now := Time.get_ticks_msec()
	if now - last_scan >= SCAN_MS and not scanning:
		scanning = true
		last_scan = now
		_scan(get_tree().root)
		_prune()
		scanning = false
	for n in watched:
		if is_instance_valid(n):
			_apply(n)
	for n in hidden:
		if is_instance_valid(n) and n is CanvasItem:
			(n as CanvasItem).visible = false
	if now - last_dump >= 5000:
		last_dump = now
		_dump()
		_probe()

const PROBE_WORDS := ["Dynamic pressure", "TWR now / max", "Time to Ap", "builder", "full torque", "always on"]

func _probe() -> void:
	var lines: PackedStringArray = []
	_probe_walk(get_tree().root, lines)
	var f := FileAccess.open("user://zh_probe.txt", FileAccess.WRITE)
	if f == null:
		return
	f.store_string("\n".join(lines))
	f.close()

func _probe_walk(n: Node, lines: PackedStringArray) -> void:
	for pl in n.get_property_list():
		var nm: String = str(pl.get("name", ""))
		if nm == "":
			continue
		if int(pl.get("type", 0)) != TYPE_STRING:
			continue
		var v = n.get(nm)
		if typeof(v) != TYPE_STRING:
			continue
		var s: String = v
		if s == "" or s.length() > 200:
			continue
		for w in PROBE_WORDS:
			if s.contains(w):
				var vis := ""
				if n is CanvasItem:
					vis = " vis=" + str((n as CanvasItem).visible)
				lines.append(n.get_class() + " path=" + str(n.get_path()) + " prop=" + nm + vis + " val=" + s.replace("\n", "\\n"))
				break
	for c in n.get_children():
		_probe_walk(c, lines)

func _dump() -> void:
	var lines: PackedStringArray = []
	var seen := {}
	_collect(get_tree().root, lines, seen)
	var f := FileAccess.open("user://zh_dump.txt", FileAccess.WRITE)
	if f == null:
		return
	f.store_string("\n".join(lines))
	f.close()

func _collect(n: Node, lines: PackedStringArray, seen: Dictionary) -> void:
	if n is Control or n is Window:
		var cls := n.get_class()
		for p in PROPS:
			if not (p in n):
				continue
			var v = n.get(p)
			if typeof(v) == TYPE_STRING and v != "" and v.length() < 300:
				var key: String = str(cls) + "|" + str(p) + "|" + str(v)
				if not seen.has(key):
					seen[key] = true
					lines.append(key)
	for c in n.get_children():
		_collect(c, lines, seen)

func _prune() -> void:
	var alive: Array = []
	for n in watched:
		if is_instance_valid(n):
			alive.append(n)
	watched = alive

## 去掉零宽字符/不换行空格，再去首尾空白、转小写：表里有些键混入了 U+200B
func _norm(s: String) -> String:
	var t := s.replace("\u200b", "").replace("\u200c", "").replace("\u200d", "")
	t = t.replace("\ufeff", "").replace("\u00a0", "")
	return t.strip_edges().to_lower()

func _lookup(s: String) -> String:
	if table.has(s):
		return String(table[s])
	var st := s.strip_edges()
	if st != "" and table.has(st):
		return String(table[st])
	var nk := _norm(s)
	if nk != "" and lower.has(nk):
		return String(lower[nk])
	return ""

## 行内 "word: value" 形式的统计行
const WORD_MAP := {
	"parts": "部件",
	"decals": "贴花",
	"dry": "干重",
	"fuel": "燃料",
	"mass": "质量",
	"crew": "乘员",
	"seats": "座位",
	"stage": "级",
	"stages": "分级",
}

## "Air: shown (7 of 12)" 这类动态行：相位名 + 已显示/可用行数
func _pattern(s: String) -> String:
	var shown := s.split(": shown (")
	if shown.size() == 2:
		var tail: String = shown[1]
		if tail.ends_with(")"):
			tail = tail.substr(0, tail.length() - 1)
			var nums := tail.split(" of ")
			if nums.size() == 2:
				var ph := _lookup(shown[0])
				if ph == "":
					ph = shown[0]
				return ph + "：显示 " + nums[0] + " / " + nums[1]
	# 更新横幅：UPDATE AVAILABLE: v0.6.2 → 有可用更新：v0.6.2
	if s.begins_with("UPDATE AVAILABLE: "):
		return "有可用更新：" + s.substr(18)
	# 天体类型标签：[Rocky planet] → 【岩石行星】
	if s.begins_with("[") and s.ends_with("]") and s.length() > 2:
		var inner := _lookup(s.substr(1, s.length() - 2))
		if inner != "":
			return "【" + inner + "】"
	# 场面计数：20 SITES / 3 SITES / 6 ORBITS
	var sc := _site_count(s)
	if sc != "":
		return sc
	# 计数短语：30 rockets / 98 parts / 1 mod
	var cnt := _counter(s)
	if cnt != "":
		return cnt
	# 相对时间：1 min ago → 1 分钟前；just now → 刚刚
	var ag := _ago(s)
	if ag != "":
		return ag
	# 作弊页上移距离：Teleport up 10 m → 上移 10 米
	if s.begins_with("Teleport up ") and s.ends_with(" m"):
		var upn := s.substr(12, s.length() - 14).strip_edges()
		if upn.is_valid_int():
			return "上移 " + upn + " 米"
	# 模组元信息行：v1.4.0 · 19 rocket parts · 12 worlds · by Rocket Foundry
	# 训练课程元信息行：Flight essentials · Build and fly · About 7 min
	if s.contains(" · "):
		var segs := s.split(" · ")
		var parts: PackedStringArray = []
		var changed := false
		for seg in segs:
			var z := _counter(seg)
			if z != "":
				parts.append(z)
				changed = true
				continue
			var zd := _duration(seg)
			if zd != "":
				parts.append(zd)
				changed = true
				continue
			if seg.begins_with("by ") and seg.length() > 3:
				parts.append("作者：" + seg.substr(3))
				changed = true
				continue
			var z2 := _about(seg)
			if z2 != "":
				parts.append(z2)
				changed = true
				continue
			var z3 := _lookup(seg)
			if z3 != "":
				parts.append(z3)
				changed = true
				continue
			parts.append(seg)
		if changed:
			return " · ".join(parts)
	if s.begins_with("by ") and s.length() > 3:
		return "作者：" + s.substr(3)
	# 课程详情：About 7 minutes. Start in the builder.
	var ab2 := _about_sentence(s)
	if ab2 != "":
		return ab2
	# 课程前置：Helpful first: Two-Stage Flight. Optional; you can start now.
	if s.begins_with("Helpful first: "):
		var rest := s.substr(14)
		var dot := rest.find(". ")
		if dot > 0:
			var first := rest.substr(0, dot)
			var zf := _lookup(first)
			if zf == "":
				zf = first
			var second := rest.substr(dot + 2).strip_edges()
			var zs := _lookup(second)
			if zs == "":
				zs = second
			return "建议先学：" + zf + "。" + zs
	# 载具平衡说明：Chemical ISP 54.5% · ion endurance 60%
	if s.begins_with("Chemical ISP ") and s.contains(" · ion endurance "):
		var body := s.substr(13)
		var mid := body.find(" · ion endurance ")
		if mid > 0:
			return "化学比冲 " + body.substr(0, mid) + " · 离子续航 " + body.substr(mid + 17)
	# 零件属性：8 W, always on / 15 W at full torque
	var wv := _watts(s)
	if wv != "":
		return wv
	# 房间码：ROOM ABCDEF → 房间 ABCDEF
	if s.begins_with("ROOM ") and s.length() > 5:
		var code := s.substr(5).strip_edges()
		if code != "" and code == code.to_upper():
			return "房间 " + code
	# 主菜单继续按钮提示：Continue 67 → 继续 67
	if s.begins_with("Continue ") and s.length() > 9:
		var cn := s.substr(9).strip_edges()
		if cn.is_valid_int():
			return "继续 " + cn
	# 暂停菜单飞船计数：1 craft here. → 此处 1 艘飞船。
	if s.ends_with(" craft here."):
		var ch := s.substr(0, s.length() - 11).strip_edges()
		if ch.is_valid_int():
			return "此处 " + ch + " 艘飞船。"
	# 模组安装按钮：Install (14 KB) / Installed (v0.4.7)
	if s.begins_with("Install (") and s.ends_with(")"):
		return "安装（" + s.substr(9, s.length() - 10) + "）"
	if s.begins_with("Installed (") and s.ends_with(")"):
		return "已安装（" + s.substr(11, s.length() - 12) + "）"
	# 模组条目：+1 more → +1 项
	if s.begins_with("+") and s.ends_with(" more"):
		var mn := s.substr(1, s.length() - 6).strip_edges()
		if mn.is_valid_int():
			return "+" + mn + " 项"
	return ""

## "About 7 minutes. Start in the builder." → "约 7 分钟。从建造器开始。"
const START_MAP := {
	"builder": "建造器",
	"flight": "飞行中",
	"sandbox": "沙盒",
	"orbit": "轨道上",
	"pad": "发射台",
	"surface": "地表",
}

func _about_sentence(s: String) -> String:
	if not s.begins_with("About "):
		return ""
	var cut := s.find(" minutes")
	if cut <= 0:
		return ""
	var num := s.substr(6, cut - 6).strip_edges()
	if not num.is_valid_int():
		return ""
	var tail := s.substr(cut + 8).strip_edges()
	if tail.begins_with("."):
		tail = tail.substr(1).strip_edges()
	var out := "约 " + num + " 分钟。"
	if tail == "":
		return out
	var tz := _lookup(tail)
	if tz != "":
		return out + tz
	if tail.begins_with("Start in the ") and tail.ends_with("."):
		var where := tail.substr(13, tail.length() - 14).strip_edges().to_lower()
		if START_MAP.has(where):
			return out + "从" + String(START_MAP[where]) + "开始。"
	return out + tail

## "About 7 min" → "约 7 分钟"
func _about(s: String) -> String:
	if s.begins_with("About ") and s.ends_with(" min"):
		var n := s.substr(6, s.length() - 6 - 4).strip_edges()
		if n.is_valid_int():
			return "约 " + n + " 分钟"
	return ""

## "32 min" → "32 分钟"；"1 hour" → "1 小时"
const DUR_SUF := [
	[" minutes", "分钟"], [" minute", "分钟"], [" mins", "分钟"], [" min", "分钟"],
	[" hours", "小时"], [" hour", "小时"], [" hrs", "小时"], [" hr", "小时"], [" h", "小时"],
	[" seconds", "秒"], [" second", "秒"], [" secs", "秒"], [" sec", "秒"], [" s", "秒"],
]

func _duration(s: String) -> String:
	var t := s.strip_edges()
	for pair in DUR_SUF:
		var suf: String = str(pair[0])
		if t.ends_with(suf):
			var head := t.substr(0, t.length() - suf.length()).strip_edges()
			if head.is_valid_int():
				return head + " " + String(pair[1])
	return ""

## "1 min ago" → "1 分钟前"；"just now" → "刚刚"
func _ago(s: String) -> String:
	var t := s.strip_edges()
	var low := t.to_lower()
	if low == "just now" or low == "a moment ago" or low == "moments ago":
		return "刚刚"
	if low == "less than a minute ago":
		return "不到 1 分钟前"
	if not low.ends_with(" ago"):
		return ""
	var head := t.substr(0, t.length() - 4).strip_edges()
	var du := _duration(head)
	if du != "":
		return du + "前"
	var zh := _lookup(head)
	if zh != "":
		return zh + "前"
	return ""

## "N + 量词" 短语：社区机库的 rockets / parts / mods，模组页的 rocket parts / worlds
const COUNTERS := {
	"rocket": "个火箭",
	"rockets": "个火箭",
	"part": "个部件",
	"parts": "个部件",
	"mod": "个模组",
	"mods": "个模组",
	"world": "个天体",
	"worlds": "个天体",
	"rocket parts": "个火箭部件",
	"vessel": "艘飞船",
	"vessels": "艘飞船",
	"star system": "个恒星系",
	"star systems": "个恒星系",
	"structure": "个结构",
	"structures": "个结构",
	"planet": "颗行星",
	"planets": "颗行星",
	"moon": "颗卫星",
	"moons": "颗卫星",
}

## "20 SITES" → "20 个站点"；"6 ORBITS" → "6 条轨道"
func _site_count(s: String) -> String:
	for suf in [" SITES", " ORBITS", " sites", " orbits"]:
		if s.ends_with(suf):
			var head := s.substr(0, s.length() - suf.length()).strip_edges()
			if head.is_valid_int():
				if suf.to_lower().strip_edges() == "sites":
					return head + " 个站点"
				return head + " 条轨道"
	return ""

func _counter(s: String) -> String:
	for key in ["rocket parts", "star systems", "star system", "rockets", "rocket", "vessels", "vessel", "structures", "structure", "planets", "planet", "moons", "moon", "parts", "part", "mods", "mod", "worlds", "world"]:
		var suf: String = " " + str(key)
		if s.ends_with(suf):
			var head := s.substr(0, s.length() - suf.length()).strip_edges()
			if head.is_valid_int():
				return head + " " + String(COUNTERS[key])
	return ""

func _translate_line(line: String) -> String:
	if line == "":
		return line
	var direct := _lookup(line)
	if direct != "":
		return direct
	var pat := _pattern(line)
	if pat != "":
		return pat
	var colon := line.find(": ")
	if colon > 0:
		var head := line.substr(0, colon)
		var tail := line.substr(colon + 2)
		if WORD_MAP.has(head):
			return String(WORD_MAP[head]) + " " + tail
		var head_zh := _lookup(head)
		if head_zh != "":
			return head_zh + "：" + tail
	return line

func _translate_block(s: String) -> String:
	if not s.contains("\n"):
		return _translate_line(s)
	var out: PackedStringArray = []
	for line in s.split("\n"):
		out.append(_translate_line(line))
	return "\n".join(out)

func _apply(n: Node) -> bool:
	var changed := false
	if n is Control or n is Window:
		for p in PROPS:
			if not (p in n):
				continue
			var v = n.get(p)
			if typeof(v) != TYPE_STRING:
				continue
			var s: String = v
			if s == "" or s.length() > 400:
				continue
			# 更新提示：直接隐藏（"UPDATE AVAILABLE: v0.6.2" / "有可用更新：v0.6.2"）
			if s.begins_with("UPDATE AVAILABLE") or s.begins_with("有可用更新"):
				if n is CanvasItem:
					(n as CanvasItem).visible = false
					if not hidden.has(n):
						hidden.append(n)
				continue
			var zh := _translate_block(s)
			if zh != "" and zh != s:
				n.set(p, zh)
				changed = true
	if n is PopupMenu:
		var pm := n as PopupMenu
		for i in pm.item_count:
			var it := pm.get_item_text(i)
			if it == "":
				continue
			var z := _lookup(it)
			if z != "" and z != it:
				pm.set_item_text(i, z)
				changed = true
	return changed

## "8 W, always on" → "8 W，常开"；"15 W at full torque" → "15 W，满扭矩时"
func _watts(s: String) -> String:
	var t := s.strip_edges()
	var cut := t.find(" W")
	if cut <= 0:
		return ""
	var head := t.substr(0, cut).strip_edges()
	if not head.is_valid_float():
		return ""
	var rest := t.substr(cut + 2)
	rest = rest.replace("\u00a0", " ").replace("  ", " ").strip_edges()
	if rest.contains("always on"):
		return head + " W，常开"
	if rest.contains("full torque"):
		return head + " W，满扭矩时"
	if rest.contains("full thrust"):
		return head + " W，满推力时"
	if rest.contains("active only while flying"):
		return head + " W，仅飞行时"
	return ""
