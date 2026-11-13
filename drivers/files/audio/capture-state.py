#!/usr/bin/env python3
"""Read-only audio recurrence snapshot; run in the desktop user's session."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import time


def run(*args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=8)
        return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"returncode": None, "stdout": "", "stderr": str(e)}


def read(path):
    try:
        return Path(path).read_text().strip()
    except OSError as e:
        return {"unavailable": str(e)}


def pipewire():
    result = run("pw-dump")
    try:
        objects = json.loads(result["stdout"])
    except (ValueError, TypeError):
        return {"returncode": result["returncode"], "error": result["stderr"] or "No valid PipeWire snapshot"}
    nodes, links = [], []
    for obj in objects:
        info = obj.get("info", {})
        props = info.get("props", {})
        if obj.get("type") == "PipeWire:Interface:Node" and "Audio" in props.get("media.class", ""):
            node = {"id": obj["id"], "state": info.get("state")}
            node["properties"] = {k: props[k] for k in (
                "application.name", "media.class", "device.id", "node.pause-on-idle",
                "session.suspend-timeout-seconds") if k in props}
            if str(props.get("node.name", "")).startswith("alsa_"):
                node["alsa_node_name"] = props["node.name"]
            node["volume"] = [{k: v for k, v in param.items() if k in (
                "volume", "mute", "channelVolumes", "softMute", "softVolumes")}
                for param in info.get("params", {}).get("Props", [])]
            nodes.append(node)
        elif obj.get("type") == "PipeWire:Interface:Link":
            links.append({k: info[k] for k in (
                "output-node-id", "input-node-id", "state") if k in info})
    return {"nodes": nodes, "links": links, "returncode": result["returncode"], "stderr": result["stderr"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", choices=("silent", "audible", "unknown"), default="unknown",
                        help="What the user actually hears; never inferred from software state")
    args = parser.parse_args()
    if os.geteuid() == 0:
        parser.error("Run as the desktop user, without sudo, to capture that user's PipeWire session.")
    now = datetime.now().astimezone()
    data = {"started": now.isoformat(), "monotonic_start": time.monotonic(),
            "reported_audibility": args.state, "kernel": os.uname().release,
            "boot_id": read("/proc/sys/kernel/random/boot_id"),
            "soundwire_srcversion": read("/sys/module/soundwire_qcom/srcversion")}
    devices = [Path("/sys/bus/platform/devices/6b10000.soundwire")]
    devices += sorted(Path("/sys/bus/soundwire/devices").glob("sdw:*:0217:0204:00:*"))
    data["power"] = {str(p): {k: read(p/"power"/k) for k in (
        "control", "runtime_status", "autosuspend_delay_ms", "runtime_active_time", "runtime_suspended_time")}
        for p in devices}
    data["pcm"] = {str(p): read(p) for p in sorted(Path("/proc/asound").glob("card*/pcm*p/sub*/status"))}
    data["pipewire"] = pipewire()
    cards = [p for p in Path("/proc/asound").glob("card*/id") if read(p) == "X1E80100Romulus"]
    data["mixer"] = {}
    if cards:
        card = cards[0].parent.name.removeprefix("card")
        for name in ("Speakers Volume", "SpkrLeft PA Volume", "SpkrRight PA Volume",
                     "WSA WSA_RX0 Digital Mute", "WSA WSA_RX1 Digital Mute",
                     "WSA WSA_RX0 Digital Volume", "WSA WSA_RX1 Digital Volume",
                     "WSA_CODEC_DMA_RX_0 Audio Mixer MultiMedia2"):
            data["mixer"][name] = run("amixer", "-c", card, "cget", "name=" + name)
    else:
        data["mixer_unavailable"] = "Expected Romulus card not found; do not guess another card."
    journal = run("journalctl", "-k", "-b", "--since=-10min", "--no-pager", "-o", "json")
    entries, visible = [], 0
    for line in journal["stdout"].splitlines():
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        visible += 1
        message = entry.get("MESSAGE", "")
        if isinstance(message, str) and re.search(r"soundwire|wsa88|qcom.apm|audioreach|adsp|clsh|parity", message, re.I):
            entries.append({k: entry[k] for k in ("__REALTIME_TIMESTAMP", "__MONOTONIC_TIMESTAMP", "MESSAGE") if k in entry})
    data["kernel_log"] = {"entries": entries, "visible_recent_entries": visible,
                          "returncode": journal["returncode"], "stderr": journal["stderr"],
                          "limit": "No entries can mean restricted access or no recent messages; it does not prove no kernel faults."}
    data["finished"] = datetime.now().astimezone().isoformat()
    data["monotonic_end"] = time.monotonic()
    folder = Path.home()/".local/state/surface-audio/recurrence"
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    target = folder/(now.strftime("%Y%m%dT%H%M%S.%f%z") + ".json")
    fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(target)
    print("Snapshot saved; audibility is user-reported. No audio settings changed.")
    if visible == 0:
        print("Kernel journal was empty or unavailable; privileged log inspection may still be needed.")


if __name__ == "__main__":
    main()
