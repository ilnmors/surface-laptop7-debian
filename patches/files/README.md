# Kernel module backports

Target: 7.3.0-31-qcom-x1e, Romulus13 Surface Laptop 7. These are module replacements, not a full new kernel version.

- USB: Prashanth K's 2026-11-06 v3 missing-HCD guard prevents the exact NULL dereference found in this Surface's EFI pstore.
- SoundWire: Lee Jones's 2026-11-03 v2 patches 06–10 add allocation bounds/cleanup, safe remove/runtime PM, clock-error checks, interrupt-mask locking and stale broadcast-IRQ handling. The combined patch adapts two context differences while retaining this kernel's existing IRQ-enable/MMIO behavior.
- Source/messages are under sources/, upstream/ and patches/. Matching original header packages are under headers/. Prebuilt reusable modules under modules/ are intentionally unsigned; the installer signs installed copies with the destination machine key.

Build: bash patches/files/build.sh /absolute/new/build-directory. Requires GCC 14, make, patch and native build prerequisites; headers/sources are local. Header counted_by attributes are ignored by GCC 14; the compiler/pahole version warnings are preserved in verification/ build logs. ABI and signature validation passed in the matched ARM64 VM.

Install: sudo bash patches/files/install.sh. setup.sh also runs this before its final Secure Boot refresh. Original packaged modules remain untouched; replacements are under /lib/modules/7.3.0-31-qcom-x1e/updates/surface/ and are signed locally. The updater regenerates initramfs and signed boot images. Active USB/audio devices were not unbound; reboot to use replacements.

Verification: unsigned test module rejected, existing signed module accepted, replacement USB and SoundWire modules and their dependencies loaded under module.sig_enforce=1. See verification/arm64-module-load.log. This tests trust and ABI, not real USB/audio/sleep behavior.

Rollback: remove only updates/surface/dwc3-qcom.ko and updates/surface/soundwire-qcom.ko, run sudo depmod -a 7.3.0-31-qcom-x1e and sudo surface-secureboot-update, then reboot. The previous packaged modules are retained.

Physical deep-resume and intermittent audio reliability remain pending. The first xHCI probe timeout and codec parity faults are not proven fixed merely by loading these modules.
