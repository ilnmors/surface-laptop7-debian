# Remaining work — 2026-11-13 reviewed handoff

## Physical click-and-drag — resolved (2026-11-15)

[click-drag/README.md](drivers/files/touchpad/click-drag/README.md): the exact-device BTN_LEFT/cache correction is installed and the user confirms both one-finger physical dragging and held-click/second-finger motion are normal. Same source preserves edge tracking; GNOME settings and calibration are unchanged. Regression checks: original 7 failures, patched 13 passes. Offline SH/Python build/test/setup and local rollback are recorded. No additional touchpad changes are pending unless the issue recurs.

## Audio — recovered after scheduled reboot (2026-11-14 23:24)

Read [POST-REBOOT.md](drivers/files/audio/diagnostics/2026-11-14/POST-REBOOT.md). User confirms sound; same kernel/module, identical selected hardware mixers. Keep the exact-speaker idle timeout 0 and observe normal pause/restart behavior; stability and power cost remain unmeasured. Profile off/on coincided with a new separate WCD-bus clash, so do not repeat it as automatic recovery. Do not hot-unbind drivers or restart ADSP. RTKit absence is a separate scheduling finding, not a demonstrated cause of persistent silence.

## Other remaining work

1. Verified after the 2026-11-19 15:00 reboot (user-initiated): default `/secureboot/vmlinuz-surface-signed.efi`, `cma=0`, CPUs 0-9 (ondemand), Secure Boot enabled, GTCH touchscreen (`spi 045E:0C6E Touchscreen`), libcamera front camera, Wi-Fi + wg0, speaker/headphone sinks. Same boot: `xhci-hcd.1.auto` (a400000) failed again with `-110` after an 18.9 s kernel phase, so the boot-trials softdep (not installed) remains the next USB step.
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

## 2026-11-19 20:55 DTB trial armed (one boot)

`drivers/files/boot-trials/install-dtb-trial.sh` built `/boot/secureboot/trial-dtb` (camera privacy LED + iris) and set the one-shot flag. The next boot uses it once, then the default image returns. After that boot run `bash drivers/files/boot-trials/check-dtb-trial.sh`, record LED/iris results and power if iris decodes, then `pkexec bash drivers/files/boot-trials/restore-dtb-trial.sh` (or promote the DTB if both work). The a400000 softdep trial comes after, as a separate variable.

### 2026-11-19 21:00 first trial boot results, second trial armed

- iris: the trial DTB bound qcom-iris (/dev/video0 decoder, /dev/video1 encoder). The generic linux-firmware `qcom/vpu/vpu30_p4.mbn` is rejected (-22, TZ signature); so is `qcvss8380_pa.mbn`. `qcvss8380.mbn` from the archived Windows package (`SurfaceUpdate/qcdx8380/`, extracted with msitools) loads through a temporary `firmware_class.path`; the decoder lists H264, HEVC, VP90, AV01.
- Camera LED: the LED hardware works (user saw it lit from sysfs), but V4L2 never claimed it. This kernel's videodev looks the LED up as `privacy`, not `privacy-led`.
- Second trial DTB (armed for one boot): `led-names = "privacy"` and iris `firmware-name = "qcom/x1e80100/microsoft/qcvss8380.mbn"`, with that firmware installed in /lib/firmware/qcom/x1e80100/microsoft/. After the boot run check-dtb-trial.sh; if both work, promote the DTB (drivers/files/touchscreen/spi-gtch/prepare.sh path) and regenerate the signed default image.

### 2026-11-19 21:20 second trial passed, promoted

Second trial boot: the camera LED follows streaming (on while `cam` streams, off after; sysfs writes refused because V4L2 claims it) and iris opens with the device firmware via `firmware-name` (decoder /dev/video2, encoder /dev/video4: H264, HEVC, VP9, AV1). `drivers/files/touchscreen/spi-gtch/prepare.sh` now adds both changes (rebuilt DTB identical to the trial DTB); `drivers/files/boot-trials/promote-dtb.sh` installed it with the firmware, re-signed the default image (embedded DTB verified) and kept the GRUB menu plus the rollback entry "Surface before iris and camera LED DTB (2026-11-19)". Effective from the next boot. Still open: playback power with hardware decoding (mpv `--hwdec=v4l2m2m-copy` or GStreamer v4l2 decoders; Firefox does not use V4L2 stateful decoders).

### 2026-11-19 22:00 waiting for the user's cold boot

