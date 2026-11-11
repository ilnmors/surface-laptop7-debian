#!/usr/bin/python3
"""Move the local console account to UID 3000 before user logins."""
import os,pwd,subprocess,shutil
from pathlib import Path
state=Path('/var/lib/surface-uid-migration')
account=pwd.getpwnam('console')
if account.pw_dir!='/home/console' or account.pw_uid not in (1001,3000):
    raise SystemExit('Unexpected console account; refusing migration')
if account.pw_uid==1001:
    try:
        pwd.getpwuid(3000)
    except KeyError:
        pass
    else:
        raise SystemExit('UID 3000 is already in use')
    for process in Path('/proc').iterdir():
        if not process.name.isdecimal(): continue
        try:
            uids=next(line for line in (process/'status').read_text().splitlines() if line.startswith('Uid:'))
        except (FileNotFoundError,ProcessLookupError,StopIteration):
            continue
        if '1001' in uids.split()[1:]:
            raise SystemExit('Console processes still running; refusing live UID change')
    for name in ('passwd','shadow','group','gshadow'):
        target=state/(name+'.before')
        if not target.exists():
            shutil.copyfile('/etc/'+name,target)
            target.chmod(0o600)
    subprocess.run(['/usr/sbin/usermod','--uid','3000','console'],check=True)
# Finish any ownership work after an interrupted earlier attempt.
subprocess.run(['/usr/bin/find','/','-xdev','-uid','1001','-exec','/usr/bin/chown','-h','3000','{}','+'],check=True)
assert pwd.getpwnam('console').pw_uid==3000
assert Path('/home/console').stat().st_uid==3000
(state/'complete').write_text('console UID 3000; primary group unchanged\n')
print('Console UID migration complete: 3000',flush=True)
