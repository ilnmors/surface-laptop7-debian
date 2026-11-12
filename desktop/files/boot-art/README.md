# Minimal Debian boot artwork

Source: Debian desktop-base /usr/share/desktop-base/debian-logos/logo-text.svg. Original vector and package copyright are included. render.py makes the grey wordmark off-white and renders a transparent watermark; no external assets or generated raster artwork are used. The preview combines that watermark and an actual bundled spinner frame. It is a layout preview, not a physical boot screenshot.

Theme: near-black background, unversioned Debian swirl/wordmark, lower spinner. Standard two-step password/update dialogs remain available. Static DejaVu Sans replaces the Cantarell theme setting; the old initramfs did not contain Cantarell even though the custom theme requested it.

The desktop rootfs hook surface-plymouth-assets runs after the distro Plymouth hook. It includes DejaVu, Cantarell and Noto CJK fonts and restores the custom watermark, which the distro two-step hook otherwise replaces with logo-text-version-64.png. The initramfs extraction test confirms the exact custom watermark and all fonts. English update progress and Korean sample text shape with zero missing glyphs on the host. Physical rendering during the next boot/offline update remains pending.

The observed 2026-11-12 offline update succeeded: libopenexr-3-1-30 3.1.13-2 → 3.2.12-1~deb13u1. PackageKit logged English Installing Updates and Rebooting messages. Square glyphs do not indicate a failed update; missing/custom-theme font selection is a suspected rendering cause, not conclusively reproduced.

Rebuild assets with /usr/bin/python3 desktop/files/boot-art/render.py. Debian python3-gi-cairo, python3-cairo and gir1.2-rsvg-2.0 are required. The generated PNG remains an offline payload. desktop/setup.sh restores the theme/hook and rebuilds initramfs; the Secure Boot post-hook refreshes the signed image. Signature verification passed after the change.
