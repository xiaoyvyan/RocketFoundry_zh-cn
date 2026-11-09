# Rocket Foundry v0.6.4 汉化说明

汉化对象：`D:\001wyh\newrf\RocketFoundry.exe`（Godot 4.7.2 mono 导出，v0.6.4）
参照工程：`D:\001wyh\rf`（v0.6.1 的完整汉化管线，本次按同一套方法移植）
当前成品：`D:\001wyh\newrf\RocketFoundry.pck`（754,610,296 字节，9149 条目，`verify_pck.py` 全量校验 `bad=0`）
构建产物副本：`D:\001wyh\newrf\build\RocketFoundry.zh.pck`

---

## 一、三条通路（缺一不可）

| 通路 | 载体 | 覆盖对象 |
| --- | --- | --- |
| 数据层 | `extract\assets\parts\*\part.json`、`catalogs\stock_parts.json` | 部件名、尺寸、变体名、说明长文 |
| 显示层 | `res://zh/zh_ui.json`（3938 条）+ `res://zh/ui_zh.gd`（autoload，`override.cfg` 注册） | 常规 UI 文本：菜单、设置、建造器、存档、模组页、暂停菜单、tooltip；另含 `_pattern()` 格式规则（`N craft here.`、`Install (14 KB)`、`+1 more`、`Continue 67`、`ROOM ABCDEF`）与 `COUNTERS` 数量单位（个恒星系 / 颗行星 / 个结构） |
| 程序集自绘 | `#US` 帽子原地等长改写（`tools\dll_patch_us.py` + `tools\us_map_hud2..6.json`） | `draw_string` 自绘、显示层拿不到的行：HUD 顶栏/底栏、分级表、资源面板、自动化面板、暂停菜单里由代码拼接的句子 |

`#US` 改写保持条目字节长度不变（中文不足处补零宽空格），PE 结构与元数据布局不动；运行期 DLL 同步到
`C:\Users\Administrator\AppData\Local\data_RocketFoundry_windows_x86_64\RocketFoundry.dll`。

---

## 二、实机验证结果（窗口 1296×759，截图在 `tools\dumps\`）

| 页面 | 状态 |
| --- | --- |
| 标题栏 | 火箭铸造厂 |
| 主菜单 / 开始游戏 / 训练（40+ 课程）/ 沙盒存档 / 新建沙盒 | 全中文 |
| 设置六页（图形·飞行读数·玩法·音频·操作·隐私） | 全中文，含浮动说明长句 |
| 建造器 | 分类页签、顶栏读数（地面推重比/湿重/最大推力/SAS 配平）、部件卡与详情长文、退出确认全中文 |
| 建造器设置面板 | 生成器设置 / 放置精度（网格 0.2 米·0.1 m·0.05 m·0.01 m·自由）/ 建造选项 / 小部件更好选中 / 手柄抓取范围 / 宽松选择区域 / 贴花吸附网格 / 改变尺寸时推开部件 / 拖到部件栏上即删除 / 部件穿插（允许重叠）/ 叠加显示 / 部件碰撞体 / 质心 |
| 社区机库 / 模组页 | 主体中文（模组名、作者名、火箭名属投稿内容，保留原文） |
| 飞行 HUD | 飞行数据「TWR 当前/最大」、分级表（分级 / Δv m/s / 推重比 / 燃烧 / 质量 t / 合计）、资源面板、底栏（速度 地面 / 离地高度 / 油门 / 引擎 / RCS / SAS / 姿态 手动 / 全部分级）、自动化面板（程序 / 状态 / 自动化运行中 / 已启用 / 添加 / 自动）|
| 暂停菜单 | 已暂停、飞行/飞船/传送/工具/作弊码/设置、本次飞行/存档与回退/离开，逐条 tooltip 全中文 |
| 飞船上 | 「此处有 1 艘飞船。」「Sol，你在此处」「飞船 · 着陆于地球 · 0 m/s」「小行星 · 环绕 Earth · 68.6 m/s」 |

---

## 三、仍保留英文（有意为之 / 未覆盖）

1. `HUD`（顶栏按钮）：与 `GetNode("HUD")` 同名，译成中文会让 `FlightScene` 抛 `Node not found`。
2. `Left`（资源面板表头）、`PAUSE` / `TAKE OVER` / `LOG`（自动化面板按钮）、`On player hotkey`：这些是单个泛用词，写入 `#US` 前被保留词黑名单拦下（`Left` 是布局节点名，`PAUSE/LOG/ADD/AUTO` 若是程序操作 id 被改写会影响自动化脚本编辑），显示层也未覆盖，故保留原文。
3. `Mass t` 已改成「质量 t」；`Earth` 等天体名在部分拼接句里仍是英文（`环绕 Earth`）。
4. 模组作者自定的模组名/描述、玩家投稿火箭名与作者名：设计上不翻。
5. `.scn` 场景内少量短语、任务/合同长篇简报、天体 `features` 地貌专名：未逐一盘点。

---

## 四、重建方法

```powershell
Stop-Process -Name RocketFoundry -Force   # 运行期 DLL 被占用，必须先关游戏
cd D:\001wyh\newrf\tools
python build_layer.py                      # 8 步：merge 译文 → 原版 DLL 打 #US → 同步运行期 DLL
                                           # → 算字集 → 换字体 → 写表 → 打包 → 覆盖安装 + 写 override.cfg
python verify_pck.py D:\001wyh\newrf\RocketFoundry.pck   # 全量校验，期望 bad=0
```

译文新增：`translate\zh_ui_3.json`（手工条）→ `merge_tr.py` 的 hand 列表已包含；
新 `#US` 映射：`tools\us_map_hud6.json` 等 → `build_layer.py` 的打补丁循环已扩展；
写表前务必 `python check_us_map.py us_map_*.json`，确认没有撞上 Godot 类型名/布局节点名。

## 五、还原

`backup\RocketFoundry.pck.orig`、`backup\RocketFoundry.dll.orig` 覆盖回原位置，删除 `override.cfg` 即可回到英文原版。
