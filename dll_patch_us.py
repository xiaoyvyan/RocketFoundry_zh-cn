# -*- coding: utf-8 -*-
"""#US 字符串原地改写：保持条目字节长度不变，中文不足处用零宽空格补齐。
list:  python dll_patch_us.py list <dll> 关键字 [关键字...]
patch: python dll_patch_us.py patch <dll> <map.json>
"""
import struct, sys, json, io

def u16(b, o): return struct.unpack_from("<H", b, o)[0]
def u32(b, o): return struct.unpack_from("<I", b, o)[0]

def parse(data):
    e = u32(data, 0x3C)
    assert data[e:e+4] == b"PE\0\0"
    nsec = u16(data, e+6); optsz = u16(data, e+20); opt = e+24
    magic = u16(data, opt)
    dd = opt + (112 if magic == 0x20b else 96)
    cli_rva = u32(data, dd + 14*8)
    so = opt + optsz
    secs = []
    for i in range(nsec):
        vs, va, rs, rp = struct.unpack_from("<IIII", data, so + 40*i + 8)
        secs.append((va, vs, rp, rs))
    def r2o(rva):
        for va, vs, rp, rs in secs:
            if va <= rva < va + max(vs, rs):
                return rp + (rva - va)
        raise ValueError(hex(rva))
    cli = r2o(cli_rva)
    md = r2o(u32(data, cli + 8))
    assert data[md:md+4] == b"BSJB"
    vl = u32(data, md + 12); p = md + 16 + vl + 2
    ns = u16(data, p); p += 2
    streams = {}
    for _ in range(ns):
        off, size = struct.unpack_from("<II", data, p); p += 8
        end = data.index(b"\0", p); name = data[p:end].decode(); p = end + 1
        p = (p + 3) & ~3
        streams[name] = (md + off, size)
    return streams

def entries(data, off, size):
    out = []
    p = 1
    while p < size:
        start = p; n = data[off + p]
        if n & 0x80 == 0: ln = n; pre = 1
        elif n & 0xC0 == 0x80: ln = ((n & 0x3F) << 8) | data[off+p+1]; pre = 2
        else: ln = ((n & 0x1F) << 24) | (data[off+p+1] << 16) | (data[off+p+2] << 8) | data[off+p+3]; pre = 4
        if ln == 0 or p + pre + ln > size:
            break
        raw = data[off+p+pre:off+p+pre+ln]
        try:
            txt = raw[:-1].decode("utf-16-le")
        except Exception:
            txt = ""
        out.append((start, pre, ln, txt))
        p += pre + ln
    return out

def main():
    cmd = sys.argv[1]; dll = sys.argv[2]
    data = bytearray(io.open(dll, "rb").read())
    st = parse(data)
    us_off, us_size = st["#US"]
    items = entries(data, us_off, us_size)
    if cmd == "list":
        keys = sys.argv[3:] or [""]
        seen = {}
        for start, pre, ln, txt in items:
            if not txt: continue
            if any(k in txt for k in keys):
                seen.setdefault((txt, ln), 0)
                seen[(txt, ln)] += 1
        for (txt, ln), c in sorted(seen.items()):
            print("%3d  len=%2d  %r" % (c, ln, txt))
    elif cmd == "patch":
        m = json.load(io.open(sys.argv[3], encoding="utf-8"))
        hit = skip = toolong = 0
        for start, pre, ln, txt in items:
            if txt not in m: continue
            zh = m[txt]
            body = zh.encode("utf-16-le")
            if len(body) + 1 > ln:
                toolong += 1
                print("TOO_LONG %r -> %r need %d have %d" % (txt, zh, len(body)+1, ln)); continue
            pad = ln - 1 - len(body)
            if pad % 2: pad -= 1
            body = body + ("\u200b" * (pad // 2)).encode("utf-16-le")
            assert len(body) + 1 == ln
            base = us_off + start + pre
            data[base:base+ln] = body + b"\x00"
            hit += 1
        io.open(dll, "wb").write(data)
        print("patched", hit, "too_long", toolong)

main()
