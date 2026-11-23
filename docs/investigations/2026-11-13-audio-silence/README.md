# Speaker silence and recovery incident — 2026-11-13

All times are KST. This record separates the initial failure from errors introduced during troubleshooting. No permanent audio fix has been demonstrated.

## Outcome

The user heard no sound from settings tests, normal playback or direct ALSA playback. Sound returned after an unexpected whole-host reboot. No explicit reboot command was issued during the recovery attempt, but the reboot followed the agent's live ADSP reset attempt. The attempt must be treated as a possible cause; the precise reset mechanism is not established.

## Timeline and evidence

| Time | Observation / action | Result |
| --- | --- | --- |
| 19:19:16 | Boot-time AudioReach timeout, opcode 1001021 | Also occurs in the next, audibly working boot; insufficient to explain silence alone. |
| 21:30:40 and 21:32:52 | SoundWire reports `SWR bus clsh detected` | Original bus faults precede codec/card reset attempts. The initial search missed the abbreviation `clsh` and incorrectly reported no errors. |
| Before 22:06 | Replaced stale removed-EQ default with physical speaker; restarted WirePlumber | Digital samples and ALSA RUNNING confirmed, but user still heard nothing. |
| Before 22:06 | Tried card-scoped soft mixer, PA gain 1/1 → 6/6 within kernel caps | Still silent. Trial removed from active configuration; reference retained under trials/. |
| Before 22:06 | Stopped audio services/sockets and tried direct stereo ALSA playback | Still silent despite active speaker DAPM paths. Four-channel playback was rejected; the Surface Pro 11 reference does not transfer directly to this Laptop 7. |
| 22:06:35–22:06:50 | Rebound both WSA884x speaker codecs | Four AudioReach 100100d timeouts and two unbalanced runtime-PM warnings. User still heard nothing. |
| 22:10:13–22:10:29 | Rebound the snd-x1e80100 platform sound card | Four more 100100d timeouts, two parity errors and three MAX_RETRY messages. User still heard nothing. |
| After the last failed test | Attempted platform-card unbind, ADSP remoteproc stop/start, then card/service restoration | Unexpected whole-host reboot; no completion output survived. The exact executed stage cannot be reconstructed. |
| 22:14:07 | Last previous-boot journal entry | No orderly shutdown sequence found. |
| 22:15:41 | New boot start reported by uptime | Same kernel, 7.3.0-31-qcom-x1e. |
| 22:15:49–22:15:50 | Journald reports system/user journals uncleanly shut down; ADSP firmware loads successfully | Supports abnormal termination, not a precise panic/watchdog diagnosis. |
| After reboot | User reports sound working; PA gains again 1/1 | Gain 1/1 alone cannot explain the failure. No further hardware reset performed. |

## What is established

- SoundWire transport faults occurred during the original silent session. Nonzero digital output did not prove audible speaker operation.
- Recovery attempts produced additional DSP/codec errors and failed to restore sound before reboot.
- Opcode 0x0100100D is APM_CMD_SHARED_MEM_UNMAP_REGIONS, not a graph-close command.
- A boot-time 1001021 timeout also exists in the working boot; do not describe the current kernel log as completely error-free.
- The live soft-mixer trial was removed. Its copy here is reference only and is not installed by setup scripts. Kernel volume/protection caps were not raised.
- The signed custom SoundWire backport remained installed. There is no stock-versus-backport comparison proving it caused the failure.

## Unknowns and limits

The trigger for the original bus clash, the exact reason speakers stayed silent, and the precise mechanism of the unexpected reboot remain unresolved. Resetting runtime hardware state through reboot is consistent with recovery but does not identify the faulty component. Current pstore is empty. Archived pstore entries exist, but were not correlated to this incident and are not evidence of this reboot's cause. No panic trace was recovered. Early firmware lookup failure followed by a successful load is not evidence that firmware remains missing.

## Follow-up and rollback information

Do not reuse live codec/card unbind or ADSP stop/start as automatic recovery: this sequence added errors and was followed by an unexpected host reboot. Preserve the working audio state. On recurrence, collect journals, sink/card state and timestamps before changing anything; include the exact `clsh` spelling in searches. Any future module comparison needs a separate planned test with a known bootable rollback.

The failed user config was moved out of the active WirePlumber directory to ~/.local/state/surface-audio/60-surface-soft-mixer.failed-*.conf. Runtime unbind/reset actions do not persist across reboot. No new kernel or firmware files were installed during this incident. Audible long-term stability and suspend/resume reliability remain unverified.

## Evidence and references

- [Saved journal evidence](reboot-journal-evidence.json): previous boot eaffbe4480614e6684035d126bfc639c; current boot 025eac43-634e-495b-b4ee-a4d4c7305eee.
- [Trial diagnostics](trials/2026-11-13-diagnosis.json).
- [Kernel AudioReach command definitions](https://raw.githubusercontent.com/torvalds/linux/master/sound/soc/qcom/qdsp6/audioreach.h).
- [Same-codec Surface Pro 11 reference](https://tangled.org/overby.me/overby.me/commit/03759aae6924e3b000a2e7f03cef85687eef2062): supporting research, not a validated Laptop 7 fix.

## Subsequent recurrence

SoundWire clash recurred at 23:56:21 after spontaneous audible recovery. See [stabilization review](STABILIZATION.md) and its saved snapshot. Reboot recovery was temporary, not a confirmed fix.
