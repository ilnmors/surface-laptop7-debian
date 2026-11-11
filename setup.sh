#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
bundle=$PWD
. /etc/os-release
if [[ $ID != debian || $VERSION_CODENAME != trixie || $(dpkg --print-architecture) != arm64 || $EUID == 0 ]]; then
  echo 'Run as your desktop user on Debian 13 ARM64.' >&2
  exit 1
fi
sha256sum --quiet -c files/SHA256SUMS
sudo -v
sudo bash files/desktop/console-uid/apply-group.sh
kernel=7.3.0-31-qcom-x1e
boot_uuid=$(sudo grub-probe --target=fs_uuid /boot)
root_uuid=$(findmnt -n -o UUID -T /)
boot_prefix=$(sudo grub-mkrelpath /boot)
boot_prefix=${boot_prefix%/}
test -n "$root_uuid"
sudo apt-get --no-download -o Dir::Etc::sourcelist=/dev/null -o Dir::Etc::sourceparts=- --no-install-recommends install \
  "$bundle"/files/debian/*.deb "$bundle"/files/desktop/packages/*.deb \
  "$bundle"/files/secureboot/packages/{sbsigntool,mokutil,zstd}_*.deb \
  "$bundle"/files/packages/{linux-image-*,sl7-audio-support_*,sl7-camera-support_*,iptsd_*}.deb
tar -C files/rootfs -cf - . | sudo tar --no-overwrite-dir --no-same-owner -C / -xf -
sudo sh -c 'for module in gpi spi-geni-qcom spi-hid uinput ath12k ath12k_wifi7; do
  grep -qxF "$module" /etc/initramfs-tools/modules || echo "$module" >> /etc/initramfs-tools/modules
done'
sudo install -m 644 files/touchscreen/surface-sl7-xplus-touchscreen.dtb /boot/surface-sl7-xplus.dtb
sudo systemctl daemon-reload
sudo udevadm control --reload-rules
sudo update-initramfs -u -k "$kernel"
sudo hostnamectl set-hostname surface
if grep -q '^127\.0\.1\.1[[:space:]]' /etc/hosts; then
  sudo sed -i -E 's/^127\.0\.1\.1[[:space:]]+.*/127.0.1.1 surface/' /etc/hosts
else
  printf '%s\n' '127.0.1.1 surface' | sudo tee -a /etc/hosts >/dev/null
fi
sudo timedatectl set-timezone Asia/Seoul
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
sudo install -d /etc/dconf/db/local.d
sudo install -m 644 files/desktop/defaults/* /etc/dconf/db/local.d/
sudo install -m 644 files/desktop/backgrounds/* /usr/share/backgrounds/
if ! grep -qxF system-db:local /etc/dconf/profile/user 2>/dev/null; then
  sudo install -d /etc/dconf/profile
  if [[ ! -e /etc/dconf/profile/user ]]; then
    printf '%s\n' user-db:user | sudo tee /etc/dconf/profile/user >/dev/null
  fi
  printf '%s\n' system-db:local | sudo tee -a /etc/dconf/profile/user >/dev/null
fi
sudo dconf update
mkdir -p "$HOME/.themes" "$HOME/.config"
cp -a files/desktop/themes/Fluent-Light "$HOME/.themes/"
if [[ ! -e "$HOME/.config/gtk-4.0" && ! -L "$HOME/.config/gtk-4.0" ]]; then
  ln -s "$HOME/.themes/Fluent-Light/gtk-4.0" "$HOME/.config/gtk-4.0"
fi
mkdir -p "$HOME/.local/share/gnome-shell/extensions" "$HOME/.config/pipewire/pipewire.conf.d"
cp -a files/desktop/extensions/. "$HOME/.local/share/gnome-shell/extensions/"
install -D -m 644 files/desktop/sl7-ibus.desktop "$HOME/.config/autostart/sl7-ibus.desktop"
for entry in org/gnome/desktop/interface org/gnome/desktop/background org/gnome/desktop/input-sources org/gnome/desktop/peripherals/touchpad org/gnome/desktop/peripherals/mouse org/gnome/shell/extensions/dash-to-dock org/gnome/shell/extensions/blur-my-shell org/gnome/shell/extensions/vitals org/gnome/shell/extensions/caffeine org/gnome/shell/extensions/appindicator org/gnome/terminal/legacy; do
  snapshot="files/desktop/settings/${entry##*/}.dconf"
  if [[ -s $snapshot ]]; then dconf load "/$entry/" < "$snapshot"; fi
done
gsettings set org.gnome.shell.extensions.user-theme name Fluent-Light
python3 - <<'PY'
from gi.repository import Gio
settings = Gio.Settings.new("org.gnome.shell")
enabled = settings.get_strv("enabled-extensions")
for extension in ("dash-to-dock@micxgx.gmail.com", "user-theme@gnome-shell-extensions.gcampax.github.com", "blur-my-shell@aunetx", "Vitals@CoreCoding.com", "caffeine@patapon.info", "appindicatorsupport@rgcjonas.gmail.com"):
    if extension not in enabled:
        enabled.append(extension)
assert settings.set_strv("enabled-extensions", enabled)
Gio.Settings.sync()
PY
sudo plymouth-set-default-theme surface-debian
sudo bash files/kernel-patches/install.sh --no-refresh
sudo bash files/secureboot/install.sh
sudo bash files/android/install.sh
python3 files/android/integrate-apps.py
echo 'Reboot to load the Surface kernel, touchscreen DTB and GNOME Shell theme. Complete MOK enrollment before enabling Secure Boot.' 
