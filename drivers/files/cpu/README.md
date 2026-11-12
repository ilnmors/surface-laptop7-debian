# X1P64100 CPU fixes

SCMI cpufreq: applied and live-tested. Firmware labels every frequency in two domains as turbo, leaving those clusters without a usable table. The small scmi-cpufreq patch clears this classification only when every valid entry is turbo. All three policies now exist, use ondemand and retain the original 710.4–3417.6 MHz range. CPU frequency changes were observed on the previously unmanaged clusters. This does not establish a measured battery-life gain.

Sources: https://github.com/dwhinham/archiso-aarch64-sp11/issues/36 and https://github.com/dwhinham/linux-sp11/pull/2 . Only the cpufreq patch is used, not the unrelated ACPI platform-profile patch. Baseline source, patch, ABI comparison and live results are saved here. `patches/files/build.sh` rebuilds the module from offline headers; `patches/setup.sh` installs and signs it with the local key.

CPU9: the current DTB addresses physical 20300, which firmware rejects with PSCI -22. The same-SoC report identifies 10300/20300 as disabled cores. `prepare-topology.py` and `.sh` produce a separate candidate restoring 20100 and excluding 20300. This is evidence from another X1P64100 device, not a fuse read from this machine. The trial is not yet verified.

## One-shot boot trial, 2026-11-12

`/boot/secureboot/trial-cpu-camera/` contains a separately signed kernel, corrected CPU DTB and trial camera module in its initramfs. GRUB next_entry selects it once and clears the selection before boot. Subsequent boots default to the stable image. A previous image is retained under `/boot/secureboot/rollback-20261112/` and appears in the four-second GRUB menu. The installed signing helper supports separate output/DTB with `--no-bootloader-update`.

After reboot: check `/sys/devices/system/cpu/online` (expected 0-9), three cpufreq policies, Secure Boot, Wi-Fi, camera frames and Open Bar extension errors. Do not promote the trial DTB merely because its signature verifies. Run `restore-previous-boot.sh` as root only to restore the pre-trial boot snapshot and remove these three overrides.
