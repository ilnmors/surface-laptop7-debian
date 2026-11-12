# Notification body investigation

GNOME notifications and banners are enabled. The installed Linux notification manager forwards summary/body received from Android without truncation. The user sees banners but usually no body; Android-side display has not been compared.

Upstream Android WayDroidService reads EXTRA_TITLE and EXTRA_TEXT using Bundle.getString. It has no MessagingStyle/BigText fallback in this path. Empty text or a CharSequence type mismatch is a candidate, not a confirmed diagnosis for this device. Also check KakaoTalk notification preview settings. No chat text or private database was collected; no Android framework replacement was installed.

Source: https://github.com/waydroid/android_frameworks_waydroid/blob/lineage-20/services/java/id/waydro/server/WayDroidService.java (onNotificationPosted).

Keep background reception enabled as requested. Do not fabricate bodies from old messages or install a polling bridge merely to hide empty banners. A complete fix needs metadata-only reproduction and an Android-side correction if that path is confirmed.
