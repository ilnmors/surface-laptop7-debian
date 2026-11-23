# Post-reboot deep-sleep review

Checked 2026-11-12 after the GPU firmware repair reboot.

- `/sys/power/mem_sleep`: s2idle [deep]. Suspend success 1, fail 0.
- Deep entry 10:59:18, exit 12:04:55 (about 65m37s wall-clock entry-to-exit). The machine returned; this is not a recurrence of the previous permanent hang.
- Kernel monotonic entry 193.305047, exit 200.691814. The 7.386767s difference combines active suspend/resume work and excludes suspended time; it is NOT a measurement of screen-on latency or resume alone.
- Regulatory-update timeout and PCIe 1c08000 L2-entry timeout remain. SPI-HID quiesced and re-probed after resume; CPUs 1–8 returned.
- Wi-Fi authentication started at monotonic 212.102087, 11.410273s after suspend exit, and authentication completed at 212.226026. This is not DHCP/DNS or Internet readiness. Connection used a different BSSID; scanning/roaming may contribute.
- No device-callback trace was armed across this reboot, so individual callback duration cannot be inferred from this journal. A fresh 256KiB-per-CPU power-only trace is now armed for the next user-controlled cycle; no forced suspend.
- Speaker user feedback is positive, but a wsa884x parity error appeared at 12:11:26. SoundWire stability is not certified; preserve current working routing and continue log checks.

## Related Wi-Fi fix candidate, not installed

Upstream series: https://lore-kernel.gnuweeb.org/ath12k/178846215597.824911.15370402365282213910.b4-ty%40oss.qualcomm.com/T/

The matching local kernel source ath12k/wmi.c assigns pdev_idx only after validation; the DROP path can reach completion with pdev_idx still 255 and no radio selected. The upstream fix assigns the parsed phy_id before validation so dropped events can signal completion. The cited upstream test uses WCN7850 hw2.0 and this device's firmware build WLAN.HMT.1.1.c7-00108-QCAHMTSWPL_V1.0_V2.0_SILICONZ_UPSTREAM-3.

This supports a concrete follow-up candidate, not proof that it alone explains this suspend path or the 11s reconnect delay. Current installed modules are out-of-tree updates/sl7; require exact source/build correspondence, signed module validation and controlled next-cycle comparison before claiming a fix. No Wi-Fi module was replaced/unloaded in this inspection.
