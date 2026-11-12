#!/bin/bash
# Root: put back the 19:25 verified module, DTB and signed image saved by install.sh.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root (pkexec bash restore.sh).' >&2; exit 1; }
kernel=7.3.0-31-qcom-x1e; sb=/boot/secureboot; saved=$sb/rollback-20261112
install -m644 "$saved/spi-hid.ko" "/lib/modules/$kernel/updates/sl7/spi-hid.ko"
install -m644 "$saved/surface-sl7-xplus.dtb" /boot/surface-sl7-xplus.dtb
depmod -a "$kernel"
cp -a "$saved/vmlinuz-surface-signed.efi" "$saved/initrd.img-$kernel" "$sb/"
echo 'Restored the verified 19:25 module, DTB and signed image.'
