# Physical click-and-drag: Romulus 045E:0C77

2026-11-15. User reports premature release during one-finger physical dragging and no movement while holding a click with one finger and moving another. Tap-to-click and tap dragging are disabled; this is not a tap-drag-lock setting.

## Defect reproduced

The installed vendor IPTSD daemon has two writers for BTN_LEFT. Physical button samples use a debounced cached state, while lift_singletouch() also emits a release when a selected contact is unstable, rejected or replaced. That release does not clear the cached pressed state. Further physical "still pressed" samples are discarded as unchanged, so the emitted click can remain released until the next physical press cycle.

The patch separates contact tracking from physical-button state **only for touchpad 045E:0C77**. Contact loss/representative changes no longer invent a button release. Explicit disable and palm blocking still force release and reset the cached state. Real button release and the existing 25 ms debounce remain unchanged. Existing edge tracking, calibration, GNOME clickfinger mode and the libinput edge fix are preserved.

## Evidence and limits

The regression harness compiles the actual production TouchDevice header with only UinputDevice replaced by an event sink. It does not inject input or record keyboard activity. Original header: 7 failures. Patched header: 13 checks passed, including single-finger instability, second-finger handover/motion, raw release, disable/re-enable, palm block recovery and unchanged behavior for another device.

These are synthetic event sequences demonstrating a real code defect, not a recording of the user's physical failure. After installation, the user confirmed both one-finger physical dragging and holding click with one finger while moving another now work normally. Raw force-threshold noise or separate libinput gesture decisions may require further measurement if symptoms remain.

Comparable upstream report: [IPTSD issue 208](https://github.com/linux-surface/iptsd/issues/208), Surface Laptop Studio 2 (045E:0C46), reports premature release while holding click and lifting another finger. It is open and concerns a different device; it is not a verified ARM fix. The present patch is a locally tested correction to the archived vendor daemon, not a claimed upstream backport.

## Offline inputs and entry points

Source: ../edge-fix/source.zip, the existing surface-xplus-project.zip vendor/iptsd snapshot. Exact original commit was not recorded. No new source or dependencies were downloaded. Apply ../edge-fix/edge-contact.patch first, then physical-button-state.patch. Existing Debian build dependencies are extracted from ../edge-fix/build-debs; compiler, Meson, Ninja, pkg-config, patch and dpkg-deb must be available.

```sh
python3 test.py             # or bash test.sh; no root/device access
bash build.sh /absolute/path/to/iptsd   # or python3 build.py ...
python3 setup.py            # or bash setup.sh; system authentication dialog
python3 restore.py          # or bash restore.sh; this machine's local backup
```

Full Surface installation uses the replaced prebuilt daemon under ../../rootfs/usr/local/libexec/surface-iptsd/ through drivers/setup.sh and its Python wrapper. The focused setup.py verifies the tested old/new hashes, discovers the exact hidraw device by VID/PID, backs up the original, replaces the executable atomically, and restarts only its IPTSD instance. Startup/registration failure restores the old binary automatically. It does not restart the touchscreen instance, edit kernel modules, or change Secure Boot.

Original SHA-256: bbc4cd4bfce32bf466799ba44e3dbd9d970eea9cc961ecb8a700f130052c33d1
Candidate SHA-256: 750247bc700539bbd8f79f867a129637a0ee840490efaf207041532cca0a8ae1

The local pre-change console-owned backup is ~/.local/state/surface-touchpad/backups/20261115T081420/iptsd. Successful system installation also stores /var/lib/surface-touchpad/20261115-click-drag/iptsd.before. restore.py currently targets the console-owned backup on this installation; it does not downgrade the offline payload. Other machines can rebuild the prior daemon by omitting physical-button-state.patch.

## Live status

Installed at 2026-11-15 08:29:44 KST. The touchpad instance runs the tested hash, registered exactly one virtual touchpad, and has zero automatic restarts. The touchscreen instance was not restarted. The user then confirmed both reported drag gestures work normally. GNOME settings and existing calibration were unchanged. Long-term reliability remains outside this short validation.
