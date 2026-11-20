#!/bin/bash
# Passive collector for the USB-C USB2 "dead port" fault: when a Type-C partner is attached but no USB device has
# enumerated on that port for 15 s, save one snapshot of every layer. It never rebinds or resets anything.
set -u
out=/var/log/surface-usbc-watch
declare -A ctrl=([0]=a600000 [1]=a800000) rep=([0]=1-07 [1]=1-0a) since=() done=()
mkdir -p "$out"
snapshot() { # port index, seconds without a device
  local i=$1 c=${ctrl[$1]} d; d="$out/$(date +%Y%m%d-%H%M%S)-port$i"; mkdir -p "$d"
  { echo "port$i ${c}.usb partner attached, no USB device for $2 s"; date -Is; uname -r; cat /proc/cmdline; } > "$d/summary.txt"
  for t in /sys/class/typec/port$i /sys/class/typec/port$i-partner; do
    [ -d "$t" ] && for f in "$t"/*; do [ -f "$f" ] && [ -r "$f" ] && printf '%s: %s\n' "$(basename "$f")" "$(tr '\n' ' ' < "$f" 2>/dev/null)"; done > "$d/$(basename "$t").txt"
  done
  for s in /sys/class/power_supply/ucsi*; do printf '%s status=%s online=%s type=%s\n' "$(basename "$s")" "$(cat "$s/status")" "$(cat "$s/online")" "$(cat "$s/usb_type" 2>/dev/null)"; done > "$d/ucsi.txt"
  lsusb -t > "$d/lsusb-tree.txt" 2>&1
  for x in /sys/devices/platform/soc@0/${c}.usb/xhci-hcd.*.auto; do
    h=/sys/kernel/debug/usb/xhci/$(basename "$x"); [ -d "$h" ] && find "$h" -maxdepth 3 -type f \( -path "*ports*" -o -name "reg-*" \) -exec sh -c 'for f; do printf "== %s\n" "$f"; cat "$f" 2>/dev/null; done' _ {} + > "$d/xhci-debugfs.txt"
  done
  [ -d "/sys/kernel/debug/${c}.usb" ] && for f in /sys/kernel/debug/${c}.usb/*; do [ -f "$f" ] && { printf "== %s\n" "$f"; timeout 2 cat "$f" 2>/dev/null; }; done > "$d/dwc3-debugfs.txt"
  grep -E "^fd[0-9a-f]{2}:" "/sys/kernel/debug/regmap/${rep[$i]}/registers" > "$d/repeater-${rep[$i]}.txt" 2>/dev/null
  journalctl -k -b -n 400 --no-pager > "$d/kernel.log" 2>&1
  ls -1dt "$out"/*-port* 2>/dev/null | tail -n +21 | xargs -r rm -rf
}
while sleep 5; do
  for i in 0 1; do
    c=${ctrl[$i]}
    if [ ! -d /sys/class/typec/port$i-partner ]; then since[$i]=0; done[$i]=0; continue; fi
    if ls -d /sys/devices/platform/soc@0/${c}.usb/xhci-hcd.*.auto/usb*/*-1 >/dev/null 2>&1; then since[$i]=0; done[$i]=0; continue; fi
    since[$i]=$(( ${since[$i]:-0} + 5 ))
    if (( since[$i] >= 15 )) && (( ${done[$i]:-0} == 0 )); then snapshot "$i" "${since[$i]}"; done[$i]=1; fi
  done
done
