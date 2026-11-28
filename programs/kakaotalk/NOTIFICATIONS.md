# KakaoTalk blank notification companion

## Verified on this device, 2026-11-12

With permission, Android logcat and unredacted notification state were inspected in memory. No chat text or raw dump was saved. A temporary D-Bus monitor reported only timestamps, desktop ID, replacement ID and title/body lengths.

A real incoming message created two records:

- `quiet_new_message`: null title and text; Waydroid sent an empty GNOME notification.
- `new_message_v4`: title and text present, MessagingStyle; the nonempty body reached GNOME.

Thus the empty companion is a confirmed source of blank boxes. No body loss was observed for the real message in this test. Earlier suspicion about MessagingStyle/getString was not reproduced and is not the fix applied.

## Fix

`sudo python3 programs/kakaotalk/fix-notifications.py` inserts a narrow guard into `/usr/lib/waydroid/tools/services/notification_manager.py`: for `com.kakao.talk` only, skip notifications whose title AND body are empty/whitespace. Return the existing ID_NONE constant. Real title-only/body-only messages and other apps are unchanged. A backup `.surface-original` is retained beside the system file. The Python installer refuses unfamiliar source layout and is idempotent; `fix-notifications.sh` calls it.

The filter was installed and the user Waydroid session restarted, then KakaoTalk reopened without reinstalling or resetting data. Guard regression checks passed. Incoming-message notifications were later confirmed to show their text.

A systemd drop-in (`drivers/files/rootfs/etc/systemd/system/waydroid-container.service.d/10-kakaotalk-notification-filter.conf`) runs the same idempotent installer before every `waydroid-container.service` start, so a Waydroid package upgrade is patched again at the next start without a manual step.

The KakaoTalk setup entry includes this filter. A Waydroid package upgrade may overwrite it: rerun the helper and restart the Waydroid session as the desktop user. To undo, remove the three marked guard lines and restart the session; use the original backup only if the installed package version has not changed. Do not replace a newly upgraded module with an old backup.

Sources: installed Waydroid `tools/services/notification_manager.py` (GPL-3.0-or-later); https://github.com/waydroid/android_frameworks_waydroid/blob/lineage-20/services/java/id/waydro/server/WayDroidService.java . No framework image replacement, conversation database read, polling bridge or additional background service is needed.
