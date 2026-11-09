import struct, sys, os

p = sys.argv[1] if len(sys.argv) > 1 else r"D:\001wyh\newrf\RocketFoundry.pck"
d = open(p, "rb").read()
print("size", len(d), hex(len(d)))
print("magic", d[:4], "ver", struct.unpack_from("<I", d, 4)[0],
      "engine", struct.unpack_from("<III", d, 8),
      "flags", struct.unpack_from("<I", d, 20)[0],
      "file_base", struct.unpack_from("<Q", d, 24)[0],
      "dir_off32", struct.unpack_from("<Q", d, 32)[0])
print("tail u32:", struct.unpack_from("<I", d, len(d) - 4)[0], "tail u64:", struct.unpack_from("<Q", d, len(d) - 8)[0])

for off_field in (struct.unpack_from("<Q", d, 32)[0], struct.unpack_from("<Q", d, len(d) - 8)[0], struct.unpack_from("<Q", d, len(d) - 4)[0]):
    if off_field >= len(d):
        print(field := off_field, "out of range")
        continue
    cnt = struct.unpack_from("<I", d, off_field)[0]
    print("dir@%x count=%d" % (off_field, cnt))
    if 0 < cnt < 20000:
        o = off_field + 4
        for i in range(3):
            ln = struct.unpack_from("<I", d, o)[0]
            raw = d[o + 4:o + 4 + ln]
            print("  entry", ln, raw)
            o += 4 + ln + 16 + 4
