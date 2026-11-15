# Audio

The active output uses the physical ALSA speaker sink directly. The separate Windows EQ virtual sink was removed at the user's request. Its configuration and source data remain under optional-windows-eq for reference; setup.sh does not activate or install this optional filter.

Live filter backup: ~/.local/state/surface-audio/50-surface-speakers.conf.disabled. PipeWire and WirePlumber were restarted and the physical speaker sink was selected. Volume was preserved at 35% during the 2026-11-14 recovery. Headphones remain a separate physical output.

Intermittent silence coincided with SoundWire bus clashes and WSA884x parity errors. Removing the filter simplifies routing but is not proof that those kernel faults are fixed. Audible stability still needs confirmation.

## 2026-11-13 incident

Sound returned after an unexpected host reboot following the agent's live ADSP recovery attempt. Original SoundWire bus clashes were initially missed; subsequent codec/card resets introduced additional DSP timeouts, runtime-PM warnings and parity errors without restoring sound. The exact reboot mechanism and original fault trigger remain unresolved. Do not repeat live hardware resets as automatic recovery.

The soft-mixer trial failed and was removed from the active user configuration. Trial files here are reference only, not installed by setup scripts. PA gain 1/1 is also present with working sound after reboot and is not a sufficient diagnosis. No kernel or firmware files were changed during these attempts.

See the [incident timeline, failed actions, evidence and follow-up](diagnostics/2026-11-13/README.md). This supersedes the initial “no kernel errors” assessment and the pending soft-mixer test status.

## Current recovery — 2026-11-14

Full user audio service/socket shutdown and restart, followed by HiFi profile reapplication, did not restore sound according to the user. An exact-speaker no-idle policy is now applied and included in drivers/setup.sh; it prevents repeated PCM close/resume transitions but is not a verified cure and may increase idle power. A normal scheduled reboot restored sound, confirmed by the user on 2026-11-14. Long-term stability remains pending. See [applied settings, results and rollback](diagnostics/2026-11-14/RECOVERY.md) and [resume instructions](RESUME.md). No hot hardware resets or module changes were made.

Post-reboot analysis: [same-kernel recovery, matched mixers and distinct WCD-bus recovery error](diagnostics/2026-11-14/POST-REBOOT.md). The selected mixer controls match between silent and recovered states. Avoid repeating profile toggles as automatic recovery.
