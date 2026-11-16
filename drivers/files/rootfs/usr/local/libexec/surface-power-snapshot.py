#!/usr/bin/env python3
"""Bounded suspend boundary telemetry; never changes hardware or power policy."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import os
import stat
import time


def read(path):
    try:
        return path.read_text().strip()[:4096]
    except OSError:
        return None


def snapshot(phase, operation):
    started = time.monotonic()
    result = {
        "version": 1, "phase": phase, "operation": operation,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "wall_seconds": time.time(),
        "boottime_seconds": time.clock_gettime(time.CLOCK_BOOTTIME),
        "boot_id": read(Path("/proc/sys/kernel/random/boot_id")),
        "mem_sleep": read(Path("/sys/power/mem_sleep")),
        "power_supplies": {}, "qcom_stats": {}, "usb": [],
        "suspend_stats": {},
    }
    for device in sorted(Path("/sys/class/power_supply").glob("*")):
        values = {}
        for key in ("type", "status", "online", "energy_now", "energy_full", "power_now"):
            value = read(device / key)
            if value is not None:
                values[key] = value
        result["power_supplies"][device.name] = values
    # These are architecture-counter ticks, not seconds. Keep raw values.
    for name in ("aosd", "cxsd", "ddr", "apss", "adsp", "adsp_island", "wpss"):
        result["qcom_stats"][name] = read(Path("/sys/kernel/debug/qcom_stats") / name)
    for device in sorted(Path("/sys/bus/usb/devices").glob("*")):
        if not (device / "idVendor").exists():
            continue
        values = {"path": device.name}
        for key in ("idVendor", "idProduct", "power/control", "power/runtime_status"):
            values[key] = read(device / key)
        result["usb"].append(values)
    for name in ("success", "fail", "last_failed_step", "last_failed_errno"):
        result["suspend_stats"][name] = read(Path("/sys/power/suspend_stats") / name)
    result["collector_ms"] = round((time.monotonic() - started) * 1000, 3)
    return result


def save(result):
    directory = Path("/var/lib/surface-power")
    directory.mkdir(mode=0o755, exist_ok=True)
    info = directory.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
        raise RuntimeError("Unsafe telemetry directory")
    log = directory / "suspend.jsonl"
    if log.exists() and log.stat().st_size >= 2 * 1024 * 1024:
        log.replace(directory / "suspend.previous.jsonl")
    fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, "w") as stream:
        stream.write(json.dumps(result, separators=(",", ":")) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("pre", "post", "manual"))
    parser.add_argument("operation", nargs="?", default="suspend")
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    result = snapshot(args.phase, args.operation)
    if args.stdout:
        print(json.dumps(result))
    else:
        if os.geteuid() != 0:
            parser.error("Writing system telemetry requires root; use --stdout for a read-only sample")
        save(result)


if __name__ == "__main__":
    main()
