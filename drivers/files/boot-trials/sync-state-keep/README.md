# Keep the sync_state boot while it stays clean (2026-11-20)

`fw_devlink.sync_state=timeout` lets DDR power-collapse in suspend (265 of 279 s on 2026-11-20) but one such boot
(2026-11-20 10:03) lost EC transmit (SSAM -110, suspend refused). Instead of making it the default, this service
re-arms the one-shot trial flag (`surface_trial_next=1` in `/boot/secureboot/trial-sync-state-20261117/grubenv`) at
every shutdown of a sync_state boot whose kernel log has no SSAM -110 and no `xhci-hcd ... can't setup: -110`.
After a faulty boot the flag stays 0, so the next boot is the default entry; re-arm by hand to resume. Decisions are
logged to `/var/log/surface-sync-state-keep.log`. Install/undo: see `install.sh`.
