# Speaker recovered after scheduled reboot — observation pending

Read [the reboot comparison](diagnostics/2026-11-14/POST-REBOOT.md). On 2026-11-14 the user confirmed sound after the scheduled 23:24 reboot. Current boot ID: `ad5da1de-571e-4655-9cd2-259a4ef0dab5`. Same signed kernel and SoundWire module; all eight selected hardware mixer controls match the silent sample.

Keep the physical speaker idle timeout at 0 for normal-use observation. It prevents repeated PCM closure, but is not a proven root-cause fix and may increase idle power. Runtime PM remains auto/3000 ms. Preserve the user's current volume (9% at the check), rather than forcing an old test volume.

Do not repeat HiFi off/on as automatic recovery: a new WCD-bus clash coincided with the previous profile-off step. Never hot-unbind codecs/cards or stop/start ADSP. If another module comparison becomes necessary, use signed boot entries and a retained fallback.

On recurrence, capture once in the console desktop session before changing playback:

```sh
bash ~/workspace/surface/drivers/files/audio/capture-state.sh --state silent
```

Use `audible` only with user feedback and note whether a stream is actually playing; the current post-reboot audible-labelled sample is idle after user confirmation. Python entry point: `capture-state.py`. Private captures are under `~/.local/state/surface-audio/recurrence/`.

No new runtime settings were changed in the post-reboot log check. RTKit is absent and real-time scheduling is unavailable; that separate finding also exists with audible playback, so it is not established as the cause of this persistent silence.
