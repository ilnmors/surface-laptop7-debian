#!/bin/bash
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
folder=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
work=$(mktemp -d /var/tmp/surface-verify.XXXXXX)
trap 'rm -rf "$work"' EXIT
python3 - "$work" <<'PY'
from pathlib import Path
import os,sys,struct
sys.path.insert(0,'/usr/local/lib/surface-secureboot')
from kernel_certificate import insert_certificate
kernel=os.uname().release
b=Path('/boot/vmlinuz-'+kernel).read_bytes();pe=struct.unpack_from('<I',b,0x3c)[0];count=struct.unpack_from('<H',b,pe+6)[0];table=pe+24+struct.unpack_from('<H',b,pe+20)[0]
for i in range(count):
 h=b[table+i*40:table+(i+1)*40]
 if h[:8].rstrip(b'\0')==b'.linux':
  size=struct.unpack_from('<I',h,8)[0];offset=struct.unpack_from('<I',h,20)[0]
  Path(sys.argv[1]+'/Image').write_bytes(insert_certificate(b[offset:offset+size],kernel,Path('/var/lib/surface-secureboot/MOK.der').read_bytes()))
  break
else:raise RuntimeError('Missing inner kernel')
PY
python3 "$folder/make-test-initrd.py" "$work"
(cd "$work/verify-initrd" && find . -print0 | cpio --null -o --format=newc --quiet) > "$work/initrd"
timeout 60s qemu-system-aarch64 -machine virt,gic-version=3 -cpu max -accel tcg,thread=multi -m 1024 -smp 2 -display none -monitor none -serial stdio -nodefaults -nic none -no-reboot -kernel "$work/Image" -initrd "$work/initrd" -append 'console=ttyAMA0 earlycon=pl011,0x09000000 rdinit=/init module.sig_enforce=1 panic=-1 cma=16M' > "$work/result.log" 2>&1
for marker in PASS_UNSIGNED_REJECTED PASS_SIGNED_ACCEPTED VERIFY_COMPLETE; do grep -q "$marker" "$work/result.log"; done
! grep -q 'FAIL_' "$work/result.log"
grep -E 'Surface Debian|VERIFY_|PASS_|unsigned module' "$work/result.log"
