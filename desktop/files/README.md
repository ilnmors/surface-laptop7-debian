# Desktop

- Fluent Light uses the upstream GNOME 48 blur Shell stylesheet from the archived Fluent source.
- Blur My Shell version 77 is included under extensions/ and enabled by setup.sh. Panel blur uses the dark style and light text, with static blur.
- settings/ contains GNOME and terminal snapshots. The terminal uses a dark navy background, bright text and saturated ANSI colors.
- packages/ includes User Themes, the common extension files, unzip and cups-pk-helper. The latter fixes the missing authorization component in GNOME's printer settings.
- packages/ also includes fonts-symbola. The terminal font (DejaVu Sans Mono via Monospace) and the other installed fonts lack media-control symbols such as U+23F5 ⏵, so they rendered as tofu boxes. Symbola covers U+23F4–U+23FA and the wider symbol blocks; fontconfig uses it automatically as fallback, without changing the terminal font. Check with `fc-list ':charset=23f5' family`.
- Site-specific printer addresses, CA and VPN settings belong outside this bundle.

Fluent source https://github.com/vinceliuice/Fluent-gtk-theme
Blur My Shell source https://extensions.gnome.org/extension/3193/blur-my-shell/

## Boot screen

Plymouth uses the stock two-step spinner with the Debian logo on a black background. Theme files and plymouthd.conf are under desktop/files/rootfs; packages/ includes Plymouth, its themes, label plugin and libplymouth5. setup.sh selects surface-debian. The signed boot updater keeps quiet/splash, hides service status and gives GRUB a hidden one-second timeout. Escape in Plymouth reveals boot details. The initramfs and signed image must be rebuilt after theme changes. Actual appearance requires a reboot.

The current boot artwork and font repair are documented in boot-art/README.md. The unversioned Debian wordmark replaces the distro versioned watermark. A post-Plymouth hook ensures that image is not overwritten and carries static/fallback fonts. See boot-art/README.md for source/rendering details.

## OxiCloud WebDAV auto-mount

`goa-webdav-mount.py` (installed as `~/.local/bin/goa-webdav-mount`) and `goa-webdav-mount.desktop` (autostart) mount the GNOME Online Accounts WebDAV volumes at login with the keyring credentials, retrying every 15 s for up to 10 minutes. gvfs buffers WebDAV uploads in memory, so copy multi-GB files with a WebDAV client instead of the mount.

## Mail (Geary)

Geary 46.0 is the mail client: it picks up the GNOME Online Accounts mail and Google accounts without its own account setup. packages/ includes geary and the dependencies it pulled in on Debian 13 (libgmime-3.0-0t64, libmessaging-menu0, libytnef0). The home mail account is added in Settings → Online Accounts → Email: IMAP `imap.example.internal` 993 (SSL), SMTP `smtp.example.internal` 587 (STARTTLS), user `il`. The internal root CA must be in the system store (site-specific, outside this bundle).
