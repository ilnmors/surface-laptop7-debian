#!/bin/bash
# Root: build a signed one-shot image with surface-sl7-xplus-trial.dtb (camera privacy LED + iris) and
# select it for the next boot only. The default signed image and the default GRUB entry stay unchanged;
# GRUB clears next_entry before booting, so the following boot returns to the default image.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
here=$(dirname "$(realpath "$0")")
kernel=$(uname -r)
out=/boot/secureboot/trial-dtb
entry='Surface DTB trial: camera LED + iris (one-shot)'
install -d -m755 "$out"
install -m644 "$here/surface-sl7-xplus-trial.dtb" "$out/surface-sl7-xplus-trial.dtb"
/usr/local/sbin/surface-secureboot-update "$kernel" --skip-module-signing \
  --dtb "$out/surface-sl7-xplus-trial.dtb" --output-directory "$out" --no-bootloader-update
python3 -I - "$entry" <<'PY'
import re, sys
from pathlib import Path
entry = sys.argv[1]
p = Path('/boot/secureboot/grub.cfg'); t = p.read_text()
i = t.find(f"menuentry '{entry}'")
if i >= 0:
    t = t[:i].rstrip() + "\n"
first = re.search(r"menuentry [^\n]+\{\n.*?\n\}", t, flags=re.S)
if not first or "/secureboot/vmlinuz-surface-signed.efi" not in first.group():
    sys.exit("Unexpected boot layout; nothing changed")
trial = re.sub(r"menuentry [^\n]+", f"menuentry '{entry}' {{", first.group(), count=1)
trial = trial.replace("/secureboot/vmlinuz-", "/secureboot/trial-dtb/vmlinuz-").replace("/secureboot/initrd.", "/secureboot/trial-dtb/initrd.")
p.write_text(t.rstrip() + "\n" + trial + "\n")
PY
# /boot/secureboot/grub.cfg does not read next_entry: like the sync_state trial, a block reads a flag from
# its own environment file, writes it back to 0 and only then selects the trial entry.
python3 -I - "$entry" <<'PY'
import sys
from pathlib import Path
entry = sys.argv[1]
p = Path('/boot/secureboot/grub.cfg'); t = p.read_text()
b, e = '# SURFACE_DTB_ONCE_BEGIN', '# SURFACE_DTB_ONCE_END'
if b in t:
    t = t[:t.index(b)] + t[t.index(e) + len(e) + 1:]
block = f"""{b}
set surface_dtb_next=0
load_env -f /secureboot/trial-dtb/grubenv surface_dtb_next
if [ "$surface_dtb_next" = "1" ]; then
 set surface_dtb_next=0
 if save_env -f /secureboot/trial-dtb/grubenv surface_dtb_next; then
  set default='{entry}'
 fi
fi
{e}
"""
anchor = '# SURFACE_SYNC_STATE_ONCE_END\n'
if anchor not in t:
    sys.exit("Unexpected boot layout; nothing changed")
p.write_text(t.replace(anchor, anchor + block, 1))
PY
grub-script-check /boot/secureboot/grub.cfg
sbverify --cert /var/lib/surface-secureboot/MOK.pem "$out/vmlinuz-surface-signed.efi"
grub-editenv /boot/grub/grubenv unset next_entry
grub-editenv "$out/grubenv" create
grub-editenv "$out/grubenv" set surface_dtb_next=1
grub-editenv "$out/grubenv" list
echo "DTB trial ready for the next boot only."
