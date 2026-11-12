# KakaoTalk in Waydroid

KakaoTalk 26.9.2 (29260920), original signed ARM64 split APKs, Android minimum API 29. Installed on Vanilla ARM64 Android 13 (API 33). No APK modification, Google services or x86 translation.

- Source page: https://apk.gold/download?split=621182/3544335/kakaotalk-free-calls-and-text . The download link on that page delivered the original APK ZIP; SHA256 is recorded in files/manifest.json.
- All four APKs passed apksigner verification. Their signer SHA256 matches com.kakao.talk in the official https://www.kakao.com/.well-known/assetlinks.json saved here.
- aapt confirmed the package name, matching version codes and arm64-v8a native library split. The downloaded archive, APKs, metadata and inspection tools remain local/offline; binaries are not committed.
- The earlier APKPure download was ARMv7-only and rejected. files/rejected-download.json records its provenance without retaining the unusable duplicate.

Run `bash programs/kakaotalk/setup.sh` or its setup.py as the desktop user. The Waydroid component must be installed first. The installer verifies the APK hashes and actual active data mount, stages public APKs temporarily, uses Android's split-install session and removes temporary copies. Existing account data is retained on reinstall. Login remains manual.

Waydroid is configured as a tablet with multiwindow mode. `waydroid upgrade -o` regenerates properties without image downloads; session/container restart applies them. KakaoTalk can also offer secondary-device login on recent phone builds; choose the secondary/tablet option to keep the primary phone registered. This script never chooses a primary-device registration or enters credentials.

The optional one-time Waydroid app cleanup lives in ../waydroid/reset-apps.sh; normal setup never deletes apps. Core Android components remain installed. Launch KakaoTalk individually from GNOME, not with show-full-ui.

Verification: official signer, ABI, Android version, installed base/splits and tablet property passed. Secondary Device was selected; the empty email/password/QR login screen was verified. No account information was entered. Shared-storage startup was repaired by the Waydroid media overlay; see ../waydroid/files/media-fix/.

## GNOME login integration

setup.sh now installs launch.py/launch.sh into ~/.local/share/surface/programs/kakaotalk, creates ~/.local/bin/kakaotalk, updates the existing individual app desktop entry, and adds ~/.config/autostart/kakaotalk.desktop. Login waits eight seconds before starting the session/app. This launcher does not install APKs, reset app data, or open the full Android desktop. Existing account state is retained.

Run `python3 programs/kakaotalk/integrate.py` to install only desktop/startup integration without reinstalling the app. Add --disable-autostart to disable login startup. A startup call with an existing session was verified; the next physical GNOME login remains to be observed.

The user requested messages after closing the window: persist.waydroid.suspend=false, Android device-idle whitelist for com.kakao.talk and POST_NOTIFICATIONS permission are applied and reproduced by setup.sh. Physical Linux suspend still suspends the device; background delivery is not promised while the Surface sleeps. Additional background power/RAM is expected; actual receipt/notifications need a real incoming message. Source: https://docs.waydro.id/usage/waydroid-prop-options . No other personal Android app was installed.

Icon: files/kakaotalk-icon.png is the actual installed KakaoTalk icon exported by Waydroid (yellow TALK bubble), not the unrelated generic Android ic_launcher resource. integrate.py copies it to the user's hicolor icons and uses that explicit path. It does not inherit stale icons from an old desktop entry.

## Physical keyboard Enter

Settings → Chats → Keyboard → Press Enter to Send must be enabled. It was off; the user confirmed the corrected behavior on 2026-11-12. This is an app preference, not a Linux key remap. Keep it in the authenticated app profile; no chat database or account secrets are bundled.
