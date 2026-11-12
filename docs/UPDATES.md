# Updates

`sudo apt update` and `sudo apt upgrade` are usable. No global update disable, package hold or security-update suppression was installed. APT dependency verification passed after installing the matching libinput10/libinput-tools pair. The upgrade simulation selected only libopenexr-3-1-30 from Debian security; it did not replace the Surface kernel or remove the patched libraries. The actual upgrade was not run.

The Surface kernel is a separately named package, linux-image-7.3.0-31-qcom-x1e-sl7, not a generic linux-image-arm64 meta-package. New board kernels must match firmware/DTB/modules and pass the existing signing pipeline before booting. Keep a working boot entry. Signing hooks alone do not make an unrelated kernel support this board.

The local libinput pair is versioned 1.28.1-1+deb13u1+surface1. Future Debian security versions may supersede it and revert the edge-palm adaptation; rebase the small patch rather than holding back security updates. Sources/build/rollback are under drivers/files/touchpad/libinput-edge.

Waydroid vendor updates can replace or conflict with the media manifest overlay. Compare the new manifest and real services before carrying this workaround forward. Normal application and Debian security updates remain enabled.
