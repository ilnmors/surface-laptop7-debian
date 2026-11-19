#!/bin/bash
# Root: remove the a400000 softdep and rebuild the initramfs; the GRUB menu is kept.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
kernel=$(uname -r); sb=/boot/secureboot
cp -a "$sb/grub.cfg" /tmp/grub.cfg.keep
rm -f /etc/modprobe.d/surface-a400000-order.conf
update-initramfs -u -k "$kernel"
cp -a /tmp/grub.cfg.keep "$sb/grub.cfg"; grub-script-check "$sb/grub.cfg"
echo 'a400000 softdep removed.'
