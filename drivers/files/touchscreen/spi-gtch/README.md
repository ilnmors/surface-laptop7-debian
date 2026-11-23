# GTCH HID-over-SPI touchscreen (promoted 2026-11-13)

13.8-inch units ship with one of two panels: ITCH (MSHW0468, HID-over-I2C on I2C9/Linux i2c8 at 0x34) or GTCH (HID-over-SPI on SP11/Linux spi10). This machine's SSDT declares both with `_STA` = 0x0F. The I2C ITCH never acknowledges 0x34 (v2 GPIO38 and v1 GPIO31 reset trials both ENXIO), while UEFI leaves the GTCH lines configured: gpio64 (power) high, gpio48 (reset) high and gpio49/50 in QSPI function 2. None are claimed by Linux. This points to the SPI panel.

`romulus13-gtch-spi.dtso` adds the GTCH regulator, pin states and `hid-over-spi` node on spi10 in QSPI mode, using this machine's SSDT resources (GpioInt 51, GpioIo 64) and the CouchLiteOS romulus15/romulus13-spi-touch description (https://github.com/Dudiebug/couchliteos, `kernel/sl7/patches/0003-romulus15-gtch-spi-touchscreen.patch`, `0101-romulus13-touchpad-and-spi-touchscreen-variant.patch`). DMA type 4 (QSPI) matches the working spi19 touchpad. `surface-sl7-xplus-gtch-trial.dtb` = `base.dtb` (the active PCIe3-off DTB) + this overlay.

The trial image in /boot/secureboot/trial-touch is signed with the machine key and selected once through GRUB `next_entry` (cleared before booting, so a failed trial returns to the default image on the next power cycle). It also carries `cma=512M` (camera buffers, see docs/investigations/2026-11-12-camera-quality/RESULTS.md).

After the trial boot: `grep -iE 'spi_hid|hid-over-spi|gtch' <(sudo journalctl -k -b)`, `libinput list-devices | grep -i touch`, and touch the screen. If it works, promote by appending the overlay to drivers/files/pcie DTB generation and kernel/setup.sh, then run surface-secureboot-update. Otherwise run `restore.sh` as root.

## Result

The one-shot trial boot (2026-11-13 08:56) bound `spi_hid` to spi1.0 (`spi 045E:0C6E Touchscreen`); iptsd attached in touchscreen mode and created the IPTSD virtual touchscreen and stylus. A 45 s capture showed 6 touches and 612 motion events. Taps work and Firefox scrolls; GNOME Terminal (VTE has no touch scrolling) and Nautilus (drag selects/drags items) do not, which is application behaviour. The overlay was promoted: `prepare.sh` builds `surface-sl7-xplus-gtch.dtb` (PCIe3-off DTB + overlay), kernel/setup.sh installs it, and the default signed image was regenerated. The previous default (spi-hid v2, no touchscreen) is GRUB "Surface previous working image". `restore.sh` is kept for the trial layout only.
