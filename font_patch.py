"""把 CJK 字体注入 Godot .fontdata（RSCC 容器 + 内嵌 TTF 原位替换）。
用法: python font_patch.py <out_dir>
"""
import struct, zstandard, glob, os, sys, io
from fontTools.ttLib import TTFont
from fontTools import subset as ftsubset

IMPORTED = r"D:\001wyh\newrf\extract\.godot\imported"
SKIP = ("lucide",)
REG = r"C:\Windows\Fonts\Deng.ttf"
BLD = r"C:\Windows\Fonts\Dengb.ttf"
CACHE = r"D:\001wyh\newrf\build\fonts"
CHARSET = r"D:\001wyh\newrf\build\charset.txt"


def rscc_decompress(b):
    assert b[:4] == b"RSCC"
    ver, bs, total = struct.unpack_from("<III", b, 4)
    nblk = (total + bs - 1) // bs
    tab = struct.unpack_from("<%dI" % nblk, b, 16)
    off = 16 + 4 * nblk
    d = zstandard.ZstdDecompressor()
    out = bytearray()
    for i in range(nblk):
        out += d.decompress(b[off:off + tab[i]], max_output_size=bs)
        off += tab[i]
    assert len(out) == total, (len(out), total)
    return bytes(out)


def rscc_compress(body, bs=4096):
    nblk = (len(body) + bs - 1) // bs
    cctx = zstandard.ZstdCompressor(level=10)
    blocks = []
    for i in range(nblk):
        blocks.append(cctx.compress(body[i * bs:(i + 1) * bs]))
    head = b"RSCC" + struct.pack("<III", 2, bs, len(body))
    head += struct.pack("<%dI" % nblk, *[len(x) for x in blocks])
    return head + b"".join(blocks)


def find_ttf(body):
    """返回 (ttf_off, ttf_len)"""
    cand = []
    for magic in (b"\x00\x01\x00\x00", b"OTTO"):
        i = body.find(magic)
        while i >= 0:
            if i >= 4:
                ln = struct.unpack_from("<I", body, i - 4)[0]
                nt = struct.unpack_from(">H", body, i + 4)[0]
                if 5 <= nt <= 40 and 5000 <= ln <= len(body) and i + ln <= len(body):
                    tag = body[i + 12:i + 16]
                    if all(32 <= c < 127 for c in tag):
                        cand.append((i, ln))
            i = body.find(magic, i + 1)
    if not cand:
        raise RuntimeError("no embedded ttf")
    return cand[0]


def build_subset(src, out_path, chars):
    import subprocess, tempfile
    tf = tempfile.mktemp(suffix=".txt")
    open(tf, "w", encoding="utf-8").write(chars)
    cmd = [sys.executable, "-m", "fontTools.subset", src, "--output-file=" + out_path,
           "--text-file=" + tf, "--layout-features=*", "--name-IDs=*", "--name-languages=*",
           "--notdef-outline", "--drop-tables+=DSIG", "--recalc-bounds"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:], r.stderr[-4000:])
        raise RuntimeError("subset failed")
    if r.stderr.strip():
        print("subset warnings:", r.stderr.strip().splitlines()[:3])
    os.remove(tf)
    return out_path


def main(out_dir):
    os.makedirs(CACHE, exist_ok=True)
    if os.path.exists(CHARSET):
        chars = open(CHARSET, encoding="utf-8").read()
    else:
        chars = "".join(chr(c) for c in range(0x20, 0x7F)) + "，。、；：？！…—·《》“”‘’（）【】"
    reg = build_subset(REG, os.path.join(CACHE, "zh_regular.ttf"), chars)
    bld = build_subset(BLD, os.path.join(CACHE, "zh_bold.ttf"), chars)
    blobs = {"reg": open(reg, 'rb').read(), "bld": open(bld, 'rb').read()}
    print("subset sizes:", len(blobs["reg"]), len(blobs["bld"]))

    n = 0
    for p in sorted(glob.glob(os.path.join(IMPORTED, "*.fontdata"))):
        name = os.path.basename(p)
        if any(s in name for s in SKIP):
            print("skip icon font", name)
            continue
        b = open(p, 'rb').read()
        body = rscc_decompress(b)
        off, ln = find_ttf(body)
        key = "bld" if ("Bold" in name) else "reg"
        new = blobs[key]
        nb = bytearray(body[:off] + new + body[off + ln:])
        struct.pack_into("<I", nb, off - 4, len(new))
        out = rscc_compress(bytes(nb))
        dst = os.path.join(out_dir, os.path.relpath(p, r"D:\001wyh\newrf\extract"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(out)
        print("patched", name[:40], "ttf", ln, "->", len(new), "file", len(b), "->", len(out))
        n += 1
    print("patched fonts:", n)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else r"D:\001wyh\newrf\extract")
