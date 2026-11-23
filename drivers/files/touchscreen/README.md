# Touchscreen

For the 13.8-inch Romulus13 Surface Laptop 7.

Superseded: the working touchscreen is GTCH over SPI ([spi-gtch/](spi-gtch/README.md)), promoted to the default image on 2026-11-13. The I2C overlay below never bound on this unit and is kept as a record.

- Source patch by Jizhou Tong, 2026-09-30. Enables I2C8 at 400 kHz, HID-over-I2C address 0x34, descriptor register 0 and GPIO38.
- romulus13-touchscreen.dts and .dtbo contain the enablement overlay.
- surface-sl7-xplus-touchscreen.dtb merges that overlay with this machine's existing touchpad and camera DTB.
- The merged DTB was installed and embedded in the signed kernel for the 2026-11-11 test.

Source https://lkml.iu.edu/2609.3/14494.html

Post-reboot audit, 2026-11-11: the overlay is active and client 10-0034 exists, but i2c_hid_of receives ENXIO (-6), "nothing at this address". The device is unbound and no touchscreen input device is created. This patch is not verified as functional on this unit. No unverified reset GPIO or 15-inch QSPI configuration was applied.

2026-11-12 follow-up: published Romulus13 v1 GPIO31 active-low reset was tested once using authenticated Debian gpiod tools, after checking the line was unclaimed. Probe still returned ENXIO (-6), and no driver bound. No reset GPIO property was added to the persistent DTB. Native gpiod packages are cached under tools/; this is a recorded diagnostic, not a setup-time automatic GPIO pulse. Source v1: https://lkml.iu.edu/2609.0/14485.html .
