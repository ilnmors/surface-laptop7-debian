# Debian swirl-only boot and login artwork

Current source: Debian desktop-base `/usr/share/desktop-base/debian-logos/logo.svg`, retained as debian-logo-source.svg with the existing package copyright. render.py renders only the swirl, without Debian wordmark or version, to watermark.png; debian-logo.svg is the matching greeter artwork. Preview includes the existing spinner. Prior wordmark files are history, not the active source.

Plymouth: desktop rootfs contains the swirl watermark. surface-plymouth-assets restores it after Debian's hook, preventing replacement with logo-text-version-64.png. GPU firmware hooks remain intact. GDM: /usr/share/gdm/dconf/99-surface-logo overrides logo AND fallback-logo to /usr/share/pixmaps/surface-debian-logo.svg. desktop/setup.sh runs generate-config without restarting the active login/session manager. Existing GDM defaults are otherwise preserved.

Validated: rendered preview inspected; extracted initramfs watermark byte-matched to installed artwork; compiled GDM logo/fallback values point at the dedicated swirl; signed boot image verifies and signed initrd matches the rebuilt image. Physical boot/login appearance remains pending. No active GNOME session was terminated for preview.

Rebuild with python3 desktop/files/boot-art/render.py. python3-gi-cairo, python3-cairo and gir1.2-rsvg-2.0 are already used by this bundle. PNG remains an offline payload; SVG and renderer are Git tracked.
