# In use (2026-11-24): `updates/surface/ov02c10.ko`, srcversion 08EF7452B0F555AA15FA25F, `vertical_blanking` 72

Earlier note, superseded: the faster rebuilt module once emitted three unsupported crop-selection ioctl errors and was withdrawn for a time; the retained sl7 driver had not been compared in that boot: live removal of the experiment was refused as in use, and no forced unload was attempted. Its on-disk replacement/override and default build/install were removed. The next signed initramfs restores the original sl7 module C8AE6F17BF899E4A937A808. Recheck after reboot before attributing every crop error to the rebuild. Fast-video experiment files remain historical only under rejected/. No permanent frame-timing change is enabled by setup.

# Surface OV02C10 faster video policy

Local policy, not an upstream image-quality fix. Existing libcamera gain helper remains rolled back because it previously flickered.

A live V4L2 trial used the driver's supported minimum vertical blanking (72 lines): mean measured frame rate rose from 18.784 to 37.445fps. No frame/control errors occurred; 150 frames completed without saving images. The trial restored blanking 1236 afterward. See ../../drivers/files/camera-quality/frame-timing-trial.json.

03-camera-fast-video.patch adds read-only fast_video (default true) and selects the sensor-declared minimum VTS at control creation and active-format setup ONLY when of_machine_is_compatible("microsoft,romulus13"). Other boards retain upstream defaults. This removes the two-lane multiplier from the default frame period on this Surface; no private register or clock rate was guessed. The driver still enforces its declared control ranges. Shorter frames reduce maximum exposure; dim-light brightness/noise must be checked. This is not a claim of Windows-equivalent color, focus or tuning.

Module built for 7.3.0-31-qcom-x1e; all 60 shared imported symbol CRCs match the previous module. The source is under sources/drivers/media/i2c/ov02c10.c, patch under patches/, headers local and output under modules/. Shared build/install SH and Python entries cover it. No global fast_video modprobe option is imposed on future stock kernels. The installed replacement is signed by the target key; current hardware is not unbound. Reboot to activate; compare FPS, brightness and flicker. Current pre-reboot cam --list-controls exposes only Contrast, so a generic libcamera FrameDurationLimits configuration was not assumed to work.

Rollback: remove only updates/surface/ov02c10.ko, run depmod and surface-secureboot-update, reboot. Original sl7 module remains. This does not require restoring the rejected gain helper.
