# Remaining work — 2026-11-13 reviewed handoff

## Physical click-and-drag — resolved (2026-11-15)

[click-drag/README.md](drivers/files/touchpad/click-drag/README.md): the exact-device BTN_LEFT/cache correction is installed and the user confirms both one-finger physical dragging and held-click/second-finger motion are normal. Same source preserves edge tracking; GNOME settings and calibration are unchanged. Regression checks: original 7 failures, patched 13 passes. Offline SH/Python build/test/setup and local rollback are recorded. No additional touchpad changes are pending unless the issue recurs.

## Audio — recovered after scheduled reboot (2026-11-14 23:24)

Read [POST-REBOOT.md](drivers/files/audio/diagnostics/2026-11-14/POST-REBOOT.md). User confirms sound; same kernel/module, identical selected hardware mixers. Keep the exact-speaker idle timeout 0 and observe normal pause/restart behavior; stability and power cost remain unmeasured. Profile off/on coincided with a new separate WCD-bus clash, so do not repeat it as automatic recovery. Do not hot-unbind drivers or restart ADSP. RTKit absence is a separate scheduling finding, not a demonstrated cause of persistent silence.

## Other remaining work

1. At the next authorized reboot, verify the promoted **default** `/secureboot/vmlinuz-surface-signed.efi` and `cma=0`, CPU 0-9, Secure Boot, GTCH touchscreen, GNOME/PipeWire camera, Wi-Fi and audio. Current live command line is still the earlier trial-touch/cma=512M boot.
2. Camera low-light noise remains. Keep production black-level tuning; do not reinstall the rejected gain-helper/color experiments blindly. Additional denoise work remains deferred.
3. Long sleep/drain comparison: use direct energy telemetry over several hours with matched brightness/120Hz/background apps. The short 43-minute 1-percentage-point result is an approximate 0.7 W estimate, not a rigorous upper bound or a Windows comparison.
4. Retain spi-hid v2, PCIe3-off, GTCH overlay, 120Hz, default CPU governor/range, full-width taskbar and native Fn toggle. No Fn daemon calibration is pending.
5. Steam/RimWorld game verification and Samsung integration remain held by user choice. Do not restart those tasks during routine maintenance.
6. The previous OxiCloud migration is recorded complete. Local account/client details and credentials stay outside the Surface bundle.
7. Generate/edit/test workspace files as console; escalate only system installation steps. Keep workspace files console:svadmins. Update STATUS.json, HTML and manifests when making changes.
8. Review local changes before committing; obtain final user approval before every push. Do not assume old pending-state lists in Git history describe the current system.

Prior experiments and chronological evidence remain in component READMEs, diagnostics and Git history.
