# Camera trials — 2026-11-12

- Original module C8AE6F17BF899E4A937A808 captures 720p at 18.78 fps without errors.
- Legal VBLANK 72 instead of 1236 gave 37.46 fps over 240 frames, zero capture errors. Shorter exposure can increase noise in dim light. The control was restored after tests.
- The rebuilt candidate 08EF7452B0F555AA15FA25F preserves the original crop metadata patch and applies the faster default only on Romulus13. It is signed and staged for the one-shot boot. Live unload was refused while the media graph held references; no forced unload was used. A sensor unbind/rebind emitted a clock-busy warning, then normal capture resumed. Do not repeat live unbinding.
- Isolated libcamera 0.7.1, CPU debayer and gain code/16 helper were tested at 720p. Community CCM produced a pink image and was rejected. Removing that CCM and using neutral gamma/saturation significantly improved color according to the user; noise remains unacceptable. The system libcamera/PipeWire stack has not been replaced.
- The noisy scene reached analogue gain 248/16 = 15.5x. Fast frames reduce the available exposure. No denoising algorithm exists in this installed CPU software-ISP path.
- Ported the published sensor-gain-step fix to the isolated 0.7 IPA (0.0625 instead of 0.145); combined neutral colors with the community exposure target 1.5. User still reports noise. This is not a verified quality fix.
- `preview.py`/`.sh` extract bundled packages into the user's cache and run isolated 720p previews. `--capture 90` is headless; `--low-gain` selects the additional AGC experiment. Neither installs system libraries. Neutral is the default; the rejected CCM is retained as research only.

## Sources and remaining work

https://github.com/bryce-hoehn/linux-surface-laptop-7/tree/main/config/OV02C10-camera — same laptop, helper/CCM/CPU processing and lower exposure target. Adapted gain divisor to the actual kernel control; its CCM was not suitable in this user's scene.
https://patchwork.libcamera.org/patch/28362/ — OV02C10 gain code/16 and black level 4096, consistent with this driver.
https://patchwork.libcamera.org/cover/28173/ and https://patchwork.libcamera.org/patch/28177/ — published OV02C10 exposure/white-balance/gain-step work, not all merged; only gain-step logic was ported in this round.
https://patchwork.libcamera.org/cover/28096/ and https://patchwork.libcamera.org/patch/28103/ — GPU temporal denoise/frame-duration work for OV32C4, rejected upstream and not tested on this Surface. Requires a noise model and GPU-path validation; not installed.

Deferred at user request: 1080p CMA allocation, validated temporal/spatial denoise, frame-duration/exposure tradeoff, integration into Firefox/PipeWire without disturbing working audio. No stored preview image or personal video is included.

## Promoted after reboot verification

The candidate loaded successfully after reboot and delivered approximately 37.5 fps over 90 frames with zero capture errors. On explicit user approval it was promoted into the standard signed boot and offline patch installer. Baseline source and 06-camera-fast-default.patch allow rebuilding it. This promotes frame timing only; noisy/pink experimental color profiles are not installed system-wide. Camera noise/1080p work stays deferred.

## CMA exhaustion and 1080p (2026-11-13)

After some uptime every capture (even 640x480) failed with `dma-heap allocation failure`: the kernel log showed `cma: reserved: alloc failed, req-size 300/900 pages, ret -16` with only ~16 MB of the 128 MB CMA free and the largest free run 31 pages. Stopping Waydroid did not change it, so the CMA is held by kernel drivers from boot. With the CMA heaps hidden in a private mount namespace (system heap only) the stock stack delivered 1280x720 and 1920x1080 at 37.5 fps over 90 frames each, so 1080p works and the failure is the CMA size, not the sensor. The kernel command line now uses `cma=512M` (GRUB, surface-secureboot-update and kernel/setup.sh; backup /boot/secureboot/grub.cfg.before-cma512); it takes effect on the next boot.

Noise remains a limit of the libcamera 0.4 CPU soft ISP: it has no denoise stage, and the 37.5 fps mode shortens exposure so dim scenes reach ~15.5x analogue gain. Options are the 18.8 fps mode (longer exposure, less noise) or an unvalidated GPU denoise path.

## Follow-up: cma=0 (2026-11-13)

`cma=512M` could not be reserved ("cma: Failed to reserve 512 MiB": the area must sit below 4 GiB, which firmware carve-outs fragment), and any `cma=` argument also disables the 128 MiB DT `linux,cma` pool. With no CMA, libcamera uses the system heap and 1080p/720p capture runs at 37.5 fps; display, GPU, Wi-Fi, audio, Bluetooth, Waydroid and video devices work. ath12k logs "qmi dma allocation failed ... will try later with small size" and uses its normal small-chunk fallback. The command line is now the explicit `cma=0` (GRUB, surface-secureboot-update, kernel/setup.sh).
