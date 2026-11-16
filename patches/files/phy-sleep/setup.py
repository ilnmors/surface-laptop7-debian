#!/usr/bin/env python3
"""Install or restore the signed PHY sleep trial; never hot-reload active PHYs."""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, struct, subprocess, sys

HERE = Path(__file__).resolve().parent
BUNDLE = HERE.parents[2]
KERNEL = "7.3.0-31-qcom-x1e"
STATE = Path("/var/lib/surface-power/phy-sleep-20261116")
BACKUP = STATE / "backup"
BOOT = Path("/boot/secureboot")
FALLBACK = BOOT / "rollback-phy-sleep-20261116"
MODULES = Path("/lib/modules") / KERNEL / "updates/surface"
HOOK = Path("/etc/initramfs-tools/hooks/surface-kernel-patches")
NAMES = ("phy-qcom-qmp-combo", "phy-qcom-qmp-usb")

def run(*args, **kw):
    return subprocess.run(args, check=True, **kw)

def digest(path):
    return hashlib.file_digest(path.open("rb"), "sha256").hexdigest()

def restore():
    manifest = json.loads((BACKUP / "manifest.json").read_text())
    for name, item in manifest.items():
        target = Path(name)
        if item is None:
            target.unlink(missing_ok=True)
        else:
            source = BACKUP / item["file"]
            if digest(source) != item["sha256"]:
                raise RuntimeError("Backup checksum mismatch: " + name)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    run("/usr/sbin/depmod", "-a", KERNEL)
    (STATE / "installed.json").unlink(missing_ok=True)
    print("Original module selection, initramfs and boot configuration restored; reboot to use them.", flush=True)

