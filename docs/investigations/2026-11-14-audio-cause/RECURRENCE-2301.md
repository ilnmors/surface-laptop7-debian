# Speaker silence recurrence — 2026-11-14 23:01–23:08 KST

## Result

The user confirmed that playback time advances while the speakers remain silent. This recurrence has a running-PCM capture and nonzero speaker-monitor samples, unlike the earlier idle snapshots. Application pause, a muted stream, and an idle/closed PCM do not explain the captured state. The fault is narrowed toward the path after the software speaker monitor (ALSA/DSP/SoundWire/codec/amplifier), but the defective component and trigger remain unconfirmed.

No recovery was attempted. Controller/codecs remain `auto`, 3000 ms. No service restart, gain/routing change, module reload, hot-unbind, ADSP operation or reboot was performed. The digital output monitor was opened twice for three seconds; only aggregate levels were saved, not audio or media metadata. A monitor connection is an observation, not a hardware-output measurement.

## Evidence

| Time (KST) | Observation |
| --- | --- |
| 23:01:55 | First snapshot: PCM1 RUNNING; PipeWire/ALSA control access was sandbox-restricted. Do not interpret the failed control reads as missing hardware. |
| 23:02:22 | Desktop-access snapshot: Firefox and physical Speaker sink running, both links active; stream/sink mutes off; PCM1 RUNNING. |
| 23:03:37 | Same running stream and PCM trigger time; data pointers continue advancing. Audibility was not separately reconfirmed at this instant. |
| 23:07:02–23:07:05 | Immediately after the user reconfirmed silence, before/after snapshots show Firefox and Speaker running. PCM hardware pointer advances by 149,280 frames in 3.11 s (48 kHz). |
| 23:07:02–23:07:05 | Physical speaker monitor contains nonzero digital samples: L/R RMS 0.0641/0.0837 and peaks 0.7382/0.9628. These are digital monitor values, not measured acoustic output. |
| 23:07:56 | Privileged kernel search since 22:50 finds no matching fresh SoundWire/WSA/APM/ADSP/parity/suspend messages. The earlier full-boot query succeeded. |

PA gains are 1/1, digital gains 81/81, digital mute off; these also occurred in previously audible states. The output is the physical Speaker sink, not the removed Windows EQ sink. Between 23:02:22 and 23:07:05 the controller and both speaker codecs remain active; their suspended-time counters do not advance. The continued silence is therefore not explained by these devices currently being asleep. A previous failed transition could still have left bad state; this capture does not prove that hypothesis.

## Same-boot faults and interpretation

The same boot records SoundWire `SWR bus clsh detected` at **2026-11-13 23:56:21** and **2026-11-14 00:12:52**. The second event was outside the previous short comparison. Neither timestamp matches this 23:01 recurrence. The boot-time APM timeout is also old. Several system-sleep cycles occurred later; the last recorded wake was 21:45:47, over an hour before this report. Do not call this an immediately observed sleep-resume failure.

The archived driver masks the clash interrupt when it handles a clash and re-enables it on the relevant runtime-resume path. A lack of a new message cannot prove a healthy bus; it also cannot prove an unlogged clash occurred now. No live interrupt-mask/register read was performed.

## Next discriminating step

Compare the same captures when sound returns naturally. Then, if a new bounded comparison is agreed, test the already proposed controller-only `on` policy over repeated ordinary pause/restart cycles with automatic restoration. Holding an already-active controller on is not a demonstrated cure for the current silent state. Keep codec policies and amplifier protection unchanged. If that comparison fails, retain a signed boot-time stock/custom driver comparison as a separate option; do not repeat live hardware resets.

Machine-readable, privacy-reviewed evidence: [recurrence-2301-evidence.json](recurrence-2301-evidence.json). Original snapshots and complete filtered kernel output remain in the console user's private state directory. This update is local and uncommitted.
