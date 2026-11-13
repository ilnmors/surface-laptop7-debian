# Fluent Light top bar

Open Bar 49, GNOME 48 compatible package from https://extensions.gnome.org/extension/6580/open-bar/ (version tag 65598). Upstream: https://github.com/neuromorph/openbar . Offline zip and unpacked extension are included.

## Clean light panel (2026-11-13)

32px full-width Mainland panel, 90% background opacity, zero margin, square outer corners, no outline or bar shadow. Light background, dark text, subtle blue hover, opaque light menus with 12px corners. It matches the existing full-width bottom taskbar. Automatic wallpaper recoloring, app/GTK/Flatpak recoloring and Blur My Shell remain off.

Vitals shows CPU and RAM only, with fixed number widths, GNOME-style icons and five-second polling. Public-IP lookup is disabled. Caffeine is visible only while active, with no countdown text. The clock keeps the date and hides weekday/seconds. The notification bell, tray apps and system controls remain available.

`desktop/setup.sh` restores the maintained Open Bar, Vitals, Caffeine and interface presets from `desktop/files/settings/`; `desktop/setup.py` uses the same implementation. Existing extensions take these setting changes immediately. A fresh install needs a new login to discover newly installed extensions.

Validation: all 35 changed settings were read back; Open Bar and Vitals report ACTIVE. No new theme/extension error was found in the recent user journal. Screenshot access was denied by GNOME, so the final appearance still needs user confirmation. Open Bar normalizes the background opacity to 90% on bar-type changes; the saved preset uses that same value. No per-extension memory benchmark was performed.

Rollback: run the matching `archive/topbar-before-clean-*/restore.sh` for this change. It restores only the 35 touched keys, leaving unrelated desktop settings intact. To remove Open Bar styling entirely, use `gnome-extensions disable openbar@neuromorph`. The earlier `before-openbar.dconf` snapshot predates later customizations and should not be restored wholesale.

## Notification button (2026-11-13)

GNOME keeps notifications inside the clock menu and only shows a small dot next to the clock. `extensions/surface-notifications@example.internal` adds a bell button to the left end of the right side of the top bar with the unread count (same rule as the shell's own indicator: unseen notifications minus queued banners). Clicking or tapping it opens the clock menu with the notification list; with Do Not Disturb on, the icon changes to the disabled bell. It is a local extension (no network, GNOME 48 only); a newly installed extension is picked up after the next login on Wayland. It is already active in the current session.
