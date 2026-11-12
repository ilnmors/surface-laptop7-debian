#!/usr/bin/env python3
"""Suppress KakaoTalk's empty companion notification; preserve real messages."""
import argparse
import os
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--target', type=Path, default=Path('/usr/lib/waydroid/tools/services/notification_manager.py'))
args = parser.parse_args()
anchor = '        app_icon = ""\n'
marker = '        # Surface: ignore KakaoTalk empty companion notifications.\n'
guard = (marker +
         '        if package_name == "com.kakao.talk" and not summary.strip() and not body.strip():\n'
         '            return INotifications.ID_NONE\n')
source = args.target.read_text()
if marker in source:
    if guard not in source:
        raise SystemExit('Existing notification patch differs; inspect before updating.')
    print('KakaoTalk empty-notification filter already installed.')
else:
    if source.count(anchor) != 1:
        raise SystemExit('Unsupported Waydroid notification manager; no file changed.')
    updated = source.replace(anchor, guard + anchor, 1)
    compile(updated, str(args.target), 'exec')
    backup = args.target.with_name(args.target.name + '.surface-original')
    if not backup.exists():
        shutil.copy2(args.target, backup)
    temporary = args.target.with_name(args.target.name + '.surface-new')
    try:
        shutil.copy2(args.target, temporary)
        temporary.write_text(updated)
        temporary.replace(args.target)
    finally:
        temporary.unlink(missing_ok=True)
    print('KakaoTalk empty-notification filter installed. Restart the Waydroid session to activate.')
