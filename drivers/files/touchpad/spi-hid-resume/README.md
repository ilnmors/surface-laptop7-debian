# spi-hid deferred resume settle (verified 2026-11-12 21:22, installer default)

The installed community spi-hid.ko (srcversion A2DC44A5E473B534676E1E3, rebuilt byte-for-byte from archive/hardware/source/surface-xplus-project.zip → kernel/modules/spi-hid) slept msleep(2000) inside the system resume callback after reset. That fixed wait was 2.455 s of a 4.76 s kernel resume (see drivers/files/sleep/diagnostics/2026-11-12-192713).

The firmware still needs ~2 s after reset, so the wait is not removed; it moves to a resume_work item:
- resume(): reset + power up, record settle_until = now + 2 s, return immediately.
- pm .complete: clear suspended and queue resume_work.
- resume_work: sleep the remaining time, enable the IRQ, then queue the existing reset_work (descriptor/HID re-creation unchanged).
- quiesce (suspend/remove) cancels resume_work first.

Expected: system resume ~2.4 s shorter; touchpad ready about 2 s after wake, as before. Result srcversion F78320E76D9CB9AFF42A4E8.

| File | Purpose |
| --- | --- |
| source/ | Unmodified archived source (matches the installed module's srcversion). |
| resume-deferred.patch | The change above. |
| build.sh | Rebuild against the bundled 7.3.0-31-qcom-x1e headers (unsigned). |
| spi-hid.ko | Built module (local payload, not in Git). |
| install.sh | Root: save verified boot to /boot/secureboot/rollback-20261112 (GRUB "Surface previous working image"), install module + PCIe3-off DTB, run surface-secureboot-update. |
| restore.sh | Root: put back the saved module, DTB and signed image. |

Rollback at boot: choose "Surface previous working image" in GRUB (hold Esc). After a successful check the older images can be deleted.

## Result (21:22 lid cycle)

Kernel resume (machine_suspend → thaw) 1.617 s, down from 4.76 s: noirq 0.628 s, early 0.520 s, dpm_resume 0.443 s. spi_hid callback 0.415 s (reset assert + power-up only). Touchpad hidraw present within 6 s of wake; Wi-Fi reconnected 2.0 s after NetworkManager wake. kernel/setup.sh installs this module over the kernel package copy.

## v2 (installed 21:47, next-boot trial)

The 21:22 result still spent 0.415 s in the spi_hid resume callback (300 ms reset assert + power-up). v2 moves the whole hardware restart into resume_work: resume() only resets driver state and marks the re-probe pending; resume_work (queued from .complete) asserts reset 300 ms, powers up, waits 2 s, enables the IRQ and queues reset_work. Expected callback time ≈ 0 and kernel resume ≈ 1.2 s; touchpad ready ≈ 2.3 s after wake. srcversion 0923360D0DE94E631C945EE; resume-deferred.patch is now the cumulative v2 change against source/. The module is stripped of debug info (44 KB instead of 715 KB) before signing.

install.sh now copies whatever signed image is running into /boot/secureboot/rollback-20261112 (GRUB "Surface previous working image") before installing. At 21:47 that is the verified v1 image (spi-hid F78320E76D9CB9AFF42A4E8). Older images (pre-cpu, previous, trial-cpu-camera, 19:25 rollback) were deleted at the user's request; /boot went from 47 % to 33 % used.
