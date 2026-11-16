#!/usr/bin/env python3
"""Build only the two system-sleep PHY modules from retained offline inputs."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, tarfile

here = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("output", type=Path, help="new absolute directory, owned by the desktop user")
args = parser.parse_args()
work = args.output
if not work.is_absolute() or work.exists():
    parser.error("use a new absolute output directory")
if os.geteuid() == 0:
    parser.error("build as the desktop user, not root")
meta = json.loads((here / "verification.json").read_text())
archive = here / "files/matching-phy-sources.tar.gz"
if hashlib.sha256(archive.read_bytes()).hexdigest() != meta["source_archive_sha256"]:
    raise SystemExit("Source archive checksum mismatch")
source = work / "source"
source.mkdir(parents=True)
headers = work / "headers"
headers.mkdir()
with tarfile.open(archive) as tar:
    tar.extractall(source, filter="data")
for package in sorted((here.parent / "headers").glob("*.deb")):
    subprocess.run(["dpkg-deb", "-x", str(package), str(headers)], check=True)
for patch in sorted((here / "patches").glob("*.patch")):
    subprocess.run(["patch", "--batch", "--fuzz=0", "-p4", "-i", str(patch)], cwd=source, check=True)
(source / "Makefile").write_text("obj-m += phy-qcom-qmp-combo.o\nobj-m += phy-qcom-qmp-usb.o\n")
subprocess.run(["make", "-C", str(headers / "usr/src" / ("linux-headers-" + meta["kernel"])), "M=" + str(source), "CC=" + os.environ.get("CC", "gcc-14"), "-j2", "modules"], check=True)
print("Unsigned modules:", source)
