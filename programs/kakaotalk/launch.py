#!/usr/bin/env python3
"""Start KakaoTalk's individual Waydroid window, preserving Android app data.

--autostart only boots the Waydroid session: KakaoTalk's boot receiver then starts its
MessengerService in the background without opening a window."""
from pathlib import Path
import argparse,fcntl,os,subprocess,time
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--autostart',action='store_true');a=p.parse_args()
if os.geteuid()==0:p.error('Run as the desktop user.')
if a.autostart:time.sleep(8)
state=Path(os.environ.get('XDG_STATE_HOME',str(Path.home()/'.local/state')))/'surface/kakaotalk';state.mkdir(parents=True,exist_ok=True)
with (state/'launch.lock').open('w') as lock:
 try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 except BlockingIOError:raise SystemExit(0)
 status=subprocess.check_output(['waydroid','status'],text=True)
 if 'Session:\tRUNNING' not in status:
  with (state/'waydroid-session.log').open('a') as log:subprocess.Popen(['waydroid','session','start'],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 for _ in range(60):
  ready=subprocess.run(['waydroid','prop','get','sys.boot_completed'],capture_output=True,text=True)
  if ready.returncode==0 and ready.stdout.strip()=='1':break
  time.sleep(1)
 else:raise SystemExit('Waydroid did not become ready; inspect '+str(state/'waydroid-session.log'))
 if a.autostart:raise SystemExit(0)
 subprocess.run(['waydroid','app','launch','com.kakao.talk'],check=True)
