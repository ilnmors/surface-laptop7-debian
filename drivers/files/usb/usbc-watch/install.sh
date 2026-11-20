#!/bin/bash
# Root: install and start the passive USB-C snapshot collector. Remove: systemctl disable --now surface-usbc-watch;
# rm /usr/local/sbin/surface-usbc-watch /etc/systemd/system/surface-usbc-watch.service
set -euo pipefail
here=$(dirname "$(realpath "$0")")
install -m755 "$here/surface-usbc-watch.sh" /usr/local/sbin/surface-usbc-watch
install -m644 "$here/surface-usbc-watch.service" /etc/systemd/system/surface-usbc-watch.service
systemctl daemon-reload; systemctl enable --now surface-usbc-watch.service
systemctl is-active surface-usbc-watch.service
