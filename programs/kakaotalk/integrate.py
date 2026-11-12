#!/usr/bin/env python3
"""Install user launchers and GNOME login startup; never reinstalls the APK."""
from pathlib import Path
import argparse,os,shutil
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--disable-autostart',action='store_true');a=p.parse_args()
if os.geteuid()==0:p.error('Run as the desktop user.')
here=Path(__file__).resolve().parent;home=Path.home();target=home/'.local/share/surface/programs/kakaotalk';target.mkdir(parents=True,exist_ok=True)
for name in ['launch.py','launch.sh']:shutil.copy2(here/name,target/name);(target/name).chmod(0o755)
binpath=home/'.local/bin/kakaotalk';binpath.parent.mkdir(parents=True,exist_ok=True)
binpath.write_text('#!/bin/sh\nexec python3 "'+str(target/'launch.py').replace('"','\\"')+'" "$@"\n');binpath.chmod(0o755)
apps=home/'.local/share/applications';apps.mkdir(parents=True,exist_ok=True)
app=apps/'waydroid.com.kakao.talk.desktop'
iconfile=home/'.local/share/icons/hicolor/256x256/apps/kakaotalk.png';iconfile.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile(here/'files/kakaotalk-icon.png',iconfile)
icon=str(iconfile)
exe='"'+str(binpath).replace('\\','\\\\').replace('"','\\"')+'"'
app.write_text('[Desktop Entry]\nType=Application\nName=KakaoTalk\nExec='+exe+'\nIcon='+icon+'\nCategories=Network;InstantMessaging;\nTerminal=false\n')
autostart=home/'.config/autostart/kakaotalk.desktop';autostart.parent.mkdir(parents=True,exist_ok=True)
autostart.write_text('[Desktop Entry]\nType=Application\nName=KakaoTalk\nExec='+exe+' --autostart\nTerminal=false\nOnlyShowIn=GNOME;\nX-GNOME-Autostart-enabled='+str(not a.disable_autostart).lower()+'\nHidden='+str(a.disable_autostart).lower()+'\n')
print('KakaoTalk app launcher installed; login autostart '+('disabled' if a.disable_autostart else 'enabled')+'. Existing Android login is preserved.')
