# REJECTED — Wi-Fi hardware regression

Do not install this rebuild. On the real Surface after boot, the replacement reported HARD rfkill blocked and Wi-Fi was unavailable. Reloading the retained sl7 module (A98E5140E078A5920DAC05E) restored hardware-unblocked state, automatic connection and Wi-Fi-bound HTTPS 200. It has been removed from active modules, depmod overrides, default build/install and initramfs. The patch/source remain reference material only. VM signature/CRC tests did not validate hardware behavior; the rebuilt baseline source fingerprint differed from the working module and should have blocked default deployment.

# ath12k regulatory completion fix

Upstream commit f2576dc0f894ef33045ba7ed057ec417988bba8a, Baochen Qiang, accepted by Jeff Johnson. Source: https://git.zx2c4.com/wireguard-linux/commit/?id=f2576dc0f894ef33045ba7ed057ec417988bba8a . The archived f2576dc0.patch is the unmodified upstream patch. It assigns pdev_idx before validation and bounds-checks it so dropped regulatory events can still signal completion. Upstream tested WCN7850 hw2.0 with this machine's exact firmware build.

ath12k-source.tar.xz is the unmodified ath12k directory from the locally retained linux-qcom-x1e-7.3.0 source. Rebuild through build.sh/build.py using the shared native header bundle. Header ABI comparisons: 344 shared imports and 130 exports consumed by the existing wifi7 module matched; vermagic matched. Rebuilt baseline srcversion differs from the old installed module, so source identity with that old build is not established by srcversion. The signed replacement and existing wifi7 consumer loaded together in a matched ARM64 guest with module.sig_enforce=1 (Y). This validates trust/linkage, not real hardware behavior.

The live old module was not unloaded; reboot is required. The replacement is selected through the bundled depmod override. Installed modules are locally signed; reusable modules/ payloads are unsigned and re-signed by the shared installer. Original sl7 module remains for rollback. The initially built ath12k-patched.ko and ath12k-original.ko are local reference payloads; the installer uses ../modules/ only.

Rollback: remove updates/surface/ath12k.ko, run depmod and surface-secureboot-update, then reboot. Remove its depmod override line when retiring the patch. Do not change regulatory country to an arbitrary value or disable regulatory checks.
