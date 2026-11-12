# Romulus edge palm exclusion fix

2026-11-12: a 30-second user-requested edge test recorded 6,389 raw events, 1,161 contact samples, full X/Y range, 26 libinput `palm detected (edge)` messages and one jump warning. This demonstrates an additional libinput suppression layer; it does not prove all IPTSD fragmentation/jumps are fixed.

The local patch disables only geometric edge palm exclusion for BUS_VIRTUAL / vendor 045e / product 0c77 / exact name IPTSD Virtual Touchpad 045E:0C77. Other devices, pressure/size palm detection, disable-while-typing, thumb detection, scrolling and kernel modules are unchanged. IPTSD contact filtering remains active.

Source: official Debian libinput 1.28.1 orig + 1+deb13u1 Debian patches. Published DSC SHA256 values were verified. https://deb.debian.org/debian/pool/main/libi/libinput/ . All four Debian patches, including sanitation fixes, remain applied. The local change is romulus-edge-palm.patch. The upstream Apple-specific edge exception illustrates the mechanism but is not falsely assigned as this device model.

Reference: https://wayland.freedesktop.org/libinput/doc/1.28.1/palm-detection.html . The documented excluded left/right/top zones match the observed region. This is a local measurement-driven adaptation, not a claim of an upstream-tested Romulus patch.

Build: `bash drivers/files/touchpad/libinput-edge/build.sh /absolute/new/workdir`. GCC, binutils, Meson, Ninja, pkg-config, Python and dpkg tools are prerequisites. Header/dependency packages are extracted locally from build-debs; the build does not install them globally. libwacom support and exported ABI symbols were retained. The package reuses the matching original Debian libinput10 archive with updated library/checksums/version.

Install: `sudo dpkg -i drivers/files/packages/libinput10_*surface1_arm64.deb drivers/files/packages/libinput-tools_*surface1_arm64.deb`. The drivers component includes it. Requires logout/login; do not kill the current GNOME session. New independent contexts already report `IPTSD 045E:0C77 edge exclusion disabled`. Human comparison is pending. No LD_PRELOAD or scroll injection is installed.

Rollback: `sudo dpkg -i drivers/files/touchpad/libinput-edge/original/libinput10_1.28.1-1+deb13u1_arm64.deb drivers/files/touchpad/libinput-edge/original/libinput-tools_1.28.1-1+deb13u1_arm64.deb`, then logout/login. Future Debian updates may supersede this package; do not pin an old security version. Rebase the small patch onto the new distro source if still needed.

Secure Boot: this is a userspace shared library, not a kernel module or EFI binary. Kernel signing/trust is untouched.

The matching libinput-tools companion is versioned together because Debian requires an exact libinput10 version. Its binaries are unchanged; only version/dependency metadata changes. `apt-get check` passes. The matching libinput-bin base package is also bundled for offline fresh installs.
