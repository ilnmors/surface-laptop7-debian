#!/usr/bin/env python3
"""Refresh manifests; excludes Git, archives ."""
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
COMPONENTS={'kernel','drivers','patches','desktop','programs'}
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
def files():
 for p in sorted(ROOT.rglob('*')):
  rel=p.relative_to(ROOT)
  if any(x in ('.git','archive','__pycache__') for x in rel.parts):continue
  if not p.is_file() or p.is_symlink() or rel.as_posix() in ('SHA256SUMS','PAYLOADS.sha256'):continue
  yield p,rel.as_posix()
entries=[(digest(p),rel) for p,rel in files()]
payloads=[x for x in entries if x[1].split('/')[0] in COMPONENTS]
(ROOT/'PAYLOADS.sha256').write_text(''.join(f'{h}  {rel}\n' for h,rel in payloads))
entries.append((digest(ROOT/'PAYLOADS.sha256'),'PAYLOADS.sha256'))
(ROOT/'SHA256SUMS').write_text(''.join(f'{h}  {rel}\n' for h,rel in sorted(entries,key=lambda x:x[1])))
print(f'{len(payloads)} component files; {len(entries)} maintained files.')
