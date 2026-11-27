#!/usr/bin/env python3
"""Refresh manifests; excludes Git, archives .
--staged: write manifests for the Git index into the index only (the working-tree files stay
as they are), so one piece of uncommitted work can be committed while others wait. Tracked files
are hashed as staged; Git-ignored payloads already listed in HEAD's SHA256SUMS are hashed from disk;
a new ignored payload is included only when named with --with."""
import argparse,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
COMPONENTS={'kernel','drivers','patches','desktop','programs'}
MANIFESTS=('SHA256SUMS','PAYLOADS.sha256')
def skip(rel):return any(x in ('.git','archive','__pycache__') for x in Path(rel).parts) or rel in MANIFESTS
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
def files():
 for p in sorted(ROOT.rglob('*')):
  rel=p.relative_to(ROOT)
  if skip(rel.as_posix()) or not p.is_file() or p.is_symlink():continue
  yield p,rel.as_posix()
def git(*args,data=None):
 return subprocess.run(['git','-C',str(ROOT),*args],input=data,capture_output=True,check=True).stdout
def staged_entries(extra):
 entries={}
 for line in git('ls-files','-s','-z').split(b'\0'):
  if not line:continue
  meta,rel=line.decode().split('\t',1);mode,blob,_=meta.split()
  if mode=='120000' or skip(rel):continue
  entries[rel]=hashlib.sha256(git('cat-file','blob',blob)).hexdigest()
 head=git('show','HEAD:SHA256SUMS').decode().splitlines()
 ignored=set(git('ls-files','--others','--ignored','--exclude-standard','-z').decode().split('\0'))
 wanted={l.split('  ',1)[1] for l in head}|set(extra)
 for rel in sorted(ignored&wanted):
  p=ROOT/rel
  if p.is_file() and not p.is_symlink() and not skip(rel):entries[rel]=digest(p)
 missing=[r for r in extra if r not in entries]
 if missing:raise SystemExit('Not an ignored payload on disk: '+', '.join(missing))
 new=sorted(r for r in ignored-wanted if r and not skip(r) and (ROOT/r).is_file() and r.split('/')[0] in COMPONENTS)
 if new:print(f'{len(new)} ignored payload(s) not in HEAD left out (name them with --with to include), e.g. {new[0]}')
 return sorted((h,rel) for rel,h in entries.items())
def build(entries):
 payloads=[x for x in sorted(entries,key=lambda x:Path(x[1]).parts) if x[1].split('/')[0] in COMPONENTS]
 pay=''.join(f'{h}  {rel}\n' for h,rel in payloads)
 allv=entries+[(hashlib.sha256(pay.encode()).hexdigest(),'PAYLOADS.sha256')]
 return pay,''.join(f'{h}  {rel}\n' for h,rel in sorted(allv,key=lambda x:x[1])),len(payloads),len(allv)
a=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
a.add_argument('--staged',action='store_true',help='write manifests for the Git index into the index only')
a.add_argument('--with',dest='extra',action='append',default=[],metavar='PATH',help='with --staged: include this new ignored payload')
o=a.parse_args()
if o.extra and not o.staged:a.error('--with needs --staged')
if o.staged:
 pay,sums,np,ne=build(staged_entries(o.extra))
 for name,text in (('PAYLOADS.sha256',pay),('SHA256SUMS',sums)):
  blob=git('hash-object','-w','--stdin',data=text.encode()).decode().strip()
  git('update-index','--cacheinfo',f'100644,{blob},{name}')
 print(f'Staged manifests: {np} component files; {ne} maintained files. Working-tree manifests unchanged.')
else:
 pay,sums,np,ne=build([(digest(p),rel) for p,rel in files()])
 (ROOT/'PAYLOADS.sha256').write_text(pay);(ROOT/'SHA256SUMS').write_text(sums)
 print(f'{np} component files; {ne} maintained files.')
