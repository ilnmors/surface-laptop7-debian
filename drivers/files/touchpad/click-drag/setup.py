#!/usr/bin/env python3
"""Install the tested Romulus click-state fix; restart only its IPTSD instance."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, time
HERE = Path(__file__).resolve().parent
TARGET = Path('/usr/local/libexec/surface-iptsd/iptsd')
CANDIDATE = HERE.parents[1] / 'rootfs/usr/local/libexec/surface-iptsd/iptsd'
OLD = 'bbc4cd4bfce32bf466799ba44e3dbd9d970eea9cc961ecb8a700f130052c33d1'
NEW = '750247bc700539bbd8f79f867a129637a0ee840490efaf207041532cca0a8ae1'
BACKUP = Path('/var/lib/surface-touchpad/20261115-click-drag/iptsd.before')
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def apply():
    if digest(CANDIDATE) != NEW:
        raise SystemExit('Candidate differs from the tested binary; aborting')
    current = digest(TARGET)
    if current not in (OLD, NEW):
        raise SystemExit('Current daemon changed since preparation; aborting')
    devices = [p.parts[-3] for p in Path('/sys/class/hidraw').glob('hidraw*/device/uevent')
               if 'HID_ID=001C:0000045E:00000C77' in p.read_text()]
    if len(devices) != 1:
        raise SystemExit('Expected exactly one 045E:0C77 touchpad')
    unit = 'iptsd@dev-' + devices[0] + '.service'
    if current == NEW:
        pid = subprocess.check_output(['systemctl', 'show', '-p', 'MainPID', '--value', unit], text=True).strip()
        if pid != '0' and digest(Path('/proc', pid, 'exe')) == NEW:
            print(json.dumps({'installed': True, 'already_active': True, 'unit': unit, 'pid': pid}))
            return
    BACKUP.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not BACKUP.exists():
        if current != OLD:
            raise SystemExit('Original backup missing; aborting')
        shutil.copy2(TARGET, BACKUP)
    if digest(BACKUP) != OLD:
        raise SystemExit('Original backup hash mismatch; aborting')
    temporary = TARGET.with_name('iptsd.drag-new')
    def replace(source):
        shutil.copyfile(source, temporary)
        os.chmod(temporary, 0o755)
        os.chown(temporary, 0, 0)
        os.replace(temporary, TARGET)
    replace(CANDIDATE)
    try:
        subprocess.run(['systemctl', 'restart', unit], check=True, timeout=20)
        time.sleep(3)
        subprocess.run(['systemctl', 'is-active', '--quiet', unit], check=True, timeout=5)
        pid = subprocess.check_output(['systemctl', 'show', '-p', 'MainPID', '--value', unit], text=True, timeout=5).strip()
        if pid == '0' or digest(Path('/proc', pid, 'exe')) != NEW:
            raise RuntimeError('Daemon executable verification failed')
        names = [p.read_text().strip() for p in Path('/sys/class/input').glob('event*/device/name')]
        if names.count('IPTSD Virtual Touchpad 045E:0C77') != 1:
            raise RuntimeError('Virtual touchpad did not register')
        print(json.dumps({'installed': True, 'unit': unit, 'pid': pid, 'sha256': NEW, 'backup': str(BACKUP)}))
    except BaseException:
        replace(BACKUP)
        subprocess.run(['systemctl', 'restart', unit], timeout=20)
        raise

if __name__ == '__main__':
    if os.geteuid() != 0:
        # Standard system authentication dialog; no password is read by this script.
        raise SystemExit(subprocess.call(['pkexec', '/usr/bin/python3', str(Path(__file__).resolve())]))
    apply()
