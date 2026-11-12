#!/usr/bin/env python3
"""Start this user's Waydroid session without opening the full Android UI."""
from pathlib import Path
import os,subprocess,time
status=subprocess.check_output(['waydroid','status'],text=True)
if 'Session:\tRUNNING' in status:raise SystemExit(0)
folder=Path(os.environ.get('XDG_STATE_HOME',str(Path.home()/'.local/state')))/'surface/waydroid';folder.mkdir(parents=True,exist_ok=True)
with (folder/'session.log').open('a') as log:subprocess.Popen(['waydroid','session','start'],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
for _ in range(60):
 time.sleep(1)
 if 'Session:\tRUNNING' in subprocess.check_output(['waydroid','status'],text=True):print('Waydroid session ready; full Android desktop was not opened.');raise SystemExit(0)
raise SystemExit('Waydroid startup timed out; inspect '+str(folder/'session.log'))
