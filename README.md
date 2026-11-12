# Surface offline setup

Debian 13 ARM64 GNOME on Surface Laptop 7 13.8-inch Snapdragon X Plus (Romulus13). Copy this entire directory, including ignored binary payloads, before reinstalling. A Git clone alone is insufficient.

```sh
python3 setup.py --plan                 # inspect actions; no sudo or changes
python3 setup.py --verify-only          # verify local payloads
bash setup.sh                          # all components, in dependency order
python3 setup.py --component desktop    # selected component
bash drivers/setup.sh                  # direct component entry
python3 drivers/setup.py               # same implementation
```

Run installation as the desktop user with sudo access. Use a compatible Debian 13 ARM64 GNOME installation with GRUB/UEFI and Debian media available for missing base dependencies. The script disables APT downloads; an incomplete dependency set fails rather than silently downloading. It does not partition disks, migrate account IDs, install Console services or restore application data.

| Directory | Contents and entry points |
| --- | --- |
| `kernel/` | Kernel package, board DTB selection, Secure Boot helpers and EFI boot chain. |
| `drivers/` | Firmware, touchpad/audio/camera support, Bluetooth recovery and device configuration. |
| `patches/` | ABI-matched USB/SoundWire module backports, sources, headers, build/install helpers. |
| `desktop/` | Fluent theme, GNOME extensions, dconf, terminal, IBus and Plymouth. |
| `programs/` | Waydroid, Steam/FEX helpers and KakaoTalk preparation. Each program has its own entry. |
| `*/files/` | Offline packages, configuration, source and reusable payloads used by the corresponding component. |
| `archive/` | Historical installer/scripts, original reports and reference snapshots; not an installation entry. |
| `tools/` | Report/checksum maintenance helpers. |

Each component has `setup.sh` and `setup.py`; Python delegates to that component's shell implementation. The top-level entry calls components in kernel → drivers → patches → desktop → programs order. Hardware stages refuse unrelated boards. Portable desktop assets are reusable on other Debian machines with native packages; see PORTABILITY.md.

First-time MOK enrollment, firmware settings, reboot and GNOME re-login are physical/manual steps. Read kernel/files/secureboot/README.md. New USB/SoundWire modules only become active after reboot. Existing touchscreen/edge tracking/audio issues are not declared solved by a successful installer run. See CURRENT.md and HARDWARE.md.

Steam runtime/game downloads and user saves are not bundled; its component repairs an existing ARM64 Steam/FEX setup. Verified ARM64 KakaoTalk APK splits and installer are bundled. Login remains manual. Android system components are retained; unwanted app launchers are hidden. No account login is automated.

SOURCES.md records origins and patch procedures. PAYLOADS.sha256 covers component payloads; SHA256SUMS covers maintained files and those payloads. Regenerate with `python3 tools/checksums.py`, then verify with `python3 setup.py --verify-only` or `sha256sum -c SHA256SUMS`. Rebuild the local HTML with `python3 tools/report.py` after updating STATUS.json.

Git tracks text/configuration, scripts and patches. Offline binaries, historical archives and private keys stay outside Git. hardware-report.html is tracked. Caddy, code-server, Kopia, Console identity, site CA/VPN and infrastructure secrets belong to the separate repository, not this bundle.
