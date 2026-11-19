#!/bin/bash
# Root: make the verified iris + camera-LED DTB the default. Keeps the current default image as a
# rollback entry and preserves the existing GRUB menu (surface-secureboot-update rewrites it otherwise).
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
bundle=$(cd "$(dirname "$(realpath "$0")")/../../.." && pwd)
kernel=$(uname -r)
sb=/boot/secureboot
rb=$sb/rollback-dtb-20261119
entry='Surface before iris and camera LED DTB (2026-11-19)'
install -m644 "$bundle/drivers/files/rootfs/usr/lib/firmware/qcom/x1e80100/microsoft/qcvss8380.mbn" \
  /lib/firmware/qcom/x1e80100/microsoft/qcvss8380.mbn
install -d -m755 "$rb"
cp -a "$sb/vmlinuz-surface-signed.efi" "$sb/initrd.img-$kernel" /boot/surface-sl7-xplus.dtb "$rb/"
cp -a "$sb/grub.cfg" "$rb/grub.cfg.before"
install -m644 "$bundle/drivers/files/touchscreen/spi-gtch/surface-sl7-xplus-gtch.dtb" /boot/surface-sl7-xplus.dtb
/usr/local/sbin/surface-secureboot-update "$kernel" --skip-module-signing --dtb /boot/surface-sl7-xplus.dtb
python3 -I - "$rb/grub.cfg.before" "$entry" <<'PY'
import re, sys
from pathlib import Path
before, entry = Path(sys.argv[1]).read_text(), sys.argv[2]
b, e = '# SURFACE_DTB_ONCE_BEGIN', '# SURFACE_DTB_ONCE_END'
if b in before:
    before = before[:before.index(b)] + before[before.index(e) + len(e) + 1:]
i = before.find("menuentry 'Surface DTB trial")
if i >= 0:
    before = before[:i].rstrip() + "\n"
first = re.search(r"menuentry [^\n]+\{\n.*?\n\}", before, flags=re.S).group()
assert "/secureboot/vmlinuz-surface-signed.efi" in first
fallback = re.sub(r"menuentry [^\n]+", f"menuentry '{entry}' {{", first, count=1)
fallback = fallback.replace("/secureboot/vmlinuz-", "/secureboot/rollback-dtb-20261119/vmlinuz-").replace(
    "/secureboot/initrd.", "/secureboot/rollback-dtb-20261119/initrd.")
Path('/boot/secureboot/grub.cfg').write_text(before.rstrip() + "\n" + fallback + "\n")
PY
grub-script-check "$sb/grub.cfg"
sbverify --cert /var/lib/surface-secureboot/MOK.pem "$sb/vmlinuz-surface-signed.efi"
python3 -I - "$sb/vmlinuz-surface-signed.efi" /boot/surface-sl7-xplus.dtb <<'PY'
import struct, sys
blob = open(sys.argv[1], 'rb').read(); want = open(sys.argv[2], 'rb').read()
pe = struct.unpack_from("<I", blob, 0x3c)[0]; n = struct.unpack_from("<H", blob, pe + 6)[0]
table = pe + 24 + struct.unpack_from("<H", blob, pe + 20)[0]
for i in range(n):
    h = blob[table + i*40: table + (i+1)*40]
    if h[:8].rstrip(b"\0") == b".dtbauto":
        size, off = struct.unpack_from("<I", h, 8)[0], struct.unpack_from("<I", h, 20)[0]
        print("embedded DTB matches:", blob[off:off+size][:len(want)] == want)
PY
rm -rf "$sb/trial-dtb"
grep -nE "^menuentry|ONCE_BEGIN" "$sb/grub.cfg"
echo "Default image now carries the iris + camera LED DTB (effective next boot)."
