# Next: verify the promoted default boot

- User authorized promotion after the one-shot CPU/camera boot succeeded. Verify /proc/cmdline uses /secureboot/vmlinuz-surface-signed.efi (not trial-cpu-camera), CPU online 0-9, three ondemand policies, Secure Boot, camera 37.5fps and Wi-Fi HTTPS.
- Open Bar is ACTIVE after login. Bottom dock has light styling and click-action=previews.
- Check post-suspend Wi-Fi/audio in a later user-initiated cycle. Noise/1080p camera work is deferred. Battery improvement is not measured.
- Promotion changes and updated HTML are local; require final confirmation before push.
- Previous signed image remains in /boot/secureboot/rollback-20261112 and as a GRUB fallback. Restore script remains under drivers/files/cpu.

Historical notes below are superseded by this section.

# Current continuation — 2026-11-12, before one-shot reboot

Read this section before historical notes below.

1. A one-shot signed CPU9/camera boot is selected in /boot/grub/grubenv. Confirm boot ID, online CPUs (expected 0-9), three ondemand policies, Secure Boot and actual module srcversions. Stable and pre-change images remain selectable. Do not promote until hardware checks pass.
2. Expected active ath12k D044C56077CC5357DC3F5BF retains both Surface rfkill guards. It passed repeated Wi-Fi-bound HTTPS checks before reboot. Repeated beacon loss root cause remains open; see known-good/README.md. The regulatory fix does not establish a beacon-loss fix.
3. Expected trial ov02c10 08EF7452B0F555AA15FA25F preserves crop metadata and defaults to faster frames. Test frame rate/errors. Do not forcibly unload the sensor. Neutral isolated libcamera color was user-approved, noise remains. Longer camera quality/1080p/denoise work is DEFERRED by the user.
4. Open Bar 49 is installed/enabled with a light floating preset, awaiting new login. Verify extension state/errors and visual appearance. Blur My Shell remains disabled.
5. Kakao Enter-to-send is confirmed fixed by the user. Code-server setting is enabled live and its repository role now deploys workspace + repository settings; repository change is committed and uploaded. New dock styling and click-action=previews are applied live; their push requires final confirmation.
6. Update STATUS.json and regenerate hardware-report.html after checks. CPU/camera trial has not yet been promoted into default DTB/camera installer. All scripts/configs and source notes are in surface; ignored offline binaries must be copied too.

---
Historical notes (superseded where they conflict with the section above):

# Immediate post-recovery verification

- Verify Wi-Fi stays unblocked/connected with original ath12k A98E5140E078A5920DAC05E; test traffic bound to Wi-Fi, not tethering. Never reinstall rejected wifi-regulatory rebuild via setup.
- Verify original ov02c10 C8AE6F17BF899E4A937A808 after reboot; compare streaming/crop-selection errors. The fast-video module was in use and was NOT forcibly unloaded.
- Verify physical boot/login show the swirl only, without Debian13 text. No GDM restart was forced.
- A matching source fingerprint, ABI/signature checks and staged real-device functional checks are distinct requirements. Guest loading alone must not be called hardware validation or justify silently replacing a working boot/network driver. The original Wi-Fi source fingerprint mismatch was material and was not handled adequately.

Earlier notes below are historical and may be superseded by these recovery instructions.

# Continue investigation

When the user says "계속", read CURRENT.md and this file, inspect the current boot, then continue unfinished investigation. Do not repeat completed installations. Keep documentation, installer inputs, checksums and Git commits synchronized. Do not copy infrastructure credentials into this bundle.

## Pending hardware verification

0. Touchpad edge-palm correction survived reboot and the user reports much improved behavior. Investigate remaining jumps only if they are still reported; do not undo the confirmed improvement blindly.

1. Secure Boot and actual replacement USB/SoundWire srcversions are verified after the 2026-11-12 reboot. Next: a user-initiated deep cycle and sustained/interrupted speaker playback. Fresh power-only trace is armed; save it after the cycle. Do not force sleep during active work.
2. If audio fails, capture timestamped SoundWire/WSA884x errors before changing routes. The five installed SoundWire patches improve error/IRQ handling but are not proven to fix parity faults.
3. CPU: current online CPUs 0-8; CPU9 failed PSCI with -22. scmi-cpufreq now loads and provides policy0 only. Investigate X1P64100 SCMI sustained-frequency/turbo classification and the CPU DT topology without inventing firmware values. SCMI perf is builtin, so its source patch needs a proper matched kernel build.
4. Touchscreen: Romulus13 I2C 0x34 does not acknowledge; v2 GPIO38 overlay is active. Compare v1 reset GPIO31 evidence and exact hardware variant before further GPIO/power changes. Do not substitute 15-inch QSPI wiring.
5. Review the Romulus USB PHY reinit-on-resume series separately from the fixed NULL crash; missing initial xHCI probe must not be conflated with PHY state loss after resume.
6. Touchpad QSPI v3 RFC has controller/board prerequisites; compare it to existing downstream GPI/GENI/SPI-HID before replacing working input.
7. Camera quality, battery/runtime and Bluetooth startup remain separate checks; retain previous rejected camera/overshoot trials as history rather than reapplying them.

