# Speaker silence — held pending recurrence

User decision, 2026-11-14: pause investigation until silence recurs. Leave the controller on `auto` (3000 ms); no permanent mitigation is installed. Do not run another power-management comparison automatically.

## Capture immediately

If a video is playing silently, keep it playing long enough to capture state. Note whether its playback time keeps advancing. Avoid pause, seeking, changing volume/output, restarting services or resetting hardware before the first capture; these may remove the evidence.

Run as `console` in the logged-in desktop session, without sudo:

```sh
bash ~/workspace/surface/drivers/files/audio/capture-state.sh --state silent
```

Equivalent Python entry point:

```sh
python3 ~/workspace/surface/drivers/files/audio/capture-state.py --state silent
```

If sound returns naturally, run once with `--state audible` using the same source and volume. Use `--state unknown` for a tool check, not a report of audible success. Each run is a finite snapshot, not a background monitor. It does not record audio, media titles, URLs or keyboard input. Collection is sequential, not an atomic trace.

Output: `~/.local/state/surface-audio/recurrence/<timestamp>.json`, mode 0600, owned by the invoking user. Captures stay outside this repository until reviewed. The helper only reads PCM, selected PipeWire properties, mixer values, runtime-PM state and recent audio-related kernel messages. It does not play test audio, change volume/power, restart services or invoke sudo. Missing journal access is recorded, not treated as an error-free kernel; obtain a separate privileged log read if needed.

## Resume diagnosis

1. Compare boot ID, kernel/module versions and failure/recovery timestamps. Confirm whether PCM and the application are actually running during the silent sample. Prior samples taken after the application became idle cannot settle that point.
2. Compare controller/codecs, routing, mute and gains between silent/audible captures. Search kernel messages for `clsh` as well as `clash`, parity, retry and APM timeouts. Successful runtime resume alone does not prove sound; absence of a fresh clash alone does not clear the bus.
3. Use the [case review and proposal](diagnostics/2026-11-14/CASES-AND-PROPOSAL.md) to choose the next test. The earlier controller-only 90-second test was normal but too short to prove a fix. A longer policy change needs a new agreed scope; the prior bounded permission is exhausted.
4. Do not hot-unbind codecs/cards, reload audio modules or stop/start ADSP. Those recovery attempts previously added errors and preceded an unexpected reboot. Any later module comparison should use signed boot entries and a retained fallback.

Evidence: [2026-11-14 measurements](diagnostics/2026-11-14/README.md), [2026-11-13 incident](diagnostics/2026-11-13/README.md). Exact cause remains unconfirmed. Restart prompt: “스피커 무음 재발. surface/drivers/files/audio/RESUME.md를 읽고 현재 상태부터 수집해.”
