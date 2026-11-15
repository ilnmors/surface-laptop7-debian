#!/usr/bin/env python3
"""Restore the pre-drag-fix daemon and restart only the Romulus touchpad instance."""
from pathlib import Path
import os, pwd, subprocess
backup = Path(pwd.getpwnam('console').pw_dir) / '.local/state/surface-touchpad/backups/20261115T081420/iptsd'
if not backup.is_file():
    raise SystemExit(f'Local pre-change backup not found: {backup}')
devices = [p.parts[-3] for p in Path('/sys/class/hidraw').glob('hidraw*/device/uevent')
           if 'HID_ID=001C:0000045E:00000C77' in p.read_text()]
if len(devices) != 1:
    raise SystemExit('Expected exactly one 045E:0C77 touchpad')
unit = 'iptsd@dev-' + devices[0] + '.service'
prefix = [] if os.geteuid() == 0 else ['sudo']
target = '/usr/local/libexec/surface-iptsd/iptsd'
subprocess.run([*prefix, 'install', '-m', '755', '-o', 'root', '-g', 'root', str(backup), target + '.restore'], check=True)
subprocess.run([*prefix, 'mv', '-f', target + '.restore', target], check=True)
subprocess.run([*prefix, 'systemctl', 'restart', unit], check=True)
print('Original daemon restored; touchpad restarted. Bundle payload was not changed.')
