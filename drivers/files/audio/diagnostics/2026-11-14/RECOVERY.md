# Speaker recovery — 2026-11-14 23:17–23:21 KST

## Applied

- Stopped PipeWire, PipeWire Pulse and WirePlumber, including both activation sockets. Confirmed speaker PCM closed and controller plus both codecs reached runtime suspend during the 10-second stop.
- Restarted the normal user audio stack. Restored physical Speaker output, unmuted, at its original 35% volume.
- Applied `user/51-surface-speaker-no-idle.conf` under `~/.config/wireplumber/wireplumber.conf.d/`. Live sink properties confirm `session.suspend-timeout-seconds=0` and `node.pause-on-idle=false`. PCM stays running while the sink is idle.
- Switched the standard card profile `HiFi -> off -> HiFi` to reapply UCM routing. Kept the original volume and physical output.

The user reported **still silent** after the complete service restart and after profile reapplication. Left/right PulseAudio playback completed successfully; that is not evidence of audible output. The first pw-play attempt timed out after 15 seconds; PipeWire clients also reported a roughly 25-second RTKit D-Bus delay. Subsequent paplay tests completed in about 1.6 seconds each. Do not equate the client timeout with a proven hardware hang. No new kernel entries were returned for the 10-minute window ending 23:18:33.

## Next action

A normal reboot was explicitly announced and accepted by shutdown at 23:22:58 KST, scheduled for 23:23:58 KST on 2026-11-14. Pre-reboot boot ID: 025eac43-634e-495b-b4ee-a4d4c7305eee. This document does not assert that the reboot has completed or that sound is restored. Verify the new boot ID and ask for audible confirmation after login. Keep the idle policy for pause/restart testing if sound returns. If not, compare the signed stock/custom SoundWire modules through a retained boot fallback; do not hot-unbind hardware or stop/start ADSP.

The idle policy is a **mitigation under evaluation**, not a confirmed kernel fix. It keeps the speaker PCM/DSP path open after playback and can increase idle battery draw. Runtime power/control remains auto on the controller and codecs; no global power policy changed. System sleep is separate and still needs validation. No gain/protection overrides, new modules, firmware or boot files were installed.

## Reproduce and undo

The driver SH entry point installs this configuration, and its Python entry point calls the same SH script. No downloads or new packages are needed. The installed rule matches only the physical Surface speaker sink; other outputs retain their idle policies.

To remove the mitigation:

```sh
rm ~/.config/wireplumber/wireplumber.conf.d/51-surface-speaker-no-idle.conf
systemctl --user restart wireplumber.service
```

Source semantics: [WirePlumber ALSA configuration](https://pipewire.pages.freedesktop.org/wireplumber/daemon/configuration/alsa.html). The default idle timeout is 5 seconds; 0 disables suspension and leaves the ALSA device busy. Existing node.pause-on-idle=false alone did not prevent the session manager's idle timeout.

Private state captures remain under `~/.local/state/surface-audio/`; no media audio or secrets are included in this bundle.

## Post-reboot verification

The scheduled reboot completed and the user confirms sound works. The new boot uses the same signed kernel/module. Log review found an additional WCD-bus clash at the prior profile-off step; avoid repeating that action as automatic recovery. See [POST-REBOOT.md](POST-REBOOT.md) for the exact timeline and limits. Idle mitigation effectiveness remains unproven beyond this short observation.
