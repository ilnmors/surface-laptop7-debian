# Next (after the 2026-11-13 maintenance pass)

1. On the trial boot: `sudo journalctl -k -b | grep -iE 'spi_hid|gtch'`, `libinput list-devices | grep -i touch`, touch the screen; check `grep Cma /proc/meminfo` (expect ~512 MB) and `cam -c 1 --capture=90 --stream=role=viewfinder,width=1920,height=1080`.
2. Touch works → promote the overlay into the PCIe3-off DTB pipeline and kernel/setup.sh, run surface-secureboot-update. Fails → run spi-gtch/restore.sh as root.
3. Camera noise: choose 37.5 fps (current) or 18.8 fps (fast_video=N, less noise in dim light).
4. Fn lock: needs a user-space daemon that tracks the keyboard lock report (ID 0x5b) and inverts the top-row mapping; requires interactive key calibration.

# Earlier next

- spi-hid v2 verified (resume 1.41 s). Remaining: multi-hour sleep-drain measurement for a precise W figure, camera noise/1080p (deferred), touchscreen (open), Fn lock (open), Kakao notification body (pending).

# Done: verify spi-hid v2 and measure sleep drain

1. After reboot: spi_hid srcversion 0923360D0DE94E631C945EE, touchpad works, Kakao window does NOT open but com.kakao.talk + MessengerService run (pkexec waydroid shell), Secure Boot, CPU 0-9, no pcie3.
2. Lid cycle: spi_hid callback ≈ 0, kernel resume ≈ 1.2 s, touchpad back ≈ 2.3 s.
3. Sleep drain: record energy_now before closing the lid, keep it closed ≥ 30 min on battery, compare on wake (Wi-Fi off/on not changed).
4. Failure: GRUB "Surface previous working image" (v1), then pkexec bash drivers/files/touchpad/spi-hid-resume/restore.sh.
Old boot images were already deleted (step 4 of the v1 checklist below is done).

# Earlier: spi-hid/PCIe3 trial verified (21:22)

Done: steps 1-2 below (resume 1.62 s). Pending: discharge measurement on battery with matched brightness/apps; user confirmation, then step 4 deletion of old boot images.


1. After reboot: cmdline default image; CPU 0-9; Secure Boot; spi_hid srcversion F78320E76D9CB9AFF42A4E8; no pcie 1bd0000 device; Wi-Fi HTTPS; touchpad works after boot.
2. Manual lid cycle: touchpad works ~2 s after wake; resume phases (expect dpm_resume ≈ 0.1 s, noirq ≈ 0.6 s); Wi-Fi reconnect; audio. Save the armed trace (pkexec).
3. If it fails: GRUB → "Surface previous working image", then pkexec bash drivers/files/touchpad/spi-hid-resume/restore.sh.
4. Once the new image is confirmed good: DELETE the old boot images (user decision): /boot/secureboot/rollback-20261112 ("previous working image"), rollback-20261112-pre-cpu, previous/ and trial-cpu-camera/, and drop the GRUB rollback entry from surface-secureboot-update. Then switch kernel/setup.sh to drivers/files/pcie/surface-sl7-xplus-pcie3-off.dtb and the spi-hid patch into the offline installer.

# Earlier (after 19:25 default-boot verification)

- Default-boot verification is complete; see CURRENT.md. Deep cycle verified 19:27 (see sleep/diagnostics/2026-11-12-192713). Candidate resume fixes: move spi_hid fixed msleep(2000) out of the system resume callback (rebuild/sign spi-hid.ko, keep rollback); investigate empty PCIe 1bd0000 before any DT disable. Remaining: battery discharge with matched conditions, camera noise/1080p (deferred), touchscreen (open), Fn lock (open), Kakao notification body (pending).

Previous checklist (completed):

- User authorized promotion after the one-shot CPU/camera boot succeeded. Verify /proc/cmdline uses /secureboot/vmlinuz-surface-signed.efi (not trial-cpu-camera), CPU online 0-9, three ondemand policies, Secure Boot, camera 37.5fps and Wi-Fi HTTPS.
- Open Bar is ACTIVE after login. Bottom dock is a fixed full-width Windows 11-style taskbar (touch cannot reveal an auto-hidden dock); click-action=previews.
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
