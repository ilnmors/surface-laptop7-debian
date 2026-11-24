#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
(( EUID == 0 )) || exec sudo /bin/bash "$PWD/install.sh"
[[ $(dpkg --print-architecture) == arm64 ]] || { echo 'These Android images are ARM64 only.' >&2; exit 1; }
apt-get --no-download --no-install-recommends -o Dir::Etc::sourcelist=/dev/null -o Dir::Etc::sourceparts=- install "$PWD"/packages/*.deb
install -d /etc/apt/sources.list.d
printf 'deb https://deb.debian.org/debian trixie-backports main\n' > /etc/apt/sources.list.d/surface-backports.list
if [[ ! -e /var/lib/waydroid/waydroid.cfg ]]; then
    if compgen -G 'images/*.img' >/dev/null; then
        install -d /usr/share/waydroid-extra/images
        cp --reflink=auto images/*.img /usr/share/waydroid-extra/images/
        # Waydroid recognizes this preinstalled-image directory and skips OTA downloads.
    else
        echo 'No local images/*.img; waydroid init downloads VANILLA from the official OTA channels (OTA-SOURCES.json).' >&2
    fi
    waydroid init -s VANILLA
fi
python3 - <<'CONFIG'
from pathlib import Path
import configparser
p=Path('/var/lib/waydroid/waydroid.cfg');c=configparser.ConfigParser();c.read(p)
if not c.has_section('properties'):c.add_section('properties')
c['properties']['persist.waydroid.multi_windows']='true'
c['properties']['ro.build.characteristics']='tablet'
c['properties']['persist.waydroid.suspend']='false'
with p.open('w') as f:c.write(f)
CONFIG
waydroid upgrade -o
systemctl enable --now waydroid-container.service
