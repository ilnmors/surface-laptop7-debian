# Suspend / resume

Current sleep mode remains deep. Earlier logs repeatedly show about five seconds between filesystem sync and process freezing. Kernel source places console preparation and PM notifiers in this interval. The exact slow function has not been measured.

Trial: files/rootfs/etc/systemd/system/systemd-suspend.service.d/50-surface-session-freeze.conf sets SYSTEMD_SLEEP_FREEZE_USER_SESSIONS=false. It avoids systemd freezing the graphical session before kernel console handoff. The kernel still freezes tasks for suspend; GNOME screen locking is unchanged.

The setting is installed and visible in systemctl show systemd-suspend.service -p Environment. No suspend was forced during active work. Improvement and resume display latency require a subsequent real sleep/wake cycle. To revert, remove that drop-in and run systemctl daemon-reload.

Reference: https://github.com/systemd/systemd/blob/v257/src/sleep/sleep.c

## Latest incident: 2026-11-11

EFI pstore confirms a kernel NULL-pointer Oops in dwc3_qcom_suspend during deep suspend entry. The a400000.usb xHCI host failed probing with -110 earlier in that boot; the USB suspend code dereferenced its missing driver data. This is a suspend-entry crash, not a confirmed power-button wake failure. Secure Boot was disabled in the affected boot.

See diagnostics/2026-11-11/README.md and the saved original crash records. A matching upstream NULL-guard patch is identified there; it is not installed. Current boot has all three xHCI hosts bound, but successful resume remains untested. Changing to s2idle alone does not eliminate the shared device-suspend code path.
