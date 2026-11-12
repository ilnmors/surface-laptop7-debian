# Deep cycle with spi-hid v2 — 2026-11-12 23:16–23:59

Boot after installing spi-hid v2 (srcversion 0923360D0DE94E631C945EE) with the PCIe3-off DTB; Secure Boot on, CPUs 0-9.

| Resume phase | v2 | v1 (19:41) | before (19:27) |
| --- | --- | --- | --- |
| dpm_resume_noirq | 0.628 s | 0.628 s | 1.699 s |
| dpm_resume_early | 0.512 s | 0.520 s | 0.514 s |
| dpm_resume | 0.240 s | 0.443 s | 2.482 s |
| machine_suspend → thaw | 1.407 s | 1.617 s | 4.76 s |

- spi_hid no longer appears among slow callbacks; "hardware restart deferred" at 23:59:45.58 and "hardware restarted" at 23:59:48.03 (touchpad ready ~2.3 s after wake, as designed). Remaining top callbacks: ath12k 0.510 s, NVMe PCIe 0.314 s, Wi-Fi PCIe 0.312 s.
- Wi-Fi: CTRL-EVENT-CONNECTED 23:59:47.80, activated 23:59:48.02 (~2.1 s after suspend exit). The roam at 00:00:26 was AP-initiated band steering (WNM disassociation imminent, 2.4 → 5 GHz), not a reconnect failure.
- Sleep drain: UPower 78 % at 23:11:41 → 77 % at 23:59:45 over a 42.8 min suspend (1 % ≈ 0.5 Wh at 50.8 Wh full). UPower reports whole percents only, so this bounds the drain to roughly ≤ 0.7 W; measure over several hours for a precise figure.
- Power-only trace saved to /var/log/surface-resume/manual/ and re-armed.
