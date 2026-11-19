# Boot trials prepared on 2026-11-19

Result: the DTB trial passed on its second attempt and was promoted on 2026-11-19 (`promote-dtb.sh`; rollback GRUB entry "Surface before iris and camera LED DTB (2026-11-19)"). The a400000 trial is still pending.

Each trial needs one attended reboot. Nothing here is installed: `/boot`, `/etc/modprobe.d` and the
initramfs are unchanged, and the default GRUB entry keeps booting the current DTB.

## 1. Device tree: camera privacy LED and iris video decoder

`surface-sl7-xplus-trial.dtb` is `drivers/files/touchscreen/spi-gtch/surface-sl7-xplus-gtch.dtb` (the
installed `/boot/surface-sl7-xplus.dtb`) with three changes made by fdtput:

| Node | Change | Purpose |
| --- | --- | --- |
| `/leds/led-camera-indicator` | `phandle = <0x2ff>` | lets the camera node refer to the LED |
| `/soc@0/cci@ac16000/i2c-bus@1/camera@36` (OV02C10) | `leds = <0x2ff>`, `led-names = "privacy"` (this kernel looks up `privacy`, not `privacy-led`) | V4L2 lights the LED while the sensor streams |
| `/soc@0/video-codec@aa00000` (iris) | `status = "okay"`, `firmware-name = "qcom/x1e80100/microsoft/qcvss8380.mbn"` (device-signed, from the Windows package; the generic vpu30_p4.mbn is rejected) | hardware video decoding (+4.3 W measured on 1080p software decode) |

Trial (installed 2026-11-19 20:55, waiting for the reboot):

```sh
pkexec bash drivers/files/boot-trials/install-dtb-trial.sh   # signed image in /boot/secureboot/trial-dtb
pkexec bash drivers/files/boot-trials/restore-dtb-trial.sh   # removes the image, entry and flag
bash drivers/files/boot-trials/check-dtb-trial.sh            # after the trial boot
```

Secure Boot blocks GRUB's `devicetree`, so the DTB is embedded in a separately signed image
(`surface-secureboot-update --output-directory /boot/secureboot/trial-dtb --no-bootloader-update`).
`/boot/secureboot/grub.cfg` does not read `next_entry`; like the sync_state trial, the
`SURFACE_DTB_ONCE` block reads `surface_dtb_next` from `/secureboot/trial-dtb/grubenv`, saves it back
as 0 and only then selects the trial entry, so the boot after the trial is the default image again.

Check after the trial boot:

- LED: open the camera (`cam -c1 --capture=30` or GNOME Snapshot); `/sys/class/leds/white:camera-indicator/brightness` must follow the stream and turn off when it stops.
- iris: `dmesg | grep -i iris`, `ls /dev/video*`, then decode with `gst-launch-1.0 ... v4l2h264dec` or `ffmpeg -c:v h264_v4l2m2m`; compare playback power with the 2026-11-18 numbers.
- Risk: the VPU may reject the generic `qcom/vpu/vpu30_p4_s6.mbn` signature on this device. That only leaves iris unprobed; the default entry is untouched either way.

## 2. a400000 load order

`a400000-order.conf` is a modprobe softdep. Trial: copy it to `/etc/modprobe.d/`, run
`update-initramfs -u`, then cold and warm boot several times and check `xhci-hcd.1.auto` for `-110`.
Rollback: remove the file and run `update-initramfs -u` again. The failure so far only appeared on boots
that spent 12–18 s longer before Linux, so judge it over several boots, not one.
