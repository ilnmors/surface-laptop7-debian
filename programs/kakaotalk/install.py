#!/usr/bin/env python3
"""Install the locally verified KakaoTalk split bundle; never logs into an account."""
from pathlib import Path
import fcntl,termios
import argparse,errno,hashlib,json,os,pty,re,shutil,subprocess,tempfile
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--data-dir',type=Path,required=True,help='Waydroid session data directory from config_session')
a=p.parse_args()
if os.geteuid()!=0:p.error('Run with sudo.')
r=Path(__file__).resolve().parent;manifest=json.loads((r/'files/manifest.json').read_text())
apks=[]
for name,digest in manifest['files'].items():
 if Path(name).name!=name:p.error('Invalid manifest filename')
 f=r/'files/apk'/name
 if hashlib.sha256(f.read_bytes()).hexdigest()!=digest:p.error('APK checksum mismatch: '+name)
 apks.append(f)
assert manifest['package']=='com.kakao.talk' and manifest['abi']=='arm64-v8a'
def android(*args):
 master,slave=pty.openpty()
 proc=subprocess.Popen(['waydroid','shell','--',*args],stdin=slave,stdout=slave,stderr=slave,start_new_session=True,preexec_fn=lambda:fcntl.ioctl(0,termios.TIOCSCTTY,0))
 os.close(slave);output=b''
 try:
  while True:
   try:block=os.read(master,65536)
   except OSError as e:
    if e.errno==errno.EIO:break
    raise
   if not block:break
   output+=block
 finally:os.close(master)
 proc.wait();text=output.decode(errors='replace').replace('\r','')
 if proc.returncode or 'Failure [' in text or text.lstrip().startswith('Error:'):raise RuntimeError(text)
 return text.strip()
if int(android('getprop','ro.build.version.sdk'))<manifest['min_sdk']:p.error('Android version too old')
if 'arm64-v8a' not in android('getprop','ro.product.cpu.abilist'):p.error('ARM64 Android required')
# Verify this is the active session mount, not an arbitrary host path.
config=Path('/var/lib/waydroid/lxc/waydroid/config_session').read_text()
data=a.data_dir.resolve()
if not any(line.startswith('lxc.mount.entry = '+str(data)+' data ') for line in config.splitlines()):p.error('data-dir is not the active Waydroid data mount')
tmp=data/'waydroid_tmp';tmp.mkdir(exist_ok=True);tmp.chmod(0o755)
session=None
try:
 with tempfile.TemporaryDirectory(prefix='kakao-',dir=tmp) as work:
  folder=Path(work);folder.chmod(0o755)
  for f in apks:shutil.copyfile(f,folder/f.name);(folder/f.name).chmod(0o644)
  created=android('pm','install-create','-r');match=re.search(r'\[(\d+)\]',created)
  if not match:raise RuntimeError(created)
  session=match[1]
  for f in apks:
   out=android('pm','install-write','-S',str(f.stat().st_size),session,f.name,'/data/waydroid_tmp/'+folder.name+'/'+f.name)
   if 'Success' not in out:raise RuntimeError(out)
  out=android('pm','install-commit',session)
  if 'Success' not in out:raise RuntimeError(out)
  session=None
 print('Installed KakaoTalk '+manifest['version']+'. Account login remains manual.')
finally:
 if session:android('pm','install-abandon',session)
