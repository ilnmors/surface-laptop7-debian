# Deep cycle after promoted default boot — 2026-11-12 19:27–19:28

Manual lid cycle on the promoted signed default image (CPU 0-9, ov02c10 08EF7452B0F555AA15FA25F, ath12k D044C56077CC5357DC3F5BF). Power-only trace saved to /var/log/surface-resume/manual/power-trace-1929.txt (raw trace stays local, not in Git) and re-armed.

| Resume phase (monotonic) | Time |
| --- | --- |
| dpm_resume_noirq | 1.699 s |
| dpm_resume_early | 0.514 s |
| dpm_resume | 2.482 s |
| machine_suspend end → thaw_processes | 4.76 s |

Slowest callbacks, all err=0: spi_hid spi0.0 2.455 s; qcom-pcie 1bd0000 1.072 s (empty port: "Device not found"); ath12k 0.512 s; qcom-pcie 1bf8000 (NVMe) 0.313 s; qcom-pcie 1c08000 (Wi-Fi) 0.312 s.

- spi_hid: spi_hid_resume() asserts reset, powers up, then sleeps a fixed msleep(2000) inside the system resume callback (spi-hid-core.c from the archived community source; module /lib/modules/<kernel>/updates/sl7/spi-hid.ko). This fixed wait is the largest single resume delay; the earlier 2.417 s measurement matches.
- 1bd0000: no device is attached, but link training still costs ~1.07 s per resume. Disabling the controller would need a confirmed board schematic/DT check first.
- Wi-Fi: wake requested at 19:28:19.50, CTRL-EVENT-CONNECTED 19:28:21.48 and DHCP lease 19:28:21.63 (~2.1 s; earlier record ~11.4 s). Wi-Fi-bound HTTPS 200 afterwards. No beacon loss in this boot. Suspend logged "Timeout waiting for L2 entry" on 1c08000 and two "Failed to set the requested Country regulatory setting" just before entry.
- Audio: no SoundWire/WSA parity messages after resume. One qcom-apm CMD timeout appears earlier in the boot.
- Correction: the 19:25 default-boot check could not read the system journal (account not in systemd-journal/adm). Its "zero kernel errors / zero beacon loss" statement was unverified; this file records the root-read result.
