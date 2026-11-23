# Investigations

Dated records of what was examined on this machine and what was found. They are evidence and history, not installation inputs: nothing in `setup.sh`/`setup.py` reads them. The component READMEs link to the record behind each setting.

| Record | Topic | Outcome |
| --- | --- | --- |
| [2026-11-11-suspend-crash](2026-11-11-suspend-crash/README.md) | Deep suspend crash | NULL dereference in dwc3-qcom after the a400000 xHCI host failed with `-110`; led to the NULL-HCD guard patch |
| [2026-11-12-camera-quality](2026-11-12-camera-quality/RESULTS.md) | Front camera frame rate and color | Legal VBLANK gave 37.5 fps; tuning candidates and rejected IPA/gain patches ([trial order](2026-11-12-camera-quality/README.md)); the two neutral candidates used by the preview tool moved to `drivers/files/camera-quality/preview/` |
| [2026-11-12-cpu-clusters](2026-11-12-cpu-clusters/x1p64100-case-36.md) | CPU clusters 1 and 2 without cpufreq | All SCMI OPPs flagged turbo; the fix in use is `drivers/files/cpu/scmi-all-boost.patch`; live-state results |
| [2026-11-12-power-and-drivers](2026-11-12-power-and-drivers/OPTIMIZATION.md) | Power after the 2026-11-12 reboot | 120 Hz kept; governor, CPU cap and NVMe comparisons; driver follow-up and the hardware recheck after deep resume |
| [2026-11-12-resume-timing](2026-11-12-resume-timing/post-reboot-review.md) | Resume timing after the GPU firmware repair | Per-device resume traces (09:02, 19:27, 23:16) and the post-reboot review |
| [2026-11-12-touchscreen-acpi](2026-11-12-touchscreen-acpi/power-sequence-check.json) | First touchscreen attempt (I2C, ACPI tables) | The device did not bind; superseded by the GTCH SPI overlay (`drivers/files/touchscreen/spi-gtch/`) |
| [2026-11-12-wifi-recovery](2026-11-12-wifi-recovery/RUNTIME-RECOVERY.md) | Wi-Fi drops | Beacon loss and a stuck scan with the original ath12k; not a password problem |
| [2026-11-13-audio-silence](2026-11-13-audio-silence/README.md) | Speaker silence and the recovery attempt | Sound returned only after a host reboot; trial configurations under `trials/`; no permanent fix |
| [2026-11-14-audio-cause](2026-11-14-audio-cause/README.md) | Cause of the speaker silence | SoundWire controller clock-stop/resume as the leading hypothesis; external cases, recurrence, recovery and post-reboot evidence |
| [2026-11-15-suspend-power](2026-11-15-suspend-power/SUSPEND.md) | Deep sleep battery drain | Measured drain per suspend with the inputs in `summary.json` |
| [2026-11-16-usb-suspend](2026-11-16-usb-suspend/USB-SUSPEND.md) | USB during suspend and the phone connection | Superseded by the tethering report; PHY system-sleep candidate |
| [2026-11-16-usb-tethering](2026-11-16-usb-tethering/TETHERING.md) | Phone USB tethering | A stale request in the phone; fixed by restarting the phone. The USB-C USB2 path can stay dead after abrupt data loss |
| [2026-11-17-sync-state-trial](2026-11-17-sync-state-trial/SYNC-STATE-TRIAL.md) | `fw_devlink.sync_state=timeout` | Lets DDR power-collapse; showed the `ss_phy_irq` wake storm that the dwc3-qcom patch later fixed |
| [2026-11-18-audio-speaker-repro](2026-11-18-audio-speaker-repro/README.md) | Automated speaker silence reproduction | SoundWire bus clash on resume of `6b10000.soundwire`; keeping the controller on avoids it |
| [2026-11-18-hardware-check](2026-11-18-hardware-check/HARDWARE-CHECK.md) | Full hardware check (phase 1) | Component-by-component results and the fix order ([report](2026-11-18-hardware-check/INVESTIGATION-REPORT.md)) |
| [2026-11-20-ss-phy-storm](2026-11-20-ss-phy-storm/trials/) | `ss_phy_irq` wake storm on sync_state boots | Trial patches: LFPS detection off did not help, all autonomous detection off stopped it; the fix in use is `patches/files/dwc3-ss-wake/` |
