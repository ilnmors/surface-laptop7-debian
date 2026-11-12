# Android apps (Waydroid)

Debian 13 ARM64; Wayland and a kernel with Binder/Binderfs required. The Surface kernel provides both as signed modules. Vanilla ARM64 Android images are included; Google Play services and x86 translation are not installed.

- packages/: Debian trixie/backports packages downloaded through APT's authenticated repository metadata.
- images/: installed system.img and vendor.img from the official Waydroid OTA channels. OTA-SOURCES.json records the release URLs, timestamps and published image hashes; installed-config.txt records the selected variants.
- install.sh: install local packages, initialize from /usr/share/waydroid-extra/images without network, select tablet/multiwindow mode and enable the container service. Existing Android data is retained.
- integrate-apps.py: run as the desktop user to hide stock Android utility launchers. Installed personal APKs are exported by Waydroid itself.

setup.sh runs both helpers. Offline property regeneration uses waydroid upgrade -o; images are not downloaded. Run Android apps from GNOME's app grid; a full Android desktop is unnecessary. Install an ARM64 APK with waydroid app install /path/app.apk. The session starts on demand; KakaoTalk login integration now starts it at GNOME login. To free its RAM, run waydroid session stop.

Verified on this machine: Android boot completed, arm64-v8a, hardware GLES with freedreno / Adreno X1-85 / Mesa 26.0.8. Calculator launched as a freeform window. Banking/DRM apps and Google-dependent apps are not verified.

Source: https://docs.waydro.id/usage/install-on-desktops and https://docs.waydro.id/usage/waydroid-prop-options . Backports is permanently enabled by user request; it is not a blanket distribution upgrade.

Optional cleanup: `bash programs/waydroid/reset-apps.sh --remove-user-apps` explicitly removes user APKs/data and nine optional factory applications for user 0. Normal setup never runs cleanup. Settings, launcher, WebView, framework and package installer remain. Original system APKs stay in the Android image; user-level removal can be reversed with `pm install-existing --user 0 PACKAGE`.

Background messaging: the user selected persist.waydroid.suspend=false so closing all windows no longer freezes Android automatically. RAM is shared across apps but each app adds allocations. Use waydroid session stop to stop all Android apps when desired; incoming messages then pause. The physical host can still suspend normally.

Physical keyboard preference: Android secure show_ime_with_hard_keyboard=0 hides the soft keyboard while a hardware keyboard is connected. The setup applies this after session startup; it does not disable the Android input method or host IBus. GNOME's accessibility screen keyboard is also disabled by the desktop component.

Appearance: Android UI night mode is disabled (`cmd uimode night no`) for the requested light/white theme. The setting is applied by Waydroid and KakaoTalk setup after Android boot readiness. An app with its own explicit theme selection may need that app's theme preference changed separately.
