# Intermittent speaker silence: cases and proposed remedy

Reviewed 2026-11-14. Research only: no new live audio settings, resets or modules were applied. See [local measurements](README.md) and [the recovery incident](../2026-11-13/README.md).

## Assessment

The leading hypothesis is a SoundWire controller clock-stop/resume problem after playback becomes idle. It is not a confirmed unique code defect. The local sequence was stream idle → PCM closed after about 5 seconds → controller/codecs suspended about 3 seconds later. Resuming playback must restore that path. The observed bus clash supports a lower-level fault, but it was not captured at every audible failure.

The 90-second controller-only `on` trial was reported normal; after restoring `auto`, the user reported normal playback, renewed silence and recovery. Only one complete codec idle/resume cycle occurred during the `on` interval. Later failure reports were not precisely aligned with running-PCM captures. Application-side stream stoppage remains possible. Successful runtime-resume return values do not establish audible output.

`auto` permits runtime power management; it is a normal policy, not itself a defect. The archived base driver already enables 3000 ms autosuspend. There is no first-install sysfs snapshot. Current readback remains `auto`, `3000`; loaded SoundWire srcversion is `3D22555E212EACB6FA11473`.

## Comparable reports and applicability

| Primary report | Reported remedy and evidence | Relevance here |
| --- | --- | --- |
| [X1E80100/Glymur IRQ/clock race, 2026-10-09](https://lkml.iu.edu/2610.1/02715.html); [developer review](https://lkml.iu.edu/2610.1/02745.html) | IRQ handling overlaps clock gating, causing intermittent clock-stop exit errors and detached speakers. The v2 change disables the IRQ before gating and enables it after restoring the clock; it received Reviewed-by. | Closest documented mechanism. The archived base source already contains these changes, and the retained custom patch preserves them. Reapplying this patch is not a new fix. This does not prove the same remaining defect on this Surface. |
| [ThinkPad X13s Qualcomm SoundWire stability series, 2023-02-09](https://lkml.iu.edu/2302.1/02033.html) | Author reported stable audio after codec changes plus synchronization, FIFO and bus-clash fixes around runtime suspend/resume. | Demonstrates this failure class and an actual stability report, but uses a different SoC/codec combination. Our source already has FIFO draining and interrupt/frame-generator handling; the old series is not an identified missing patch. |
| [Snapdragon Surface Laptop 7 audio support, issue 2](https://github.com/bryce-hoehn/linux-surface-laptop-7/issues/2) | Contributors describe enabling audio through upstream ALSA UCM profiles. | Exact model, but basic enablement rather than a demonstrated cure for pause/restart silence. Our Speaker profile already exists and produces sound. |
| [Surface Pro 11 gain/routing change](https://tangled.org/overby.me/overby.me/commit/03759aae6924e3b000a2e7f03cef85687eef2062) | Removes hardware-volume ownership from the sound server and reapplies routing after system resume. Author verified configuration generation, explicitly leaving lasting audio stability unverified. | Same WSA884x family, different machine. Our soft-mixer/gain trial failed to restore sound; PA 1/1 occurs in audible and silent states. Do not copy the Pro 11 channel/routing settings or present this as a proven cure. |

A separate [Surface Pro 11 alsactl boot-race diagnosis](https://github.com/ooaklee/linux-surface-pro-11-oe/blob/main/docs/adr/adr-0035-audio-boot-race-alsactl.md) is marked superseded. Its correction identifies opcode `0x01001021` as GET_SPF_STATE, not GRAPH_OPEN, and rejects masking distribution ALSA state services. Old search excerpts are not evidence that the original diagnosis was valid.

No independently verified, exact-model cure for this particular intermittent symptom was established by this search. Public patch review, successful configuration parsing and a completed hardware reliability test are different evidence levels.

## Recommended order

1. **Validate the narrow mitigation already tried.** In a separately authorized longer comparison, keep only `6b10000.soundwire/power/control=on` for 15–30 minutes, with the same playback source/volume and at least 20 pause/restart cycles including pauses longer than 10 seconds. Record audible failure times, stream/PCM state, controller state and new errors. The duration and cycle count are a proposed test plan, not a proven reliability threshold. Preserve codec power policies and amplifier protection limits. Restore `auto` at the end or on failure. No ADSP/card reset is part of this test.
2. **Persist only after evidence.** If repeat testing supports it, make a rule scoped to this exact controller and machine. Measure idle battery draw under matched conditions before calling the trade-off acceptable. Check whole-system sleep/resume separately: runtime PM and system sleep are different paths. Holding the bus on may cost power and does not repair state already damaged before the change. This would be a mitigation, not a kernel root-cause fix.
3. **If it still fails, compare the driver at boot.** Compare the packaged SoundWire module with the current additional backport using the same kernel/configuration, signed modules and a retained boot fallback. Do not hot-unbind the card or stop ADSP. The extra patch is a variable to isolate, not an established culprit. Select a further kernel change only after locating a missing relevant fix or a specific reproduced defect.

A secondary isolation test could disable only the speaker node's WirePlumber idle suspension (`session.suspend-timeout-seconds=0`). This keeps more of the PCM/audio path open and may use more power than the controller-only trial; it was not tested here. Existing `node.pause-on-idle=false` does not disable the session manager's delayed suspension. Merely extending the 3-second kernel delay would reduce transitions, but cannot solve failures after longer pauses.

## Scope and rollback

No permanent workaround, gain increase, ALSA-state deletion, module replacement, service restart or reboot was performed in this research. The previous temporary change was restored. Existing Secure Boot signing and CPU/display policies are untouched. The exact failure in this machine remains unresolved.

Official semantics: [Linux runtime PM](https://docs.kernel.org/power/runtime_pm.html), [PipeWire node and session properties](https://docs.pipewire.org/page_man_pipewire-props_7.html). Local source: `patches/files/sources/drivers/soundwire/qcom.c`; existing backport: `patches/files/patches/02-soundwire-qcom-v2-backport.patch`. These summaries and local evidence are available offline; the linked upstream pages require network access. No new payload was downloaded or installed.
