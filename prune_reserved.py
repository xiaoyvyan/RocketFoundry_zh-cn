import json, os, shutil, time

TR = r"D:\001wyh\newrf\translate"
TABLES = ["zh_test.json", "zh_ui_1.json", "zh_ui_2.json", "zh_mt.json"]

# Godot 内建类名（大小写敏感 + 全大写形式）——被当作 type name 使用，绝不能译
TYPES = """Node Node2D Control Button Label RichTextLabel Panel PanelContainer PopupPanel Window
AcceptDialog ConfirmationDialog LineEdit TextEdit SpinBox Slider HSlider VSlider Range ProgressBar
TextureButton TextureProgressBar CheckBox CheckButton OptionButton MenuButton LinkButton ItemList Tree
TreeItem PopupMenu Popup TabBar TabContainer ScrollContainer MarginContainer VBoxContainer HBoxContainer
GridContainer CenterContainer AspectRatioContainer FlowContainer SplitContainer HSplitContainer
VSplitContainer ColorRect TextureRect NinePatchRect Sprite2D Sprite3D Texture2D GradientTexture2D
Camera2D Camera3D CanvasLayer CanvasItem Viewport SubViewport Container BoxContainer BaseButton
ColorPicker ColorPickerButton ColorPickerPopup FileDialog Timer Tween AnimationPlayer AnimationTree
Theme StyleBoxEmpty StyleBoxFlat StyleBoxTexture Gradient GradientTexture1D Curve CurveTexture
Line2D Polygon2D CollisionShape2D CollisionPolygon2D Area2D StaticBody2D RigidBody2D CharacterBody2D
Shape2D RectangleShape2D CircleShape2D CapsuleShape2D SegmentShape2D World2D Physics2D GodotObject
Object RefCounted Resource PackedScene NodePath StringName Variant InputEvent InputEventKey InputEventMouse
InputEventMouseButton InputEventMouseMotion InputEventAction InputEventJoypadButton InputEventJoypadMotion
InputEventScreenTouch InputEventScreenDrag InputEventMagnifyGesture InputEventPanGesture InputEventMIDI
AudioStreamPlayer AudioStreamPlayer2D AudioStreamPlayer3D AudioStream AudioStreamOggVorbis
AudioStreamMP3 AudioStreamWAV AudioEffect AudioBusLayout RichTextEffect FontFile FontVariation Font
SystemFont TextServer Label3D MeshInstance3D MultiMeshInstance3D MultiMesh Image ImageTexture
CameraAttributes Environment WorldEnvironment DirectionalLight2D PointLight2D Light2D Light3D CanvasModulate
TileMap TileMapLayer TileSet ShaderMaterial ShaderMaterial CanvasItemMaterial StandardMaterial3D
Curve3D Path2D PathFollow2D RemoteTransform2D Marker2D CPUParticles2D GPUParticles2D
GPUParticlesCollision2D RayCast2D VisibleOnScreenNotifier2D VisibleOnScreenEnabler2D
Parallax2D ParallaxLayer ParallaxBackground AnimatedSprite2D AnimationMixer EditorPlugin""".split()

# 代码里当节点名/内部键用的一批布局词（Title case 形式）
LAYOUT = """Backdrop Background Border Bottom Body Card Cards Center Chrome Column Columns Content
Contents Context Deck Divider Edge Ends Footer Frame Frames Front Gap Grid Group Groups Handle Header
Heading Height Hidden Hide Icon Icons Inner Label Labels Layer Layers Left Line Lines Margin Marker
Middle Mount Outer Overlay Padding Panel Panels Pivot Placeholder Root Row Rows Rule Scroll Separator
Shadow Shell Spacer Spacing Stack Stroke Surface Tab Tabs Text Title Track Width Wrapper""".split()

reserved = set(TYPES) | set(LAYOUT)
# 大写形式也一并加入（很可能是同一字符串的常量形式），但只针对 TYPES，避免误伤 UI 大写标签
reserved |= {t.upper() for t in TYPES}

stamp = time.strftime("%Y%m%d_%H%M%S")
bkdir = os.path.join(TR, "bak_" + stamp)
os.makedirs(bkdir, exist_ok=True)

dropped_total = {}
for t in TABLES:
    p = os.path.join(TR, t)
    if not os.path.exists(p):
        continue
    shutil.copy2(p, os.path.join(bkdir, t))
    d = json.load(open(p, encoding="utf-8"))
    dropped = {k: v for k, v in d.items() if k in reserved}
    kept = {k: v for k, v in d.items() if k not in reserved}
    json.dump(kept, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dropped_total[t] = dropped
    print(t, "before", len(d), "dropped", len(dropped), "after", len(kept))

allk = set()
for v in dropped_total.values():
    allk |= set(v)
print("unique dropped", len(allk))
print("DROPPED:", json.dumps(sorted(allk), ensure_ascii=False))
print("backup:", bkdir)
