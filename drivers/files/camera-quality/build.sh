#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
bundle=$PWD
output=${1:?Usage: build.sh /absolute/path/to/output.so}
[[ $output = /* ]]
work=$(mktemp -d)
dpkg-source -x libcamera_0.4.0-7.dsc "$work/src"
cd "$work/src"
patch -p1 < "$bundle/ov02c10-debian-0.4.patch"
meson setup build --buildtype=release -Dpipelines=simple -Dipas=simple \
  -Dcam=enabled -Dqcam=disabled -Dgstreamer=disabled -Ddocumentation=disabled \
  -Dtest=false -Dv4l2=false -Dpycamera=disabled -Dlc-compliance=disabled
ninja -C build src/ipa/simple/ipa_soft_simple.so
install -m 644 build/src/ipa/simple/ipa_soft_simple.so "$output"