- a400000 softdep installed (`drivers/files/boot-trials/install-a400000-trial.sh`; GRUB rollback "Surface before a400000 softdep (2026-11-19)"; undo with `restore-a400000-trial.sh`). First boot after this is the user's cold boot. Check `xhci-hcd.1.auto` (-110 or bound), `systemd-analyze` kernel time, and record per boot (cold/warm) before judging.
- The same boot first uses the promoted iris + camera LED DTB from the default image: confirm the LED follows `cam` and `/dev/video*` lists Iris Decoder/Encoder without any temporary firmware path.
- Hardware decoding (1080p H.264, GStreamer): CPU 86% -> 28% of one core; battery 8.22 W (openh264) vs 5.18 W (v4l2h264dec), gauge updates slowly, so re-measure over several minutes with energy_now deltas.

### 2026-11-19 21:55 cold boot 1 after the a400000 softdep

Default signed image; kernel 6.9 s + userspace 9.6 s. `xhci-hcd.1.auto` bound (no -110), six USB root hubs. Promoted DTB confirmed from the default image: Iris Decoder/Encoder (/dev/video3, /dev/video4) without a firmware path override, camera LED on while `cam` streams and off after. a400000 log so far: cold 1 = OK. Keep logging each boot (cold/warm, kernel time) until the failure has had several chances to recur.

### 2026-11-19 22:20 hardware decoding power (battery, 3 min windows, power_now mean every 5 s)

1080p H.264 Big Buck Bunny at real-time speed through GStreamer: idle 3.88 W, openh264dec 6.75 W, v4l2h264dec (iris) 2.50 W. energy_now updates in large steps and is unusable over 3 minutes; power_now changed every 5 s. Software decoding costs about +3 W over idle; iris decoding stays at idle level. Players still need V4L2 decode support (GStreamer/mpv); Firefox keeps software decoding.

### 2026-11-20 09:05 overnight deep sleep with the promoted DTB and the a400000 softdep

One s2idle/deep suspend, 22:14 -> 09:02 KST (10 h 48 min), success 1 / fail 0. Battery 37.58 -> 31.92 Wh: 5.66 Wh, **0.52 W average** (about 1.0 %/h), down from 0.77-0.88 W on 11/16. The deepest states still never entered (qcom_stats cxsd/aosd/ddr count 0), and the ADSP subsystem counter rose by about 4.1 million during the sleep: both are the next sleep-power leads.

### 2026-11-20 09:30 PHY AON clamp fix installed, sync_state trial armed

