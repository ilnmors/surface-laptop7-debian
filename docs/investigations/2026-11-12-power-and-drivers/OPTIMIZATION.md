# Power assessment after the 2026-11-12 reboot

## Applied

- Preserve native 2304x1536 at 120Hz and 1.5 scale, as requested. The panel advertises 24–120Hz, but the current MSM DRM connector exposes no vrr_capable property and its driver sources contain no VRR support. GNOME experimental VRR was not enabled without the required capability.
- Enable WCN7850 station power saving (iw power_save on; NetworkManager wifi.powersave=3). The current driver supports station/dynamic PS. The active NM profile uses the default policy. Five gateway probes succeeded (0% loss, ~5ms mean), association remained up and no ath12k crash/timeout/failure appeared during the short observation. Real power reduction and repeated sleep/reconnect reliability are not yet measured. Disable with iw ... set power_save off / wifi.powersave=2 if a regression occurs. WoWLAN and PCIe deep-power settings were not changed.
- Include gen70500_sqe.fw and gen70500_gmu.bin in initramfs. Early boot repeatedly requested missing GPU firmware before the root filesystem supplied it. The new GPU hook includes both files; post-build extraction and signed-image verification passed. Next-boot removal of those errors is pending.

## Assessed without forcing unproven settings

- SCMI policy0 covers CPUs 0–3 only; CPU9 still fails PSCI -22. A temporary 12s+12s ondemand/schedutil comparison showed schedutil could request 806400kHz, but external power invalidated watt comparisons. The original ondemand governor was restored; no new CPU cap/governor service was installed. No claimed energy saving follows from that short observation.
- GNOME idle dimming is already enabled. Backlight was ~16% in the initial snapshot. Do not lower the user's required 120Hz or impose new suspend timers.
- PCIe root ports already use runtime auto; an unused port was suspended. Endpoint runtime control=on does not itself prove NVMe autonomous power saving is disabled; NVMe's configured APST latency limit is 100000us. No blanket USB autosuspend, PCIe force-ASPM or powertop auto-tune was applied.
- clk_ignore_unused/pd_ignore_unused protect incomplete board clock/domain descriptions. Runtime domain inspection already shows unused camera/video domains off. Removing the boot flags blindly can break devices and is not a measured optimization.
- The previous ~0.575W sleep / ~7.64W mixed awake baseline predates these changes. No new clean battery discharge comparison exists yet. Measure on battery at matched brightness, radios, 120Hz and app workload after the next manual sleep.

## Explicit background-app choice

KakaoTalk starts at GNOME login. By user choice persist.waydroid.suspend=false keeps Android alive after its last window closes; KakaoTalk is exempt from Android device-idle optimization and notifications are allowed. This preserves the possibility of incoming messages while awake, at additional background power/RAM cost. It does not keep the physical Surface awake during Linux suspend or guarantee delivery on an unsupported network/app configuration. Actual incoming-message verification is the user's test.

Waydroid measured ~1.26GiB PSS with the current apps/processes (90 processes); this is not fixed overhead for all workloads. Shared Android services are reused, while additional apps allocate private memory. No Discord or other personal APK was installed.

References:
- https://docs.kernel.org/admin-guide/pm/cpufreq.html
- https://kernel.org/doc/html/latest/driver-api/clk.html
- https://lists.infradead.org/pipermail/ath12k/2024-February/001457.html
- https://github.com/bryce-hoehn/linux-surface-laptop-7/issues/7
- https://docs.waydro.id/usage/waydroid-prop-options
