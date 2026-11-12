# OV02C10 camera gain backport
Status: Rolled back on this Surface Laptop 7. The patched preview flickered and the user saw no image-quality improvement. The bundled patch remains available for reference.

This is the sensor helper from [libcamera patch 28734](https://patchwork.libcamera.org/patch/28734/), tested upstream on Surface Pro 12. The Debian backport registers OV02C10 with analogue gain code / 16 and a 16-bit black level of 4096. It changes the libcamera software ISP module only.

| File | Use |
| --- | --- |
| `ov02c10-v3.patch` | Original upstream submission. |
| `ov02c10-debian-0.4.patch` | Same helper adapted to the Debian source layout. |
| `libcamera_0.4.0*` | Debian 0.4.0-7 source and packaging. |
| `ipa_soft_simple.so`, `module.sha256` | ARM64 module and its checksum. |
| `build.sh` | Rebuild using the source bundle and Debian development tools. |
| `install.sh` | Apply or restore the module using a Debian local diversion. |

After installing Debian `libcamera-ipa:arm64` version `0.4.0-7`, run `bash drivers/files/camera-quality/install.sh` from the Surface directory. Restart camera apps. Run the same command with `rollback` before changing the Debian libcamera version or to restore the original module.

```sh
timeout 20s cam -c 1 --capture=120 --stream=role=viewfinder,width=1280,height=720
qcam --renderer=qt
```

On this Surface Laptop 7, 720p was about 18.8 fps before and after the patch. The patched module completed 120 frames and removed the missing sensor helper warning. The generic tuning-file warning remains. Visual quality requires checking the preview under the same lighting.
