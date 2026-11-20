#!/bin/bash
# Passive logger for the SSAM -110 fault (the EC UART stops transmitting). Every 10 s it reads the EC UART (b88000,
# ttyHS0) byte counters and appends a line when they change. The EC sends input and status events on its own, so RX
# growing while TX stays flat is normal between requests; the fault marker is the kernel's own SSAM timeout, so every
# new "surface_serial_hub ... -110" kernel message is logged with the counters at that moment (FAULT).
# It only reads; it never writes to the UART, rebinds or resets anything.
set -u
log=/var/log/surface-ssam-uart-watch/uart.log; mkdir -p "${log%/*}"
echo "$(date -Is) start boot=$(cat /proc/sys/kernel/random/boot_id) cmdline=$(cat /proc/cmdline)" >> "$log"
counters() { local l; l=$(grep "MMIO:0x0000000000b88000" /proc/tty/driver/qcom_geni_uart) || return 1
  echo "tx=$(sed -n 's/.* tx:\([0-9]*\).*/\1/p' <<<"$l") rx=$(sed -n 's/.* rx:\([0-9]*\).*/\1/p' <<<"$l") flags=${l##* }"; }
journalctl -k -f -n 0 -o short-iso --no-pager 2>/dev/null | grep --line-buffered -E "surface_serial_hub.*-110|ssam.*-110" |
  while read -r line; do echo "$(date -Is) FAULT $(counters) | ${line#* }" >> "$log"; done &
prev=""
while sleep 10; do
  c=$(counters) || continue
  [ "${c%% flags*}" = "${prev%% flags*}" ] && continue
  echo "$(date -Is) $c" >> "$log"; prev=$c
done
