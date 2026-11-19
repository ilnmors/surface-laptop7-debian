#!/bin/bash
# Root: remove the one-shot DTB trial image and its GRUB entry; the default image is untouched.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
entry='Surface DTB trial: camera LED + iris (one-shot)'
grub-editenv /boot/grub/grubenv unset next_entry
python3 -I - "$entry" <<'PY'
import sys
from pathlib import Path
p = Path('/boot/secureboot/grub.cfg'); t = p.read_text()
b, e = '# SURFACE_DTB_ONCE_BEGIN', '# SURFACE_DTB_ONCE_END'
if b in t:
    t = t[:t.index(b)] + t[t.index(e) + len(e) + 1:]
i = t.find(f"menuentry '{sys.argv[1]}'")
if i >= 0:
    t = t[:i].rstrip() + "\n"
p.write_text(t)
PY
grub-script-check /boot/secureboot/grub.cfg
rm -rf /boot/secureboot/trial-dtb
echo 'DTB trial removed.'
