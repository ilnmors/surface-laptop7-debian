#!/bin/bash
# Root: install dwc3-qcom with the ss-wake fix and phy-qcom-qmp-combo back to the AON-clamp build (normal
# autonomous detection). Both are signed by surface-secureboot-update; the current image goes to rollback-trial
# and the GRUB menu is preserved.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
here=$(dirname "$(realpath "$0")"); files=$(realpath "$here/..")
kernel=$(uname -r); sb=/boot/secureboot; rb=$sb/rollback-trial; upd=/lib/modules/$kernel/updates/surface
entry='Surface before the current PHY trial'
free_mb=$(df -m --output=avail /boot | tail -1 | tr -d ' ')
(( free_mb >= 600 )) || { echo "only ${free_mb} MB free on /boot" >&2; exit 1; }
declare -A src=([dwc3-qcom.ko]="$here/dwc3-qcom.ko" [phy-qcom-qmp-combo.ko]="$files/phy-sleep/files/aon-clamp/phy-qcom-qmp-combo.ko")
declare -A want
for m in "${!src[@]}"; do want[$m]=$(modinfo -F srcversion "${src[$m]}"); done
rm -rf "$rb"; install -d -m755 "$rb"
cp -a "$sb/vmlinuz-surface-signed.efi" "$sb/initrd.img-$kernel" "$rb/"
cp -a "$sb/grub.cfg" "$rb/grub.cfg.before"
for m in "${!src[@]}"; do cp -a "$upd/$m" "$rb/" ; install -m644 "${src[$m]}" "$upd/$m"; done
depmod -a "$kernel"
/usr/local/sbin/surface-secureboot-update "$kernel" --dtb /boot/surface-sl7-xplus.dtb
python3 -I - "$rb/grub.cfg.before" "$entry" <<'PY'
import re, sys
from pathlib import Path
before, entry = Path(sys.argv[1]).read_text(), sys.argv[2]
i = before.find(f"menuentry '{entry}'")
if i >= 0:
    j = before.find("\n}\n", i); before = before[:i] + before[j + 3:]
first = re.search(r"menuentry [^\n]+\{\n.*?\n\}", before, flags=re.S).group()
fb = re.sub(r"menuentry [^\n]+", f"menuentry '{entry}' {{", first, count=1)
fb = fb.replace("/secureboot/vmlinuz-", "/secureboot/rollback-trial/vmlinuz-").replace("/secureboot/initrd.", "/secureboot/rollback-trial/initrd.")
Path('/boot/secureboot/grub.cfg').write_text(before.rstrip() + "\n" + fb + "\n")
PY
grub-script-check "$sb/grub.cfg"
sbverify --cert /var/lib/surface-secureboot/MOK.pem "$sb/vmlinuz-surface-signed.efi"
for m in "${!src[@]}"; do v=$(modinfo -F srcversion "$upd/$m"); [[ $v == "${want[$m]}" ]] || { echo "$m mismatch $v" >&2; exit 1; }; echo "$m $v signer=$(modinfo -F signer "$upd/$m")"; lsinitramfs "$sb/initrd.img-$kernel" | grep -q "updates/surface/$m" && echo "  in signed initrd"; done
grep -cE "^menuentry" "$sb/grub.cfg" | sed 's/^/menu entries: /'; df -h /boot | tail -1
