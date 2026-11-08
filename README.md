# Rocket Foundry 汉化说明

汉化对象：RocketFoundry.exe（Godot 4.7.2 mono 导出，游戏版本 v0.6.1）
汉化方式：直接改写游戏资源包 `RocketFoundry.pck` 内的 .NET 程序集字符串 + 替换内置字体为带中文字形的子集字体。
当前状态：**技术链路全部打通并已在真实游戏画面验证**；译文覆盖为第一批（约 1369 条），界面骨架已中文化，其余正文仍在英文。

---

## 一、当前效果（实机验证）

| 位置 | 状态 |
| --- | --- |
| 主菜单 | `继续` `开始游戏` `训练` `多人` `社区机库` `更多` `模组` `设置` 全中文；副标题「终极 2D 太空建造」 |
| 设置页 | 标题「设置」，标签页「图形 / 飞行读数 / 玩法 / 音频 / 操作 / 隐私」全中文 |
| 设置·图形页 | 13 行全部中文：浅色模式、帧率上限、显示帧率、边缘平滑、行星分辨率、界面尺寸、全屏(F11)、发动机镜头抖动、远处飞船标记、体积尾焰、昼夜光照、残骸、残骸保留比例（选项值 关 / 完整 / 均衡 / 引爆 / 保留 亦中文） |
| 设置·玩法页 | 手柄抓取范围、部件重叠作弊、慢动作时间加速、点火时全油门、多人聊天、多人网络状态、温度单位、默认引力模型、引力助推建议、轨道线分段数（选项 渐隐 / 全部 / 拼接圆锥 / N 体 已译） |
| 设置·隐私页 | 分享游戏分析数据 + 说明段落 |
| 设置·操作页 | 「按键设置」弹窗：建造器 / 时间与视角 / 飞行 / 舱外活动 分组与 60 余条按键说明 |
| 飞行 HUD | `星图` `保存` `载入` `时间加速` `着陆` `离地高度` `垂直速度` `水平速度` `油门` `姿态` `手动` `自动` `速度` `高度` `电池` 等中文 |
| 中文字形 | 正常渲染，无方框/豆腐块（已把 7 个内置 TTF 换成等线 + 常用字子集） |

仍未翻译：训练/教程列表与长句、任务与合同文案、社区机库页面、天体名称与描述、飞行读数编辑器里的条目名称与说明、音频页部分行、部件编辑器内部提示等。

---

## 二、为什么必须同时改两个位置（关键坑）

游戏首次启动时，会把 pck 内的 .NET 运行时与程序集**解压到磁盘**：

```
%LOCALAPPDATA%\data_RocketFoundry_windows_x86_64\RocketFoundry.dll
```

运行时实际加载的是这份副本，**不是 pck 里的那份**。因此：
- 只改 pck → 界面毫无变化（本机踩过这个坑）；
- 必须两边一起改，或用一键脚本 `tools\apply_zh.py`（它同时覆盖 pck 与这份副本）。

另一个限制：游戏不支持 `--main-pack` 指定别的资源包，只能原地替换 `RocketFoundry.pck`。

---

## 三、目录与文件

