# Fluent Light top bar

Open Bar 49, GNOME 48 compatible package from https://extensions.gnome.org/extension/6580/open-bar/ (version tag 65598). Upstream: https://github.com/neuromorph/openbar . Offline zip and unpacked extension are included.

Preset: 32px floating light panel, 6px margin, 14px corners, dark text, blue accents and matching light menus. App/GTK/Flatpak theming and automatic wallpaper recoloring are off. Blur My Shell stays disabled. Vitals uses five-second polling; Caffeine and tray indicators remain available. No per-extension memory attribution was measured.

`desktop/setup.sh` installs the extension and restores `settings/openbar.dconf`. A new login is required to discover a newly installed extension on this running Wayland session. The preset has been saved; visual verification after login is pending.

Rollback: `gnome-extensions disable openbar@neuromorph`. The prior enabled extensions and settings are in `before-openbar.dconf`; avoid loading that entire snapshot over later unrelated changes. Fluent theme CSS is retained underneath.
