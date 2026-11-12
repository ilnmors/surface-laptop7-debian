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
