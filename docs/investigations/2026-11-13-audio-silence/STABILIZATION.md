# Audio recurrence and stabilization review

## New evidence, 2026-11-13 23:54–23:57 KST

The user reported spontaneous recovery and another loss of sound. A privileged kernel read around 23:55 showed no post-initialization SoundWire faults. A later read captured a NEW `SWR bus clsh detected` at 23:56:21 on 6b10000.soundwire. Thus the earlier observation was time-bounded, not a guarantee of stability. No device reset, sound test, service restart or audio configuration change was made during this review.

At 23:57:04 the speaker node was suspended, Firefox's playback node idle, and PCM1 closed. Speaker/stream mute flags were false. PA gains remained 1/1 and WSA digital gains 81/81, with digital mute off. These readings do not establish that a running PCM was silent: the application was idle when sampled. The report time and capture time can differ. Do not interpret normal idle suspension as proof of a defect.

The current boot therefore confirms recurrence without the earlier live reset attempts. It rules out describing reboot recovery as a stable fix. It does not prove which runtime transition caused the clash. The controller masks its clash interrupt after handling it, so raw message counts are not a reliable count of every subsequent physical fault.

## Ranked stabilization candidates — researched, NOT applied

1. **Controlled speaker-only idle-suspend comparison.** Official PipeWire/WirePlumber configuration supports `session.suspend-timeout-seconds = 0` on the exact physical speaker node. Existing `node.pause-on-idle = false` is a different setting and does not disable the session-manager timeout. This avoids repeated idle close/reopen transitions and is a focused diagnostic mitigation, not a proven fix. Keep all volume/protection limits and headphone policy unchanged. Compare start/stop behavior and new kernel faults over repeated normal use, then compare battery draw. Remove the trial if ineffective. Applying this requires reloading the session manager and must be treated as a separate test, not silently installed by setup.
2. **IRQ/clock synchronization fix — inspect equivalence before backport.** Oleg Keri's 2026-10-07 patch describes X1E80100 clock-stop races causing clashes/parity errors. However the archived current build source already calls `disable_irq(ctrl->irq)` immediately before gating hclk; this synchronously waits for IRQ handling. The retained Lee Jones patch does not remove that call. The published `synchronize_irq` addition targets a different source context, so absence of that exact spelling is not evidence that synchronization is missing. No speculative kernel change was made.
3. **System-sleep runtime-PM patch — separate suspend investigation.** Qualcomm's 2026-11-12 proposal adds forced runtime suspend/resume for system sleep, tested on Glymur CRD, not this Surface. Current archived source lacks the proposed system-sleep callbacks. There was no system suspend in this boot before this recurrence; this patch does not directly explain the observed event. Do not combine it with an idle trial.
4. **Stock-versus-custom SoundWire comparison.** Existing backport signing/ABI validation did not prove hardware stability. A future comparison must preserve a signed bootable rollback and change one component per reboot. Do not unbind codecs/cards or stop ADSP live.

## Excluded shortcuts

- The failed soft-mixer/PA-gain trial remains removed; no repeat of gain changes as a claimed fix.
- No copying Surface Pro 11 four-channel routing to this two-channel Laptop.
- No masking alsa-restore based on the old Surface Pro 11 boot-race article: the current upstream article explicitly retracts that diagnosis and corrects opcode 1001021 to GET_SPF_STATE. This machine's boot-time occurrence alone does not establish a playback graph failure.
- RTKit is absent and produces startup warnings, but the same session has audible periods. It is a separate scheduling-quality concern, not demonstrated cause of the bus clash.

## References and captured data

- [Recurrence snapshot](recurrence-235707.json), privacy-filtered to audio state; no message/media titles saved.
- [Official WirePlumber example](https://github.com/PipeWire/wireplumber/blob/master/src/config/wireplumber.conf.d.examples/alsa.conf).
- [Official PipeWire property reference](https://docs.pipewire.org/page_man_pipewire-props_7.html).
- [IRQ/clock race patch, author posting](https://lists.openwall.net/linux-kernel/2026/10/07/1712).
- [System sleep patch, author posting](https://lore-kernel.gnuweeb.org/b4-sent/20261112-qcom-swr-system-sleep-v1-1-a61a83f6475d%40oss.qualcomm.com/T/).
- [Retracted boot-race diagnosis](https://github.com/ooaklee/linux-surface-pro-11-oe/blob/main/docs/adr/adr-0035-audio-boot-race-alsactl.md).

This review changes documentation only. No stabilization candidate has yet been installed or validated on this machine.
