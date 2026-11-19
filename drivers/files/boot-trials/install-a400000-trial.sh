#!/bin/bash
# Root: install the a400000 load-order softdep into the initramfs. The initramfs hook re-signs the default image and
# rewrites /boot/secureboot/grub.cfg, so the current menu is restored afterwards with a pre-trial rollback entry.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
here=$(dirname "$(realpath "$0")")
kernel=$(uname -r)
sb=/boot/secureboot
rb=$sb/rollback-a400000-20261119
entry='Surface before a400000 softdep (2026-11-19)'
install -d -m755 "$rb"
cp -a "$sb/vmlinuz-surface-signed.efi" "$sb/initrd.img-$kernel" "$rb/"
cp -a "$sb/grub.cfg" "$rb/grub.cfg.before"
install -m644 "$here/a400000-order.conf" /etc/modprobe.d/surface-a400000-order.conf
update-initramfs -u -k "$kernel"
python3 -I - "$rb/grub.cfg.before" "$entry" <<'PY'
import re, sys
from pathlib import Path
before, entry = Path(sys.argv[1]).read_text(), sys.argv[2]
i = before.find(f"menuentry '{entry}'")
if i >= 0:
    before = before[:i].rstrip() + "\n"
first = re.search(r"menuentry [^\n]+\{\n.*?\n\}", before, flags=re.S).group()
assert "/secureboot/vmlinuz-surface-signed.efi" in first
fallback = re.sub(r"menuentry [^\n]+", f"menuentry '{entry}' {{", first, count=1)
fallback = fallback.replace("/secureboot/vmlinuz-", "/secureboot/rollback-a400000-20261119/vmlinuz-").replace(
    "/secureboot/initrd.", "/secureboot/rollback-a400000-20261119/initrd.")
Path('/boot/secureboot/grub.cfg').write_text(before.rstrip() + "\n" + fallback + "\n")
PY
grub-script-check "$sb/grub.cfg"
sbverify --cert /var/lib/surface-secureboot/MOK.pem "$sb/vmlinuz-surface-signed.efi"
lsinitramfs "$sb/initrd.img-$kernel" | grep -q 'etc/modprobe.d/surface-a400000-order.conf'
echo "softdep in the signed initrd:"; unmkinitramfs "$sb/initrd.img-$kernel" /tmp/a400-initrd >/dev/null 2>&1 && cat /tmp/a400-initrd/main/etc/modprobe.d/surface-a400000-order.conf 2>/dev/null | grep softdep || true; rm -rf /tmp/a400-initrd
grep -nE "^menuentry" "$sb/grub.cfg"
