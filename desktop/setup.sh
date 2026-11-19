#!/bin/bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib.sh"
surface_init desktop "$@"
[[ $(dpkg --print-architecture) == arm64 ]] || { echo 'Use native packages on other architectures; see PORTABILITY.md.' >&2; exit 1; }
offline_apt "$bundle/desktop/files/debian/*.deb" "$bundle/desktop/files/packages/*.deb"
restore_tree desktop/files/rootfs
sudo install -d /etc/dconf/db/local.d
sudo install -m 644 desktop/files/defaults/* /etc/dconf/db/local.d/
sudo install -m 644 desktop/files/backgrounds/* /usr/share/backgrounds/
if ! grep -qxF system-db:local /etc/dconf/profile/user 2>/dev/null; then
  sudo install -d /etc/dconf/profile
  if [[ ! -e /etc/dconf/profile/user ]]; then
    printf '%s\n' user-db:user | sudo tee /etc/dconf/profile/user >/dev/null
  fi
  printf '%s\n' system-db:local | sudo tee -a /etc/dconf/profile/user >/dev/null
fi
sudo dconf update
if [[ -x /usr/share/gdm/generate-config ]]; then sudo /usr/share/gdm/generate-config; fi
mkdir -p "$HOME/.themes" "$HOME/.config"
for theme in Fluent-Light Fluent-teal-Light Fluent-orange-Light; do
  cp -a "desktop/files/themes/$theme" "$HOME/.themes/"
done
if [[ ! -e "$HOME/.config/gtk-4.0" && ! -L "$HOME/.config/gtk-4.0" ]]; then
  ln -s "$HOME/.themes/Fluent-orange-Light/gtk-4.0" "$HOME/.config/gtk-4.0"
elif [[ -L "$HOME/.config/gtk-4.0" && ( $(readlink -f "$HOME/.config/gtk-4.0") == "$HOME/.themes/Fluent-Light/gtk-4.0" || $(readlink -f "$HOME/.config/gtk-4.0") == "$HOME/.themes/Fluent-teal-Light/gtk-4.0" ) ]]; then
  ln -sfn "$HOME/.themes/Fluent-orange-Light/gtk-4.0" "$HOME/.config/gtk-4.0"
fi
mkdir -p "$HOME/.local/share/gnome-shell/extensions" "$HOME/.config/pipewire/pipewire.conf.d"
cp -a desktop/files/extensions/. "$HOME/.local/share/gnome-shell/extensions/"
install -D -m 644 desktop/files/sl7-ibus.desktop "$HOME/.config/autostart/sl7-ibus.desktop"
install -D -m 755 desktop/files/goa-webdav-mount.py "$HOME/.local/bin/goa-webdav-mount"
install -D -m 644 desktop/files/goa-webdav-mount.desktop "$HOME/.config/autostart/goa-webdav-mount.desktop"
for entry in org/gnome/desktop/interface org/gnome/desktop/background org/gnome/desktop/input-sources org/freedesktop/ibus/panel org/gnome/desktop/peripherals/touchpad org/gnome/desktop/peripherals/mouse org/gnome/shell/extensions/dash-to-dock org/gnome/shell/extensions/openbar org/gnome/shell/extensions/appindicator org/gnome/terminal/legacy; do
  snapshot="desktop/files/settings/${entry##*/}.dconf"
  if [[ -s $snapshot ]]; then dconf load "/$entry/" < "$snapshot"; fi
done
gsettings set org.gnome.shell.extensions.user-theme name Fluent-Light
python3 - <<'PY'
from gi.repository import Gio
settings = Gio.Settings.new("org.gnome.shell")
enabled = settings.get_strv("enabled-extensions")
for extension in ("dash-to-dock@micxgx.gmail.com", "user-theme@gnome-shell-extensions.gcampax.github.com", "openbar@neuromorph", "appindicatorsupport@rgcjonas.gmail.com"):
    if extension not in enabled:
        enabled.append(extension)
assert settings.set_strv("enabled-extensions", enabled)
Gio.Settings.sync()
PY
sudo plymouth-set-default-theme surface-debian
if [[ -d /lib/modules/$(uname -r) ]]; then sudo update-initramfs -u -k "$(uname -r)"; fi

gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled false

# Home printer: Samsung SL-T2270DW over driverless IPP Everywhere; the repository's Kea reserves 192.0.2.100.
# lpadmin -m everywhere queries the printer, so an unreachable printer only skips this step.
if command -v lpadmin >/dev/null; then
  if sudo lpadmin -p printer -E -v ipp://192.0.2.100/ipp/print -m everywhere -D "Samsung SL-T2270DW" -L home \
       -o PageSize=A4 -o printer-is-shared=false; then
    lpoptions -d printer >/dev/null
  else
    echo 'printer: 192.0.2.100 did not answer; run desktop/setup.sh again on the home network.' >&2
  fi
fi