- `patches/files/phy-sleep/patches/03-qmp-combo-x1e80100-pcs-aon-offsets.patch` (qualcomm-linux PR #1357, lore 20261030105515.1948430-1-tapas.rana@oss.qualcomm.com): x1e80100_usb3dpphy_cfg used offsets without `usb3_pcs_aon`, so autonomous mode wrote the AON clamp into PCS_MISC. Built on top of 01/02 (only the AON line differs from v5); `install-aon-clamp.sh` installed the signed combo module (srcversion 0A74E69E94C0DD14BD50B53; usb module unchanged 601E8F5D...), refreshed initramfs and image, rollback "Surface before PHY AON clamp fix (2026-11-20)".
- One-shot `fw_devlink.sync_state=timeout` trial armed (`surface_trial_next=1`). After that boot: check `/proc/cmdline`, USB-A/USB-C, charging; then ONE attended `systemctl suspend` with the lid open (power button to wake), `pm_debug_messages=1`; record `/sys/power/pm_wakeup_irq`, PDC 17/47 interrupt counts and cxsd/aosd/ddr counts. If it still storms, do not close the lid; reboot to the default entry.

### 2026-11-20 09:45 sync_state trial with the AON clamp fix: storm unchanged; trial A armed

- Attended lid-open suspend on the sync_state boot (AON clamp fix active): wake IRQ 188 (a600000 ss_phy_irq) 82,847 times, 193 (a800000) 26,542; cxsd/aosd/ddr stayed 0; "Wakeup pending. Abort". a400000 again -110 on the sync_state boot (deferred-probe timing). The clamp fix is kept but is not the cause.
- Code reading: dwc3-qcom arms ss_phy_irq unconditionally (level-high from DT); qmp-combo enables autonomous mode with ARCVR_DTCT_EN | ALFPS_DTCT_EN in host SS mode. Both combo PHYs are initialized (runtime active, usage 2), so autonomous mode is armed on idle ports.
- One variable at a time. Trial A (installed, `trials/04-trial-no-alfps-detect.patch`, srcversion 10CECE68674D50A8CFDCE15): receiver detection only (no ALFPS_DTCT_EN). Rollback entry "Surface before ALFPS-off trial (2026-11-20)". sync_state one-shot armed. After the reboot: one attended lid-open suspend; if the storm stops, write the real fix (ALFPS only while an SS device is attached); either way reinstall the AON-clamp-only module (`files/aon-clamp/`) with install-combo-module.sh until then.

### 2026-11-20 09:50 trial A rejected; trial 2 prepared

- Trial A (receiver detection only): storm unchanged (ss_phy_irq 75,779 a600000 / 20,212 a800000, cxsd 0, abort). LFPS detection is not the cause. a400000 bound on that sync_state boot.
- Trial 2 (installed, `trials/05-trial-no-autonomous-detect.patch`, srcversion 5683C0DA8CF5F181A714386): autonomous detection mask 0. Storm persists -> the line is high regardless of the detectors (clear/clamp order, PHY power-down or the DT trigger polarity). Storm stops -> receiver detection misbehaves. The first install failed: /boot (2 GB) was full of per-trial rollback copies; the reboot was cancelled 5 s before it fired (a pipeline hid the failure). Cleanup kept the default image, rollback-20261112 and rollback-aon-clamp-20261120 (last verified good), freed about 1 GB, removed four stale menu entries and the empty initrd.img.new, and disarmed the flag. install-combo-module.sh now refuses to start under 600 MB free and trials reuse one rollback-trial copy.

### 2026-11-20 09:53 trial 2: the storm is gone — autonomous receiver detection is the cause

Trial 2 (no autonomous detection) on the sync_state boot: ss_phy_irq 0 / 0, suspend success (deep, 32 s, woken by IRQ 232), DDR count 0 -> 626, cxsd/aosd still 0. With trial A (receiver detection only) the storm stayed, so `ARCVR_DTCT_EN` on an idle port is what keeps ss_phy_irq high. Real fix: arm receiver/LFPS detection (or the ss_phy_irq wake) only on ports with an attached SuperSpeed device; new connections still wake through the USB2 DP/DM lines. Next blocker: CXSD/AOSD still never entered.

### 2026-11-20 10:05 fix under test: dwc3-qcom arms ss_phy_irq only with a SuperSpeed device attached

`patches/files/dwc3-ss-wake/01-dwc3-qcom-ss-wake-only-with-ss-device.patch` on top of the installed null-HCD build (base rebuild matches the installed 8554A2970EC29806E65733C): reads the USB3 root hub (shared_hcd) at suspend and arms ss_phy_irq only on ports with a SuperSpeed device; empty ports keep the DP/DM wake lines. Installed with `dwc3-ss-wake/install.sh` (dwc3-qcom 373A6F05E3EFE6B7721A44D) together with the AON-clamp PHY module (normal autonomous detection back, 0A74E69E94C0DD14BD50B53); rollback-trial holds the trial-2 image. sync_state one-shot armed. Tests after the reboot: lid-open suspend with no USB device, then with the phone attached (it enumerates at 480M only, so no SuperSpeed device is available for the attached-port case).

## 2026-11-20 afternoon (default boot 14:22, no sync_state)

- SSAM: the 10:03 sync_state boot lost EC transmit (requests and suspend prepare/D0 notifications timed out, -110,
  7 of 8 suspends failed). After the 14:22 default reboot EC requests work (fan read; TX 355 -> 383). The first logger
  version's `STALL` marks were false positives (RX grows from EC events by itself); it now logs kernel SSAM -110 as
  `FAULT` (drivers/files/diagnostics/). Open question: does sync_state=timeout cause the transmit loss? Three earlier
  sync_state boots had no -110 but only 1-2 suspends each.
- Attended suspend 14:26-14:28 on the default boot, nothing attached: success, no SSAM error, EC and Wi-Fi fine after
  resume. APSS slept (count +1, ~90 s); DDR, CXSD, AOSD 0, as expected without sync_state (DDR entered only on the
  sync_state boot, trial 2). ADSP counted +10,383 entries in ~90 s (~110/s): the audio DSP keeps waking during sleep.
- Shift+Hangul now toggles ibus-hangul (switch-keys `Hangul,Shift+Hangul`; user value, system dconf and bundle default).
- Waydroid: ReteKey (F-Droid 0.2.3) installed and set as the input method; the PHYSICAL_KEYBOARD notification channel
  is off (importance 0, verified after a session restart). The user still assigns the KO/EN key in ReteKey.

## 2026-11-20 evening: CXSD investigation closed (sync_state trial boot 18:01)

Three attended suspends on the sync_state boot, all successful, no SSAM -110, EC fine after resume, ss_phy_irq 0.
DDR power collapse works (265 s of 279 s, 2,915 entries); CXSD/AOSD stay 0. Ruled out as the CXSD blocker:
- USB and PCIe system wakeup: disabling it on a400000/a600000/a800000 and both root ports changed nothing.
- PCIe links: both controllers retrain on every resume, so dw_pcie_suspend_noirq took the D3cold path and
  qcom_pcie_suspend_noirq released clocks, bandwidth and the OPP vote (upstream v7.3 code read). Wi-Fi logs
  "Timeout waiting for L2 entry" but the link still goes down.
- Speaker SoundWire hold: ADSP ~105 sleep entries/s with the controller held on or suspended.
- Linux RPMh votes (rpmh_send_msg trace across one suspend, resolved via cmd-db): apps_rsc left cx.lvl, mx.lvl and
  mmcx.lvl at level 0 before suspend; the sleep set zeroes every BCM (MC0, SH0, SH1, SN0, CN0, QUP0-2, ACV).
- Linux <-> DSP traffic is ~1 IPCC/GLINK interrupt per second.
Remaining blocker is outside the Linux apps votes: another subsystem's RSC (the ADSP wakes ~100 times a second on its
own timer) or AOP policy. Seeing it needs firmware-side visibility that Linux does not provide, so the work stops here
by decision (2026-11-20). Default boot keeps sync_state off: DDR collapse needs it, but the 10:03 sync_state boot lost
EC transmit (cause unknown; three later sync_state suspends were clean). The SSAM logger keeps watching for -110.

