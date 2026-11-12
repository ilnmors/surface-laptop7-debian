# IPTSD contact calibration

Device: Snapdragon Surface Laptop 7, SPI HID 045E:0C77.

The [ARM Surface project](https://github.com/bryce-hoehn/linux-surface-laptop-7) documents per-device calibration. An [Intel Surface Laptop 7 report](https://github.com/linux-surface/iptsd/issues/192) describes similar light-touch jitter, but is not evidence of the same ARM transport fault or a verified ARM fix.

The calibration tool collected 2,458 contact samples with the regular IPTSD service paused. The recommended `measured-2mm.conf` still produced five jump warnings in 15 seconds and was rolled back. `measured-10mm.conf` is an untested wider variant. `previous.conf` is the restored setting and matches the bundled rootfs.

To restore the previous calibration on this installation, run from the Surface directory:

```sh
sudo install -m 644 drivers/files/touchpad/previous.conf /etc/iptsd.d/91-calibration-045E-0C77.conf
sudo systemctl restart iptsd@dev-hidraw0.service
```

Confirm the active instance with `systemctl list-units 'iptsd@*'` if the HID device number changes.

## Edge contact tracking

The 7.5 mm overshoot trial did not fix the problem and was removed. The active 045E:0C77 trial uses the Windows DLL's compiled 10-frame, two-frame and 0.65/0.85 normalized weak-force defaults. Up to two weak frames can pass before release, and a recovered signal resets the weak-frame count. A frame with no local signal releases immediately. It compares local Linux heatmap peak contrast to the last valid frame as a substitute for normalized force. A 100 ms maximum and a 4 mm edge band bound the trial. It releases the contact when the signal drops below the gate.

The daemon loaded and registered the touchpad. The previous version produced five jump warnings in a 15-second edge test. The user reported improved tracking. The updated two-frame version is installed and registered, with its edge behavior still to be compared. The values and static analysis are recorded in `archive/windows-touchpad/`.

- `edge-fix/edge-contact.patch` contains the source change.
- `edge-fix/build.sh` rebuilds it using the archived source and the local build packages.
- `drivers/files/rootfs/usr/local/libexec/surface-iptsd/` holds the daemon and runtime libraries.
- `drivers/files/rootfs/etc/systemd/system/iptsd@.service.d/90-surface-edge.conf` selects the patched daemon. The stock daemon remains installed.

To roll back, remove `/etc/systemd/system/iptsd@.service.d/90-surface-edge.conf`, run `sudo systemctl daemon-reload`, and restart the active `iptsd@dev-hidraw*.service` instance listed by `systemctl list-units 'iptsd@*'`.

## Measured libinput edge suppression

The 2026-11-12 30-second test found 26 geometric edge-palm exclusions while IPTSD emitted valid full-range coordinates. A narrowly matched libinput patch is installed; logout/login is required for GNOME to load it. See libinput-edge/README.md for source, build, validation and rollback. This does not claim to fix the separate single jump warning or all upstream contact fragmentation.
