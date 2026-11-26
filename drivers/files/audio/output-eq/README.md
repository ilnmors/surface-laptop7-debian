# Per-output EQ

`output-eq.py` applies an [AutoEq](https://github.com/jaakkopasanen/AutoEq) `ParametricEQ.txt` to one audio output, for example a Bluetooth headset. No EQ values are kept here: pick the file for your headphones from AutoEq's `results/` (or write your own in the same format).

- Each EQ is a WirePlumber smart filter (`filter.smart.target`) loaded by the user's `filter-chain.service`. It is inserted only in front of its target sink; other outputs (speakers, the headphone jack) stay unfiltered. When the target disconnects the filter is skipped, and it returns when the device reconnects.
- Uses only PipeWire's built-in `param_eq` (PipeWire 1.4, WirePlumber 0.5); nothing is installed.
- Changes only `~/.config/pipewire/filter-chain.conf.d/60-output-eq-<name>.conf` and `~/.config/pipewire/eq/<name>.txt`, then restarts `filter-chain.service`. Not run by `setup.sh`.

```
drivers/files/audio/output-eq/output-eq.py list
drivers/files/audio/output-eq/output-eq.py set <name> --sink <node.name> --file <ParametricEQ.txt>
drivers/files/audio/output-eq/output-eq.py remove <name>
```

- `set` checks the file (only `Preamp:` and `Filter N:` lines) and that the sink is connected; `--force` targets a sink that is offline now. Running `set` again with the same name replaces that EQ.
- A Bluetooth A2DP sink is named `bluez_output.<MAC with _>.1`; the headset profile (HFP) uses a different sink, so the EQ applies to music playback, not calls.
- The AutoEq `Preamp` lowers the level to avoid clipping; raise the volume to compensate.
- Rollback: `output-eq.py remove <name>`, or delete the `.conf` file and run `systemctl --user restart filter-chain`.

Tested 2026-11-26 with a Sony WH-CH720N over A2DP (SBC): the Firefox stream was linked through the filter to the headset sink; malformed files, bad names and absent sinks were refused; `remove` restored the plain routing.
