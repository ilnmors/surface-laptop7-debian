#!/bin/bash
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
(( EUID != 0 )) || { echo 'Run as the Waydroid desktop user.' >&2; exit 1; }
python3 "$here/../waydroid/start-session.py"
sudo python3 "$here/install.py" --data-dir "$HOME/.local/share/waydroid/data"
sudo waydroid shell -- settings put secure show_ime_with_hard_keyboard 0
sudo waydroid shell -- cmd uimode night no
waydroid prop set persist.waydroid.suspend false
sudo waydroid shell -- dumpsys deviceidle whitelist +com.kakao.talk
sudo waydroid shell -- pm grant com.kakao.talk android.permission.POST_NOTIFICATIONS
python3 "$here/integrate.py"
python3 "$here/launch.py"
printf '%s\n' 'KakaoTalk opened. Choose secondary/tablet-device login; enter your credentials yourself.'
