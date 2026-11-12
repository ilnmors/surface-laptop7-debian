#!/usr/bin/env python3
"""Start this user's Waydroid session without opening the full Android UI."""
from pathlib import Path
import os,subprocess,time
folder=Path(os.environ.get('XDG_STATE_HOME',str(Path.home()/'.local/state')))/'surface/waydroid'
status=subprocess.check_output(['waydroid','status'],text=True)
if 'Session:\tRUNNING' not in status:
 folder.mkdir(parents=True,exist_ok=True)
 with (folder/'session.log').open('a') as log:subprocess.Popen(['waydroid','session','start'],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
for _ in range(60):
 status=subprocess.check_output(['waydroid','status'],text=True)
 prop=subprocess.run(['waydroid','prop','get','sys.boot_completed'],capture_output=True,text=True) if 'Session:\tRUNNING' in status else None
 if prop is not None and prop.returncode==0 and prop.stdout.strip()=='1':
  print('Waydroid session and Android boot ready; full Android desktop was not opened.');raise SystemExit(0)
 time.sleep(1)
raise SystemExit('Waydroid startup timed out; inspect '+str(folder/'session.log'))
