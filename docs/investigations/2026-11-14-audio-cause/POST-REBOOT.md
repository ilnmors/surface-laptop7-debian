# Speaker recovery: reboot log comparison

2026-11-14, checked 23:26–23:28 KST. **The user confirms audible playback after reboot.** Long-term stability is not established.

## What the evidence supports

The strongest working explanation is a persistent failure in the kernel/DSP/SoundWire/codec output path. Before reboot, Firefox sent nonzero digital samples and ALSA PCM advanced while the user heard silence. Full audio service/socket restart and normal HiFi profile reapplication both failed. With the same kernel and SoundWire module, a normal reboot restored audible sound.

This does not isolate a particular firmware function, bus transaction or amplifier defect. It also does not prove runtime autosuspend caused the failure. Reboot resets several layers at once; there was no synchronized new speaker-bus error at the 23:07 silent capture.

## Timeline and responsibility

| Time (KST) | Observation | Interpretation |
| --- | --- | --- |
| Nov 13 23:56:21; Nov 14 00:12:52 | `6b10000.soundwire: SWR bus clsh detected` | Real historical errors on the WSA884x speaker bus, not timestamps for the latest silence. |
| Nov 14 23:07 | User-confirmed silence, running PCM and nonzero output-monitor samples | App was sending audio; digital playback success did not imply audible output. |
| 23:17 | All user audio services/sockets stopped; PCM closed, controller/codecs suspended; restarted | User still heard nothing. Normal service recovery failed. |
| 23:20:42.321 | `6ad0000.soundwire: SWR bus clsh detected` at the HiFi profile-off step | New error coinciding with the assistant's recovery action. Sysfs maps this bus to WCD9380, distinct from the WSA884x speaker bus. It cannot explain the earlier silence. Do not repeat this profile toggle as an automatic recovery. |
| 23:23:58.717 | logind: scheduled reboot begins | Matches the explicitly announced `shutdown -r +1`. |
| 23:24:00.068–.117 | reboot.target reached, filesystems syncing, journal stopped | Normal orderly shutdown; no evidence of an unrequested crash in this transition. The watchdog warning occurs during this requested shutdown. |
| 23:24:15 onward | New boot; ADSP firmware loads and processor is up | Same signed kernel/module. User confirms sound now works. No SoundWire clash/parity errors in the current-boot query ending 23:27:09. |

## Warnings that do not explain this silence by themselves

- ADSP firmware initially returns ENOENT, then the same boot successfully loads the 21,940,664-byte image and starts ADSP. Present on both boots; not evidence of permanently absent audio firmware.
- APM opcode `1001021` times out once during initialization on both boots, including the now-audible boot. It is not sufficient evidence for this intermittent failure.
- `rtkit` is not installed (`dpkg` status `un`). PipeWire, WirePlumber and GNOME report RealtimeKit unavailable; audio data-loop threads currently use normal `TS` scheduling. This is a separate scheduling deficiency, not a sufficient explanation for this persistent silence: playback is now audible with the warning still present. No RTKit installation or audio restart was performed during this log check.

## Current state and limits

- Kernel `7.3.0-31-qcom-x1e`; loaded SoundWire srcversion `3D22555E212EACB6FA11473`, identical before/after. Secure Boot is enabled. Default signed image and `cma=0` are active.
- All eight captured hardware mixer controls match the silent sample, including PA 1/1, digital mute off, RX volume 81 and speaker routing. The user-facing volume is now 9%, not the pre-reboot 35–39%; it was left unchanged. The post-reboot snapshot is idle after the user's audible confirmation, not a synchronized same-volume playback A/B recording.
- The exact speaker rule `session.suspend-timeout-seconds=0` remains active, with `node.pause-on-idle=false`. PCM continues running between streams. This avoids repeated idle closure, but is a mitigation under evaluation and may increase idle power. Controller and codec power/control remain `auto`, 3000 ms.
- Read-only inspection this turn; no test audio, service restart, driver reset or further reboot. Do not hot-unbind audio hardware or restart ADSP. Observe normal use and pause/restart behavior; collect a finite snapshot only if silence returns.

[Recovery steps and rollback](RECOVERY.md) · [prior silent evidence](RECURRENCE-2301.md) · [WirePlumber idle policy semantics](https://pipewire.pages.freedesktop.org/wireplumber/daemon/configuration/alsa.html).
