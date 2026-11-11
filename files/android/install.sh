#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
(( EUID == 0 )) || exec sudo /bin/bash "$PWD/install.sh"
[[ $(dpkg --print-architecture) == arm64 ]] || { echo 'These Android images are ARM64 only.' >&2; exit 1; }
apt-get --no-download --no-install-recommends -o Dir::Etc::sourcelist=/dev/null -o Dir::Etc::sourceparts=- install "$PWD"/packages/*.deb
install -d /etc/apt/sources.list.d
printf 'deb https://deb.debian.org/debian trixie-backports main\n' > /etc/apt/sources.list.d/surface-backports.list
if [[ ! -e /var/lib/waydroid/waydroid.cfg ]]; then
    install -d /usr/share/waydroid-extra/images
    cp --reflink=auto images/*.img /usr/share/waydroid-extra/images/
    # Waydroid recognizes this preinstalled-image directory and skips OTA downloads.
    waydroid init -s VANILLA
fi
python3 - <<'CONFIG'
from pathlib import Path
import configparser
p=Path('/var/lib/waydroid/waydroid.cfg');c=configparser.ConfigParser();c.read(p)
if not c.has_section('properties'):c.add_section('properties')
c['properties']['persist.waydroid.multi_windows']='true'
with p.open('w') as f:c.write(f)
CONFIG
systemctl enable --now waydroid-container.service
