#!/bin/bash
# Root: remove the one-shot GTCH touchscreen trial and its GRUB entry.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
grub-editenv /boot/grub/grubenv unset next_entry
python3 -I - <<'PY'
from pathlib import Path
p = Path('/boot/secureboot/grub.cfg'); t = p.read_text()
i = t.find("menuentry 'Surface touchscreen trial (one-shot)'")
if i >= 0:
    t = t[:i]
p.write_text(t)
PY
grub-script-check /boot/secureboot/grub.cfg
rm -rf /boot/secureboot/trial-touch
echo 'Touchscreen trial removed; the signed default image is unchanged.'
