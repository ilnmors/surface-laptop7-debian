# Fluent Light top bar

Open Bar 49, GNOME 48 compatible package from https://extensions.gnome.org/extension/6580/open-bar/ (version tag 65598). Upstream: https://github.com/neuromorph/openbar . Offline zip and unpacked extension are included.

## Alpine palette and balanced top bar (2026-11-13)

Open Bar's native Trilands layout separates three rounded light groups: Activities and CPU/RAM on the left, clock/date in the center, notification bell, input source, tray and system controls on the right. CPU/RAM were moved out of the crowded right group. The Lago di Braies wallpaper and cream/sage/teal Fluent palette are documented in [ALPINE-THEME.md](ALPINE-THEME.md). Each group is 34px high with 14px corners, 6px outer spacing, subtle borders and no shadow. No additional extension is required.

Vitals keeps fixed-width CPU/RAM numbers, GNOME-style icons and five-second polling. Caffeine appears only while active, without timer text. The date remains; weekday/seconds are hidden. The legacy IBus tray icon is disabled; GNOME's native English/Korean indicator and language-switching keys remain available. Existing bottom taskbar and notification behavior are preserved.

`desktop/setup.sh` restores the Open Bar, Vitals, Caffeine, interface and IBus panel presets in `desktop/files/settings/`; `desktop/setup.py` uses the same implementation. Existing extensions take these changes immediately. Open Bar's built-in style refresh was triggered. A fresh install needs a new login only to discover newly installed extensions.

Validation: live values match the maintained presets. Final appearance needs user feedback because GNOME does not allow an external screenshot. No per-extension memory benchmark was performed.

Rollback for this layout: run the matching `archive/topbar-before-balanced-*/restore.sh`. It restores only the 18 touched keys. Earlier flat-bar backups remain under `archive/topbar-before-clean-*`. To remove Open Bar styling entirely, use `gnome-extensions disable openbar@neuromorph`; do not restore old full desktop snapshots over unrelated later changes.

## Notification button (2026-11-13)

GNOME keeps notifications inside the clock menu and only shows a small dot next to the clock. `extensions/surface-notifications@example.internal` adds a bell button to the left end of the right side of the top bar with the unread count (same rule as the shell's own indicator: unseen notifications minus queued banners). Clicking or tapping it opens the clock menu with the notification list; with Do Not Disturb on, the icon changes to the disabled bell. It is a local extension (no network, GNOME 48 only); a newly installed extension is picked up after the next login on Wayland. It is already active in the current session.
