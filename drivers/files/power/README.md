# Battery measurements

Captured 2026-11-12T09:02:27.575261+09:00. Battery full 50.78 Wh; design 52.33 Wh; reported health 97.04%. This is fuel-gauge telemetry, not an independent power meter.

| Measurement | Result |
| --- | --- |
| Latest deep sleep | 11-12 03:33:48 → 11-12 08:51:33 KST (5.296 hours) |
| Charge boundary samples | 73.00% → 67.00% |
| Sleep energy estimate | 3.046 Wh |
| Sleep mean | 0.575 W / 1.133 percentage points per hour |
| Sample offsets | 35.1s before entry; resume sample rounded to the same second |
| Awake weighted average | 7.644 W across 2.665 sampled hours / 319 intervals |
| Simple full-battery equivalent at that awake average | 6.64 hours; 50% equivalent 3.32 hours |

UPower discharging rate samples are time-weighted with trapezoids; gaps >120 seconds and all intervals overlapping suspend are excluded. Charging samples are excluded. Other sleep intervals lacked close discharging boundary samples, so they are not reported as clean battery measurements. Percentage granularity is about 1 point; sleep values are estimates with roughly a percentage point of boundary/gauge uncertainty. The observed workload includes Firefox, Steam/FEX, Waydroid and development work, not a controlled idle/web benchmark.

Windows comparison: this machine has no retained Windows battery/SleepStudy baseline. Microsoft recommends <5% over 16 hours for Modern Standby (~0.3125 percentage points/hour); the observed Linux sleep rate is about 3.6× that recommendation. SleepStudy flags >=1%/hour as high drain. These are Windows diagnostic targets, not proof of this unit's measured Windows consumption.

Microsoft's Snapdragon Surface Laptop 7 13.8-inch specification advertises up to 13 hours web / 20 hours local video under its own test conditions. The mixed Linux average equivalent (6.6 hours) cannot isolate an OS penalty against those tests. Battery wear (~3%) alone does not explain a large runtime gap. Brightness/120Hz, GPU/software workload, radios, platform sleep firmware and incomplete CPU power policies need controlled comparison. No new power tuning is claimed from these numbers.

Sources:
- https://learn.microsoft.com/en-us/surface/tech-specs/surface-laptop-snapdragon-tech-specs
- https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/modern-standby-sleepstudy
- https://learn.microsoft.com/en-us/windows-hardware/test/hlk/testref/36463e42-7d6e-408e-933f-dbf56ea41e65

Refresh with `python3 tools/battery.py` while UPower history is available. Raw aggregate history/timestamps used in calculation are in battery-measurement.json. No battery serial or account information is saved.
