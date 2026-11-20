# Diagnostic services installed on the Surface

Temporary, read-only collectors. Each one only reads state and writes logs; none of them changes, rebinds or resets a
device. Remove all of them with `pkexec bash drivers/files/diagnostics/remove-all.sh` (add `--purge-logs` to delete
their logs too). Add every new diagnostic service to this table and to `units` in `remove-all.sh`.

| Unit | Installed | Files | Logs | Purpose | Source |
| --- | --- | --- | --- | --- | --- |
| `surface-usbc-watch.service` | 2026-11-20 | `/usr/local/sbin/surface-usbc-watch`, `/etc/systemd/system/surface-usbc-watch.service` | `/var/log/surface-usbc-watch/` (last 20 snapshots) | Snapshot every USB layer when a Type-C partner stays attached with no USB device for 15 s | `drivers/files/usb/usbc-watch/` |
| `surface-ssam-uart-watch.service` | 2026-11-20 | `/usr/local/sbin/surface-ssam-uart-watch`, `/etc/systemd/system/surface-ssam-uart-watch.service` | `/var/log/surface-ssam-uart-watch/uart.log` | Log the EC UART TX/RX counters every 10 s (changes only); `FAULT` lines carry each kernel SSAM -110 message with the counters at that moment | `drivers/files/diagnostics/ssam-uart-watch/` |

## Finding that started the SSAM logger (2026-11-20)

In boot 2026-11-20 10:03 (sync_state trial) 7 of 8 suspend attempts failed in `ssam_serial_hub_pm_prepare` with
`display-off notification failed: -110`; the 10:11 resume also logged `D0-entry`/`display-on` -110. Reading the fan
through the EC timed out as well. Across one request the EC UART (`b88000`, irq 153) TX counter stayed at 877 bytes
while RX kept rising, so the EC is talking but the Surface stopped transmitting early in the boot. Clocks
(`gcc_qupv3_wrap0_s2_clk` 64 MHz) and interconnect votes were present and CTS was asserted. The 15 boots before showed
no -110. The USB-C port that died after the 10:11 resume may be a consequence (the EC never heard D0-entry).

Correction (2026-11-20 14:30): the first logger version marked `STALL` whenever TX stayed flat while RX grew. That is
normal: the EC sends input and status events on its own and the Surface transmits only for requests. After the 14:22
reboot it marked STALL within 20 s while an EC request (fan speed) still worked and TX rose 355 -> 383. The 10:30
measurement stands (a request timed out and TX did not move), but the logger cannot tell when that began. The logger
now records kernel SSAM -110 messages as `FAULT` with the counters at that moment.
