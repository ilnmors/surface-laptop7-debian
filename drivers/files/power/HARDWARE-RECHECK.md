# Hardware recheck after deep resume

2026-11-12:

- Touchscreen: I2C 8-0034 exists, no driver symlink and no usable touchscreen input. Existing overlay is not proof of working hardware. No guessed reset GPIO applied.
- CPU: online 0–8; CPU9 still fails PSCI -22. Only policy0 CPUs 0–3: ondemand, max 3417600kHz. CPU settings unchanged by user request.
- Camera: OV02C10 is listed as the internal front camera. After deep resume, 1280x720 ABGR8888 captured 90/90 frames, exit 0, mean reported FPS excluding the first 18.7824. Frames were not written to disk. Generic uncalibrated tuning and missing helper warnings remain; previous rejected gain patch remains rolled back. This is functional streaming, not a quality improvement.
- Speakers: user reports sound appears good. One wsa884x parity error occurred after resume; continue monitoring rather than declaring the bus issue solved.
- GPU: no prior missing-zap/GMU-OOB/GPU-init-failure messages in this boot; user confirmed graphics recovered.

See ../sleep/diagnostics/2026-11-12-post-reboot-review.md and ../camera-quality/latest-capture-check.json.