## User decisions

- Scroll injection was declined; do not install it.
- Samsung integration is deferred; describe capabilities only.
- Android apps should appear individually in GNOME, not as a full Android desktop.
- hardware-report.html is now tracked by the latest user instruction.
- Kopia Console changes belong to repository only; do not deploy them on the current Surface.

## Infrastructure follow-up (outside this bundle)

Console Caddy/code-server roles were applied successfully. The old operational SSH certificate was renewed with the old CA for one year, preserving key and principals. Both old and renewed certificates were rejected in the VMM login test; investigate server trust/principals when authorized. Never replace the operational certificate with the new repository CA before server redeployment.

## Installation and program follow-up

- Modular setup is implemented. Use --plan before installation and --verify-only to check payloads. Do not run a full live reinstall merely to validate refactoring. Console UID/GID and infrastructure services belong to repository, not this hardware installer.
- Steam runtime/FEX root and games are not fully bundled. Existing Steam helpers are reproducible, not a complete offline Steam installation. Game-only click and Korean rendering verification are paused by user request.
- KakaoTalk ARM64 is installed and official-signer verified. Secondary Device login screen has been verified; account login remains the user’s action. Android core components are retained.
- The next manual deep sleep was captured and saved under drivers/files/sleep/diagnostics/2026-11-12-090205/. SPI-HID ~2.417s and PCIe/Wi-Fi ~2.219s dominate resume. Re-arm only if another comparison is needed. No automatic forced sleep.

## Resume in this same conversation

The user will type "계속" in this session. Read this file and CURRENT.md, check the latest Git commits and current boot, then resume unresolved hardware investigations. At the 5% limit notification, new investigation was stopped; documentation, verification and commits were completed/recorded separately. Kopia was not deployed.

## Latest desktop/program verification

- Next physical boot/offline update: verify minimal Debian wordmark and readable update text. The rebuilt initramfs contains the exact custom watermark, static/fallback fonts and GPU firmware; signed-image verification passed.
- Confirm KakaoTalk login autostart and real incoming messages after closing its window. Background Android is explicitly enabled by user choice; this trades power/RAM for availability. Keep physical host sleep unchanged.
- Android keyboard popup is suppressed with a physical keyboard; Android light mode is selected. No Discord/other personal apps were installed.
- Preserve 120Hz. Panel VRR range alone is insufficient: current MSM connector has no vrr_capable property.
- Wi-Fi PS is now on; monitor reconnection and test battery discharge with matched brightness/120Hz/apps. Old 0.575W sleep and 7.64W awake figures are pre-change baselines. Governor was restored because charging invalidated comparison.

## Latest follow-up (2026-11-12)

- CPU left unchanged after the comparison; see drivers/files/power/CPU-AND-DRIVER-CHECK.md. Driver APST/ASPM/USB power saving already enabled. CPU9 topology remains unresolved; do not guess DTB addresses.
- Nextcloud actual DAV export incomplete; HTTPS and approved infra SSH timed out. Retry only after access returns; verify/revoke the temporary browser-login app password. Tools remain repository/tools/*.tmp.
- PET repaired locally and in the repository role; existing commits amended, no corrective commit added. Reload the editor window if needed.
- Kakao notification body unresolved; see programs/kakaotalk/NOTIFICATIONS.md.

## Notification follow-up

Real incoming-message evidence confirmed an empty quiet_new_message companion plus a correctly forwarded message notification. The narrow host filter is installed and the Waydroid session restarted. Await a new real message to verify the display; see programs/kakaotalk/NOTIFICATIONS.md. No chat content retained. Driver follow-up: drivers/files/power/DRIVER-FOLLOWUP.md.

## Display recovery complete

User confirmed normal graphics after reboot with complete GPU firmware. KakaoTalk autostart restored; earlier temporary-autostart-disable instructions are superseded. New incoming-message notification verification remains pending.

## Next comparison after verified deep return

One post-repair deep cycle succeeded. Save the newly armed trace after the next manual cycle; do not re-arm before saving. Track Wi-Fi regulatory completion/L2 timeout, ~11.4s authentication-start delay, and the post-resume WSA parity warning. User currently reports working speakers; do not reset audio blindly. Camera stays ~18.8fps; CPU9 and touchscreen remain open. See drivers/files/sleep/diagnostics/2026-11-12-post-reboot-review.md.

## Next boot: staged regulatory/camera fixes

Expect ath12k srcversion D61DA424018CF1563587D2E; verify ov02c10 srcversion against installed payload and fast_video=Y. Both modules are signed and embedded in initramfs with the complete GPU firmware. Measure real camera FPS and brightness/flicker; compare deep and Wi-Fi timing. Boot tracing is now enabled. Fn non-toggling media-default/fixed LED, CPU9 and touchscreen remain unresolved (GPIO31 trial did not bind). No extra SoundWire change: the loaded backport already disables/waits for its IRQ before clock gating, so adding another synchronize_irq would be redundant. Current good speaker routing is preserved.
