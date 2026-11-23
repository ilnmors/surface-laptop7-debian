# Runtime Wi-Fi recovery — 2026-11-12

- Original ath12k A98E5140E078A5920DAC05E was active; neither rfkill block was set.
- Authentication had succeeded before repeated beacon loss, a stuck pending scan and a transmit queue flush failure. This does not establish a bad password.
- Reloaded the existing ath12k_wifi7 and ath12k modules, retaining USB tethering. No candidate module or connection secret was installed or changed.
- Reconnection authenticated successfully, acquired DHCP and returned HTTP 200 from https://www.debian.org with curl explicitly bound to wlP4p1s0.
- Regulatory update timeout also occurred during reconnection. Recovery is confirmed; the underlying recurring firmware/driver fault is not resolved.
- If repeated, capture logs first. The regulatory candidate preserving both Surface rfkill guards remains a separate unvalidated trial.
