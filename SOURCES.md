# Offline sources and transformations

PAYLOADS.sha256 records every offline payload's SHA-256. SHA256SUMS covers the complete bundle except Git internals and historical archives; the HTML is now tracked. Archive material remains on disk as provenance; historical scripts are not the installer.

| Payload | Source / version | Transformation and reproduction |
| --- | --- | --- |
| Surface kernel and headers | Ubuntu Concept x1e PPA, linux-qcom-x1e 7.3.0-31.31 | Original URLs, sizes and SHA-512: archive/install/sources/verified-manifest.json. Local kernel package is +sl7.2; build references: archive/hardware/source/. |
| USB suspend module | Same matching kernel source; Prashanth K, 2026-11-06, https://lists.openwall.net/linux-kernel/2026/11/06/466 | Missing HCD NULL guard; patches/files/patches/01-usb-null-hcd.patch. Build/install helpers and corresponding source are alongside it. |
| Qualcomm SoundWire module | Lee Jones v2 series, 2026-11-03, https://lists.openwall.net/linux-kernel/2026/11/03/ | Patches 06–10: allocation bounds, remove/runtime PM, clock error checking, IRQ-mask locking and stale broadcast completion. Original messages/patches in patches/files/upstream/. Combined 7.3 backport retains existing IRQ sequencing and MMIO guards. |
| Touchpad transport and Wi-Fi | Community snapshots: surface-xplus-project.zip (kept as drivers/files/touchpad/edge-fix/source.zip) and archive/hardware/source/surface-laptop7-community.zip; https://github.com/bryce-hoehn/linux-surface-laptop-7 | GPI/GENI QSPI/SPI-HID backports and Romulus13 ath12k rfkill guards. Original local build and DT scripts remain archived. Exact archive origins not fully recorded; do not invent missing commit IDs. |
| Touchscreen DTB | Jizhou Tong v2, 2026-09-30, https://lkml.iu.edu/2609.3/14494.html | I2C8/0x34/GPIO38 overlay merged with the working board DTB. Source/overlay/merged binary in drivers/files/touchscreen/. It never bound on this unit; superseded by the GTCH SPI overlay in drivers/files/touchscreen/spi-gtch/. |
| Audio topology | linux-firmware commit bfc1d7433ddd92302d2c59287a5c00477c8a8bd7 | Exact URL and original SHA-256: archive/hardware/source/TOPOLOGY-SOURCE.json. Romulus topology and UCM in rootfs. |
| Windows OEM files | Microsoft Surface Laptop 7 ARM package 26.091.9400.0, https://www.microsoft.com/en-us/download/details.aspx?id=106120 | MSI SHA-256 and analysis in archive/windows-touchpad/README.md. Linux weak-contact tracking is an adaptation, not a Windows driver binary running on Linux. |
| IPTSD calibration/edge daemon | https://github.com/alex-lentz/iptsd and the local archived source | drivers/files/touchpad/README.md and edge-fix/{edge-contact.patch,build.sh}. Rejected wider calibration and camera trials remain documented. |
| Camera metadata / ISP trial | Matching kernel OV02C10 metadata backport; libcamera 0.4.0, https://patchwork.libcamera.org/patch/28734/ | drivers/files/camera-quality/ has original Debian source inputs, patches and build/install helper. ISP quality trial was rolled back after flicker; it is not enabled by setup.sh. |
| Fluent Light | https://github.com/vinceliuice/Fluent-gtk-theme, commit 7a49a464b0188c340101c52965c18190b1c694cf | Archived original source/commit in archive/desktop/. Rounded translucent topbar changes in desktop/files/topbar/; installed theme snapshot in desktop/files/themes/. |
| GNOME extensions | https://extensions.gnome.org/ ; upstream metadata.json in each extension | Vitals 86, Caffeine 61, AppIndicator 66; Blur My Shell and dock/User Themes are bundled or supplied as Debian packages. GNOME 48 compatibility and settings snapshots recorded in desktop/files/. |
| Debian packages | Authenticated Debian trixie, updates, security and explicitly enabled backports repositories | .deb control metadata records exact package/version/architecture. Installers use local files with downloads disabled; missing base dependencies must come from matching Debian installation media. |
| Terminal symbol fallback font | Debian trixie fonts-symbola 2.60-2 (all), https://packages.debian.org/trixie/fonts-symbola | Unmodified .deb in desktop/files/packages/, installed by desktop/setup.sh. Provides U+23F4–U+23FA (e.g. ⏵) that DejaVu Sans Mono and other bundled fonts lack, so fontconfig fallback stops rendering tofu in GNOME Terminal. |
| Image thumbnailer | Debian trixie libgdk-pixbuf2.0-bin 2.42.12+dfsg-4+deb13u1 (arm64), https://packages.debian.org/trixie/libgdk-pixbuf2.0-bin, SHA-256 7dab6d0f7f25c64a645d446253f8cb8f7ca79813eb801519b7be02d512a79820 (matches the archive metadata) | Unmodified .deb in desktop/files/packages/, installed by desktop/setup.sh. Provides gdk-pixbuf-thumbnailer so Files shows JPEG/PNG/GIF/TIFF thumbnails. |
| spi-hid deferred resume | Archived community source kernel/modules/spi-hid (surface-xplus-project.zip), srcversion A2DC44A5E473B534676E1E3 | drivers/files/touchpad/spi-hid-resume/resume-deferred.patch moves the 2 s post-reset settle from the resume callback to a work item; built against bundled headers, signed on the machine. |
| PCIe3-off DTB | Verified Surface DTB (09fd6331…) | drivers/files/pcie/prepare-pcie3-off.sh sets only pcie@1bd0000 status=disabled. |
| Secure Boot helpers | Local scripts using Linux insert-sys-cert semantics and Debian shim/GRUB/sign-file | kernel/files/secureboot/ describes certificate insertion, signing hooks, original references and isolated VM verification. Every target generates/keeps its own private signing key outside this bundle. |
| Waydroid | Debian 1.6.3+ds-2~bpo13+1 and official https://ota.waydro.id/ | programs/waydroid/files/OTA-SOURCES.json records official channel metadata and download URLs/hashes. Vanilla ARM64 system/vendor images are used without modification; the local copies were deleted on 2026-11-24 and are downloaded again from OTA. Local adaptation sets multiwindow mode and adds individual GNOME launchers. |

