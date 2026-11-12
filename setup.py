#!/usr/bin/env python3
"""Offline Surface installer: one entry point or selected components."""
import argparse,hashlib,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
COMPONENTS=('kernel','drivers','patches','desktop','programs')
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--component',choices=COMPONENTS,action='append',help='Repeat to select components, executed in dependency order')
p.add_argument('--plan',action='store_true',help='Print actions without sudo or changes')
p.add_argument('--verify-only',action='store_true',help='Verify all bundled offline files without system changes')
a=p.parse_args()
if a.verify_only:
 failed=[]
 for line in (ROOT/'PAYLOADS.sha256').read_text().splitlines():
  digest,name=line.split('  ',1);path=ROOT/name;h=hashlib.sha256()
  try:
   with path.open('rb') as f:
    for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
   if h.hexdigest()!=digest:failed.append(name)
  except OSError:failed.append(name)
 if failed:print('Verification failed: '+', '.join(failed),file=sys.stderr);sys.exit(1)
 print('All offline payload checksums match.');sys.exit(0)
selected=[c for c in COMPONENTS if not a.component or c in a.component]
if not a.plan:
 subprocess.run([sys.executable,str(ROOT/'setup.py'),'--verify-only'],check=True)
for index,component in enumerate(selected,1):
 print(f'[{index}/{len(selected)}] {component}',flush=True)
 subprocess.run(['bash',str(ROOT/component/'setup.sh'),*(['--plan'] if a.plan else [])],check=True,
                env={**os.environ,'SURFACE_PAYLOADS_VERIFIED':'1'})
if not a.plan:print('Installation complete. Reboot to load kernel/driver changes; complete MOK enrollment first if required.')
