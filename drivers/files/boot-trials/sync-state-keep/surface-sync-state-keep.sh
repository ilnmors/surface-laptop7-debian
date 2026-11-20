#!/bin/bash
# At shutdown: keep booting the sync_state trial entry only while it stays clean. If this boot used
# fw_devlink.sync_state=timeout and its kernel log has no SSAM -110 and no USB controller setup failure, re-arm the
# one-shot GRUB flag so the next boot uses the trial entry again; otherwise leave it unarmed (next boot = default).
set -u
env=/boot/secureboot/trial-sync-state-20261117/grubenv
log=/var/log/surface-sync-state-keep.log
grep -q "fw_devlink.sync_state=timeout" /proc/cmdline || { echo "$(date -Is) default boot; flag left as is" >> $log; exit 0; }
bad=$(journalctl -k -b --no-pager -q | grep -E "surface_serial_hub.*-110|ssam.*-110|xhci-hcd.*can't setup: -110" | head -3)
if [ -n "$bad" ]; then
  echo "$(date -Is) sync_state boot had a fault; flag NOT re-armed (next boot = default): $(tr '\n' ' ' <<<"$bad" | cut -c1-300)" >> $log
else
  grub-editenv "$env" set surface_trial_next=1 && echo "$(date -Is) sync_state boot clean; flag re-armed" >> $log
fi