## Reproduction

Use bash setup.sh or python3 setup.py as the desktop user on this Surface. Both execute the same installer. Rebuild replacement kernel modules with patches/files/build.sh in a new build directory; its source and header inputs are local. Sign on the destination with that machine's trusted key. Never reuse this machine's private keys or Bluetooth address on another device.

Unrecorded historical download URLs are explicitly marked above. Preserve the archived manifest and original packages; a plausible upstream URL is not proof of the exact original download.

## Modular layout and additional sources (2026-11-12)

Payloads were moved byte-for-byte from files/ into kernel/files, drivers/files, patches/files, desktop/files and programs/waydroid/files. Rootfs Plymouth assets moved to desktop; device firmware/configuration remains under drivers. The pre-refactor installer copy was deleted on 2026-11-24. New entry points preserve one shell implementation per component. No CA/private credentials were added.

- Steam Korean fonts: installed Debian fonts-noto-cjk package, /usr/share/fonts/opentype/noto; license bundled with regular/bold TTC files under programs/steam/files/fonts. These are copied unmodified into the FEX root, not patched. Game behavior remains unverified/paused.
- Touchpad source ZIP: drivers/files/touchpad/edge-fix/source.zip is the surface-xplus-project.zip community snapshot (its byte-identical archive copy was removed on 2026-11-24). edge-contact.patch records local modifications. Source build dependencies remain an explicit prerequisite; the offline installer uses the prebuilt daemon.
- Touchpad upstream comparison: https://github.com/bryce-hoehn/linux-surface-laptop-7 and https://github.com/linux-surface/iptsd/issues/192 . Issue 192 is Intel and must not be presented as an ARM fix. QSPI RFC https://lists.openwall.net/linux-kernel/2026/11/05/3628 has transport/reset prerequisites; no partial driver swap was installed.
- Kakao APKPure 26.9.2: https://d.apkpure.net/b/XAPK/com.kakao.talk?versionCode=29260920 downloaded as kakaotalk.download; contains ARMv7 split only. Rejected, not installed. Official signer allowlist is saved from https://www.kakao.com/.well-known/assetlinks.json . ARM64 distribution remains pending; no app binary was patched.

## libinput geometric edge exclusion

