# If the speaker goes silent again

Policy in use since 2026-11-18 (see [README.md](README.md)): the speaker SoundWire controller `6b10000.soundwire` is held at `power/control=on` by `/etc/udev/rules.d/90-surface-speaker-swr-on.rules`, which avoids the bus clash on runtime resume that caused the silence. Background: [cause](../../../docs/investigations/2026-11-14-audio-cause/README.md), [reproduction](../../../docs/investigations/2026-11-18-audio-speaker-repro/README.md).

1. Capture once in the desktop session before changing playback:

   ```sh
   bash ~/workspace/surface-laptop7-debian/drivers/files/audio/capture-state.sh --state silent
   ```

   Use `--state audible` only with the user's confirmation and note whether a stream is actually playing. Python entry point: `capture-state.py`. Captures go to `~/.local/state/surface-audio/recurrence/`.
2. Check that the controller is still held on: `cat /sys/bus/platform/devices/6b10000.soundwire/power/control` should read `on`; look for `SWR bus clsh detected` in the kernel log.
3. Do not hot-unbind codecs or cards, stop or start the ADSP, or toggle the HiFi profile off and on as a recovery: a profile-off step once coincided with a new WCD bus clash. If a module comparison is needed, use signed boot entries and keep a working entry.

RTKit is absent, so real-time scheduling is unavailable; that also holds while audio works and is not a known cause.