| 路径 | 说明 |
| --- | --- |
| `RocketFoundry.pck` | 当前已汉化的资源包（生效中） |
| `backup\RocketFoundry.pck.orig` | 原版资源包备份，**勿删** |
| `backup\RocketFoundry.dll.orig` | 原版程序集备份，**勿删**（每次构建都从它还原，避免叠加注入） |
| `backup\RocketFoundry.dll.extracted_orig` | 原版「解压出来的程序集副本」备份，**勿删** |
| `extract\` | pck 解包工作区（9044 个文件，已被就地修改） |
| `translate\` | 译文数据：`zh_ui_1.json` / `zh_ui_2.json`（手写）、`zh_mt.json`（机翻过滤后）、`zh_all.json`（合并结果，唯一生效源） |
| `translate\todo_strings.txt` | 尚未翻译的候选字符串（3.2 万条，按长度排序），下一轮补译直接从这里挑 |
| `build\` | 构建中间产物：汉化 pck、字体子集、字符集 |
| `tools\` | 全部脚本，见下 |

### 脚本

| 脚本 | 作用 |
| --- | --- |
| `apply_zh.py` | **一键汉化**：构建 → 覆盖 pck → 同步程序集副本 |
| `build_zh.py` | 全流程构建：合并译文 → 还原 DLL → 注入 → 生成字体字集 → 换字体 → 打包 |
| `inject_dll.py` | 把译文写回 DLL 的 `#US` 字符串堆（等长替换，补零宽空格，零风险） |
| `font_patch.py` | 解压 `RSCC` 字体容器、替换内嵌 TTF 为中文子集、重新压缩回写 |
| `pack_pck.py` | 按原目录结构重新打包 pck |
| `merge_tr.py` | 合并手写表与机翻表（手写优先） |
| `post_mt.py` / `clean_mt.py` | 机翻结果过滤（去误译、去 markup、去未翻译） |
| `todo_list.py` | 生成待译清单 |
| `verify_pck.py` | 校验 pck 目录结构、条目 md5、以及中文是否真的写进去了 |
| `verify_ui.py` | 核对设置页词条是否真的进了实际加载的 DLL |
| `add_settings.py` / `add_keys.py` | 成批追加设置页与按键设置译文（自动跳过超长项） |
| `near.py` / `find_labels.py` / `list_labels.py` | 从字符串堆里定位并列出界面标签，找漏译用 |

---

## 四、如何继续补译（重要）

1. 从 `translate\todo_strings.txt` 里挑句子，译好后写入 `zh_ui_2.json`（键必须**与游戏内字符串完全一致**，含大小写与首尾空格，例如 `Continue ` 带尾空格）。
2. 跑 `python D:\001wyh\rf\tools\apply_zh.py`，它会自动重算字体字集（**新译文里的字会自动进字体，不会显示方块**）、重打包并安装。
3. 译名规则（当前采用的约定）：
   - 部件 `part` → 部件；级 `stage` → 分级；贮箱 `tank` → 贮箱；推力/比冲/质量保留专业词。
   - 天体专名暂保留英文（`Local Volume`、`Virgo Cluster`、`SA(s)b` 等），避免半中半英的拼接误差。
   - 自动化事件名（`*.PRESSED`、`*.UPDATED`）、命名空间方法名（`Host.*`、`Launch.*`）、shader 源码、`#RRGGBB` 颜色值、纯 id **一律不译**。

### 已知限制
- 译文长度不得超过原字符串字符数，超出会被跳过（当前 10 条因此未写入，列表见 `zh_all.json.toolong.json`）。真要突破需要重写 IL 与重排字符串堆，风险高。
- 机翻（MyMemory）质量一般，`zh_mt.json` 里已过滤掉明显误译；仍建议后续人工校对。

---

## 五、回退到原版

```
copy backup\RocketFoundry.pck.orig  RocketFoundry.pck
copy backup\RocketFoundry.dll.extracted_orig  %LOCALAPPDATA%\data_RocketFoundry_windows_x86_64\RocketFoundry.dll
```

（若想彻底重置，删除 `%LOCALAPPDATA%\data_RocketFoundry_windows_x86_64` 目录，游戏会从 pck 重新解压。）

---

## 六、验证记录

- `--headless --quit` 启动：exit 0，输出 `引导就绪  (数据: …)`，仅有原版就带有的 `audio/menu_music.ogg` 加载报错（与汉化无关）。
- 实机窗口截图：主菜单、设置页（图形/玩法/操作/隐私）、飞行 HUD 确认中文字形与文案正常。
- 程序集内核对：图形页 13 行、玩法页 10 行、隐私页标题、按键设置分组等字符串均已写入实际加载的 DLL（`tools\verify_ui.py` 可复查）。
- 当前译文规模：`zh_all.json` 1786 条；最近一次注入 matched 1573 / written 1563 / too_long 10。
