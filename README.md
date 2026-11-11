# Surface Laptop 7 offline setup

Debian 13 ARM64 GNOME on the 13.8-inch Snapdragon X Plus Surface Laptop 7. Copy this entire directory to external storage before reinstalling. Keep Debian installation media separately.

1. Install Debian 13 ARM64 with GNOME, GRUB in UEFI mode, ext4, and a user with sudo access. Set the hostname to `surface`. Use the same Debian point release or compatible package versions.
2. Log in to GNOME and open a terminal. From this folder run `bash setup.sh`. The script verifies its files and uses local packages with downloads disabled. If a base dependency is missing, install it from Debian media and rerun.
3. Reboot through Debian Surface. Verify Wi-Fi, Bluetooth, touchpad, touchscreen, sound and uname -r. The expected kernel is 7.3.0-31-qcom-x1e. Complete the one-time MOK enrollment in files/secureboot/README.md before enabling Secure Boot.

The script derives the boot and root identifiers from the new installation. It restores the hardware stack, hostname, Seoul timezone, Fluent Light, bottom auto-hiding dock, terminal palette, Korean input, wallpaper and input settings. It installs the existing touchpad tuning plus the Romulus13 touchscreen DTB. See [HARDWARE.md](HARDWARE.md) for the camera test DTB and Secure Boot notes.

See files/touchscreen/, files/audio/, files/secureboot/ and files/desktop/ for short procedures and sources.

For the OV02C10 backport that was tested and rolled back, see [Camera patch](files/camera-quality/README.md).

Fluent Light uses the upstream blur Shell style with Blur My Shell. Theme and extension files are included for offline installation.

## Files

| Path | Contents |
| --- | --- |
| `setup.sh` | Post-install script for a fresh Debian GNOME session. |
| `files/packages/` | Patched kernel and DTBs, camera and audio support, and IPTSD. |
| `files/debian/` | Debian firmware, desktop and audio packages for offline use. |
| `files/rootfs/` | WCN7850 and Surface firmware, initramfs hook, input module list and Wi-Fi settings. |
| `archive/hardware/source/` | Kernel source, patch files, device-tree sources and build references. |
| `files/desktop/themes/` | Installed Fluent Light and compact variants, ready to copy. |
| `archive/desktop/` | Upstream Fluent source snapshot and commit. |
| `files/desktop/packages/` | Debian User Themes extension and matching common package. |
| `files/desktop/settings/` | Current GNOME, dock, input and terminal settings captured from the desktop session. |
| `files/desktop/defaults/`, `backgrounds/`, `sl7-ibus.desktop` | Original desktop defaults, wallpapers and IBus autostart. |
| `archive/install/` | Original build report, installer, package downloads, sources, audio, camera and signed boot tooling. |
| `archive/surface-prep/` | Firmware archive, touchpad calibration, original IPTSD package and Wi-Fi board tooling. |
| `archive/records/` | Original install plans, patches, checks and previous settings. Historical scripts may contain old disk identifiers and destructive steps. |
| `archive/boot/before-cleanup/` | Pre-cleanup GPT, EFI and boot configuration records for reference. |
| `SHA256SUMS` | Checksums of the offline files. Verify with `sha256sum -c SHA256SUMS`. |

Live recovery images are excluded. Private signing keys and account data are excluded. The post-install script does not use the recovery partition or the historical installer. The Codex installer archive is available under `archive/install/packages/` for separate installation and sign-in.
