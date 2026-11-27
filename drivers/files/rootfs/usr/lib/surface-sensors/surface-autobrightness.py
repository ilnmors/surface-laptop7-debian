#!/usr/bin/env python3
"""System-wide smooth 12-bit ambient-light backlight controller (Surface Laptop 7).

Reads lux directly from libssc via GObject Introspection (SSC-2.typelib) with
zero subprocesses and drives the panel backlight via sysfs at ~62 Hz using an
exact critically damped second-order spring (C1 velocity-continuous glide).
"""

import glob
import math
import os
import signal
import sys
import time

import gi

gi.require_version("GLib", "2.0")
gi.require_version("SSC", "2")
from gi.repository import GLib, SSC  # noqa: E402

FRAME_MS = 16          # ~62.5 Hz animation
SPRING_OMEGA = 3.6     # rad/s: snappy (~0.8s bulk) yet blends smoothly across 1s ticks
DEADBAND_FRAC = 0.015  # ignore < 1.5% drift when settled
MANUAL_TOL = 20        # raw units (~0.5%) to detect manual adjustment
MIN_FRAC = 0.06        # never dim below 6% automatically
MAX_FRAC = 1.00
MANUAL_COOLDOWN_S = 1.0
RETRY_MS = 2000


def find_backlight():
    paths = sorted(glob.glob("/sys/class/backlight/*"))
    if not paths:
        raise RuntimeError("No backlight device under /sys/class/backlight/")
    d = paths[0]
    with open(os.path.join(d, "max_brightness"), "r", encoding="utf-8") as f:
        max_bl = int(f.read().strip())
    return d, max_bl


def lux_to_base_frac(lux: float) -> float:
    x = math.log10(max(lux, 0.0) + 1.0)
    u = max(0.0, min(1.0, x / 4.2))
    return 0.08 + 0.92 * (u ** 1.85)


