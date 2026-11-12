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
cp -a desktop/files/themes/Fluent-Light "$HOME/.themes/"
if [[ ! -e "$HOME/.config/gtk-4.0" && ! -L "$HOME/.config/gtk-4.0" ]]; then
  ln -s "$HOME/.themes/Fluent-Light/gtk-4.0" "$HOME/.config/gtk-4.0"
fi
mkdir -p "$HOME/.local/share/gnome-shell/extensions" "$HOME/.config/pipewire/pipewire.conf.d"
cp -a desktop/files/extensions/. "$HOME/.local/share/gnome-shell/extensions/"
install -D -m 644 desktop/files/sl7-ibus.desktop "$HOME/.config/autostart/sl7-ibus.desktop"
for entry in org/gnome/desktop/interface org/gnome/desktop/background org/gnome/desktop/input-sources org/gnome/desktop/peripherals/touchpad org/gnome/desktop/peripherals/mouse org/gnome/shell/extensions/dash-to-dock org/gnome/shell/extensions/blur-my-shell org/gnome/shell/extensions/vitals org/gnome/shell/extensions/caffeine org/gnome/shell/extensions/appindicator org/gnome/terminal/legacy; do
  snapshot="desktop/files/settings/${entry##*/}.dconf"
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
if [[ -d /lib/modules/$(uname -r) ]]; then sudo update-initramfs -u -k "$(uname -r)"; fi

gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled false
