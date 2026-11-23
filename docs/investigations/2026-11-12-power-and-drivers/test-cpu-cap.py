#!/usr/bin/env python3
"""Temporary four-core CPU cap comparison; restores original sysfs settings."""
import hashlib,json,multiprocessing as mp,os,signal,time
from pathlib import Path
POLICY=Path('/sys/devices/system/cpu/cpufreq/policy0')
def load(cpu,stop,counter):
 os.sched_setaffinity(0,{cpu})
 while not stop.is_set():
  hashlib.pbkdf2_hmac('sha256',b'public-benchmark',b'fixed',20000)
  counter.value+=1
if __name__=='__main__':
 if os.geteuid()!=0:raise SystemExit('Run as root.')
 battery=next(p for p in Path('/sys/class/power_supply').glob('*') if (p/'type').exists() and (p/'type').read_text().strip()=='Battery')
 if (battery/'status').read_text().strip()!='Discharging':raise SystemExit('Unplug external power first.')
 original={n:(POLICY/n).read_text().strip() for n in ['scaling_max_freq','scaling_governor']}
 cpus=[int(x) for x in (POLICY/'affected_cpus').read_text().split()]
 if cpus!=[0,1,2,3]:raise SystemExit('Expected the known SCMI policy for CPUs 0-3.')
 result={'original':original,'affected_cpus':cpus,'note':'Whole-system battery gauge under four pinned CPU workers; short sequential samples, not a full runtime benchmark. Other clusters are not controlled.','phases':[]}
 stop=mp.Event();counts=[mp.Value('L',0,lock=False) for _ in cpus];workers=[]
 def interrupted(*_):raise KeyboardInterrupt
 signal.signal(signal.SIGTERM,interrupted)
 try:
  for cpu,counter in zip(cpus,counts):
   worker=mp.Process(target=load,args=(cpu,stop,counter),daemon=True);worker.start();workers.append(worker)
  (POLICY/'scaling_governor').write_text('performance')
  for cap in [int(original['scaling_max_freq']),2976000,2515200,int(original['scaling_max_freq'])]:
   (POLICY/'scaling_max_freq').write_text(str(cap));time.sleep(3)
   samples=[];start_count=sum(x.value for x in counts);start=time.monotonic()
   for _ in range(12):
    status=(battery/'status').read_text().strip()
    if status!='Discharging':raise RuntimeError('External power/state changed; aborting comparison.')
    samples.append({'power_w':abs(int((battery/'power_now').read_text()))/1e6,'frequency_khz':int((POLICY/'scaling_cur_freq').read_text())});time.sleep(1)
   elapsed=time.monotonic()-start;done=sum(x.value for x in counts)-start_count
   row={'cap_khz':cap,'seconds':elapsed,'jobs_per_second':done/elapsed,'mean_system_w':sum(x['power_w'] for x in samples)/len(samples),'frequency_range_khz':[min(x['frequency_khz'] for x in samples),max(x['frequency_khz'] for x in samples)],'samples':samples};result['phases'].append(row)
   print(json.dumps({k:v for k,v in row.items() if k!='samples'}),flush=True)
 finally:
  stop.set()
  for worker in workers:
   worker.join(timeout=2)
   if worker.is_alive():worker.terminate();worker.join()
  for n,v in original.items():(POLICY/n).write_text(v)
  result['restored']={n:(POLICY/n).read_text().strip() for n in original}
  (Path(__file__).parent/'cpu-cap-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
  print('Original frequency cap and governor restored.',flush=True)
