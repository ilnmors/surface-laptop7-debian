# Touchscreen

For the 13.8-inch Romulus13 Surface Laptop 7.

- Source patch by Jizhou Tong, 2026-09-30. Enables I2C8 at 400 kHz, HID-over-I2C address 0x34, descriptor register 0 and GPIO38.
- romulus13-touchscreen.dts and .dtbo contain the enablement overlay.
- surface-sl7-xplus-touchscreen.dtb merges that overlay with this machine's existing touchpad and camera DTB.
- setup.sh installs the merged DTB. The Secure Boot updater embeds the same DTB in the signed kernel.
- Reboot and check for a touchscreen in libinput list-devices. Actual finger and multitouch operation still needs testing on this machine.

Source https://lkml.iu.edu/2609.3/14494.html

Post-reboot audit, 2026-11-11: the overlay is active and client 10-0034 exists, but i2c_hid_of receives ENXIO (-6), "nothing at this address". The device is unbound and no touchscreen input device is created. This patch is not verified as functional on this unit. No unverified reset GPIO or 15-inch QSPI configuration was applied.
