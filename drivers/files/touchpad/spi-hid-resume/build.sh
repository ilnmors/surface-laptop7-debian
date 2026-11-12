#!/bin/bash
# Rebuild spi-hid.ko with the deferred resume settle. Output is unsigned; surface-secureboot-update signs it.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
work=${1:?Usage: build.sh /absolute/new-build-directory}
[[ $work == /* && ! -e $work ]] || { echo 'Use a new absolute build directory.' >&2; exit 1; }
mkdir -p "$work/headers"
for package in "$here"/../../../../patches/files/headers/*.deb; do dpkg-deb -x "$package" "$work/headers"; done
cp -a "$here/source" "$work/spi-hid"
patch --batch --fuzz=0 -d "$work/spi-hid" -p1 < "$here/resume-deferred.patch"
make -C "$work/headers/usr/src/linux-headers-7.3.0-31-qcom-x1e" M="$work/spi-hid" CC="${CC:-gcc-14}" modules
echo "$work/spi-hid/spi-hid.ko"
