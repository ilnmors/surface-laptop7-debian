#!/bin/bash
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
sudo bash "$here/files/install.sh"
python3 "$here/start-session.py"
sudo python3 "$here/files/media-fix/apply.py"
python3 "$here/start-session.py"
bash "$here/download-link.sh"
sudo waydroid shell -- settings put secure show_ime_with_hard_keyboard 0
sudo waydroid shell -- cmd uimode night no
python3 "$here/files/integrate-apps.py"
waydroid app install "$here/files/keyboard/com.retekey_206.apk"
sudo bash "$here/files/keyboard/korean-input.sh"
waydroid session stop
policy="$HOME/.local/share/waydroid/data/system/notification_policy.xml"
! sudo test -e "$policy.keyboard-off" || sudo cp -p "$policy.keyboard-off" "$policy"
python3 "$here/start-session.py"
