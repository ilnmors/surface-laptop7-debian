# Offline sources and transformations

files/SHA256SUMS records every offline payload's SHA-256. SHA256SUMS covers the complete bundle except Git internals and the intentionally untracked HTML report. Archive material remains on disk as provenance; historical scripts are not the installer.

| Payload | Source / version | Transformation and reproduction |
| --- | --- | --- |
| Surface kernel and headers | Ubuntu Concept x1e PPA, linux-qcom-x1e 7.3.0-31.31 | Original URLs, sizes and SHA-512: archive/install/sources/verified-manifest.json. Local kernel package is +sl7.2; build references: archive/hardware/source/. |
| USB suspend module | Same matching kernel source; Prashanth K, 2026-11-06, https://lists.openwall.net/linux-kernel/2026/11/06/466 | Missing HCD NULL guard; files/kernel-patches/patches/01-usb-null-hcd.patch. Build/install helpers and corresponding source are alongside it. |
| Qualcomm SoundWire module | Lee Jones v2 series, 2026-11-03, https://lists.openwall.net/linux-kernel/2026/11/03/ | Patches 06–10: allocation bounds, remove/runtime PM, clock error checking, IRQ-mask locking and stale broadcast completion. Original messages/patches in files/kernel-patches/upstream/. Combined 7.3 backport retains existing IRQ sequencing and MMIO guards. |
| Touchpad transport and Wi-Fi | Community snapshots in archive/hardware/source/surface-xplus-project.zip and surface-laptop7-community.zip; https://github.com/bryce-hoehn/linux-surface-laptop-7 | GPI/GENI QSPI/SPI-HID backports and Romulus13 ath12k rfkill guards. Original local build and DT scripts remain archived. Exact archive origins not fully recorded; do not invent missing commit IDs. |
| Touchscreen DTB | Jizhou Tong v2, 2026-09-30, https://lkml.iu.edu/2609.3/14494.html | I2C8/0x34/GPIO38 overlay merged with the working board DTB. Source/overlay/merged binary in files/touchscreen/. It still fails probing on this unit. |
| Audio topology | linux-firmware commit bfc1d7433ddd92302d2c59287a5c00477c8a8bd7 | Exact URL and original SHA-256: archive/hardware/source/TOPOLOGY-SOURCE.json. Romulus topology and UCM in rootfs. |
| Windows OEM files | Microsoft Surface Laptop 7 ARM package 26.091.9400.0, https://www.microsoft.com/en-us/download/details.aspx?id=106120 | MSI SHA-256 and analysis in archive/windows-touchpad/README.md. Linux weak-contact tracking is an adaptation, not a Windows driver binary running on Linux. |
| IPTSD calibration/edge daemon | https://github.com/alex-lentz/iptsd and the local archived source | files/touchpad/README.md and edge-fix/{edge-contact.patch,build.sh}. Rejected wider calibration and camera trials remain documented. |
| Camera metadata / ISP trial | Matching kernel OV02C10 metadata backport; libcamera 0.4.0, https://patchwork.libcamera.org/patch/28734/ | files/camera-quality/ has original Debian source inputs, patches and build/install helper. ISP quality trial was rolled back after flicker; it is not enabled by setup.sh. |
| Fluent Light | https://github.com/vinceliuice/Fluent-gtk-theme, commit 7a49a464b0188c340101c52965c18190b1c694cf | Archived original source/commit in archive/desktop/. Rounded translucent topbar changes in files/desktop/topbar/; installed theme snapshot in files/desktop/themes/. |
| GNOME extensions | https://extensions.gnome.org/ ; upstream metadata.json in each extension | Vitals 86, Caffeine 61, AppIndicator 66; Blur My Shell and dock/User Themes are bundled or supplied as Debian packages. GNOME 48 compatibility and settings snapshots recorded in files/desktop/. |
| Debian packages | Authenticated Debian trixie, updates, security and explicitly enabled backports repositories | .deb control metadata records exact package/version/architecture. Installers use local files with downloads disabled; missing base dependencies must come from matching Debian installation media. |
| Secure Boot helpers | Local scripts using Linux insert-sys-cert semantics and Debian shim/GRUB/sign-file | files/secureboot/ describes certificate insertion, signing hooks, original references and isolated VM verification. Every target generates/keeps its own private signing key outside this bundle. |
| Waydroid | Debian 1.6.3+ds-2~bpo13+1 and official https://ota.waydro.id/ | files/android/OTA-SOURCES.json records official channel metadata and download URLs/hashes. Vanilla ARM64 system/vendor images are copied without modification. Local adaptation sets multiwindow mode and adds individual GNOME launchers. |

## Reproduction

Use bash setup.sh or python3 setup.py as the desktop user on this Surface. Both execute the same installer. Rebuild replacement kernel modules with files/kernel-patches/build.sh in a new build directory; its source and header inputs are local. Sign on the destination with that machine's trusted key. Never reuse this machine's private keys or Bluetooth address on another device.

Unrecorded historical download URLs are explicitly marked above. Preserve the archived manifest and original packages; a plausible upstream URL is not proof of the exact original download.
