#!/bin/bash
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
work=${1:?Usage: build.sh /new/absolute/build-directory}
[[ $work == /* && ! -e $work ]] || exit 1
mkdir -p "$work/source" "$work/headers"
tar -xf "$here/ath12k-source.tar.xz" -C "$work/source"
for package in "$here"/../headers/*.deb; do dpkg-deb -x "$package" "$work/headers"; done
for patchfile in "$here/known-good/sl7-rfkill-core.c.patch" "$here/known-good/sl7-rfkill-wmi.c.patch" "$here/f2576dc0.patch"; do
    patch --batch --fuzz=0 -d "$work/source" -p1 < "$patchfile"
done
headers=$work/headers/usr/src/linux-headers-7.3.0-31-qcom-x1e
make -C "$headers" M="$work/source/drivers/net/wireless/ath/ath12k" CC="${CC:-gcc-14}" -j4 modules
[[ $(modinfo -F srcversion "$work/source/drivers/net/wireless/ath/ath12k/ath12k.ko") == D044C56077CC5357DC3F5BF ]]
echo 'Preserved Surface rfkill guards and upstream regulatory completion patch built; sign with the target key.'
