# Preserved-baseline ath12k build

Original A98E5140E078A5920DAC05E is reproduced from the saved source plus both Romulus13/WCN7850 rfkill guards. Adding upstream f2576dc0 produces D044C56077CC5357DC3F5BF. Shared import CRCs were checked. The signed candidate is loaded, unblocked, authenticated and passed repeated Wi-Fi-bound HTTPS 200 checks. The offline rebuild script reproduced its srcversion again.

The patch completes a regulatory update even when its event is dropped, preventing a false wait timeout. It does not prove the cause of beacon loss or fix every transmit failure. Original source and both guard patches remain available. Rejected D61DA424018CF1563587D2E must not be installed.

Local sequence: successful EAP → beacon loss → repeated reassociation/scans → pending scan loop → one transmit queue flush failure. EAP succeeded again after reload. A password error is not established. No continuous data/beacon samples were collected during the initial failure, so AP beacon loss cannot be separated conclusively from firmware/driver loss.

Primary sources:
- https://git.zx2c4.com/linux-rng/commit/drivers/net/wireless/ath?id=f2576dc0f894ef33045ba7ed057ec417988bba8a
- https://lore-kernel.gnuweeb.org/ath12k/01da3719-51c4-4f0d-a3f9-f0e5c95dbb80@oss.qualcomm.com/T/ — same chipset and firmware, similar resume symptoms, unresolved.
- https://lore-kernel.gnuweeb.org/linux-wireless/0bd012e7-4115-4401-b067-1ab616918729@0pe.de/T/ — initial regression claim was RETRACTED after another client lost the same AP beacons. Do not cite it as a confirmed kernel regression.

Next recurrence: correlate station beacon counters and Wi-Fi-bound reachability before reload. Power save remains on; disabling it did not solve the published same-firmware case. Long-term and post-suspend validation remain pending.