def apply():
    if os.uname().release != KERNEL:
        raise RuntimeError("This build is only for " + KERNEL)
    if (STATE / "installed.json").exists():
        print("Trial is already installed; live validation follows after reboot.")
        return
    if (BACKUP / "manifest.json").exists():
        raise RuntimeError("A previous backup exists; preserve it and review before another installation")
    meta = json.loads((HERE / "verification.json").read_text())
    for name in NAMES:
        source = HERE / "files" / (name + ".ko")
        if digest(source) != meta["modules"][name]["sha256_signed"]:
            raise RuntimeError("Module checksum changed")
        version = subprocess.check_output(["/usr/sbin/modinfo", "-F", "vermagic", str(source)], text=True)
        if not version.startswith(KERNEL + " "):
            raise RuntimeError("Kernel ABI mismatch")
    if not meta.get("guest_signature_and_abi", "").startswith("passed"):
        raise RuntimeError("Signature/ABI verification must pass first")
    STATE.mkdir(parents=True, exist_ok=True, mode=0o755)
    BACKUP.mkdir(mode=0o755)
    paths = [BOOT / "vmlinuz-surface-signed.efi", BOOT / ("initrd.img-" + KERNEL), BOOT / "grub.cfg", Path("/boot/initrd.img-" + KERNEL), Path("/boot/efi/EFI/debian/grub.cfg"), HOOK]
    paths += [MODULES / (name + ".ko") for name in NAMES]
    manifest = {}
    for path in paths:
        if path.exists():
            rel = str(path).lstrip("/")
            target = BACKUP / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            manifest[str(path)] = {"file": rel, "sha256": digest(target)}
        else:
            manifest[str(path)] = None
    (BACKUP / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    grub = (BOOT / "grub.cfg").read_text()
    first = re.search(r"menuentry [^\n]+\{\n.*?\n\}", grub, flags=re.S)
    if not first or "/secureboot/vmlinuz-surface-signed.efi" not in first.group():
        raise RuntimeError("Unexpected boot layout; no mutation performed")
    fallback_entry = re.sub(r"menuentry [^\n]+", "menuentry 'Surface before PHY sleep patch (2026-11-16)' {", first.group(), count=1)
    fallback_entry = fallback_entry.replace("/secureboot/vmlinuz-", "/secureboot/rollback-phy-sleep-20261116/vmlinuz-").replace("/secureboot/initrd.", "/secureboot/rollback-phy-sleep-20261116/initrd.")
    FALLBACK.mkdir(exist_ok=True)
    for name in ["vmlinuz-surface-signed.efi", "initrd.img-" + KERNEL]:
        shutil.copy2(BOOT / name, FALLBACK / name)
        if digest(FALLBACK / name) != digest(BOOT / name):
            raise RuntimeError("Boot fallback checksum mismatch")
    # Preserve the exact DTB embedded in the current signed default image.
    blob = (BOOT / "vmlinuz-surface-signed.efi").read_bytes()
    pe = struct.unpack_from("<I", blob, 0x3c)[0]
    count = struct.unpack_from("<H", blob, pe + 6)[0]
    table = pe + 24 + struct.unpack_from("<H", blob, pe + 20)[0]
    for i in range(count):
        header = blob[table + i * 40:table + (i + 1) * 40]
        if header[:8].rstrip(bytes([0])) == b".dtbauto":
            size = struct.unpack_from("<I", header, 8)[0]
            offset = struct.unpack_from("<I", header, 20)[0]
            (BACKUP / "current.dtb").write_bytes(blob[offset:offset + size])
            break
    else:
        raise RuntimeError("Cannot preserve the current embedded DTB")
    try:
        MODULES.mkdir(parents=True, exist_ok=True)
        for name in NAMES:
            shutil.copyfile(HERE / "files" / (name + ".ko"), MODULES / (name + ".ko"))
            (MODULES / (name + ".ko")).chmod(0o644)
        hook = HOOK.read_text()
        if "manual_add_modules phy_qcom_qmp_combo phy_qcom_qmp_usb" not in hook:
            HOOK.write_text(hook.rstrip() + "\nmanual_add_modules phy_qcom_qmp_combo phy_qcom_qmp_usb\n")
        print("Backups verified; signing modules and refreshing initramfs/boot image.", flush=True)
        run("/usr/local/sbin/surface-secureboot-update", KERNEL, "--dtb", str(BACKUP / "current.dtb"))
        # Keep the prior command line/menu, adding an exact-current-image fallback.
        (BOOT / "grub.cfg").write_text(grub.rstrip() + "\n" + fallback_entry + "\n")
        run("/usr/bin/grub-script-check", str(BOOT / "grub.cfg"))
        efi = Path("/boot/efi/EFI/debian/grub.cfg")
        saved = manifest.get(str(efi))
        if saved:
            shutil.copy2(BACKUP / saved["file"], efi)
        entries = subprocess.check_output(["/usr/bin/lsinitramfs", str(BOOT / ("initrd.img-" + KERNEL))], text=True)
        for name in NAMES:
            if "/updates/surface/" + name + ".ko" not in entries:
                raise RuntimeError("Replacement absent from initramfs: " + name)
        run("/usr/bin/sbverify", "--cert", "/var/lib/surface-secureboot/MOK.pem", str(BOOT / "vmlinuz-surface-signed.efi"))
        result = {"kernel": KERNEL, "modules": {name: subprocess.check_output(["/usr/sbin/modinfo", "-F", "srcversion", name], text=True).strip() for name in NAMES}, "boot_id_before": Path("/proc/sys/kernel/random/boot_id").read_text().strip(), "hardware_validation": "pending reboot and sleep measurement", "fallback": str(FALLBACK)}
        (STATE / "installed.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result), flush=True)
    except BaseException:
        restore()
        raise

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--restore", action="store_true")
    parser.add_argument("--system", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not args.system:
        if os.geteuid() == 0:
            parser.error("Start this installer as the desktop user")
        command = ["pkexec", "/usr/bin/python3", "-I", str(Path(__file__).resolve()), "--system"]
        if args.restore:
            command.append("--restore")
        run(*command)
    else:
        if os.geteuid() != 0:
            parser.error("System step requires authentication")
        if args.restore:
            restore()
        else:
            apply()

if __name__ == "__main__":
    main()
