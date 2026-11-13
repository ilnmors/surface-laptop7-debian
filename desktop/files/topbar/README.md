# Fluent top bar

Open Bar 49 for GNOME 48, from https://extensions.gnome.org/extension/6580/open-bar/ (version tag 65598). Upstream: https://github.com/neuromorph/openbar . The offline zip and unpacked extension are included.

## Current appearance

One continuous 34px opaque light Mainland panel, zero outside margin, zero outer radius/border and no shadow. This removes the wallpaper-visible gaps caused by the earlier Trilands layout. CPU/RAM are on the left, the clock/date is centered, and notifications, native English/Korean input, tray and system controls are on the right.

Vitals uses fixed-width values, GNOME icons and five-second polling. Caffeine appears only while active without timer text. The clock keeps the date and hides weekday/seconds. The legacy IBus tray icon is hidden; native input switching is retained.

Keep the established Fluent-Light Shell, including its Surface panel CSS additions. The alpine wallpaper and teal GTK3/GTK4 application theme remain applied. See [ALPINE-THEME.md](ALPINE-THEME.md) for image source, theme build and GTK4 behavior. No additional extension or resident process was introduced for the wallpaper.

## Apply and verify

`desktop/setup.sh` and `desktop/setup.py` restore the same maintained Open Bar, Vitals, Caffeine, interface and IBus panel presets in `desktop/files/settings/`. Existing extensions accept setting changes without logout. Open Bar was re-enabled and its stylesheet regenerated live. A fresh install requires a new login only to discover newly installed extensions.

Open Bar resets opacity to 0.9 on a bar-type change; the final live opacity was set back to 1.0 after that callback. Mainland, opacity 1.0, margin 0 and active extensions were read back. Appearance still needs user confirmation; no screenshot or memory benchmark is claimed.

## Rollback

Targeted backups are in `archive/topbar-before-balanced-*` and `archive/alpine-theme-before-*`. Their `restore.sh` files restore only the recorded keys; the alpine backup also restores the previous managed GTK4 symlink. These backups predate the final Mainland correction. To remove Open Bar styling, use `gnome-extensions disable openbar@neuromorph`. Do not restore old full-desktop snapshots over unrelated later settings.

## Notification button

`surface-notifications@example.internal` adds a bell and unread count on the right. It uses the Shell counting rule: unseen notifications minus queued banners. Clicking it opens the clock notification menu; Do Not Disturb changes the bell icon. It is a local GNOME 48 extension with no network access and is already active in the current session.
