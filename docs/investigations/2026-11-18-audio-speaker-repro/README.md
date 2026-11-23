# Speaker silence reproduction — 2026-11-18

Automated loop (`spk-repro.sh`): suspend the speaker sink with `pactl suspend-sink` (closes the PCM), wait 1–10 s (the speaker SoundWire controller `6b10000.soundwire` autosuspends after 3 s), reopen with a 0.8 s 1.5 kHz tone at 25% volume and detect it on the internal microphone (Goertzel at 1.5 kHz vs 1.1/1.9 kHz; silent if the ratio < 8, normal ratios 80–600). On a silent cycle it saves the recording, runtime PM states, PCM status and SoundWire kernel lines. The installed no-idle WirePlumber rule was not changed.

| Run | Controller policy | Cycles | Silent | SoundWire clashes in the window |
| --- | --- | --- | --- | --- |
| auto400 (18:36–19:20) | `auto` (runtime suspend 3 s) | 400 (258 resumed from suspended) | 6 real (2 events × 3 cycles) + 1 noise false positive | **6b10000 ×2**, 6ad0000 ×10 |
| on400 (20:49–21:35) | `on` (held active) | 400 | **0** | **none** |

- Both silence events start within one second after `qcom_swrm_irq_handler: SWR bus clsh detected` on **6b10000** (18:40:01.7 → 18:40:02, 18:42:31.6 → 18:42:32). During silence the PCM is RUNNING and every SoundWire master/codec is `active`; sound returns after the next controller suspend/resume (~10 s, 3 cycles). Clashes on 6ad0000 never silenced the speakers.
- Holding only the speaker controller active removed both the clashes and the silence over 400 cycles; its awake cost is within measurement noise (3.73 vs 3.74 W, ADSP still idles at ~103 entries/s).
- Conclusion: the 2026-11-14 silence is a SoundWire bus clash on the speaker bus during controller runtime resume; the speaker bus stays broken until the next resume.
