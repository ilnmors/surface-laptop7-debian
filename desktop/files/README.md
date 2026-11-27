# Desktop

- Fluent Light uses the upstream GNOME 48 blur Shell stylesheet from the archived Fluent source.
- settings/ contains GNOME and terminal snapshots. The terminal uses a dark navy background, bright text and saturated ANSI colors.
- packages/ includes User Themes, the common extension files, unzip and cups-pk-helper. The latter fixes the missing authorization component in GNOME's printer settings.
- packages/ also includes fonts-symbola. The terminal font (DejaVu Sans Mono via Monospace) and the other installed fonts lack media-control symbols such as U+23F5 ⏵, so they rendered as tofu boxes. Symbola covers U+23F4–U+23FA and the wider symbol blocks; fontconfig uses it automatically as fallback, without changing the terminal font. Check with `fc-list ':charset=23f5' family`.
- packages/ also includes libgdk-pixbuf2.0-bin. It ships `gdk-pixbuf-thumbnailer` and `/usr/share/thumbnailers/gdk-pixbuf-thumbnailer.thumbnailer`, which make Files (Nautilus) thumbnails for JPEG, PNG, GIF, BMP, TIFF and other gdk-pixbuf formats; without it only the HEIF, JXL, WebP, SVG, PDF, video and font thumbnailers exist and ordinary photos show a generic icon. After installing it on a system that already tried, remove `~/.cache/thumbnails/fail` (cached failures are not retried) and run `nautilus -q`. Check with `gdk-pixbuf-thumbnailer -s 256 file:///usr/share/backgrounds/<image>.jpg /tmp/t.png`.
- setup.sh adds the home printer (IPP Everywhere, default) from the untracked `local/site.env` (template `local.example/site.env`) when it answers. CA and VPN settings stay outside this bundle.

Fluent source https://github.com/vinceliuice/Fluent-gtk-theme

## Boot screen

Plymouth uses the stock two-step spinner with the Debian logo on a black background. Theme files and plymouthd.conf are under desktop/files/rootfs; packages/ includes Plymouth, its themes, label plugin and libplymouth5. setup.sh selects surface-debian. The signed boot updater keeps quiet/splash, hides service status and gives GRUB a hidden one-second timeout. Escape in Plymouth reveals boot details. The initramfs and signed image must be rebuilt after theme changes. Actual appearance requires a reboot.

The current boot artwork and font repair are documented in boot-art/README.md. The unversioned Debian wordmark replaces the distro versioned watermark. A post-Plymouth hook ensures that image is not overwritten and carries static/fallback fonts. See boot-art/README.md for source/rendering details.

## OxiCloud WebDAV auto-mount

`goa-webdav-mount.py` (installed as `~/.local/bin/goa-webdav-mount`) and `goa-webdav-mount.desktop` (autostart) mount the GNOME Online Accounts WebDAV volumes at login with the keyring credentials, retrying every 15 s for up to 10 minutes. gvfs buffers WebDAV uploads in memory, so copy multi-GB files with a WebDAV client instead of the mount.

## Mail

The mail client moved to `programs/mail/` on 2026-11-27 (terminal: Alpine with mbsync, notmuch and msmtp). Geary and its own dependencies (libmessaging-menu0, libytnef0) were removed from packages/; libgmime-3.0-0t64 moved to `programs/mail/files/packages/` because notmuch needs it. The home mail account is still added in Settings → Online Accounts → Email: IMAP `imap.example.internal` 993 (SSL), SMTP `smtp.example.internal` 587 (STARTTLS), user `il`. The internal root CA must be in the system store (site-specific, outside this bundle).

## Removed extensions (2026-11-19)

Vitals, Caffeine, Blur My Shell (already disabled) and the Surface notification button were removed at the user's request. The remaining extensions are Dash to Dock, User Themes, Open Bar and AppIndicator Support. A running session keeps the old extension files until `gnome-extensions disable` and removal from `~/.local/share/gnome-shell/extensions/`.
