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
| `docs/` | `UPDATES.md` (how updates interact with the local packages) and `investigations/` (dated records behind the settings). |
| `tools/` | Checksum and battery maintenance helpers. |

Each component has `setup.sh` and `setup.py`; Python delegates to that component's shell implementation. The top-level entry calls components in kernel → drivers → patches → desktop → programs order. Hardware stages refuse unrelated boards. Portable desktop assets are reusable on other Debian machines with native packages; see PORTABILITY.md.

First-time MOK enrollment, firmware settings, reboot and GNOME re-login are physical/manual steps. Read kernel/files/secureboot/README.md. New USB/SoundWire modules only become active after reboot. A successful installer run does not prove device behavior; see "Support and limits" below.

Steam runtime/game downloads and user saves are not bundled; its component repairs an existing ARM64 Steam/FEX setup. Verified ARM64 KakaoTalk APK splits and installer are bundled. Login remains manual. Android system components are retained; unwanted app launchers are hidden. No account login is automated.

SOURCES.md records origins and patch procedures. PAYLOADS.sha256 covers component payloads; SHA256SUMS covers maintained files and those payloads. Regenerate with `python3 tools/checksums.py`, then verify with `python3 setup.py --verify-only` or `sha256sum -c SHA256SUMS`.

Git tracks text/configuration, scripts and patches. Offline binaries, historical archives and private keys stay outside Git. Caddy, code-server, Kopia, Console identity, site CA/VPN and infrastructure secrets belong to the separate repository, not this bundle.

## Support and limits

What the installed setup provides on this machine, and what it does not. Investigation notes and procedures are in the component directories.

| Area | Provided | Limits |
| --- | --- | --- |
| Boot | Locally signed kernel image with an embedded DTB through Debian shim/GRUB; Secure Boot on; each promoted boot change keeps a GRUB rollback entry | First-time MOK enrollment and firmware settings are manual ([kernel/files/secureboot/README.md](kernel/files/secureboot/README.md)) |
| Touchscreen, touchpad, keyboard | GTCH touchscreen over SPI with IPTSD; touchpad click-drag and edge-palm fixes; Shift+Hangul input switching | The touchpad is ready about 2 s after resume; the firmware Fn toggle is kept |
| Display, CPU | 120 Hz; 10 cores through scmi-cpufreq with the default governor and range | — |
| Camera, video | Front camera through libcamera and PipeWire with black-level tuning, privacy LED; Iris hardware decoding and encoding (H.264, HEVC, VP9, AV1) through V4L2 | Low-light noise; the IR (Windows Hello) camera is not supported; Firefox decodes in software |
| Audio | Speakers and headphones through the Romulus topology and UCM, SoundWire backports | Intermittent speaker silence has occurred and is not claimed fixed ([drivers/files/audio/README.md](drivers/files/audio/README.md)) |
| Wireless, USB | Wi-Fi, Bluetooth with a persistent address, all USB ports, phone tethering | The `a400000` controller can fail to start at boot; the USB-C USB2 path can stay dead after abrupt data loss until dwc3-qcom is rebound; USB-C display hot-plug is slow |
| Sleep | `deep` sleep with locking before sleep; dwc3-qcom and QMP PHY fixes for sleep | Lid-closed suspends have occasionally not resumed ([drivers/files/sleep/README.md](drivers/files/sleep/README.md)); the deepest SoC states are not reached |
| Android, programs | Waydroid (ARM64) and KakaoTalk preparation | Arbitrary APK compatibility is not guaranteed; Steam and its games are not bundled |

## License

GPL-2.0-only (see [LICENSE](LICENSE)), the license of the Linux kernel that the patches and device tree overlays derive from. Bundled third-party components keep their own licenses: the Fluent GTK themes under `desktop/files/themes/` (GPL-3.0) and each GNOME extension under `desktop/files/extensions/` (see its metadata). Firmware and other binary payloads are not part of the repository.
