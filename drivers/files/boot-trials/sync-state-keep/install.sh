#!/bin/bash
# Root: install the shutdown-time sync_state keeper. Undo: systemctl disable --now surface-sync-state-keep;
# rm /usr/local/sbin/surface-sync-state-keep /etc/systemd/system/surface-sync-state-keep.service;
# grub-editenv /boot/secureboot/trial-sync-state-20261117/grubenv set surface_trial_next=0
set -euo pipefail
here=$(dirname "$(realpath "$0")")
install -m755 "$here/surface-sync-state-keep.sh" /usr/local/sbin/surface-sync-state-keep
install -m644 "$here/surface-sync-state-keep.service" /etc/systemd/system/surface-sync-state-keep.service
systemctl daemon-reload; systemctl enable --now surface-sync-state-keep.service
systemctl is-active surface-sync-state-keep.service
