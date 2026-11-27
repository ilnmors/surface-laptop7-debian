#!/bin/bash
set -euo pipefail

if (( EUID != 0 )); then
  echo "Run as root (via pkexec)." >&2
  exit 1
fi

systemctl disable --now surface-autobrightness.service 2>/dev/null || true
systemctl disable surface-sensors.service 2>/dev/null || true
systemctl stop iio-sensor-proxy.service 2>/dev/null || true
systemctl stop surface-sensors.service 2>/dev/null || true

rm -rf \
  /usr/lib/surface-sensors \
  /var/lib/surface-sensors \
  /usr/local/bin/monitor-sensor \
  /usr/local/bin/ssccli \
  /etc/dbus-1/system.d/net.hadess.SensorProxy.conf \
  /usr/share/polkit-1/actions/net.hadess.SensorProxy.policy \
  /etc/udev/rules.d/80-surface-iio-sensor-proxy.rules \
  /etc/systemd/system/surface-autobrightness.service \
  /etc/systemd/system/surface-sensors.service \
  /etc/systemd/system/iio-sensor-proxy.service \
  /etc/systemd/system/iio-sensor-proxy.service.d \
  /etc/dconf/db/local.d/90-surface-autobrightness \
  /usr/lib/systemd/system-sleep/surface-sensors

dconf update 2>/dev/null || true
systemctl daemon-reload
echo "Rolled back all staged surface-sensors files. Reboot cleanly if the sensor service had started."
