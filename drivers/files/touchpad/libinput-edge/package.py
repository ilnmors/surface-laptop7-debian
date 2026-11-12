#!/usr/bin/env python3
"""Repackage matching Debian libinput10 with the narrowly patched shared library."""
from pathlib import Path
import hashlib,subprocess,sys,tempfile,shutil
here=Path(__file__).resolve().parent
library=Path(sys.argv[1]);output=Path(sys.argv[2]).resolve()
original=here/'original/libinput10_1.28.1-1+deb13u1_arm64.deb'
assert hashlib.sha256(original.read_bytes()).hexdigest()=='a2acd04f3b1e9e91d22a26b63650087a179b6b3dbaddadc92d89edfbb2075ae1'
with tempfile.TemporaryDirectory(prefix='surface-libinput-package-') as folder:
 root=Path(folder)
 subprocess.run(['dpkg-deb','-R',str(original),str(root)],check=True)
 target=root/'usr/lib/aarch64-linux-gnu/libinput.so.10.13.0'
 assert target.exists()
 shutil.copy2(library,target)
 subprocess.run(['strip','--strip-unneeded',str(target)],check=True)
 control=root/'DEBIAN/control'
 text=control.read_text().replace('Version: 1.28.1-1+deb13u1\n','Version: 1.28.1-1+deb13u1+surface1\n')
 assert 'Version: 1.28.1-1+deb13u1+surface1' in text
 control.write_text(text)
 entries=[]
 for f in sorted(root.rglob('*')):
  if f.is_file() and not f.is_symlink() and f.relative_to(root).parts[0]!='DEBIAN':entries.append(hashlib.md5(f.read_bytes()).hexdigest()+'  '+f.relative_to(root).as_posix()+'\n')
 (root/'DEBIAN/md5sums').write_text(''.join(entries))
 subprocess.run(['dpkg-deb','--root-owner-group','-b',str(root),str(output)],check=True)
print(output)

# Matching tools have an exact-version dependency; keep them consistent.
with tempfile.TemporaryDirectory(prefix='surface-libinput-tools-') as folder:
 root=Path(folder)
 subprocess.run(['dpkg-deb','-R',str(here/'original/libinput-tools_1.28.1-1+deb13u1_arm64.deb'),str(root)],check=True)
 control=root/'DEBIAN/control'
 control.write_text(control.read_text().replace('1.28.1-1+deb13u1','1.28.1-1+deb13u1+surface1'))
 companion=output.parent/'libinput-tools_1.28.1-1+deb13u1+surface1_arm64.deb'
 subprocess.run(['dpkg-deb','--root-owner-group','-b',str(root),str(companion)],check=True)
print(companion)
