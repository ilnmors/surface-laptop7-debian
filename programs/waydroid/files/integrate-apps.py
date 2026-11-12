#!/usr/bin/env python3
"""Hide Android utility launchers; Waydroid exports installed personal apps."""
from pathlib import Path
import os
folder=Path(os.environ.get('XDG_DATA_HOME',str(Path.home()/'.local/share')))/'applications'
folder.mkdir(parents=True,exist_ok=True)
for p in folder.glob('surface-android-*.desktop'):
 p.unlink()
# Keep installed personal APK launchers visible; suppress stock Android utilities.
stock=('com.android.calculator2','com.android.settings','org.lineageos.jelly','org.lineageos.recorder','org.lineageos.etar','org.lineageos.aperture','com.android.deskclock','com.android.gallery3d','com.android.documentsui','com.android.contacts','org.lineageos.eleven')
for package in stock:
 p=folder/('waydroid.'+package+'.desktop')
 text=p.read_text() if p.exists() else '[Desktop Entry]\nType=Application\nName=Android utility\nExec=waydroid app launch '+package+'\n'
 text='\n'.join(x for x in text.splitlines() if not x.startswith(('NoDisplay=','Hidden=')))+'\nNoDisplay=true\n'
 p.write_text(text)
print('Stock Android utility launchers hidden. Installed personal apps remain individual windows.')
