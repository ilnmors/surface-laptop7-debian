# Quick CPU/driver verification

## CPU cap experiment — evaluated, NOT applied

The machine has no exposed watt-based powercap interface. Only SCMI policy0 (CPUs 0–3) exposes frequency limits; nine logical CPUs are online out of ten described in the current board tree. Four pinned PBKDF2 workers ran continuously; each phase had 3s settling + 12s measurement.

| Cap | Whole-system battery power | Throughput vs average baseline |
| --- | --- | --- |
| 3.4176GHz first baseline | 30.09W | 1569.4 jobs/s |
| 2.976GHz | 22.40W (21.4% lower) | 89.5% |
| 2.5152GHz | 17.15W (39.8% lower) | 75.5% |
| 3.4176GHz final baseline | 26.90W | 1486.6 jobs/s |

These are short whole-system battery-gauge samples under an intentionally four-core workload. Baseline drift was 3.20W. They are not package-watt limits, not control of all cores and not a prediction of everyday runtime. Light workloads below the cap may not benefit. User requested leaving CPU settings alone: ondemand and max 3417600kHz are restored; no persistent limiter is installed.

## CPU9 startup failure — narrowed, no CPU/DTB change

The actual DTB lists cpu@20300 but not cpu@20100. Logical CPU9 corresponds to the former. Firmware rejects its PSCI CPU_ON request and Linux reports -22; Linux maps invalid PSCI parameters/address to EINVAL. Other secondary cores start, so a target CPU topology/fuse mapping mismatch is a plausible cause, not a global CPU_ON failure.

The archived build-surface-dtb.py explicitly removes cpu@10300 and cpu@20100, retaining cpu@20300, then validates the count as ten. That count check did not verify every target against this machine's firmware. Upstream hamoa.dtsi labels cpu@20100 as physical cpu9 and cpu@20300 as physical cpu11; logical numbering changes after deletions. The exact correct fused-core map needs firmware/ACPI evidence. No replacement address or DTB was guessed/applied, per user instruction.

## Driver power saving verified

- NVMe get-feature 0x0c: APSTE enabled, 100ms idle → PS4. Controller reports a non-operational PS4 with 5ms entry/10ms exit. Read-only inspection; no NVMe feature writes.
- SSD and Wi-Fi endpoint PCIe links: ASPM L1 enabled and L1.1/L1.2 controls enabled. No forced ASPM policy.
- USB root hubs usb1–usb6: power/control auto and runtime suspended. No need for blanket autosuspend changes.
- Wi-Fi station power save remains on, with no observed ath12k failure/crash/timeout in this boot.
- No touchscreen driver bound to I2C 8-0034; this remains unresolved. CPU9 remains offline.
- Left/right sample playback commands completed without a SoundWire parity/bus-clash log, but actual audibility still needs user confirmation. New-module manual deep resume has not yet been recorded (suspend success/fail still 0/0 at this check).

Inspection tools: native nvme-cli/libnvme packages downloaded from authenticated Debian APT and extracted into a temporary directory, not globally installed. nvme-power.json excludes serial/identity fields.

References: https://docs.kernel.org/admin-guide/pm/cpufreq.html and https://docs.kernel.org/power/powercap/powercap.html .
