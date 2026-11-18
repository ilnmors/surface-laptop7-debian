# Suspend / resume

Current sleep mode remains deep. Earlier logs repeatedly show about five seconds between filesystem sync and process freezing. Kernel source places console preparation and PM notifiers in this interval. The exact slow function has not been measured.

Trial: drivers/files/rootfs/etc/systemd/system/systemd-suspend.service.d/50-surface-session-freeze.conf sets SYSTEMD_SLEEP_FREEZE_USER_SESSIONS=false. It avoids systemd freezing the graphical session before kernel console handoff. The kernel still freezes tasks for suspend; GNOME screen locking is unchanged.

The setting is installed and visible in systemctl show systemd-suspend.service -p Environment. No suspend was forced during active work. Improvement and resume display latency require a subsequent real sleep/wake cycle. To revert, remove that drop-in and run systemctl daemon-reload.

Reference: https://github.com/systemd/systemd/blob/v257/src/sleep/sleep.c

## Latest incident: 2026-11-11

EFI pstore confirms a kernel NULL-pointer Oops in dwc3_qcom_suspend during deep suspend entry. The a400000.usb xHCI host failed probing with -110 earlier in that boot; the USB suspend code dereferenced its missing driver data. This is a suspend-entry crash, not a confirmed power-button wake failure. Secure Boot was disabled in the affected boot.

See diagnostics/2026-11-11/README.md and the saved original crash records. The matching NULL-guard patch is installed for the next boot. Current boot has all three xHCI hosts bound, but successful resume remains untested. Changing to s2idle alone does not eliminate the shared device-suspend code path.

The replacement USB module is installed and signed; physical resume verification still requires a reboot. See ../../../patches/files/README.md.

## Measure the next manual suspend

`sudo python3 drivers/files/sleep/trace-resume.py arm` enables only power callback events in an isolated trace instance (256 KiB per CPU). Suspend/resume manually. Then run the same command with `save`; use `disarm` to remove the instance. It does not suspend, change sleep mode, or trace keyboard/network data. Monotonic timestamps separate device callback delays from time spent asleep. Four successful deep cycles were recorded in the current boot; no physical performance claim is made for the pending USB/SoundWire replacements.

## Persistent tracking

surface-resume-trace.service (boot-time power-callback trace, saved to /var/log/surface-resume/<boot-id>/ on orderly shutdown) was removed on 2026-11-18. The 21 saved traces are in archive/diagnostics/surface-resume-traces-20261118.tar.gz (not in Git). A hang never saves a trace, so it did not help with the deep-sleep hangs; use trace-resume.py for a manual attended cycle.
