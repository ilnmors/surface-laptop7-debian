# Surface hardware configuration

Device: Surface Laptop 7 13.8-inch, Snapdragon X Plus, Romulus13. Current kernel 7.3.0-31-qcom-x1e on Debian 13 ARM64. CURRENT.md is the current status; SOURCES.md records provenance; NEXT.md lists unresolved work.

| Component | Installed setup | Verification limit |
| --- | --- | --- |
| Secure Boot | Debian shim/GRUB, locally signed embedded-DTB kernel and modules, builtin public certificate | Physical boot confirmed. Private key is not bundled; first enrollment requires firmware/MOK interaction. |
| USB/deep sleep | Matching dwc3_qcom NULL-HCD backport | Exact crash identified; signed/ABI VM test passed; reboot and real sleep/wake pending. |
| Audio | Romulus topology/UCM, direct physical speakers, five SoundWire backports | New module requires reboot. Recurrent WSA884x parity faults are not claimed fixed. |
| Touchpad | GPI/GENI/SPI-HID plus scoped IPTSD weak-contact tracking | Existing calibration retained; input edge stability still needs user testing. |
| Touchscreen | Romulus13 I2C overlay | Device does not acknowledge; unresolved. |
| Wi-Fi/Bluetooth | Romulus WCN7850 rfkill workaround, firmware, persistent Bluetooth address recovery | Current interfaces work; repeated resume/startup reliability remains a separate test. |
| Camera | Working board overlay and OV02C10 metadata patch | Soft-ISP quality trial was rolled back after flicker; not auto-enabled. |
| CPU/power | scmi-cpufreq loaded and persisted | Policy0 present; other cluster policies and CPU9 failure unresolved. |
| Android | Waydroid Vanilla ARM64, Binder and multiwindow app launchers | Boot and Adreno rendering confirmed; arbitrary APK compatibility not guaranteed. |

Run the documented top-level installer rather than archived scripts. It preserves the packaged kernel/modules and installs replacements separately. Review kernel/files/secureboot/, patches/files/, drivers/files/touchscreen/ and programs/waydroid/files/ before device-specific troubleshooting.
