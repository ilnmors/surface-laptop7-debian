#!/bin/bash
# Root, with the Waydroid session running (install the APK first as the session user:
# `waydroid app install com.retekey_206.apk`, as setup.sh does): Korean input inside Android and no "physical keyboard" notification.
# 1. Install ReteKey (F-Droid build 0.2.3/206, MIT; Hangul 2-beolsik on physical keyboards, assignable KO/EN key)
#    and make it the default input method. The AOSP keyboard stays installed.
# 2. Turn off Android's PHYSICAL_KEYBOARD notification channel (package "android", blockable system channel) in
#    /data/system/notification_policy.xml: this script writes the edited copy (.keyboard-off); setup.sh stops the
#    session, puts the copy in place and starts the session again (open apps such as KakaoTalk close).
set -euo pipefail
here=$(dirname "$(realpath "$0")")
apk=$here/com.retekey_206.apk
echo "bc57304266886af0268ba1a3bafb899ad3916df126496f7aca15709bb6948e42  $apk" | sha256sum -c --quiet -
ws() { waydroid shell -- sh -c "$1"; }
waydroid status | grep -q "Container:.*RUNNING" || { echo "start the Waydroid session first"; exit 1; }
for i in $(seq 30); do ws 'pm list packages com.retekey' | grep -q com.retekey && break; sleep 2; done
ws 'pm list packages com.retekey' | grep -q com.retekey || { echo "install the APK as the session user first: waydroid app install $apk"; exit 1; }
ime=$(ws 'ime list -a -s' | grep '^com.retekey/' | head -1 | tr -d '\r')
[ -n "$ime" ] || { echo "ReteKey's input method was not found"; exit 1; }
ws "ime enable $ime >/dev/null; ime set $ime >/dev/null"
echo "input method: $(ws 'settings get secure default_input_method')"
p=/data/system/notification_policy.xml
# Write the edited policy next to the live file; setup.sh restarts the session and puts it in place, because the
# running system_server keeps the channel in memory (an in-place `stop`/`start` inside Waydroid does not reload it).
if ws "abx2xml $p -" | grep -q '<channel id="PHYSICAL_KEYBOARD"[^>]*importance="0"'; then
  echo "physical keyboard notification already off"
else
  ws "[ -e $p.before-keyboard ] || cp -p $p $p.before-keyboard
      abx2xml $p /data/local/tmp/np.xml
      sed -i 's/\\(<channel id=\"PHYSICAL_KEYBOARD\"[^>]*\\) importance=\"[0-9]\"/\\1 importance=\"0\"/' /data/local/tmp/np.xml
      grep -q '<channel id=\"PHYSICAL_KEYBOARD\"[^>]* importance=\"0\"' /data/local/tmp/np.xml
      xml2abx /data/local/tmp/np.xml $p.keyboard-off; chown system:system $p.keyboard-off; chmod 600 $p.keyboard-off
      rm -f /data/local/tmp/np.xml"
  echo "edited policy written to $p.keyboard-off; restart the session and copy it over $p while it is stopped"
fi
echo "Next, in ReteKey's settings (open it from the app list): Physical keyboard -> set the KO/EN key by pressing the 한/영 key."
