#!/usr/bin/env python3
"""Summarize UPower history against current-boot suspend intervals; no device changes."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,subprocess,statistics
r=Path(__file__).resolve().parent.parent
obj='/org/freedesktop/UPower/devices/battery_qcom_battmgr_bat'
def history(kind):
 data=json.loads(subprocess.check_output(['busctl','--json=short','call','org.freedesktop.UPower',obj,'org.freedesktop.UPower.Device','GetHistory','suu',kind,'43200','0'],text=True))
 return sorted(data['data'][0])
charge=history('charge');rate=history('rate');battery=None
for d in Path('/sys/class/power_supply').glob('*'):
 try:
  if (d/'type').read_text().strip()=='Battery':battery=d;break
 except OSError:pass
if battery is None:raise SystemExit('Battery not found')
def value(name):
 try:return float((battery/name).read_text())
 except OSError:return None
full=value('energy_full')/1e6;design=value('energy_full_design')/1e6
raw=subprocess.check_output(['journalctl','-b','-k','--no-pager','-o','short-unix','-g','PM: suspend entry|PM: suspend exit'],text=True)
sleeps=[];start=None
for line in raw.splitlines():
 try:t=float(line.split()[0])
 except (ValueError,IndexError):continue
 if 'suspend entry' in line:start=t
 elif 'suspend exit' in line and start is not None:sleeps.append((start,t));start=None
rows=[]
for start,end in sleeps:
 before=[x for x in charge if x[0]<=start and x[2]==2];after=[x for x in charge if x[0]>=end-1 and x[2]==2]
 row={'start':start,'end':end,'hours':(end-start)/3600}
 if before and after:
  a,b=before[-1],after[0];pre_age=start-a[0];post_age=b[0]-end
  row.update(before_sample=a,after_sample=b,before_gap_seconds=pre_age,after_gap_seconds=post_age)
  if pre_age<=120 and post_age<=120 and b[1]<=a[1] and end-start>=600:
   pp=a[1]-b[1];row.update(eligible=True,drop_percentage_points=pp,estimated_wh=pp/100*full,mean_w=pp/100*full/row['hours'],percentage_points_per_hour=pp/row['hours'])
  else:row['eligible']=False
 rows.append(row)
energy=seconds=0;samples=0
for a,b in zip(rate,rate[1:]):
 dt=b[0]-a[0]
 if 0<dt<=120 and a[2]==b[2]==2 and a[1]>0 and b[1]>0 and not any(a[0]<end and b[0]>start for start,end in sleeps):
  energy+=(a[1]+b[1])/2*dt;seconds+=dt;samples+=1
result={'captured_at':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),'full_wh':full,'design_wh':design,'health_percent':full/design*100,'current_energy_wh':value('energy_now')/1e6,'instant_power_w':abs(value('power_now')/1e6),'sleep_intervals':rows,'awake_weighted_mean_w':energy/seconds if seconds else None,'awake_sampled_hours':seconds/3600,'awake_intervals':samples,'method':'UPower discharging intervals only; rate trapezoids <=120s, excluding any suspend overlap. Sleep charge samples must be within 120s of both boundaries; >=10 minute sessions only. Percent is quantized; estimates include boundary transition uncertainty.','sources':['https://learn.microsoft.com/en-us/surface/tech-specs/surface-laptop-snapdragon-tech-specs','https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/modern-standby-sleepstudy','https://learn.microsoft.com/en-us/windows-hardware/test/hlk/testref/36463e42-7d6e-408e-933f-dbf56ea41e65']}
folder=r/'drivers/files/power';folder.mkdir(exist_ok=True)
archive=folder/'measurements';archive.mkdir(exist_ok=True)
(archive/(datetime.now().strftime('%Y-%m-%d-%H%M%S')+'.json')).write_text(json.dumps(result,indent=2)+'\n')
if result['awake_weighted_mean_w'] is not None and any(row.get('eligible') for row in rows):
 (folder/'battery-measurement.json').write_text(json.dumps(result,indent=2)+'\n')
else:print('No complete discharging sleep/awake comparison: preserving the previous report baseline.')
print(json.dumps({k:v for k,v in result.items() if k!='sleep_intervals'},indent=2))
for row in rows:
 if row.get('eligible'):print('SLEEP',json.dumps(row))
