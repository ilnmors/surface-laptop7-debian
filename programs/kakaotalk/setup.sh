#!/bin/bash
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
(( EUID != 0 )) || { echo 'Run as the Waydroid desktop user.' >&2; exit 1; }
python3 "$here/../waydroid/start-session.py"
sudo python3 "$here/install.py" --data-dir "$HOME/.local/share/waydroid/data"
waydroid app launch com.kakao.talk
printf '%s\n' 'KakaoTalk opened. Choose secondary/tablet-device login; enter your credentials yourself.'
