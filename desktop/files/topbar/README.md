# Fluent Light top bar

Open Bar 49, GNOME 48 compatible package from https://extensions.gnome.org/extension/6580/open-bar/ (version tag 65598). Upstream: https://github.com/neuromorph/openbar . Offline zip and unpacked extension are included.

Preset: 32px floating light panel, 6px margin, 14px corners, dark text, blue accents and matching light menus. App/GTK/Flatpak theming and automatic wallpaper recoloring are off. Blur My Shell stays disabled. Vitals uses five-second polling; Caffeine and tray indicators remain available. No per-extension memory attribution was measured.

`desktop/setup.sh` installs the extension and restores `settings/openbar.dconf`. A new login is required to discover a newly installed extension on this running Wayland session. The preset has been saved; visual verification after login is pending.

Rollback: `gnome-extensions disable openbar@neuromorph`. The prior enabled extensions and settings are in `before-openbar.dconf`; avoid loading that entire snapshot over later unrelated changes. Fluent theme CSS is retained underneath.

## Notification button (2026-11-13)

GNOME keeps notifications inside the clock menu and only shows a small dot next to the clock. `extensions/surface-notifications@example.internal` adds a bell button to the left end of the right side of the top bar with the unread count (same rule as the shell's own indicator: unseen notifications minus queued banners). Clicking or tapping it opens the clock menu with the notification list; with Do Not Disturb on, the icon changes to the disabled bell. It is a local extension (no network, GNOME 48 only); a new extension is picked up after the next login on Wayland.
