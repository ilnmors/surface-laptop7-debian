# Audio

The active output uses the physical ALSA speaker sink directly. The separate Windows EQ virtual sink was removed at the user's request. Its configuration and source data remain under optional-windows-eq for reference; setup.sh does not activate or install this optional filter.

Live filter backup: ~/.local/state/surface-audio/50-surface-speakers.conf.disabled. PipeWire and WirePlumber were restarted and the physical speaker sink was selected. Current volume is 30%. Headphones remain a separate physical output.

Intermittent silence coincided with SoundWire bus clashes and WSA884x parity errors. Removing the filter simplifies routing but is not proof that those kernel faults are fixed. Audible stability still needs confirmation.

## 2026-11-13 incident

Sound returned after an unexpected host reboot following the agent's live ADSP recovery attempt. Original SoundWire bus clashes were initially missed; subsequent codec/card resets introduced additional DSP timeouts, runtime-PM warnings and parity errors without restoring sound. The exact reboot mechanism and original fault trigger remain unresolved. Do not repeat live hardware resets as automatic recovery.

The soft-mixer trial failed and was removed from the active user configuration. Trial files here are reference only, not installed by setup scripts. PA gain 1/1 is also present with working sound after reboot and is not a sufficient diagnosis. No kernel or firmware files were changed during these attempts.

See the [incident timeline, failed actions, evidence and follow-up](diagnostics/2026-11-13/README.md). This supersedes the initial “no kernel errors” assessment and the pending soft-mixer test status.

## Current decision — 2026-11-14

Held at the user’s request until silence recurs; no permanent fix established. Use the [resume procedure and read-only capture helper](RESUME.md) before changing playback or audio state. The current runtime-PM policy remains auto.