class SmoothAutoBrightness:
    def __init__(self):
        self.bl_dir, self.max_bl = find_backlight()
        self.bl_file = os.path.join(self.bl_dir, "brightness")
        self.bl_power_file = os.path.join(self.bl_dir, "bl_power")

        self.loop = GLib.MainLoop()
        self.was_off = False
        self.quitting = False

        self.current_raw = float(self.read_raw())
        self.vel = 0.0
        self.last_written_raw = int(round(self.current_raw))
        self.target_raw = self.current_raw
        self.last_lux = None
        self.user_offset = 0.0
        self.last_manual_ts = 0.0
        self.last_tick_ts = 0.0
        self.fade_source_id = 0

        self.sensor = None
        self.meas_handler_id = 0
        self.retry_id = 0

    def read_raw(self) -> int:
        with open(self.bl_file, "r", encoding="utf-8") as f:
            return int(f.read().strip())

    def panel_is_off(self) -> bool:
        try:
            if os.path.exists(self.bl_power_file):
                with open(self.bl_power_file, "r", encoding="utf-8") as f:
                    if int(f.read().strip()) != 0:
                        return True
        except OSError:
            pass
        return self.read_raw() == 0

    def write_raw(self, value: int) -> None:
        clamped = max(1, min(self.max_bl, int(value)))
        try:
            with open(self.bl_file, "w", encoding="utf-8") as f:
                f.write(f"{clamped}\n")
            self.last_written_raw = clamped
        except OSError as exc:
            print(f"write({clamped}) failed: {exc}", file=sys.stderr, flush=True)

    def check_manual_change(self) -> bool:
        actual = self.read_raw()
        if actual == 0:
            self.was_off = True
            self.stop_fade()
            return True
        if self.was_off:
            self.was_off = False
            self.current_raw = float(actual)
            self.target_raw = float(actual)
            self.vel = 0.0
            self.last_written_raw = actual
            return False
        if abs(actual - self.last_written_raw) > MANUAL_TOL:
            self.stop_fade()
            self.current_raw = float(actual)
            self.target_raw = float(actual)
            self.last_written_raw = actual
            self.last_manual_ts = time.monotonic()
            if self.last_lux is not None:
                base = lux_to_base_frac(self.last_lux)
                actual_frac = actual / self.max_bl
                self.user_offset = max(-0.45, min(0.45, actual_frac - base))
                print(
                    f"Manual brightness {actual}/{self.max_bl} ({actual_frac*100:.1f}%); "
                    f"offset={self.user_offset*100:+.1f}%",
                    flush=True,
                )
            return True
        return False

    def stop_fade(self) -> None:
        if self.fade_source_id:
            GLib.source_remove(self.fade_source_id)
            self.fade_source_id = 0
        self.vel = 0.0

    def start_fade(self) -> None:
        if not self.fade_source_id:
            self.last_tick_ts = time.monotonic()
            self.fade_source_id = GLib.timeout_add(FRAME_MS, self.on_fade_tick)

    def on_fade_tick(self) -> bool:
        if self.panel_is_off():
            self.was_off = True
            self.stop_fade()
            return False
        if self.check_manual_change():
            return False

        now = time.monotonic()
        dt = max(0.004, min(0.05, now - self.last_tick_ts))
        self.last_tick_ts = now

        # Exact analytical critically damped spring: x'' + 2*w*x' + w^2*x = 0
        w = SPRING_OMEGA
        x = self.current_raw - self.target_raw
        v = self.vel
        exp_term = math.exp(-w * dt)
        tmp = v + w * x
        new_x = (x + tmp * dt) * exp_term
        new_v = (v - w * tmp * dt) * exp_term

        self.current_raw = max(1.0, min(float(self.max_bl), self.target_raw + new_x))
        self.vel = new_v

        if abs(new_x) <= 0.75 and abs(new_v) <= 5.0:
            self.current_raw = self.target_raw
            self.vel = 0.0
            final_int = int(round(self.current_raw))
            if final_int != self.last_written_raw:
                self.write_raw(final_int)
            self.fade_source_id = 0
            return False

        next_int = int(round(self.current_raw))
        if next_int != self.last_written_raw:
            self.write_raw(next_int)
        return True

    def handle_lux(self, lux: float) -> None:
        if lux < 0.0 or not math.isfinite(lux):
            return
        if self.panel_is_off():
            self.was_off = True
            return
        if self.check_manual_change():
            return
        if time.monotonic() - self.last_manual_ts < MANUAL_COOLDOWN_S:
            return

        if self.last_lux is None:
            self.last_lux = lux
            actual = self.read_raw()
            self.current_raw = float(actual)
            self.last_written_raw = actual
            self.vel = 0.0
            base = lux_to_base_frac(lux)
            self.user_offset = max(-0.35, min(0.35, (actual / self.max_bl) - base))
            print(
                f"Initial lux={lux:.1f}, brightness={actual}/{self.max_bl}, "
                f"base={base*100:.1f}%, offset={self.user_offset*100:+.1f}%",
                flush=True,
            )
            return

        self.last_lux = lux
        desired_frac = max(MIN_FRAC, min(MAX_FRAC, lux_to_base_frac(lux) + self.user_offset))
        desired_raw = desired_frac * self.max_bl

        if not self.fade_source_id:
            if abs(desired_raw - self.current_raw) < self.max_bl * DEADBAND_FRAC:
                return

        self.target_raw = desired_raw
        self.start_fade()

    def on_measurement(self, _sensor, intensity: float) -> None:
        self.handle_lux(float(intensity))

    def close_sensor(self) -> None:
        if self.sensor is not None:
            if self.meas_handler_id:
                try:
                    self.sensor.disconnect(self.meas_handler_id)
                except Exception:
                    pass
                self.meas_handler_id = 0
            try:
                self.sensor.close_sync(None)
            except Exception as exc:
                print(f"sensor close_sync: {exc}", file=sys.stderr, flush=True)
            self.sensor = None

    def open_sensor(self) -> bool:
        self.retry_id = 0
        if self.quitting:
            return False
        self.close_sensor()
        try:
            sensor = SSC.SensorLight.new_sync(None)
            self.meas_handler_id = sensor.connect("measurement", self.on_measurement)
            sensor.open_sync(None)
            self.sensor = sensor
            print("Opened native libssc light sensor stream", flush=True)
        except Exception as exc:
            print(f"Failed to open libssc light sensor: {exc}; retrying in 2s", file=sys.stderr, flush=True)
            self.close_sensor()
            self.retry_id = GLib.timeout_add(RETRY_MS, self.open_sensor)
        return False

    def run(self) -> None:
        def handle_quit(*_args):
            self.quitting = True
            if self.retry_id:
                GLib.source_remove(self.retry_id)
                self.retry_id = 0
            self.stop_fade()
            self.close_sensor()
            self.loop.quit()

        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGTERM, handle_quit)
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, handle_quit)
        GLib.idle_add(self.open_sensor)
        self.loop.run()


if __name__ == "__main__":
    SmoothAutoBrightness().run()
