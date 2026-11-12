#!/usr/bin/env python3
"""Remove only an orphan OMX declaration that blocks shared-storage startup."""
from pathlib import Path
import configparser,os,subprocess,xml.etree.ElementTree as ET
if os.geteuid()!=0:raise SystemExit('Run with sudo.')
base=Path('/var/lib/waydroid');root=base/'rootfs';manifest=root/'vendor/etc/vintf/manifest.xml'
if not manifest.is_file():raise SystemExit('Start a Waydroid session first so vendor files are mounted.')
c=configparser.ConfigParser();c.read(base/'waydroid.cfg')
if c['waydroid'].get('vendor_type')!='MAINLINE':raise SystemExit('This adaptation is for MAINLINE vendor only; inspect other images separately.')
services=[p for d in ('system/bin','vendor/bin','odm/bin') for p in (root/d).glob('**/*media.omx*service*')]
if services:print('An OMX service binary exists; leaving the manifest unchanged.');raise SystemExit(0)
original=manifest.read_bytes();tree=ET.fromstring(original)
entries=[x for x in tree.findall('hal') if x.findtext('name')=='android.hardware.media.omx']
if not entries:print('No orphan OMX declaration remains.');raise SystemExit(0)
if len(entries)!=1:raise SystemExit('Unexpected OMX manifest structure.')
backup=base/'surface-media-fix/original-vendor-manifest.xml';backup.parent.mkdir(exist_ok=True)
if not backup.exists():backup.write_bytes(original)
tree.remove(entries[0]);ET.indent(tree,space='    ')
target=base/'overlay/vendor/etc/vintf/manifest.xml';target.parent.mkdir(parents=True,exist_ok=True)
target.write_bytes(ET.tostring(tree,encoding='utf-8',xml_declaration=True)+b'\n')
subprocess.run(['waydroid','upgrade','-o'],check=True)
print('Removed orphan OMX HAL declaration through the supported vendor overlay; original image is unchanged.')
