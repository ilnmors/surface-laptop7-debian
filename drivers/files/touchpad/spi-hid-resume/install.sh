#!/bin/bash
# Root: keep the verified boot as GRUB "Surface previous working image", install the deferred-resume
# spi-hid.ko and the PCIe3-off DTB, then sign modules/initramfs/kernel with the existing machine key.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root (pkexec bash install.sh).' >&2; exit 1; }
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
kernel=7.3.0-31-qcom-x1e
sb=/boot/secureboot
module=/lib/modules/$kernel/updates/sl7/spi-hid.ko
dtb_new=$here/../../pcie/surface-sl7-xplus-pcie3-off.dtb
[[ $(modinfo -F vermagic "$here/spi-hid.ko") == "$kernel "* ]]
[[ $(fdtget -t s "$dtb_new" /soc@0/pcie@1bd0000 status) == disabled ]]
if [[ ! -e $sb/rollback-20261112-pre-cpu ]]; then
  mv "$sb/rollback-20261112" "$sb/rollback-20261112-pre-cpu"
  mkdir "$sb/rollback-20261112"
  cp -a "$sb/vmlinuz-surface-signed.efi" "$sb/initrd.img-$kernel" "$sb/rollback-20261112/"
  cp -a /boot/surface-sl7-xplus.dtb "$module" "$sb/rollback-20261112/"
  printf 'Verified default boot of 2026-11-12 19:25 (CPU 0-9, camera 37.5 fps) before spi-hid/PCIe3 change.\n' > "$sb/rollback-20261112/README"
fi
install -m644 "$here/spi-hid.ko" "$module"
install -m644 "$dtb_new" /boot/surface-sl7-xplus.dtb
depmod -a "$kernel"
/usr/local/sbin/surface-secureboot-update
modinfo -F srcversion "$module"; modinfo -F signer "$module"
grep -c menuentry "$sb/grub.cfg"
