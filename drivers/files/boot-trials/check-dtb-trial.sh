#!/bin/bash
# After the one-shot DTB trial boot: read-only checks for the camera privacy LED and the iris decoder.
# Run as console; journal/dmesg lines need sudo (pass through when available).
echo "== boot"; cat /proc/cmdline | grep -o 'BOOT_IMAGE=[^ ]*'
S=$(secret-tool lookup purpose surface-work-sudo 2>/dev/null)
k() { if [ -n "$S" ]; then printf '%s\n' "$S" | sudo -S -p '' journalctl -k -b --no-pager; else journalctl -k -b --no-pager 2>/dev/null; fi; }
echo "== iris"; k | grep -iE 'iris|venus|vpu|aa00000' | tail -8
ls /dev/video* 2>/dev/null; for d in /dev/video*; do v4l2-ctl -d "$d" --info 2>/dev/null | grep -E 'Driver name|Card type' | tr '\n' ' '; echo " $d"; done
echo "== LED"; L=/sys/class/leds/white:camera-indicator; [ -d "$L" ] || L=$(ls -d /sys/class/leds/*camera* 2>/dev/null | head -1); echo "led=$L"
echo "idle brightness: $(cat $L/brightness 2>/dev/null)"
( cam -c1 --capture=60 >/dev/null 2>&1 & ); sleep 2; echo "streaming brightness: $(cat $L/brightness 2>/dev/null)"; sleep 4; echo "after stream: $(cat $L/brightness 2>/dev/null)"
echo "== errors"; k | grep -iE ' error|failed|probe.*-[0-9]+' | grep -viE 'xhci|wcd|soundwire' | tail -10
