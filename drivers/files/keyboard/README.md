# Function row and Fn toggle

Hardware: Surface Aggregator HID keyboard, Microsoft 045E:006C.

User requirement: media/brightness actions by default, F1–F12 only while holding Fn; tapping Fn must not toggle the mode, with a fixed indicator state.

A physical test confirmed that Fn currently toggles its indicator and top-row behavior. That proves ordinary firmware Fn Lock works, not the requested permanent non-toggling mode.

The live HID descriptor exposes the lock indicator as an INPUT report (ID 0x5b, Generic Desktop usage 0x99). Output LEDs cover Num/Caps/Scroll only. The Linux driver exposes no fn_lock/fn_mode sysfs switch and the input keyboard does not report KEY_FN. No supported writable permanent-lock command has been identified. GNOME key remapping cannot prevent a toggle already handled by the keyboard controller or hold its physical LED on.

No misleading LED-only patch, media-to-F-key remap or guessed vendor HID write was installed. This exact request remains unresolved; currently select media mode with the physical Fn toggle, then hold Fn for F1–F12. LED permanence is not implemented.

Reference: https://support.microsoft.com/en-us/surface/accessories/cover-keyboard/special-keys-and-function-keys-for-surface-keyboards-or-type-covers . Device-specific evidence is the running report_descriptor and driver source drivers/hid/surface-hid/surface_hid.c.

## Decision (2026-11-13)

A user-space normalizer was built and verified (Fn is reported as BTN_0, scan 0x10097, so the top row could follow "Fn held" instead of the firmware lock), but the firmware still toggled the Fn LED and lock on every tap. The user chose to remove it and keep the keyboard's native Fn toggle. No daemon, package or setup step remains. Feature report 0xd4 (vendor page 0xff00, usages 0xe0/0xe1) was read but never written; whether it holds the lock state is unverified.
