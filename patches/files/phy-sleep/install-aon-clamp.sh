#!/bin/bash
# Root: install phy-qcom-qmp-combo with the X1E80100 PCS_AON clamp offsets fix (patches/03-...) on top of the
# system-sleep patch. Keeps the current image as a GRUB rollback entry and preserves the GRUB menu.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
here=$(dirname "$(realpath "$0")")
kernel=$(uname -r); sb=/boot/secureboot; rb=$sb/rollback-aon-clamp-20261120
mod=/lib/modules/$kernel/updates/surface/phy-qcom-qmp-combo.ko
entry='Surface before PHY AON clamp fix (2026-11-20)'
want=$(modinfo -F srcversion "$here/files/aon-clamp/phy-qcom-qmp-combo.ko")
install -d -m755 "$rb"
cp -a "$sb/vmlinuz-surface-signed.efi" "$sb/initrd.img-$kernel" "$mod" "$rb/"
cp -a "$sb/grub.cfg" "$rb/grub.cfg.before"
install -m644 "$here/files/aon-clamp/phy-qcom-qmp-combo.ko" "$mod"
/usr/local/sbin/surface-secureboot-update "$kernel" --dtb /boot/surface-sl7-xplus.dtb
python3 -I - "$rb/grub.cfg.before" "$entry" <<'PY'
import re, sys
from pathlib import Path
before, entry = Path(sys.argv[1]).read_text(), sys.argv[2]
i = before.find(f"menuentry '{entry}'")
if i >= 0: before = before[:i].rstrip() + "\n"
first = re.search(r"menuentry [^\n]+\{\n.*?\n\}", before, flags=re.S).group()
assert "/secureboot/vmlinuz-surface-signed.efi" in first
fb = re.sub(r"menuentry [^\n]+", f"menuentry '{entry}' {{", first, count=1)
fb = fb.replace("/secureboot/vmlinuz-", "/secureboot/rollback-aon-clamp-20261120/vmlinuz-").replace("/secureboot/initrd.", "/secureboot/rollback-aon-clamp-20261120/initrd.")
Path('/boot/secureboot/grub.cfg').write_text(before.rstrip() + "\n" + fb + "\n")
PY
grub-script-check "$sb/grub.cfg"
sbverify --cert /var/lib/surface-secureboot/MOK.pem "$sb/vmlinuz-surface-signed.efi"
[[ $(modinfo -F srcversion "$mod") == "$want" ]] && echo "installed srcversion $want"
modinfo -F signer "$mod" | sed 's/^/signer: /'
lsinitramfs "$sb/initrd.img-$kernel" | grep -q "updates/surface/phy-qcom-qmp-combo.ko" && echo "module in signed initrd"
grep -nE "^menuentry" "$sb/grub.cfg"
