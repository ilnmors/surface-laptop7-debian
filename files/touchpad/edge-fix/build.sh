#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
bundle=$PWD
output=${1:?Usage: build.sh /absolute/path/to/iptsd}
[[ $output = /* ]]
work=$(mktemp -d)
python3 - "$bundle/../../../archive/hardware/source/surface-xplus-project.zip" "$work" <<'PY'
import sys
from pathlib import Path
from zipfile import ZipFile
with ZipFile(sys.argv[1]) as archive:
    for member in archive.namelist():
        if "/vendor/iptsd/" not in member or member.endswith("/"):
            continue
        target = Path(sys.argv[2]) / member.split("/vendor/iptsd/", 1)[1]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(member))
PY
cd "$work"
patch -p1 < "$bundle/edge-contact.patch"
root=$work/deps
for package in "$bundle"/build-debs/*.deb; do dpkg-deb -x "$package" "$root"; done
cat > "$root/usr/share/pkgconfig/Microsoft.GSL.pc" <<'PC'
prefix=/usr
Name: Microsoft.GSL
Description: Microsoft Guidelines Support Library headers
Version: 4.0.0
Cflags: -I${prefix}/include
PC
export PKG_CONFIG_PATH="$root/usr/lib/aarch64-linux-gnu/pkgconfig:$root/usr/share/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="$root" CPLUS_INCLUDE_PATH="$root/usr/include"
meson setup build --prefix=/usr --libdir=lib/aarch64-linux-gnu -Ddebug_tools=[] -Db_lto=false -Dwerror=false --wrap-mode=nofallback
ninja -C build -j 4 src/iptsd
install -m 755 build/src/iptsd "$output"
