#!/bin/bash
set -euo pipefail
(( EUID == 0 )) || exec sudo /bin/bash "$0" "$@"
kernel=7.3.0-31-qcom-x1e
saved=/boot/secureboot/rollback-20261112
for file in vmlinuz-surface-signed.efi "initrd.img-$kernel" grub.cfg; do test -f "$saved/$file"; done
for file in vmlinuz-surface-signed.efi "initrd.img-$kernel" grub.cfg; do install -m644 "$saved/$file" "/boot/secureboot/$file"; done
install -m644 "$saved/surface-sl7-xplus.dtb" /boot/surface-sl7-xplus.dtb
for file in ath12k.ko ov02c10.ko scmi-cpufreq.ko; do rm -f "/lib/modules/$kernel/updates/surface/$file"; done
depmod -a "$kernel"
grub-editenv /boot/grub/grubenv unset next_entry
printf '%s\n' 'Previous signed boot restored. Reboot to use its original modules.'