## 2026-11-21 state for the next session

- The repository is public as `surface-laptop7-debian` (GPL-2.0-only). Personal values (printer, mail hosts, VPN name) live only in the untracked `local/`; keep it that way and run a privacy check before every push.
- Boot: sync_state trial boots are kept by `boot-trials/sync-state-keep` while each boot is free of SSAM -110 and xhci -110.
- Applied: `logind.conf.d/50-surface-lock-before-sleep.conf` (`InhibitDelayMaxSec=15`). A lid opened while a slow gnome-shell was still locking had left the display off for ~20 s after resume; a normal close/open locks in 1 s and lights the display 0.5 s after resume.
- Firefox V4L2 hardware decoding was tried with rpi-ffmpeg 8.1.2 (DRM PRIME output, AV1 V4L2 decoder): Iris opened, no picture. Rolled back; only Debian FFmpeg remains.
- Pending, attended:
  1. Overnight lid-closed sleep on battery on a sync_state boot; compare with 0.52 W (default boot, 2026-11-19/20). Check that no session inhibitor (e.g. a stuck Nautilus transfer) is active first.
  2. Suspend with a USB device attached on USB-A and on USB-C: does a D+ (dp_hs_phy) line wake it within ~40 s (as reported on the 15-inch model, omarchy #18970)?
  3. USB-C monitor attached across suspend/resume, and the HPD delay (port 1: 39 s).
- Offered to the community: test omarchy-dragon-sl7 patch 0124 (geni UART keeps the engine clocked in suspend; aimed at SSAM -110 after back-to-back suspends). Needs a module build and an approved reboot.
## 2026-11-22 failed resume overnight and back-to-back test

- 2026-11-21 22:03 lid-closed suspend (sync_state boot). 03:18:45 the machine woke with the lid still closed (no
  "Lid opened"; wake source unknown, pm_debug_messages was off), logind re-suspended 27 s later at 03:19:12, and the
  log ends after "Filesystems sync". No SSAM -110 logged, nothing in pstore; the next boot was the user's at 12:08.
  Both wakes that night logged `ttyHS0: Unable to drain transmitter` (the SSAM UART).
- Attended reproduction 12:45-12:49 (lid open, pm_debug_messages=1): three suspends 25 s apart, each woken by the
  power button (wake IRQ pmic_pwrkey every time). All three resumed; no SSAM -110, no UART drain warning,
  dp_hs_phy_1 0. Not reproduced. Untested differences: lid closed, hours-long sleep, the unknown self-wake source.
- `pm_debug_messages` is now on at every boot (`rootfs/etc/tmpfiles.d/50-surface-pm-debug.conf`, installed). When a
  self-wake or hang recurs, follow the checks in [drivers/files/sleep/README.md](drivers/files/sleep/README.md).

## External commitments (open until the result is posted)

Record of every post: [docs/EXTERNAL-CONTRIBUTIONS.md](docs/EXTERNAL-CONTRIBUTIONS.md). Rules for external posts are in AGENT.md ("External contributions"): user approval of the final text, a one-line AI-use and verification note, point-by-point review answers.

| Where | Promise | State |
| --- | --- | --- |
| qBitnaut/omarchy-dragon-sl7 #39 | Test their patch 0124 (geni UART keeps the engine clocked in suspend) on 7.3 against the SSAM -110 after back-to-back suspends, and report back | Open: needs a module build and an approved reboot |
| omacom/omarchy #18970 | If the D+ (dp_hs_phy) wake or the lid-line wake reproduces on the 13.8-inch model, add the numbers | Open: needs the attended device-attached suspend test (pending item 2) |
| bryce-hoehn/linux-surface-laptop-7 PR #28 | Answer review comments on the romulus13 touchscreen row | Closed: answered 2026-11-21 (iptsd dependency in the README row; touchscreen tested with the patched daemon, an unpatched source build and the unchanged ELLX package). The reviewer thanked the testing and merged it 2026-11-21 22:00 UTC |
| #39, #18970, PR #28 | The posts lack the AI-use and verification line | Left as posted (user decision); new posts carry the line |
