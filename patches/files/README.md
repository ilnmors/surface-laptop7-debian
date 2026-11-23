# Kernel module backports

Target: 7.3.0-31-qcom-x1e, Romulus13 Surface Laptop 7. These are module replacements, not a full new kernel version.

- USB: Prashanth K's 2026-11-06 v3 missing-HCD guard prevents the exact NULL dereference found in this Surface's EFI pstore.
- SoundWire: Lee Jones's 2026-11-03 v2 patches 06–10 add allocation bounds/cleanup, safe remove/runtime PM, clock-error checks, interrupt-mask locking and stale broadcast-IRQ handling. The combined patch adapts two context differences while retaining this kernel's existing IRQ-enable/MMIO behavior.
- Source/messages are under sources/, upstream/ and patches/. Matching original header packages are under headers/. Prebuilt reusable modules under modules/ are intentionally unsigned; the installer signs installed copies with the destination machine key.

Build: bash patches/files/build.sh /absolute/new/build-directory. Requires GCC 14, make, patch and native build prerequisites; headers/sources are local. Header counted_by attributes are ignored by GCC 14; the compiler/pahole version warnings are preserved in verification/ build logs. ABI and signature validation passed in the matched ARM64 VM.

Install: sudo bash patches/files/install.sh. setup.sh also runs this before its final Secure Boot refresh. Original packaged modules remain untouched; replacements are under /lib/modules/7.3.0-31-qcom-x1e/updates/surface/ and are signed locally. The updater regenerates initramfs and signed boot images. Active USB/audio devices were not unbound; reboot to use replacements.

Verification: unsigned test module rejected, existing signed module accepted, replacement USB and SoundWire modules and their dependencies loaded under module.sig_enforce=1. See verification/arm64-module-load.log. This tests trust and ABI, not real USB/audio/sleep behavior.

Rollback: remove only updates/surface/dwc3-qcom.ko and updates/surface/soundwire-qcom.ko, run sudo depmod -a 7.3.0-31-qcom-x1e and sudo surface-secureboot-update, then reboot. The previous packaged modules are retained.

Deep suspend and resume with these modules work. The a400000 xHCI probe timeout at boot is handled by a softdep (`drivers/files/boot-trials/`), not by these modules; the speaker silence is avoided by holding the SoundWire controller on (`drivers/files/audio/`).

## Other replacements in use

Loaded on the current boot from `/lib/modules/7.3.0-31-qcom-x1e/updates/surface/` (srcversion):

| Module | Build | Notes |
| --- | --- | --- |
| dwc3-qcom | `373A6F05E3EFE6B7721A44D` | NULL-HCD guard plus SuperSpeed wake only with a SuperSpeed device attached ([dwc3-ss-wake/](dwc3-ss-wake/)) |
| phy-qcom-qmp-combo | `0A74E69E94C0DD14BD50B53` | System-sleep callbacks and the AON clamp fix ([phy-sleep/](phy-sleep/README.md)) |
| ath12k | `D044C56077CC5357DC3F5BF` | The original source with both Romulus13 rfkill guards plus the upstream regulatory fix f2576dc0 ([wifi-regulatory/known-good/](wifi-regulatory/known-good/README.md)). The first Wi-Fi rebuild (`D61DA424018CF1563587D2E`) caused a hard-rfkill regression and is rejected ([wifi-regulatory/README.md](wifi-regulatory/README.md)) |
| ov02c10 | `08EF7452B0F555AA15FA25F` | Minimum vertical blanking on Romulus13 for about 37.5 fps ([CAMERA-FRAME-TIMING.md](CAMERA-FRAME-TIMING.md)) |
| scmi-cpufreq | `3A225A33A62E1578048E341` | All SCMI OPPs usable so clusters 1 and 2 get cpufreq (`drivers/files/cpu/`) |
| soundwire-qcom | `3D22555E212EACB6FA11473` | The SoundWire backports above |

spi-hid v2 (`0923360D0DE94E631C945EE`) is loaded from `updates/sl7/` (`drivers/files/touchpad/spi-hid-resume/`). The `updates/sl7/` copies of ath12k and ov02c10 are the original builds and are shadowed by `updates/surface/`.
