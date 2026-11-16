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

## 2026-11-16 USB and overnight power follow-up

- USB tethering remains unresolved: Samsung mode reconfiguration failed to produce a network interface; another port enumerated then disconnected. RNDIS/NCM load under Secure Boot succeeded. The 45-second root-hub-on test did not restore detection and both hubs are back on auto. User confirmed the same cable/phone work on another PC. Targeted xHCI and UCSI child re-registration completed without detecting the phone; awaiting the requested physical reconnect. If still failing, the documented Microsoft shutdown/20-second power-button procedure is the next physical step; do not silently power off.
- Overnight deep drain: 43→15% in 16h 27m (~0.88 W / 1.70 pp/h). Do not attribute this to the phone connected only after wake.
- The passive sleep hook now writes `/var/lib/surface-power/suspend.jsonl`. After the next natural sleep, compare same-boot pre/post battery energy and raw Qualcomm counters. A manual sample succeeded; real sleep-boundary execution is untested. Do not force sleep, reset audio or hot-unbind USB for this check.
- USB PHY system-sleep clock gating is a researched candidate, not an applied fix. See `drivers/files/power/2026-11-16-USB-SUSPEND.md` for evidence, limits and hook rollback.
- These follow-up changes are local/uncommitted. Obtain fresh commit/push approval.

Latest steering (2026-11-16): phone charging and MTP enumeration work after reconnect, but tethering remains unavailable. User declined phone debugging and stopped USB work. Focus only on fixing deep-sleep battery drain; Qualcomm PHY system-sleep patch review/build is in progress.

2026-11-16 13:53: the signed USB PHY system-sleep trial is installed for the next boot (current boot still runs the original modules). After reboot, verify srcversions and USB, then compare a natural ≥2 h battery sleep in `/var/lib/surface-power/suspend.jsonl` against 0.77–0.88 W. Rollback: boot menu 'Surface before PHY sleep patch (2026-11-16)' or `setup.py --restore`. See [phy-sleep README](patches/files/phy-sleep/README.md). `clk_ignore_unused`/`pd_ignore_unused` removal remains a separate single-variable candidate, not attempted.

## 2026-11-16 USB tethering — resolved, port fault remains

Cause: a stale pending USB tethering request inside the phone rejected new requests (error 18); a phone restart fixed it and RNDIS tethering works. Phone developer options and debugging are disabled again. Remaining Surface issue: after abrupt USB data loss the USB-C USB2 path stays dead until the dwc3-qcom controller is rebound. See [tethering report](drivers/files/usb/2026-11-16-TETHERING.md).
- WireGuard `wg0` MTU is fixed at 1360 (largest value that passes over phone tethering; 1420 stalled SSH/TLS). Connection setting plus `dispatcher.d/90-surface-wg-mtu`.
