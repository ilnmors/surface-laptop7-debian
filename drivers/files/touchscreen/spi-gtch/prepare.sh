#!/bin/bash
# Build the default Surface DTB: verified PCIe3-off DTB + GTCH HID-over-SPI touchscreen overlay,
# plus the iris video decoder and the camera privacy LED.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
dtc -@ -I dts -O dtb -o "$here/romulus13-gtch-spi.dtbo" "$here/romulus13-gtch-spi.dtso"
fdtoverlay -i "$here/../../pcie/surface-sl7-xplus-pcie3-off.dtb" -o "$here/surface-sl7-xplus-gtch.dtb" "$here/romulus13-gtch-spi.dtbo"
dtb="$here/surface-sl7-xplus-gtch.dtb"
# iris video decoder (2026-11-19 trial): the generic linux-firmware vpu30_p4.mbn is rejected by the
# firmware signature check; the device-signed qcvss8380.mbn from the Windows package loads.
fdtput -t s "$dtb" /soc@0/video-codec@aa00000 status okay
fdtput -t s "$dtb" /soc@0/video-codec@aa00000 firmware-name qcom/x1e80100/microsoft/qcvss8380.mbn
# Camera privacy LED: V4L2 lights it while the OV02C10 streams. This kernel looks it up as "privacy".
led=$(fdtget -t x "$dtb" /leds/led-camera-indicator phandle 2>/dev/null || true)
if [[ -z $led ]]; then
  led=$(dtc -I dtb -O dts "$dtb" 2>/dev/null | grep -oE 'phandle = <0x[0-9a-f]+>' | grep -oE '0x[0-9a-f]+' |
        python3 -I -c 'import sys; print("%x" % (max(int(x, 16) for x in sys.stdin.read().split()) + 1))')
  fdtput -t x "$dtb" /leds/led-camera-indicator phandle "$led"
fi
fdtput -t x "$dtb" /soc@0/cci@ac16000/i2c-bus@1/camera@36 leds "$led"
fdtput -t s "$dtb" /soc@0/cci@ac16000/i2c-bus@1/camera@36 led-names privacy
[[ $(fdtget -t s "$dtb" /soc@0/video-codec@aa00000 status) == okay ]]
[[ $(fdtget -t s "$dtb" /soc@0/geniqup@ac0000/spi@a88000/touchscreen@0 compatible) == hid-over-spi ]]
[[ $(fdtget -t s "$here/surface-sl7-xplus-gtch.dtb" /soc@0/pcie@1bd0000 status) == disabled ]]
echo "$here/surface-sl7-xplus-gtch.dtb"
