#!/usr/bin/python3
"""Expose individual Android apps in the current GNOME user's app list."""
from pathlib import Path
import os
folder=Path(os.environ.get('XDG_DATA_HOME',str(Path.home()/'.local/share')))/'applications'
folder.mkdir(parents=True,exist_ok=True)
apps={'com.android.calculator2':('Calculator','accessories-calculator'),'com.android.settings':('Settings','preferences-system'),'org.lineageos.jelly':('Browser','web-browser')}
for package,(label,icon) in apps.items():
    (folder/('surface-android-'+package+'.desktop')).write_text('[Desktop Entry]\nType=Application\nName=Android '+label+'\nExec=waydroid app launch '+package+'\nIcon='+icon+'\nCategories=Utility;X-WayDroid-App;\nTerminal=false\n')
print('Individual Android app launchers installed. User-installed APKs are exported by Waydroid automatically.')
