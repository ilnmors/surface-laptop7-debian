# Reusing this bundle on Debian

Read CURRENT.md first. setup.sh / python3 setup.py is the complete installer for this Surface on Debian 13 ARM64. It is not a generic installer for an unrelated PC. python3 setup.py --verify-only only checks files.

| Component | Scope | Reuse rule |
| --- | --- | --- |
| Qcom kernel, X Plus CPU DTB, touchscreen/touchpad/camera overlays | Surface Laptop 7 13.8-inch ARM64 only | Never copy to x86, Surface Pro, Intel Surface or the 15-inch model. |
| GPI/GENI/SPI-HID, ath12k rfkill, Bluetooth local-address helper, Romulus audio firmware/UCM | Specific device/chipset | Match device IDs and board wiring before reuse. Do not reuse this machine's Bluetooth address. |
| USB NULL guard and Qualcomm SoundWire patches | Matching driver/kernel ABI | Sources, patches, build and rollback are in patches/files/. Build against the target kernel and sign with its own trusted key. |
| Secure Boot insertion/signing hooks | This kernel layout and ARM64 boot chain | Do not copy private keys. Validate target kernel format, certificate reservation, architecture and EFI layout first. |
| Fluent theme, GNOME extensions, dconf snapshots, terminal palette, IBus | Portable Debian GNOME settings | Copy from desktop/files/, checking GNOME extension versions. Install native-architecture Debian packages, not the bundled ARM64 .deb files on x86. Back up dconf first. |
| Waydroid | Debian Wayland with Binder | Helpers are in programs/waydroid/files/. Bundled images are ARM64 only; obtain the correct official images on other architectures. No Google Play or x86 emulation is assumed. |
| UID 3000, svadmins GID 2000 | This user's repository convention | Do not impose these IDs on an unrelated Debian system. Account migration requires a separate session/reboot. |
| Site CA, VPN, server access and Console code-server/Caddy | Outside this hardware bundle | Use the separate repository roles and encrypted secrets. They are deliberately not copied here. |

## Procedure for a person or AI agent

1. Inspect architecture, Debian/GNOME/kernel versions, model/compatible strings and device IDs. Check CURRENT.md for verified versus pending behavior.
2. Select only matching rows above. Preserve current configuration and a working boot entry before changing drivers. Do not execute archive/ scripts; they are historical references.
3. For a non-Surface desktop, restore only the chosen theme/extension/dconf categories using the steps in desktop/files/ and native distro packages. Avoid setup.sh's hardware, accounts and boot steps.
4. For this Surface, verify files, run bash setup.sh or python3 setup.py as the desktop user, then complete first-time MOK enrollment if needed. Review kernel/files/secureboot/README.md.
5. Verify boot, module signatures, devices and one user-initiated sleep/wake cycle. A successful build or module load does not prove device behavior. Record unresolved faults rather than declaring success.
6. Update installer inputs, concise English procedures, SOURCES.md and both checksum manifests after every change. Commit documentation, scripts, patches and configuration; keep payloads/data/private keys outside Git. hardware-report.html is tracked by user request.

## Component selection

The installer no longer migrates Console UID/GID, hostname or timezone. Prepare infrastructure identity through the repository. Each component has SH/Python entry points; use `python3 setup.py --plan` or `--component desktop`. Bundled packages are ARM64; reuse portable desktop sources/settings with native Debian packages on other architectures. Hardware/kernel/patch stages explicitly check Romulus13. A component run does not guarantee unresolved hardware behavior or restore Steam runtime/account data.