Official Debian pool source libinput_1.28.1.orig.tar.gz (SHA256 a13f8c9a7d93df3c85c66afd135f0296701d8d32f911991b7aa4273fdd6a42a3) and libinput_1.28.1-1+deb13u1.debian.tar.xz (413b1238c335cced8f2698fc0bc8c0c6605034324a9528d841726ba1d3575f56), checked against the downloaded DSC. Preserve all four Debian patches. The local patch and build/package helper are in drivers/files/touchpad/libinput-edge/. Original rollback package SHA256 a2acd04f3b1e9e91d22a26b63650087a179b6b3dbaddadc92d89edfbb2075ae1 from authenticated APT metadata. Build dependencies were downloaded through APT and extracted into a temporary build root, not installed globally. The modified package is versioned +surface1; do not hold back newer Debian security updates.

## KakaoTalk ARM64 acquired

Source https://apk.gold/download?split=621182/3544335/kakaotalk-free-calls-and-text delivered KakaoTalk ZIP SHA256 377ff35febd1d60498efb160caaec29a02ed94d8eb073f3b038c59a3f3d255f0. Four unmodified APKs had per-file SHA256 in manifest.json (local copies and the ZIP deleted on 2026-11-24); since then install.py accepts any version whose APKs carry the official Kakao signer (official-assetlinks.json) and pass the aapt checks. apksigner verified every split against the official Kakao assetlinks signer allowlist; aapt verified package com.kakao.talk, version 29260920, min SDK29 and ARM64 split. Installed on API33 without entering account credentials. Initial APKPure ARMv7 duplicate was rejected and removed; metadata retained. AAPT inspection packages came from authenticated Debian APT.

## Waydroid shared-storage initialization

MediaProvider/StorageManager timed out while IOmx/IOmxStore attempted to start a service absent from the MAINLINE vendor image. The supported vendor overlay now removes that orphan declaration only. Source, baseline manifest, exact preconditions and rollback are in programs/waydroid/files/media-fix/. This follows the same diagnosed mechanism as https://gist.github.com/jstockdale/36c4b6a858726d08dc6b1e93f6b37473 after checking local service absence and logs; no Samsung/QTI binary imports were copied. Original system/vendor images remain unmodified.

## Post-reboot evaluation, boot artwork and power configuration

2026-11-12 boot verified Secure Boot integrity mode and the actual replacement USB/SoundWire srcversions. User reports much improved touchpad behavior. Later boots validated deep suspend and resume; the speaker silence is handled by the SoundWire controller policy in drivers/files/audio/.

Debian desktop-base logo-text.svg is the source of desktop/files/boot-art/debian-wordmark-source.svg; render.py changes neutral grey to off-white and rasterizes through librsvg/cairo. COPYRIGHT is retained. The post-Plymouth initramfs hook preserves the custom watermark and includes static/fallback fonts. Both original artwork source and transformation are recorded, with no site credentials. GPU firmware inclusion copies the already installed gen70500 files unmodified; sources retain the existing firmware provenance.

WCN7850 power-save uses the existing driver's supported station PS, persisted by NetworkManager rather than replacing firmware or kernel code. The short link check passed; no claimed runtime extension has been measured. KakaoTalk login/background settings are normal user/Android settings; sources and rollback are in programs/kakaotalk/README.md and docs/investigations/2026-11-12-power-and-drivers/OPTIMIZATION.md.

## Regulatory and camera follow-up

ath12k f2576dc0 comes unmodified from the upstream WireGuard Linux kernel mirror; matching source snapshot, header packages and rebuild inputs are retained in patches/files. The OV02C10 fast_video change is a local Romulus13 policy using the already declared minimum VTS; it is not the rejected libcamera gain helper or a manufacturer color calibration. See patches/files/CAMERA-FRAME-TIMING.md. GPIO31 reset evidence came from the published Romulus13 touchscreen v1; a one-off trial failed and is not replayed by setup. Diagnostic gpiod/libgpiod3 packages were downloaded through authenticated Debian APT and extracted locally under /var/tmp, with original .deb payloads retained in drivers/files/touchscreen/tools.

## 2026-11-12 follow-up

- CPU: `drivers/files/cpu/README.md` records the X1P64100 report, upstream pull request, baseline source and local topology trial.
- Wi-Fi: `patches/files/wifi-regulatory/known-good/README.md` records the upstream completion fix, preserved Surface guards and the retracted beacon-loss regression claim.
- Camera: `docs/investigations/2026-11-12-camera-quality/RESULTS.md` records exact tested/rejected color profiles, public OV02C10 patches, isolated Debian 0.7.1 packages and deferred GPU-denoise research.
- Open Bar 49: GNOME Extensions version tag 65598, source https://github.com/neuromorph/openbar , offline zip + source under desktop. No app or Flatpak recoloring enabled.

