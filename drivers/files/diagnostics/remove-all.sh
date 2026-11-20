#!/bin/bash
# Root: stop and remove every diagnostic service listed in DIAGNOSTIC-SERVICES.md. Logs under /var/log are kept
# unless --purge-logs is given.
set -uo pipefail
units=(surface-usbc-watch surface-ssam-uart-watch)
for u in "${units[@]}"; do
  systemctl disable --now "$u.service" 2>/dev/null
  rm -f "/etc/systemd/system/$u.service" "/usr/local/sbin/$u"
  [ "${1:-}" = --purge-logs ] && rm -rf "/var/log/$u"
done
systemctl daemon-reload
for u in "${units[@]}"; do
  if [ -e "/etc/systemd/system/$u.service" ] || [ -e "/usr/local/sbin/$u" ]; then echo "$u: NOT removed"; else echo "$u: removed"; fi
done
