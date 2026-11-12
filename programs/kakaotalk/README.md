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