## Alpine desktop palette (2026-11-13)

Photo by Luca Bravo: [Boathouse on a mountain lake](https://unsplash.com/photos/brown-house-near-body-of-water-zAjdgNXsMeg), [Unsplash License](https://unsplash.com/license). A 3200×2134 provider-resized JPEG is retained under `desktop/files/backgrounds/`; URL, SHA256 and processing details are in `desktop/files/topbar/alpine-theme.json`.

Wallpaper since 2026-11-19 (afternoon): Frederic Edwin Church, *Cross in the Wilderness* (1857, Museo Nacional Thyssen-Bornemisza, Madrid), public domain. 3000×1983 JPEG (SHA-1 df8133107998184fe49535c36e12041413482f01, as listed by Commons; source Art Renewal Center) from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Cross_in_the_Wilderness_Frederic_Edwin_Church.jpg), unmodified, stored as `desktop/files/backgrounds/church-cross-in-the-wilderness.jpg` (kept out of Git; hash in PAYLOADS.sha256). The Friedrich painting below stays in the bundle as the previous wallpaper.

Previous wallpaper (2026-11-19 morning): Caspar David Friedrich, *Morning in the Riesengebirge* (1810–1811, Alte Nationalgalerie, Berlin), public domain. 3000×1882 JPEG from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Caspar_David_Friedrich,_Morgen_im_Riesengebirge.jpg), stored as `desktop/files/backgrounds/friedrich-morning-in-the-riesengebirge.jpg` (kept out of Git like the earlier photo; hash in PAYLOADS.sha256). The Luca Bravo photo stays in the bundle as the previous wallpaper.

The `Fluent-teal-Light` variant was built from the already archived Fluent source with the upstream installer (`-t teal -c light -s standard`). Debian trixie arm64 SassC and libsass packages are retained in `desktop/files/topbar/build-tools/`; only the maintained dock CSS is appended after generation. See `desktop/files/topbar/ALPINE-THEME.md` for exact offline reproduction and rollback.

Waydroid host downloads: local `programs/waydroid/download-link.py` and `.sh` integrate the shared-storage path documented at https://docs.waydro.id/faq/setting-up-a-shared-folder . Access uses a per-user ACL instead of changing Android owners. Debian trixie `acl` is retained under `programs/waydroid/files/packages/`; exact package/hash and reproduction are in `programs/waydroid/files/README.md`.

Audio trial (2026-11-13): official WirePlumber ALSA `api.alsa.soft-mixer` documentation at https://pipewire.pages.freedesktop.org/wireplumber/daemon/configuration/alsa.html and the kernel x1e80100 speaker caps at https://raw.githubusercontent.com/torvalds/linux/master/sound/soc/qcom/x1e80100.c . A same-codec Surface Pro 11 report is linked in `drivers/files/audio/README.md`; it is supporting evidence, not a verified Laptop 7 fix.

## Audio recurrence case review — 2026-11-14

[Cases, primary links and applicability](docs/investigations/2026-11-14-audio-cause/CASES-AND-PROPOSAL.md) compare the X1 IRQ/clock fix, X13s stability series, Surface Laptop 7 UCM enablement and Surface Pro 11 configuration attempts with retained local source and measurements. No new patch or payload installed; proposed runtime-PM mitigation remains unconfirmed.

## Physical click state (2026-11-15)

Local source fix in drivers/files/touchpad/click-drag/physical-button-state.patch, applied after edge-contact.patch to the same archived vendor IPTSD ZIP. No downloads. The production TouchDevice header reproduces seven failures before the fix and passes all 13 synthetic regression checks after it. Source and binary hashes, the comparable but unresolved SLS2 issue 208, offline build/test entry points and rollback are documented in click-drag/README.md and verification.json. This is not a Windows force-calibration change or an upstream-verified ARM patch.

Video decoder firmware since 2026-11-19: `qcvss8380.mbn` from the Microsoft Surface Laptop 7 ARM package 26.091.9400.0 (`SurfaceUpdate/qcdx8380/`, extracted with msitools from `archive/windows-touchpad/SurfaceLaptop7_ARM_Win11_26100_26.091.9400.0.msi`), installed as `drivers/files/rootfs/usr/lib/firmware/qcom/x1e80100/microsoft/qcvss8380.mbn` (local payload, hash in PAYLOADS.sha256). The X Plus (`qcvss8380_pa.mbn`) build and the generic linux-firmware `qcom/vpu/vpu30_p4.mbn` are rejected by the firmware signature check.
