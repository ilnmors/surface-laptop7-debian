#!/usr/bin/env python3
"""Verify signatures and module ABI in a RAM-only ARM64 guest without network."""
from pathlib import Path
import argparse, json, os, shutil, subprocess, tempfile
here = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--image", type=Path, default=Path("/var/lib/surface-power/phy-sleep-20261116/Image"))
args = parser.parse_args()
if os.geteuid() == 0:
    parser.error("run the guest as the desktop user")
meta = json.loads((here / "verification.json").read_text())
bundle = here.parents[2]
with tempfile.TemporaryDirectory(prefix="surface-phy-verify-") as tmp:
    work = Path(tmp)
    subprocess.run(["python3", str(bundle / "kernel/files/secureboot/verification/make-test-initrd.py"), str(work)], check=True)
    root = work / "verify-initrd"
    commands = []
    copied = set()
    for module in meta["modules"]:
        deps = subprocess.check_output(["/usr/sbin/modprobe", "--show-depends", module], text=True)
        for line in deps.splitlines():
            if not line.startswith("insmod "):
                continue
            original = Path(line.split()[1])
            name = original.name.split(".ko")[0]
            if name in copied:
                continue
            copied.add(name)
            target = root / (name + ".ko")
            if name in meta["modules"]:
                target.write_bytes((here / "files" / (name + ".ko")).read_bytes())
            elif original.suffix == ".zst":
                target.write_bytes(subprocess.check_output(["zstd", "-qdc", str(original)]))
            else:
                target.write_bytes(original.read_bytes())
            commands.append(f"if /bin/busybox insmod /{target.name}; then echo PASS_{name}; else echo FAIL_{name}; fi")
    init = root / "init"
    init.write_text(init.read_text().replace("echo VERIFY_COMPLETE", "\n".join(commands) + "\necho VERIFY_COMPLETE"))
    names = b"\0".join(b"./" + str(p.relative_to(root)).encode() for p in sorted(root.rglob("*"))) + b"\0"
    with (work / "initrd").open("wb") as output:
        subprocess.run(["cpio", "--null", "-o", "--format=newc", "--quiet"], input=names, stdout=output, cwd=root, check=True)
    with (here / "vm-module-load.log").open("w") as log:
        proc = subprocess.run(["qemu-system-aarch64", "-machine", "virt,gic-version=3", "-cpu", "max", "-accel", "tcg,thread=multi", "-m", "1024", "-smp", "2", "-display", "none", "-monitor", "none", "-serial", "stdio", "-nodefaults", "-nic", "none", "-no-reboot", "-kernel", str(args.image), "-initrd", str(work / "initrd"), "-append", "console=ttyAMA0 rdinit=/init module.sig_enforce=1 panic=-1 cma=16M"], stdout=log, stderr=subprocess.STDOUT, timeout=60)
    text = (here / "vm-module-load.log").read_text()
    required = ["PASS_UNSIGNED_REJECTED", "PASS_SIGNED_ACCEPTED", "VERIFY_COMPLETE"] + ["PASS_" + name for name in meta["modules"]]
    if proc.returncode or "FAIL_" in text or not all(x in text for x in required):
        raise SystemExit("Guest verification failed; inspect vm-module-load.log")
    print("\n".join(line for line in text.splitlines() if "PASS_" in line or "VERIFY_COMPLETE" in line))
print("Signature/ABI checks passed; physical PHY suspend behavior still requires a boot and sleep test.")
