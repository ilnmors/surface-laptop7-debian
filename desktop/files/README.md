# Desktop

- Fluent Light uses the upstream GNOME 48 blur Shell stylesheet from the archived Fluent source.
- Blur My Shell version 77 is included under extensions/ and enabled by setup.sh. Panel blur uses the dark style and light text, with static blur.
- settings/ contains GNOME and terminal snapshots. The terminal uses a dark navy background, bright text and saturated ANSI colors.
- packages/ includes User Themes, the common extension files, unzip and cups-pk-helper. The latter fixes the missing authorization component in GNOME's printer settings.
- Site-specific printer addresses, CA and VPN settings belong outside this bundle.

Fluent source https://github.com/vinceliuice/Fluent-gtk-theme
Blur My Shell source https://extensions.gnome.org/extension/3193/blur-my-shell/

## Boot screen

Plymouth uses the stock two-step spinner with the Debian logo on a black background. Theme files and plymouthd.conf are under desktop/files/rootfs; packages/ includes Plymouth, its themes, label plugin and libplymouth5. setup.sh selects surface-debian. The signed boot updater keeps quiet/splash, hides service status and gives GRUB a hidden one-second timeout. Escape in Plymouth reveals boot details. The initramfs and signed image must be rebuilt after theme changes. Actual appearance requires a reboot.
