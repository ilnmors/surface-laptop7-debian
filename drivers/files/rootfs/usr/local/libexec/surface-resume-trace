#!/usr/bin/env python3
"""Trace only kernel power callbacks; never suspends the machine."""
import argparse,os
from pathlib import Path
from datetime import datetime
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('action',choices=('arm','save','disarm'))
p.add_argument('--output',type=Path)
a=p.parse_args()
if os.geteuid()!=0:p.error('Run with sudo.')
root=Path('/sys/kernel/tracing/instances/surface-resume')
events=('suspend_resume','device_pm_callback_start','device_pm_callback_end')
if a.action=='arm':
 if root.exists() and (root/'tracing_on').read_text().strip()=='1':p.error('Trace already armed; save it before clearing.')
 root.mkdir(exist_ok=True)
 (root/'tracing_on').write_text('0')
 (root/'buffer_size_kb').write_text('256')
 (root/'trace_clock').write_text('mono')
 (root/'trace').write_text('')
 for e in events:(root/'events/power'/e/'enable').write_text('1')
 (root/'tracing_on').write_text('1')
 print('Power-only trace armed (256 KiB per CPU). Suspend/resume manually, then run save. No sleep was initiated.')
elif a.action=='save':
 if not root.exists():p.error('No trace instance.')
 (root/'tracing_on').write_text('0')
 output=a.output or Path(__file__).parent/'diagnostics'/datetime.now().strftime('%Y-%m-%d-%H%M%S')/'power-trace.txt'
 output.parent.mkdir(parents=True,exist_ok=True);output.write_text((root/'trace').read_text())
 print(output)
else:
 if root.exists():
  (root/'tracing_on').write_text('0')
  for e in events:(root/'events/power'/e/'enable').write_text('0')
  root.rmdir()
 print('Power trace disabled.')
