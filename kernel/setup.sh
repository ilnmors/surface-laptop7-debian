#!/bin/bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib.sh"
surface_init kernel "$@"
offline_apt "$bundle/kernel/files/packages/*.deb" "$bundle/kernel/files/secureboot/packages/sbsigntool_*.deb" "$bundle/kernel/files/secureboot/packages/mokutil_*.deb" "$bundle/kernel/files/secureboot/packages/zstd_*.deb"
boot_uuid=$(sudo grub-probe --target=fs_uuid /boot)
root_uuid=$(findmnt -n -o UUID -T /)
boot_prefix=$(sudo grub-mkrelpath /boot); boot_prefix=${boot_prefix%/}
test -n "$root_uuid"
sudo install -m644 drivers/files/pcie/surface-sl7-xplus-pcie3-off.dtb /boot/surface-sl7-xplus.dtb
# Deferred-resume touchpad module replaces the kernel package copy; secureboot/install.sh signs it.
sudo install -m644 drivers/files/touchpad/spi-hid-resume/spi-hid.ko /lib/modules/$kernel/updates/sl7/spi-hid.ko
sudo depmod -a "$kernel"
cat <<GRUB | sudo tee /etc/grub.d/09_surface >/dev/null
#!/bin/sh
cat <<'ENTRY'
menuentry 'Debian 13 - Surface Laptop 7 X Plus' --id surface-debian {
  insmod mmap
  insmod fdt
  search --no-floppy --fs-uuid --set=root $boot_uuid
  cutmem 0x8800000000 0x8fffffffff
  linux $boot_prefix/vmlinuz-$kernel root=UUID=$root_uuid ro clk_ignore_unused pd_ignore_unused cma=128M arm64.nopauth stubble.dtb_override=false console=tty0
  devicetree $boot_prefix/surface-sl7-xplus.dtb
  initrd $boot_prefix/initrd.img-$kernel
}
ENTRY
GRUB
sudo chmod 755 /etc/grub.d/09_surface
sudo install -d /etc/default/grub.d
printf '%s\n' 'GRUB_DEFAULT=surface-debian' 'GRUB_TIMEOUT=3' | sudo tee /etc/default/grub.d/90-surface.cfg >/dev/null
sudo update-grub
sudo bash kernel/files/secureboot/install.sh
