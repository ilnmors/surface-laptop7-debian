#!/bin/bash
# Root: save the currently running signed image as GRUB "Surface previous working image",
# install the deferred-resume spi-hid.ko and the PCIe3-off DTB, then sign with the machine key.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root (pkexec bash install.sh).' >&2; exit 1; }
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
kernel=7.3.0-31-qcom-x1e
sb=/boot/secureboot
module=/lib/modules/$kernel/updates/sl7/spi-hid.ko
dtb_new=$here/../../pcie/surface-sl7-xplus-pcie3-off.dtb
[[ $(modinfo -F vermagic "$here/spi-hid.ko") == "$kernel "* ]]
[[ $(fdtget -t s "$dtb_new" /soc@0/pcie@1bd0000 status) == disabled ]]
rm -rf "$sb/rollback-20261112.new"; mkdir "$sb/rollback-20261112.new"
cp -a "$sb/vmlinuz-surface-signed.efi" "$sb/initrd.img-$kernel" /boot/surface-sl7-xplus.dtb "$module" "$sb/rollback-20261112.new/"
printf 'Signed image that was running before install.sh on %s (spi-hid %s).\n' "$(date -Is)" "$(modinfo -F srcversion "$module")" > "$sb/rollback-20261112.new/README"
rm -rf "$sb/rollback-20261112"; mv "$sb/rollback-20261112.new" "$sb/rollback-20261112"
install -m644 "$here/spi-hid.ko" "$module"
install -m644 "$dtb_new" /boot/surface-sl7-xplus.dtb
depmod -a "$kernel"
/usr/local/sbin/surface-secureboot-update
modinfo -F srcversion "$module"; modinfo -F signer "$module"
grep -c menuentry "$sb/grub.cfg"
