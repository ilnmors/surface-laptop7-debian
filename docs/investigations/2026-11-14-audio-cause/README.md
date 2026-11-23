# Audio cause investigation — 2026-11-14

**Latest: silence recurred at 23:01; [23:07 running-PCM and digital-signal evidence](RECURRENCE-2301.md) is now available. The earlier measurements below remain historical. No new power comparison or recovery was performed.**

## Conclusion and confidence

**Confirmed:** SoundWire controller 6b10000.soundwire reported a bus clash at 2026-11-13 23:56:21 KST. The user repeatedly associates silence with pause/video-change followed by playback. The failure is intermittent, including spontaneous audible recovery.

**Leading hypothesis, not a proven root cause:** the controller's automatic runtime suspend/clock-stop and resume path contributes to failure. Baseline auto produced a user-reported failure; the explicitly authorized 90-second controller-on test was reported normal; after restoring auto the user initially reported normal playback, then renewed silence, then spontaneous recovery. This A/B/A result supports further testing of the power transition path but is not a statistically sufficient or precisely time-aligned proof of a unique defect.

Do not describe this as a verified permanent fix. No permanent policy or driver change was installed.

## Measurements

| Stage | Capture | What it establishes |
| --- | --- | --- |
| Initial passive 48 s | runtime-trace-000155.json | Broad unfiltered trace was noisy; its lack of retained audio events must not be used as proof of absent transitions. User reported a normal restart. |
| Filtered auto baseline, 100 s | filtered-runtime-trace-000512.json | 191 snapshots, 168 RPM trace entries with no buffer loss. Four speaker-running periods; one full controller resume. Controller resume ~3.2 ms, both codecs active within ~12.5 ms, success returns, no new kernel clash. User reported silence during this test, but the later silent snapshot was idle/PCM closed. |
| Silent report snapshot | silent-reproduction-000446.json | Mutes off, PA 1/1, digital 81/81. Firefox idle and PCM closed: cannot prove silence during active playback. |
| Controller held on, 90.053 s | controller-pm-ab-001005.json | 172 snapshots, controller continuously active, four running periods. Two codecs still suspended and resumed during one full idle cycle while the controller stayed on. User reported normal output. |
| Restored auto, 55 s | restored-auto-001155.json | Policy auto confirmed. One successful controller/codec resume, no new clash. Only Mutter was captured as running; Firefox remained idle. User's later video and renewed-silence reports were not synchronized to this window. |

Generic runtime-PM idle return codes such as -EBUSY/-EAGAIN and resume return 1 (already active) are not proof of hardware failure. A successful driver return also does not prove audible output. No microphone or playback audio was recorded; snapshots retain state and application names, not media titles.

## Was auto the original setting?

The archived original driver source, before the custom Lee Jones patch, sets a 3000 ms autosuspend delay, uses autosuspend and enables runtime PM at qcom.c lines 1692–1696. The retained patch does not introduce those settings. The inspected live /etc udev, modprobe, system-sleep, TLP and WirePlumber directories contain no overriding SoundWire power-control policy. Earlier maintained/archive installation scripts yielded no custom policy for this controller.

Thus auto is consistent with the original driver policy and was not newly introduced by this investigation. There is no saved sysfs reading from the first Debian installation, so its exact historical value cannot be certified. Kernel revisions, firmware and custom module changes may affect behavior even when the policy string remains auto.

## Existing IRQ fix and remaining limits

The archived base source already has enable_irq in runtime resume and disable_irq immediately before hclk gating in runtime suspend. This matches Oleg Keri's October 9 v2 fix. The older October 7 synchronize_irq patch is not a demonstrated missing fix. The loaded module's srcversion is 3D22555E212EACB6FA11473, matching the retained custom SoundWire module metadata. A stock-versus-custom runtime comparison has not been performed.

The available evidence does not identify a specific defective instruction, firmware component or codec timing rule. The old bus clash may leave state that is not reflected by subsequent successful runtime-PM returns. Application-side stream stoppage is not excluded by the idle snapshots. More than one cause may exist.

## Changes and restoration

Only one hardware policy was changed, after explicit user approval: /sys/bus/platform/devices/6b10000.soundwire/power/control was held at on for 90.053 seconds, then restored to its original auto. The controller was already active when the write occurred. All four private trace instances were removed. No codec/card unbind, ADSP stop/start, module reload, audio-service restart, volume/protection change or reboot was performed.

Next discriminating experiment would be a longer same-source pause/restart comparison with real-time audible-failure markers, retaining only the controller-on difference. Its duration and permission must be agreed separately; the 90-second authorization does not authorize a permanent policy. Record power consumption before considering a lasting workaround. Live ADSP/card resets remain excluded.

## Sources

- [IRQ/clock fix v2](https://lists.openwall.net/linux-kernel/2026/10/09/721).
- [Linux runtime PM semantics](https://docs.kernel.org/power/runtime_pm.html).
- [Linux trace instances and event tracing](https://docs.kernel.org/trace/ftrace.html).
- [Machine-readable assessment](cause-assessment.json).
- [Previous incident and subsequent stabilization research](../2026-11-13-audio-silence/STABILIZATION.md).
- [Comparable cases and proposed remedy](CASES-AND-PROPOSAL.md).
