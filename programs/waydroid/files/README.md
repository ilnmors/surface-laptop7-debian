# Android apps (Waydroid)

Debian 13 ARM64; Wayland and a kernel with Binder/Binderfs required. The Surface kernel provides both as signed modules. Vanilla ARM64 Android images are not bundled (deleted 2026-11-24); install.sh uses images/*.img when present and otherwise lets `waydroid init` download them from the official OTA channels; Google Play services and x86 translation are not installed.

- packages/: Debian trixie/backports packages downloaded through APT's authenticated repository metadata.
- images/ (not bundled; optional): system.img and vendor.img from the official Waydroid OTA channels. OTA-SOURCES.json records the release URLs, timestamps and published image hashes; installed-config.txt records the selected variants.
- install.sh: install local packages, initialize from /usr/share/waydroid-extra/images (or from OTA when images/ is empty), select tablet/multiwindow mode and enable the container service. Existing Android data is retained.
- integrate-apps.py: run as the desktop user to hide stock Android utility launchers. Installed personal APKs are exported by Waydroid itself.

setup.sh runs both helpers. Offline property regeneration uses waydroid upgrade -o; images are not downloaded. Run Android apps from GNOME's app grid; a full Android desktop is unnecessary. Install an ARM64 APK with waydroid app install /path/app.apk. The session starts on demand; KakaoTalk login integration now starts it at GNOME login. To free its RAM, run waydroid session stop.

Verified on this machine: Android boot completed, arm64-v8a, hardware GLES with freedreno / Adreno X1-85 / Mesa 26.0.8. Calculator launched as a freeform window. Banking/DRM apps and Google-dependent apps are not verified.

Source: https://docs.waydro.id/usage/install-on-desktops and https://docs.waydro.id/usage/waydroid-prop-options . Backports is permanently enabled by user request; it is not a blanket distribution upgrade.

Optional cleanup: `bash programs/waydroid/reset-apps.sh --remove-user-apps` explicitly removes user APKs/data and nine optional factory applications for user 0. Normal setup never runs cleanup. Settings, launcher, WebView, framework and package installer remain. Original system APKs stay in the Android image; user-level removal can be reversed with `pm install-existing --user 0 PACKAGE`.

Background messaging: the user selected persist.waydroid.suspend=false so closing all windows no longer freezes Android automatically. RAM is shared across apps but each app adds allocations. Use waydroid session stop to stop all Android apps when desired; incoming messages then pause. The physical host can still suspend normally.

Physical keyboard preference: Android secure show_ime_with_hard_keyboard=0 hides the soft keyboard while a hardware keyboard is connected. The setup applies this after session startup; it does not disable the Android input method or host IBus. GNOME's accessibility screen keyboard is also disabled by the desktop component.

Appearance: Android UI night mode is disabled (`cmd uimode night no`) for the requested light/white theme. The setting is applied by Waydroid and KakaoTalk setup after Android boot readiness. An app with its own explicit theme selection may need that app's theme preference changed separately.

## Host download link

`programs/waydroid/setup.sh` now calls `download-link.sh` after Android boot readiness. The shell entry point delegates to `download-link.py`; either can be run separately as the desktop user. They create `<XDG Downloads>/waydroid` pointing to `~/.local/share/waydroid/data/media/0/Download`. The current machine uses `~/Downloads/waydroid`. Existing conflicting files or links are never replaced.

The helper uses the invoking UID, not a fixed account. When access is missing, a narrowly scoped sudo helper adds traverse-only ACLs to the three Android storage parent directories, read/write access to Download, and inheritable ACLs on its directories. Existing Android owners are retained; private app data is not recursively shared. Existing correct ACLs and links need no new sudo operation. The existing installer installs the bundled `acl` DEB offline.

Run `python3 programs/waydroid/download-link.py --check` for read-only verification. Live setup was rerun on the existing link without replacing it or prompting for unnecessary privileges; link, read/write access and default ACL checks passed. A clean Android installation was not performed for this check.

To remove the host shortcut, unlink only `<XDG Downloads>/waydroid`; do not recursively delete through it. The shared Android files remain in their original storage.

Offline dependency: `programs/waydroid/files/packages/acl_2.3.2-2+b1_arm64.deb`, downloaded through authenticated Debian trixie APT metadata. SHA256: `099b5f8bfa3ffea30a10308a89a5467d3fa7d8d16b94df931f0299344c2a4291`.
