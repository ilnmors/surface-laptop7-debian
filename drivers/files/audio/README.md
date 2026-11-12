# Audio

The active output uses the physical ALSA speaker sink directly. The separate Windows EQ virtual sink was removed at the user's request. Its configuration and source data remain under optional-windows-eq for reference; setup.sh does not activate or install this optional filter.

Live filter backup: ~/.local/state/surface-audio/50-surface-speakers.conf.disabled. PipeWire and WirePlumber were restarted and the physical speaker sink was selected. Current volume is 30%. Headphones remain a separate physical output.

Intermittent silence coincided with SoundWire bus clashes and WSA884x parity errors. Removing the filter simplifies routing but is not proof that those kernel faults are fixed. Audible stability still needs confirmation.
