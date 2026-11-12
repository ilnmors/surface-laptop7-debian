#!/bin/bash
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
sudo bash "$here/files/install.sh"
python3 "$here/start-session.py"
sudo python3 "$here/files/media-fix/apply.py"
python3 "$here/files/integrate-apps.py"
