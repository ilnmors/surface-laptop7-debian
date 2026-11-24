# Fluent top bar

Open Bar 49 for GNOME 48, from https://extensions.gnome.org/extension/6580/open-bar/ (version tag 65598). Upstream: https://github.com/neuromorph/openbar . The offline zip and unpacked extension are included.

## Current appearance

One continuous 34px light Mainland panel at 0.9 background opacity, zero outside margin, zero outer radius/border and no shadow. This removes the wallpaper-visible gaps caused by the earlier Trilands layout. The clock/date is centered; notifications, native English/Korean input, tray and system controls are on the right. Since 2026-11-19 there are no widget extensions (Vitals, Caffeine removed).

The clock keeps the date and hides weekday/seconds. The legacy IBus tray icon is hidden; native input switching is retained.

Keep the established Fluent-Light Shell, including its Surface panel CSS additions. The wallpaper and GTK theme are Church's *Cross in the Wilderness* with Fluent orange since 2026-11-19 ([CHURCH-THEME.md](CHURCH-THEME.md)); the earlier alpine/teal set is in [ALPINE-THEME.md](ALPINE-THEME.md) for image source, theme build and GTK4 behavior. No additional extension or resident process was introduced for the wallpaper.

## Apply and verify

`desktop/setup.sh` and `desktop/setup.py` restore the same maintained Open Bar, interface and IBus panel presets in `desktop/files/settings/`. Existing extensions accept setting changes without logout. Open Bar was re-enabled and its stylesheet regenerated live. A fresh install requires a new login only to discover newly installed extensions.

Open Bar resets opacity to 0.9 on a bar-type change; the user kept 0.9. The snapshot in `desktop/files/settings/openbar.dconf` was refreshed from the live settings on 2026-11-24 (Mainland, opacity 0.9, margin 0, teal accent).

## Rollback

The older targeted backups (`archive/topbar-before-*`, `archive/alpine-theme-before-*`) were deleted on 2026-11-24; the current theme's rollback is `archive/church-theme-before-2026-11-19/restore.sh`. To remove Open Bar styling, use `gnome-extensions disable openbar@neuromorph`. Do not restore old full-desktop snapshots over unrelated later settings.

## Notification button

Removed on 2026-11-19 at the user's request: the stock clock menu shows notifications. A running session needs `gnome-extensions disable surface-notifications@example.internal` once; setup.sh no longer installs or enables it.
