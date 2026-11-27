# Ambient light sensor and smooth automatic brightness

Surface Laptop 7 13.8" (`microsoft,romulus13`, Snapdragon X Plus `X1P-64-100`, SoC ID `615`, revision `2.1`) exposes its AMS TCS3430 ambient light / color sensor (`SEN2`/`SEN3`, `MSHW0473`/`0474`) behind the Qualcomm ADSP Sensor Core (SSC), not on Linux I2C.

## Architecture

```
TCS3430 -> ADSP sensor_pd <- hexagonrpcd (serves /var/lib/surface-sensors/root)
        -> QRTR/QMI -> libssc (SSC-2.typelib) -> surface-autobrightness.service -> /sys/class/backlight/backlight/brightness
```

- `hexagonrpcd` (`linux-msm/hexagonrpc` commit `dd9ac70c026e1bad93e8cffa3801255b8ceb551e` + `0001-apps-std-support-writable-sensor-registry.patch`) serves the OEM sensor JSON configs and lets the ADSP write its runtime registry under `/var/lib/surface-sensors/root/sensors/persist/`.
- `libssc` (`DylanVanAssche/libssc` commit `54dd13e36d65c21263cf5b0f4a70c230a77b26bc` + `0001-light-use-surface-color-sensor.patch`) reads illuminance from Microsoft's `color` sensor (`ambient_light` reports 0 on this hardware). Installed privately under `/usr/lib/surface-sensors/` alongside its GObject Introspection typelib `girepository-1.0/SSC-2.typelib`.
- `iio-sensor-proxy` 3.9 (`0085ddf8ecb173a1c5fcf2344aa40e561125354f`, built with `-Dssc-support=enabled`) and `monitor-sensor` / `ssccli` are also installed privately for standard D-Bus clients and diagnostics.
- `surface-autobrightness.service` runs `/usr/lib/surface-sensors/surface-autobrightness.py` system-wide (gated on `microsoft,romulus13`). It opens `SSC.SensorLight` directly via GObject Introspection (`GI_TYPELIB_PATH=/usr/lib/surface-sensors/girepository-1.0`) and drives the 12-bit (`0..4095`) panel backlight at ~62 Hz using an exact critically damped second-order spring (`SPRING_OMEGA=3.6 rad/s`), tracking manual brightness adjustments as a live offset.
- GNOME's built-in `gsd-power` auto-brightness is disabled system-wide via `/etc/dconf/db/local.d/90-surface-autobrightness` (`ambient-enabled=false`) for two verified reasons:
  1. GNOME 48 `gsd-power` steps backlight in coarse 1% (~41/4095) jumps once per second without fade interpolation.
  2. After deep suspend/resume, `iio-sensor-proxy`'s `drv-ssc-light` wedged at `0.00 lux` even after restarting `iio-sensor-proxy.service`, whereas direct `libssc` streams accurate lux immediately on every resume.
- `/usr/lib/systemd/system-sleep/surface-sensors` stops `surface-autobrightness.service` and `iio-sensor-proxy.service` on `pre` suspend (otherwise an open SSC indication stream wakes deep sleep repeatedly) and restarts them after a 1.5 s `post` delay.

## Verified behavior (2026-11-27)

- Fresh boot: `surface-sensors.service` populates `/var/lib/surface-sensors/root/sensors/persist/registry/` cleanly (~1.28 MB, no zero-size `color_calibration.bin`).
- Audio coexistence: ADSP speaker playback works normally alongside the sensor core.
- Smooth auto-brightness: continuous native `libssc` GI streaming (`NRestarts=0`), smooth 12-bit fade across rapid light transitions, manual offset tracking.
- Deep suspend/resume: 22m04s (`1324.271 s`) continuous deep sleep with zero spurious wakeups (woke by user `IRQ 175`); `surface-autobrightness.service` stopped cleanly on `pre`, restarted automatically at `post`, and recovered live lux readings within ~2 s.

## Safety and rollback

- Never restart `surface-sensors.service` or unbind the ADSP live; enable it and let a clean reboot initialize `sensor_pd`.
- To remove all installed sensor binaries, configs, systemd units, dconf override, and sleep hook:

```sh
sudo bash drivers/files/sensors/rollback.sh
```

Then reboot cleanly so the ADSP starts without `surface-sensors.service`.
