# Korean input in Waydroid (2026-11-20)

Android in Waydroid had only the AOSP keyboard, which has no Korean, and the host's IBus does not reach Android, so the
한/영 key had nothing to switch. `korean-input.sh` (root, session running) installs ReteKey
(`com.retekey_206.apk`, F-Droid build 0.2.3, MIT, source https://github.com/rubidus-api/retekey_apk; SHA-256 from the
F-Droid index: `bc57304266886af0268ba1a3bafb899ad3916df126496f7aca15709bb6948e42`) and makes it the default input method.
ReteKey composes 2-beolsik Hangul from a physical keyboard and lets the KO/EN key be assigned in its settings.
Android maps the Surface 한/영 key (evdev 122, KEY_HANGEUL) to `KANA` through `Generic.kl`.

The same script turns off Android's "physical keyboard" notification (channel `PHYSICAL_KEYBOARD` of package
`android`, `blockable_system="true"`) by setting its importance to 0 in `/data/system/notification_policy.xml`. The running system_server keeps the
channel in memory and an in-place `stop`/`start` inside Waydroid did not reload it, so the script writes the edited
copy as `notification_policy.xml.keyboard-off`; `setup.sh` stops the session, copies it over the live file
(host path `~/.local/share/waydroid/data/system/`) and starts the session again. Verified 2026-11-20: channel
importance 0 and no keyboard notification after the restart. The original is kept as
`notification_policy.xml.before-keyboard`; to undo, stop the session, copy it back and start the session.
To undo the keyboard: `waydroid shell -- ime set com.android.inputmethod.latin/.LatinIME` and uninstall com.retekey.
