#!/bin/bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib.sh"
surface_init drivers "$@"
test -d "/lib/modules/$kernel" || { echo 'Apply kernel/setup.sh first.' >&2; exit 1; }
if dpkg-query -W -f='${Version}' libinput10 2>/dev/null | grep -q .; then
  installed_libinput=$(dpkg-query -W -f='${Version}' libinput10)
  if dpkg --compare-versions "$installed_libinput" gt '1.28.1-1+deb13u1+surface1'; then
    echo 'A newer libinput security version is installed; rebase the local patch before restoring this older package.' >&2; exit 1
  fi
fi
offline_apt "$bundle/drivers/files/debian/*.deb" "$bundle/drivers/files/packages/*.deb"
restore_tree drivers/files/rootfs
sudo sh -c 'for module in gpi spi-geni-qcom spi-hid uinput ath12k ath12k_wifi7; do
  grep -qxF "$module" /etc/initramfs-tools/modules || echo "$module" >> /etc/initramfs-tools/modules
done'
sudo systemctl daemon-reload
sudo udevadm control --reload-rules
if [[ -x /usr/local/sbin/surface-secureboot-update ]]; then
  sudo /usr/local/sbin/surface-secureboot-update "$kernel"
else
  echo 'Secure Boot updater missing; apply kernel/setup.sh first.' >&2; exit 1
fi
