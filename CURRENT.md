# Latest recovery status — supersedes staged experiments below

Wi-Fi experiment rejected after hardware rfkill regression. Current loaded/next-boot ath12k is original sl7 A98E5140E078A5920DAC05E; unblocked, automatically connected and Wi-Fi-bound HTTPS 200 verified. Camera experiment is removed from disk/default setup but still loaded until reboot because in-use removal was refused; next boot restores sl7 C8AE6F17BF899E4A937A808. Both experiments are excluded from automatic installation. Boot/login use only the Debian swirl; initrd and compiled GDM settings checked.

# Current Surface configuration

Updated after the 2026-11-12 09:31 KST reboot. Debian 13 ARM64 GNOME; Surface Laptop 7 13.8-inch Romulus13 X Plus. Console UID 3000 / svadmins GID 2000.

## Boot and drivers

- Secure Boot is enabled; kernel lockdown is integrity. Kernel remains 7.3.0-31-qcom-x1e. The offline update installed only the OpenEXR security fix, not a new kernel.
- The actual loaded replacement modules are now verified: dwc3_qcom srcversion 8554A2970EC29806E65733C; soundwire_qcom 3D22555E212EACB6FA11473. Signature/ABI tests and real boot loading passed. No failed system services were found.
- Touchpad: the libinput edge-palm exception is active after reboot; user reports much improved behavior. Existing Windows-analysis-based IPTSD contact tracking/calibration remains. This does not certify every contact/jump case fixed.
- Bluetooth automatically recovered and is powered on. Speaker output exists and no SoundWire parity/bus-clash error appeared during this boot's short observation. User has not yet confirmed audio; sustained playback and new-module deep resume remain pending.
- Touchscreen still has no usable input device. CPU9 still fails PSCI -22; only policy0 for CPUs 0–3 is exposed by SCMI. Camera quality patch remains rolled back. These are not solved by the successful boot.

## Power and sleep

- Native display remains 2304x1536 / 120Hz / 1.5 scale by user request. The panel reports 24–120Hz, but the current DRM connector has no vrr_capable property. Dynamic refresh was not enabled without driver capability.
- WCN7850 station power saving is enabled and persisted through NetworkManager. Short link test: 5/5 gateway replies, ~5ms mean, no ath12k error/crash/timeout during observation. Repeated deep resume and clean battery comparison remain pending.
- Ondemand governor retained. A short schedutil test changed frequency correctly, but external power invalidated power readings; no permanent CPU cap/governor change was made.
- Previous-boot baseline: ~5.296h sleep lost ~6 percentage points (~3.046Wh, 0.575W); sampled awake mean ~7.64W. It predates current changes and is not a measured improvement. See drivers/files/power/.
- Previous power trace identified SPI-HID ~2.417s plus PCIe/Wi-Fi resume delays. A fresh power-only trace is armed for the next user-controlled deep cycle. No forced suspend was initiated.

## Desktop and boot appearance

- Fluent Light, GNOME extensions, terminal palette and Korean IBus remain installed.
- Plymouth now uses an unversioned off-white Debian vector wordmark on a near-black background and the bundled spinner. The custom watermark, static/fallback fonts and gen70500 GPU firmware are verified in the rebuilt initramfs; the signed image passes sbverify. Physical appearance on next boot/update remains pending.
- The offline update's square glyphs were not an update failure. PackageKit reports successful OpenEXR update and English progress messages. Earlier initramfs lacked the Cantarell font selected by the theme. Static DejaVu and explicit fallback inclusion address this mismatch; the exact physical symptom is not conclusively reproduced.

## Personal programs

- Waydroid Vanilla ARM64 and genuine signed KakaoTalk 26.9.2 splits are installed. Secondary Device login screen was verified earlier; account data is preserved.
- KakaoTalk is registered in GNOME's app grid and login autostart (8-second delay). Only its individual window opens. Launcher and setup are separate; startup never reinstalls or resets the app. The icon now uses the real exported yellow TALK artwork rather than an inherited settings icon.
- By user choice Android stays running when all windows close; KakaoTalk is exempt from Android idle optimization and notifications are permitted. This has background RAM/power cost; Linux host suspend remains unchanged. Real incoming-message/notification delivery still needs a user test.
- Physical-keyboard mode: Android show_ime_with_hard_keyboard=0; GNOME accessibility screen keyboard disabled. IBus/input methods remain installed. Android UI is explicitly light/white (night mode no).
- Waydroid measured ~1.26GiB PSS with 90 processes in one snapshot. Shared services are reused; additional apps still allocate private memory. No Discord or other additional personal APK was installed.
- Steam SDK repair is verified; FEX Korean fonts are installed. Game-only click/Korean visual verification remains paused at user request.

## Reproduction and scope

kernel/, drivers/, patches/, desktop/ and programs/ contain component SH/Python installers and offline payloads. A Git clone alone excludes binary payloads and is not a complete offline backup. Setup does not restore user data or a complete Steam runtime, repartition disks, or replace Console infrastructure roles. Initial MOK enrollment, firmware settings, reboot and login remain manual.

HTML, generation script, status data, documents, configuration and patches are tracked in Git. Private signing keys, site CA/VPN/server credentials and raw binary payloads are excluded. Console/Caddy/Kopia/code-server are managed in the separate repository.

## Display recovery verified

The earlier GPU initramfs hook omitted the Microsoft zap shader. It now includes qcdxkmsuc8380.mbn alongside SQE/GMU firmware. After reboot the user confirmed normal graphics; Secure Boot remains enabled and previous GPU init errors are absent from this boot. KakaoTalk autostart has been restored. Night Light and Blur My Shell remain disabled from recovery.

## Latest deep-sleep and hardware check

This boot completed one deep cycle (success 1/fail 0). Entry 10:59:18, exit 12:04:55. Wi-Fi regulatory and PCIe L2 warnings remain; authentication began 11.4s after suspend exit. Fresh device power trace is armed. User reports working speakers but one later codec parity error remains. Camera streamed 90/90 frames at 720p, ~18.8fps; touchscreen and CPU9 remain unresolved. See drivers/files/power/HARDWARE-RECHECK.md. These later observations supersede earlier statements that no cycle occurred.

## Staged hardware fixes before automatic reboot

Wi-Fi regulatory completion commit f2576dc0 is installed with ath12k srcversion D61DA424018CF1563587D2E. Romulus13-only minimum-frame-period camera policy is installed with ov02c10 srcversion BFE86F0F9657EDF53C56CD3 (fast_video=Y). Both signed modules loaded in the matched signature-enforcing ARM64 guest; initial image contains exact installed modules and complete GPU firmware. Live hardware still uses previous modules until reboot. After reboot verify those versions, camera FPS/brightness/flicker, deep callbacks/Wi-Fi reconnection and audio errors. Power callback tracing is boot-enabled. Fn non-toggling media-default/fixed LED, CPU9 and touchscreen remain unresolved.
