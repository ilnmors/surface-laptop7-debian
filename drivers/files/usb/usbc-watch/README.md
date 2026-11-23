# USB-C dead-port snapshot collector (2026-11-20)

The USB-C USB2 path sometimes stays dead after a disconnect or a resume (no attach events at all; charging also stops);
rebinding dwc3-qcom brings it back (see ../../../../docs/investigations/2026-11-16-usb-tethering/TETHERING.md). Ruled out on 2026-11-20: runtime PM (both
controllers have `power/control=on`), the eUSB2 repeater losing its settings (pmic@7 0xfd00-0xfdff identical before and
after the rebind) and Type-C role switching (no usb_role switch; dwc3 is host-only). The fault did not reproduce on demand,
so this collector waits for it.

`surface-usbc-watch` checks both ports every 5 s. When a Type-C partner is attached but no USB device has enumerated on that
controller for 15 s it saves one snapshot to `/var/log/surface-usbc-watch/<time>-port<N>/` (Type-C and UCSI attributes,
xHCI debugfs port registers, dwc3 debugfs, the port's repeater registers, the kernel log), then waits until the port
recovers or the partner leaves. It keeps the last 20 snapshots and never rebinds or resets anything. A phone set to
"charging only" also produces a snapshot; check `summary.txt` and the phone's mode before reading one.

Port map: Type-C port0 = a600000.usb, repeater SPMI 1-07 (pmic@7); port1 = a800000.usb, repeater 1-0a (pmic@a).

Install: `pkexec bash drivers/files/usb/usbc-watch/install.sh`. Listed in `../../diagnostics/DIAGNOSTIC-SERVICES.md`; remove with `../../diagnostics/remove-all.sh`.
