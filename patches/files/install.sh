#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
(( EUID == 0 )) || exec sudo /bin/bash "$PWD/install.sh" "$@"
kernel=7.3.0-31-qcom-x1e
test -d "/lib/modules/$kernel"
for module in modules/"$kernel"/*.ko; do
  [[ $(modinfo -F vermagic "$module") == "$kernel "* ]] || exit 1
  install -D -m644 "$module" "/lib/modules/$kernel/updates/surface/${module##*/}"
done
install -m755 ../../drivers/files/rootfs/etc/initramfs-tools/hooks/surface-kernel-patches /etc/initramfs-tools/hooks/surface-kernel-patches
depmod -a "$kernel"
if [[ ${1:-} != --no-refresh ]]; then
  /usr/local/sbin/surface-secureboot-update
fi
echo 'dwc3-qcom, QMP PHY, SoundWire, ath12k, OV02C10 and SCMI cpufreq modules installed for the next boot; active hardware was not unbound.'
