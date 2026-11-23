#!/bin/bash
set -euo pipefail
folder=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
work=${1:?Usage: build.sh /absolute/build-directory}
[[ $work == /* && ! -e $work ]] || { echo 'Use a new absolute build directory.' >&2; exit 1; }
mkdir -p "$work/headers" "$work/source"
for package in "$folder"/headers/*.deb; do dpkg-deb -x "$package" "$work/headers"; done
cp -a "$folder/sources/." "$work/source/"
for patchfile in "$folder"/patches/*.patch; do patch --batch --fuzz=0 -d "$work/source" -p1 < "$patchfile"; done
mkdir -p "$work/source/drivers/cpufreq"
cp "$folder/../../drivers/files/cpu/baseline/scmi-cpufreq.c" "$work/source/drivers/cpufreq/"
patch --batch --fuzz=0 -d "$work/source" -p1 < "$folder/../../drivers/files/cpu/scmi-all-boost.patch"
printf 'obj-m += scmi-cpufreq.o\n' > "$work/source/drivers/cpufreq/Makefile"
printf 'obj-m += dwc3-qcom.o\n' > "$work/source/drivers/usb/dwc3/Makefile"
printf 'obj-m += soundwire-qcom.o\nsoundwire-qcom-y := qcom.o\n' > "$work/source/drivers/soundwire/Makefile"
printf 'obj-m += ov02c10.o\n' > "$work/source/drivers/media/i2c/Makefile"
headers=$work/headers/usr/src/linux-headers-7.3.0-31-qcom-x1e
for sub in drivers/usb/dwc3 drivers/soundwire drivers/cpufreq drivers/media/i2c; do
  make -C "$headers" M="$work/source/$sub" CC="${CC:-gcc-14}" -j4 modules
done
echo 'Unsigned modules built. Install and sign them with the target machine key before rebooting.'

bash "$folder/wifi-regulatory/build.sh" "$work/wifi"
