# Current state — reviewed 2026-11-13

## Observed in the running system

- Booted at 08:56 through `/secureboot/trial-touch/vmlinuz-surface-signed.efi` with `cma=512M`. The 512 MiB reservation failed; `/proc/meminfo` reports CmaTotal=0. The current boot is not proof that the new default command line has been used.
- CPU online 0-9, Secure Boot enabled, spi-hid v2 srcversion 0923360D0DE94E631C945EE. The physical 045E:0C6E touchscreen and IPTSD virtual touchscreen/stylus exist.
- The saved default image uses the promoted GTCH SPI DTB, PCIe3-off and explicit `cma=0`; a previous working image remains in GRUB. Reboot into the default image is a remaining check, not required for this read-only handoff review.

## Claude changes reviewed

- Touchscreen: GTCH SPI panel trial succeeded and was promoted to the default/offline DTB pipeline.
- Resume: spi-hid defers hardware restart; recorded kernel resume 4.76 → 1.41 s. Touchpad readiness still occurs about 2.3 s after wake; Wi-Fi about 2.1 s. These are different measurements.
- Camera: no-CMA/system-heap path, dma-heap udev access and user black-level tuning support GNOME/PipeWire. Recorded 720p/1080p 37.5fps; user reported better color. Low-light grain remains; the rejected sensor-helper IPA is still not a production fix.
- Desktop: full-width always-visible taskbar with window previews, Open Bar, Symbola fallback. Boot-screen appearance confirmed in the handoff record. Native Fn toggle retained by user choice; experimental normalizer removed.
- KakaoTalk: background-only login launch and notifications recorded as working. Steam game checks and Samsung integration remain held.
- Repository: reviewed OxiCloud binding/OIDC provisioning, retired-stack archive, release pins, Authelia-only application login settings, Sure UI-based LLM configuration and `.agent-workspace` rename. This is local change review, not validation of a fresh server deployment.

## Ownership and validation

- Workspace generation/editing/checks run as console. Root-owned entries in repository (47) were returned to console:svadmins; Surface already had console ownership. System-installed files retain required root ownership.
- `console` ran the installer plan and offline checksum verification. Raw upstream data/offline payloads remain local as before.
- No push or reboot was performed by this handoff review. Future pushes require final user confirmation; local AGENT.md files carry the workflow and ownership rule.

## Desktop refresh (2026-11-13)

Use one continuous opaque Mainland top bar: 34px high, zero outer margin/radius/border, 100% background opacity. Trilands was removed after the user reported the transparent gaps between white component groups. Keep CPU/RAM on the left, clock in the center and notification/input/system controls on the right. The alpine photo and teal GTK3/GTK4 app theme remain; Shell stays Fluent-Light. Settings were refreshed live; appearance awaits user confirmation. The wallpaper, app theme and panel settings are documented separately in `desktop/files/topbar/ALPINE-THEME.md`.

## Waydroid downloads

Waydroid setup creates `<XDG Downloads>/waydroid` after Android boot readiness, using the shared SH/Python helper in `programs/waydroid/download-link.*`. It grants narrowly scoped ACL access with the current desktop UID while preserving Android owners. The ACL package is bundled for offline installation. Existing correct setup is idempotent; `--check` is read-only. The current `~/Downloads/waydroid` link and inherited ACLs passed live verification.

## Audio investigation (2026-11-13)

User confirmed sound returned after an unexpected host reboot following the live ADSP recovery attempt. Initial SoundWire clashes were missed in the first log search; codec/card rebinds then added DSP timeouts, runtime-PM and parity errors without restoring sound. Soft-mixer trial failed and was removed. No permanent fix or exact reboot mechanism is established. Preserve working audio; do not repeat live hardware resets automatically. See [incident record](drivers/files/audio/diagnostics/2026-11-13/README.md) and saved journals for chronology and evidence. These findings supersede the earlier error-free-kernel and pending-trial claims.

Audio follow-up: a new SoundWire clash occurred at 23:56:21 without further resets. Recovery was temporary. Stabilization candidates and applicability limits are in [STABILIZATION.md](drivers/files/audio/diagnostics/2026-11-13/STABILIZATION.md); none is installed.

2026-11-14 cause investigation: original driver already enables 3-second autosuspend. A user-approved 90-second controller-on trial was reported normal; auto was restored, with later user-reported silence/recovery. Runtime controller power transition is the leading hypothesis, not a confirmed unique code defect. All private traces were removed; no permanent mitigation installed. See [cause assessment](drivers/files/audio/diagnostics/2026-11-14/README.md).

2026-11-14 external-case review: the closest X1 SoundWire IRQ/clock-stop fix is already present in the archived base source. Older X13s stability fixes support the failure class; Surface Pro 11 gain/routing changes are not a verified cure for this machine. Proposed next step is a longer controller-only runtime-PM comparison with power measurement, followed by a signed boot-time stock/custom module comparison only if necessary. Research did not change the live system. See [cases and proposal](drivers/files/audio/diagnostics/2026-11-14/CASES-AND-PROPOSAL.md).

2026-11-14 user decision: audio investigation is held until recurrence. Preserve current settings. A finite read-only capture helper and [resume procedure](drivers/files/audio/RESUME.md) are ready; no monitor or automatic recovery was installed.

2026-11-14 23:01 recurrence: investigation resumed read-only after the user reported silence. At 23:07 the user reconfirmed advancing playback with no sound; Firefox/Speaker links and PCM were running, pointers advanced, and digital speaker-monitor samples were nonzero. Controller/codecs stayed active without suspended-time growth. No new matching kernel errors occurred near this capture; two earlier same-boot clashes are not synchronized proof of this event. No live mitigation or recovery was applied. See [recurrence evidence](drivers/files/audio/diagnostics/2026-11-14/RECURRENCE-2301.md).

2026-11-14 23:21 active recovery: normal service/socket shutdown reached closed PCM and suspended devices, but restart and HiFi profile reapplication both failed to restore audible sound. Installed exact-speaker no-idle policy (timeout 0) as a mitigation under evaluation. Normal reboot is being prepared and announced, not yet recorded as completed. No module/firmware change or live hardware reset. See [recovery and rollback](drivers/files/audio/diagnostics/2026-11-14/RECOVERY.md).

2026-11-14 23:28 reboot comparison: scheduled shutdown was orderly; user confirms sound after boot ad5da1de-571e-4655-9cd2-259a4ef0dab5. Same signed kernel/module and identical selected hardware mixer controls. A separate WCD-bus clash at 23:20:42 coincided with profile-off; no current-boot clash in the 23:27 query. Preserve working output and evaluate the idle policy through normal use. See [post-reboot evidence](drivers/files/audio/diagnostics/2026-11-14/POST-REBOOT.md).

2026-11-15 physical click-drag: installed the narrow 045E:0C77 BTN_LEFT/debounce-cache fix at 08:29:44 KST. The user confirms one-finger physical dragging and held-click/second-finger motion are both normal. Original code fails 7 regression checks; the patched header passes all 13. Live executable matches the offline payload, service restarts=0; calibration and GNOME settings unchanged. See [click-drag and rollback](drivers/files/touchpad/click-drag/README.md).
