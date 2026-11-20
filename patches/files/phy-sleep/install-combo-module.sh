#!/bin/bash
# Root: install a given phy-qcom-qmp-combo.ko (signed by surface-secureboot-update), keeping the current image as a
# GRUB rollback entry and preserving the GRUB menu. Usage: install-combo-module.sh <module.ko> <rollback-dir-name> <entry title>
# Trials reuse rollback-trial so only one trial copy stays on /boot.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
src=$(realpath "$1"); name=$2; entry=$3
kernel=$(uname -r); sb=/boot/secureboot; rb=$sb/$name
mod=/lib/modules/$kernel/updates/surface/phy-qcom-qmp-combo.ko
want=$(modinfo -F srcversion "$src")
# A new image, initrd and the rollback copy need about 450 MB; /boot is 2 GB and filled up once (2026-11-20).
free_mb=$(df -m --output=avail /boot | tail -1 | tr -d ' ')
(( free_mb >= 600 )) || { echo "only ${free_mb} MB free on /boot; clean old rollbacks first" >&2; exit 1; }
# Reusing a name (e.g. rollback-trial for every trial) replaces that copy instead of adding another.
rm -rf "$rb"
install -d -m755 "$rb"
cp -a "$sb/vmlinuz-surface-signed.efi" "$sb/initrd.img-$kernel" "$mod" "$rb/"
cp -a "$sb/grub.cfg" "$rb/grub.cfg.before"
install -m644 "$src" "$mod"
/usr/local/sbin/surface-secureboot-update "$kernel" --dtb /boot/surface-sl7-xplus.dtb
python3 -I - "$rb/grub.cfg.before" "$entry" "$name" <<'PY'
import re, sys
from pathlib import Path
before, entry, name = Path(sys.argv[1]).read_text(), sys.argv[2], sys.argv[3]
i = before.find(f"menuentry '{entry}'")
if i >= 0: before = before[:i].rstrip() + "\n"
first = re.search(r"menuentry [^\n]+\{\n.*?\n\}", before, flags=re.S).group()
assert "/secureboot/vmlinuz-surface-signed.efi" in first
fb = re.sub(r"menuentry [^\n]+", f"menuentry '{entry}' {{", first, count=1)
fb = fb.replace("/secureboot/vmlinuz-", f"/secureboot/{name}/vmlinuz-").replace("/secureboot/initrd.", f"/secureboot/{name}/initrd.")
Path('/boot/secureboot/grub.cfg').write_text(before.rstrip() + "\n" + fb + "\n")
PY
grub-script-check "$sb/grub.cfg"
sbverify --cert /var/lib/surface-secureboot/MOK.pem "$sb/vmlinuz-surface-signed.efi"
[[ $(modinfo -F srcversion "$mod") == "$want" ]] && echo "installed srcversion $want"
lsinitramfs "$sb/initrd.img-$kernel" | grep -q "updates/surface/phy-qcom-qmp-combo.ko" && echo "module in signed initrd"
grep -cE "^menuentry" "$sb/grub.cfg" | sed 's/^/menu entries: /'
