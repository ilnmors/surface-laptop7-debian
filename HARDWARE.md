# Surface Laptop 7 hardware setup

Debian 13 ARM64, 13.8-inch Snapdragon X Plus (Romulus13). Copy this folder to external storage before reinstalling. Set the hostname to `surface` in the installer.

| Device | Applied change |
| --- | --- |
| Wi-Fi | Romulus13 ath12k rfkill patches, WCN7850 board alias, WLAN.HMT.1.1.c7-00108 firmware, and NetworkManager power saving disabled. |
| Touchpad | Qualcomm GPI and GENI SPI and Surface SPI-HID replacements, early module loading, and the touchpad overlay on the 10-core X Plus DTB. |
| Webcam | CCI/CAMSS device-tree overlay and OV02C10 crop metadata patch. Test capture reached 720p at 30 fps with green tint and flicker. |
| Audio | Romulus speaker topology and ALSA UCM, with a systemd service to start the ADSP after root mounts. Audio sometimes required reactivating the profile. |

The packages use Ubuntu Concept 7.3.0-31.31. Reference patches, source archives, and original build scripts are in `archive/hardware/source/`. Package names retain their original dependency identifiers.

## Install from local files

Use a Debian GNOME installation with kmod, initramfs-tools, firmware-qcom-soc, and the standard GNOME audio stack (PipeWire, WirePlumber, dbus-user-session and ALSA UCM). Debian prerequisites can be installed from Debian media. Use installed versions when they satisfy the dependencies. The Surface payload is bundled.

```sh
cd ~/workspace/surface
sha256sum -c SHA256SUMS
tar -C files/rootfs -cf - . | sudo tar --no-overwrite-dir --no-same-owner -C / -xf -
sudo sh -c 'for m in gpi spi-geni-qcom spi-hid uinput ath12k ath12k_wifi7; do
  grep -qxF "$m" /etc/initramfs-tools/modules || echo "$m" >> /etc/initramfs-tools/modules
done'
sudo apt-get --no-download install ./files/packages/linux-image-*.deb
sudo apt-get --no-download install ./files/packages/sl7-audio-support_*.deb
# Optional webcam test support
sudo apt-get --no-download install ./files/packages/sl7-camera-support_*.deb
sudo update-initramfs -u -k 7.3.0-31-qcom-x1e
sudo update-grub
```

Keep the Debian boot entry for recovery. For the first test with Secure Boot disabled, edit the Surface GRUB entry. Keep the generated root and initrd paths and append `clk_ignore_unused pd_ignore_unused cma=128M arm64.nopauth stubble.dtb_override=false console=tty0` to the Linux line. Insert `devicetree /boot/surface-sl7-xplus.dtb` before the initrd line. Use `/surface-sl7-xplus.dtb` if GRUB's root is a separate /boot filesystem. For webcam testing, use `surface-sl7-xplus-camera.dtb`. The previous entry also used `cutmem 0x8800000000 0x8fffffffff` before loading Linux. After testing, persist the entry in `/etc/grub.d/40_custom` and run `sudo update-grub`.

## Secure Boot

The previous signed entry used a kernel with an embedded DTB and a separate initramfs. Its module tree mixed an Ubuntu build key and a local Surface key. Booting a signed EFI image only verifies the boot image. The running kernel must also trust the signatures of each module and its dependencies.

Use a signed kernel with the Surface DTB embedded. Build in the module-signing certificate or verify that the kernel trusts the enrolled MOK for module loading. Sign replacement modules with the trusted key, regenerate the initramfs from that same module tree, and boot the signed EFI image through Debian shim. Enroll the public certificate through MokManager. Keep the private key on the installed system. Verify the Secure Boot test before selecting it as the default.

```sh
mokutil --sb-state
sudo journalctl -k -b | grep -Ei 'lockdown|module verification|key.*reject|signature|unknown symbol'
modinfo -F signer ath12k
modinfo -F signer spi-hid
```
