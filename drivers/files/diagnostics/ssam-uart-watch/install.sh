#!/bin/bash
# Root: install and start the EC UART counter logger. Listed in ../DIAGNOSTIC-SERVICES.md; remove with ../remove-all.sh.
set -euo pipefail
here=$(dirname "$(realpath "$0")")
install -m755 "$here/surface-ssam-uart-watch.sh" /usr/local/sbin/surface-ssam-uart-watch
install -m644 "$here/surface-ssam-uart-watch.service" /etc/systemd/system/surface-ssam-uart-watch.service
systemctl daemon-reload; systemctl enable --now surface-ssam-uart-watch.service
systemctl is-active surface-ssam-uart-watch.service
