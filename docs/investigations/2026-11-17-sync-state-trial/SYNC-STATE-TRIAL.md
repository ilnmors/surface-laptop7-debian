# Single-variable trial: fw_devlink.sync_state=timeout — 2026-11-17

## Why

Every baseline deep sleep in `/var/lib/surface-power/suspend.jsonl` (PHY-only reference, including the 0.516 W night and the 0.66 W 6 h 13 m sleep of 2026-11-17 16:16–22:30, no USB device attached) shows **CXSD/AOSD/DDR count 0**: only the CPU subsystem collapses. These suppliers never finish state sync, so unused clocks/power domains stay voted on:

- `100000.clock-controller` (GCC), `3d90000.clock-controller` (GPUCC), `1700000.interconnect`, `interconnect-1`

The withdrawn Codex trial (boot 8a4806f5) did reach CXSD, but it changed three things at once (ADSP notifier, this flag, deepest-idle residency guard) and then woke immediately from a600000 `ss_phy_irq` and hung. This trial changes only the boot flag.

## Change

- `/boot/secureboot/grub.cfg`: one extra entry `Surface trial: sync_state=timeout (2026-11-17)` = the default entry with `fw_devlink.sync_state=timeout` added after `ro`; same signed image, initramfs and DTB.
- One-shot block: GRUB reads `surface_trial_next` from `/secureboot/trial-sync-state-20261117/grubenv`, saves it back to 0 and only then selects the trial. Later boots use the normal default.
- Backup: `/var/lib/surface-power/sync-state-20261117/grub.cfg.before` (sha256 `73ad2f08…`).

## Checks after the trial boot

1. `cat /proc/cmdline` contains `fw_devlink.sync_state=timeout`.
2. `state_synced` = 1 for the four suppliers above.
3. USB hosts/hubs, display 120 Hz, touchpad/touchscreen, Wi-Fi + wg0, audio, camera.
4. Attended short deep sleep with the lid open (power button to wake). Compare CXSD/AOSD/DDR counts before/after and wake reason. If it returns within seconds: do not close the lid, record, reboot to the normal entry (with approval).
5. Only if 4 is clean: long sleep, energy from `suspend.jsonl`.

## Rollback

- Hang during boot: hold power, power on again — the flag is already consumed, the normal entry boots.
- Remove the trial: `cp /var/lib/surface-power/sync-state-20261117/grub.cfg.before /boot/secureboot/grub.cfg` (root).

## Result (trial boot 1a9b4911, 2026-11-17 22:58–23:06)

- Boot: flag applied, all four suppliers `state_synced=1` (forced at 25.6 s). 120 Hz, Wi-Fi/wg0, audio sinks, camera nodes, no failed units.
- `xhci-hcd.1.auto` (a400000) `can't setup: -110` 1 ms after the forced sync; 4 root hubs instead of 6. **Not caused by the flag:** the following normal boot (74a7f298, 2026-11-18) and normal boot 7eaa4187 (2026-11-17 13:16) failed the same way, also right when the deferred-probe timeout messages print. It is the intermittent a400000 failure already seen before; the three normal boots in between were fine.
- **Sleep:** user closed the lid at 23:02. CXSD/AOSD/DDR **were reached** (cxsd 0 → 35 over 8 suspends), but every suspend returned after ~2 s and GNOME re-suspended every ~30 s. The 9th entry (23:06:47, 18.53 Wh) never returned: no resume log, no pstore. The user forced a restart at 10:21 the next day with about 12% left (≈1.1 W average while hung, not a sleep figure).
- Same pattern as the withdrawn three-variable trial, now with sync_state alone: sync_state is what opens CXSD, and reaching CXSD exposes an immediate wake source followed by a hang.
- Next boot used the normal entry (flag consumed). Do not re-arm until the wake source is identified with the lid open (one attended suspend, `pm_wakeup_irq`).

## Wake source (attended trial boot, 2026-11-18 17:57)

- Same one-shot entry; suppliers synced; a400000 failed again (`-110`), so every trial boot so far lost a400000.
- One `systemctl suspend` with the lid open at 17:59:14, `pm_debug_messages=1`: CXSD 0 → 1, returned within ~2 s.
- `/sys/power/pm_wakeup_irq` = **188 = PDC 17 `ss_phy_irq` (Level) of a600000** (USB-C port 1); 55,569 interrupts during the attempt. Also triggered: IRQ 192 = PDC 47 `ss_phy_irq` of a800000 (USB-C port 2), 3,159. All USB2 wake lines (dp/dm_hs) 0. Nothing was connected to either port.
- So with CXSD reachable, both idle SuperSpeed PHY wake lines are asserted level-high and storm. Matches the two upstream items Codex had listed: the X1E combo PHY AON clamp offsets fix (2026-10-30 v2) and the dwc3-qcom series selecting wake IRQs from the actual SuperSpeed link state (2026-11-06). Evaluate them one at a time with sync_state on.
