#!/usr/bin/env python3
"""Install the KakaoTalk ARM64 split APKs in files/apk after checking Kakao's official signer; never logs into an account."""
from pathlib import Path
import fcntl,termios
import argparse,errno,json,os,pty,re,shutil,subprocess,tempfile
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--data-dir',type=Path,required=True,help='Waydroid session data directory from config_session')
a=p.parse_args()
if os.geteuid()!=0:p.error('Run with sudo.')
r=Path(__file__).resolve().parent;PACKAGE='com.kakao.talk'
# Any version is accepted when every APK is signed by a certificate Kakao publishes for com.kakao.talk.
signers={x.replace(':','').lower() for e in json.loads((r/'official-assetlinks.json').read_text()) if e.get('target',{}).get('namespace')=='android_app' and e['target'].get('package_name')==PACKAGE for x in e['target'].get('sha256_cert_fingerprints',[])}
if not signers:p.error('official-assetlinks.json lists no '+PACKAGE+' signer')
if not shutil.which('apksigner'):p.error('apksigner is required: sudo apt install apksigner')
apks=sorted((r/'files/apk').glob('*.apk'))
if not apks:p.error('No APKs in '+str(r/'files/apk')+'; download the current KakaoTalk ARM64 split APKs (see README.md) and put them there')
def badging(tools):
 lib=':'.join(str(tools/d) for d in ('usr/lib/aarch64-linux-gnu/android','usr/lib/7zip'))
 out={}
 for f in apks:
  text=subprocess.run([str(tools/'usr/lib/android-sdk/build-tools/debian/aapt'),'dump','badging',str(f)],env={**os.environ,'LD_LIBRARY_PATH':lib},capture_output=True,text=True,check=True).stdout
  m=re.search(r"^package: name='([^']*)' versionCode='([^']*)' versionName='([^']*)'(?:.* split='([^']*)')?",text,re.M)
  if not m:p.error('Not an APK aapt can read: '+f.name)
  sdk=re.search(r"^sdkVersion:'(\d+)'",text,re.M);abi=re.search(r"^native-code: (.*)$",text,re.M)
  out[f]=dict(package=m[1],code=m[2],name=m[3],split=m[4],sdk=int(sdk[1]) if sdk else 1,abi=re.findall(r"'([^']+)'",abi[1]) if abi else [])
 return out
with tempfile.TemporaryDirectory(prefix='kakao-aapt-') as t:
 for deb in sorted((r/'files/tools').glob('*.deb')):subprocess.run(['dpkg-deb','-x',str(deb),t],check=True)
 info=badging(Path(t))
for f in apks:
 v=subprocess.run(['apksigner','verify','--print-certs',str(f)],capture_output=True,text=True)
 certs=set(re.findall(r'^Signer #\d+ certificate SHA-256 digest: ([0-9a-f]{64})$',v.stdout,re.M))
 if v.returncode or not certs:p.error('apksigner rejected '+f.name+': '+(v.stderr or v.stdout).strip())
 if not certs<=signers:p.error(f.name+' is not signed by the official Kakao certificate')
 if info[f]['package']!=PACKAGE:p.error(f.name+' is '+info[f]['package']+', not '+PACKAGE)
base=[f for f in apks if not info[f]['split']]
if len(base)!=1:p.error('Expected exactly one base APK, found '+str(len(base)))
base=info[base[0]]
if len({i['code'] for i in info.values()})!=1:p.error('APKs have different versionCodes')
if len({i['split'] for i in info.values()})!=len(apks):p.error('Duplicate split APKs')
if not any('arm64-v8a' in i['abi'] for i in info.values()):p.error('No arm64-v8a native code; add the config.arm64_v8a split')
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
if int(android('getprop','ro.build.version.sdk'))<base['sdk']:p.error('Android version too old')
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
 print('Installed KakaoTalk '+base['name']+' ('+base['code']+'). Account login remains manual.')
finally:
 if session:android('pm','install-abandon',session)
