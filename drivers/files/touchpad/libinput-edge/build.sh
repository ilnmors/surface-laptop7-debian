#!/bin/bash
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
work=${1:?Usage: build.sh /absolute/new-build-directory}
[[ $work == /* && ! -e $work ]] || { echo 'Use a new absolute directory.' >&2; exit 1; }
mkdir -p "$work/deps"
tar -xzf "$here/libinput_1.28.1.orig.tar.gz" -C "$work"
source_dir=$work/libinput-1.28.1
tar -xJf "$here/libinput_1.28.1-1+deb13u1.debian.tar.xz" -C "$source_dir"
while IFS= read -r patchname; do
 [[ -z $patchname || $patchname == \#* ]] && continue
 patch --batch --fuzz=0 -d "$source_dir" -p1 < "$source_dir/debian/patches/$patchname"
done < "$source_dir/debian/patches/series"
patch --batch --fuzz=0 -d "$source_dir" -p1 < "$here/romulus-edge-palm.patch"
for package in "$here"/build-debs/*.deb; do dpkg-deb -x "$package" "$work/deps"; done
python3 - "$work/deps" <<'PY'
from pathlib import Path
import sys
r=Path(sys.argv[1])
for p in r.rglob('*.so'):
 if p.is_symlink() and not p.exists():
  host=(Path('/')/p.relative_to(r)).parent/p.readlink()
  if host.exists():p.unlink();p.symlink_to(host.resolve())
PY
export PKG_CONFIG_SYSROOT_DIR=$work/deps
export PKG_CONFIG_PATH=$work/deps/usr/lib/aarch64-linux-gnu/pkgconfig:$work/deps/usr/share/pkgconfig
meson setup "$work/build" "$source_dir" --prefix=/usr --libdir=lib/aarch64-linux-gnu --buildtype=release -Ddebug-gui=false -Ddocumentation=false -Dtests=false -Dlibwacom=true
ninja -C "$work/build" -j4 libinput.so.10.13.0
python3 "$here/package.py" "$work/build/libinput.so.10.13.0" "$work/libinput10_surface_arm64.deb"
