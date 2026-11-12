# PCIe3 (1bd0000) disabled (next-boot trial, 2026-11-12)

`/soc@0/pcie@1bd0000` is the SoC's x8 `pcie3` controller (domain 3). On this Romulus13 unit no endpoint ever links ("Device not found" at boot and on every resume), yet link training cost 1.07 s per resume. It is not Surface Connect: Surface Connect carries power, USB and DisplayPort through the USB/DP PHYs, not PCIe. Wi-Fi is pcie4 (1c08000) and NVMe is pcie6a (1bf8000); both stay enabled.

`prepare-pcie3-off.sh` copies the verified DTB (`base.dtb`, identical to drivers/files/touchscreen/surface-sl7-xplus-touchscreen.dtb and the CPU-topology DTB) and changes only `status = "disabled"` on that controller. The PHY at 1be0000 stays enabled because GCC lists its pipe clock as a clock input; with no consumer it stays powered down. Output sha256 b4d00b98…ee07.

Installed by drivers/files/touchpad/spi-hid-resume/install.sh. kernel/setup.sh still installs the previous DTB until this trial is verified.
