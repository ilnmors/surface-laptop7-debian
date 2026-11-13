#!/bin/bash
# Build the default Surface DTB: verified PCIe3-off DTB + GTCH HID-over-SPI touchscreen overlay.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
dtc -@ -I dts -O dtb -o "$here/romulus13-gtch-spi.dtbo" "$here/romulus13-gtch-spi.dtso"
fdtoverlay -i "$here/../../pcie/surface-sl7-xplus-pcie3-off.dtb" -o "$here/surface-sl7-xplus-gtch.dtb" "$here/romulus13-gtch-spi.dtbo"
[[ $(fdtget -t s "$here/surface-sl7-xplus-gtch.dtb" /soc@0/geniqup@ac0000/spi@a88000/touchscreen@0 compatible) == hid-over-spi ]]
[[ $(fdtget -t s "$here/surface-sl7-xplus-gtch.dtb" /soc@0/pcie@1bd0000 status) == disabled ]]
echo "$here/surface-sl7-xplus-gtch.dtb"
