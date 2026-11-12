#!/usr/bin/env python3
"""Capture only this virtual touchpad plus an independent libinput context."""
import argparse,json,os,select,struct,subprocess,time
from pathlib import Path
from datetime import datetime
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--seconds',type=int,default=30);a=p.parse_args()
if not 1<=a.seconds<=120:p.error('seconds must be 1..120')
names=[x for x in Path('/sys/class/input').glob('event*/device/name') if 'IPTSD Virtual Touchpad' in x.read_text()]
if len(names)!=1:p.error('Expected exactly one IPTSD touchpad')
device='/dev/input/'+names[0].parts[-3]
folder=Path(__file__).parent/'diagnostics'/datetime.now().strftime('%Y-%m-%d-%H%M%S');folder.mkdir(parents=True)
command=['libinput','debug-events','--device',device,'--set-click-method=clickfinger','--set-scroll-method=twofinger','--set-profile=flat','--verbose']
fd=os.open(device,os.O_RDONLY|os.O_NONBLOCK);event=struct.Struct('llHHi');samples=[];positions={};slot=0;events=0;presses=0
start=time.monotonic()
with (folder/'libinput.txt').open('w') as log:
 proc=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT)
 try:
  while time.monotonic()-start<a.seconds:
   if not select.select([fd],[],[],0.1)[0]:continue
   data=os.read(fd,event.size*256)
   for sec,usec,kind,code,value in event.iter_unpack(data):
    events+=1
    if kind==3:
     if code==47:slot=value
     elif code in (53,54,57,48,49):positions.setdefault(slot,{})[code]=value
    elif kind==1 and code==272 and value==1:presses+=1
    elif kind==0 and code==0:
     for sl,v in positions.items():
      if v.get(57,-1)>=0 and 53 in v and 54 in v:samples.append([round(sec+usec/1e6,6),sl,v[53],v[54],v.get(48),v.get(49)])
 finally:
  os.close(fd);proc.terminate()
  try:proc.wait(timeout=2)
  except subprocess.TimeoutExpired:proc.kill();proc.wait()
result={'device':device,'duration':round(time.monotonic()-start,2),'raw_events':events,'physical_click_presses':presses,'columns':['kernel_monotonic_seconds','slot','x','y','major','minor'],'contacts':samples,'libinput_exit':proc.returncode}
(folder/'raw-touchpad.json').write_text(json.dumps(result))
print(folder,flush=True);print('Raw events:',events,'contact samples:',len(samples),'physical clicks:',presses,flush=True)
