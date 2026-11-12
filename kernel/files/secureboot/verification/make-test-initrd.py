from pathlib import Path
import subprocess,shutil,re,struct,sys
base=Path(sys.argv[1]);root=base/'verify-initrd'
for folder in ('bin','proc','sys','dev'):(root/folder).mkdir(parents=True,exist_ok=True)
shutil.copyfile('/usr/bin/busybox',root/'bin/busybox');(root/'bin/busybox').chmod(0o755)
libs=subprocess.check_output(['ldd','/usr/bin/busybox'],text=True)
for name in set(re.findall(r'(/[\w./+-]+)',libs)):
 p=Path(name)
 if not p.is_file():continue
 target=root/str(p).lstrip('/');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p.resolve(),target)
signed=subprocess.check_output(['zstd','-dc','/lib/modules/7.3.0-31-qcom-x1e/kernel/drivers/net/dummy.ko.zst'])
assert signed.endswith(b'~Module signature appended~\n')
header=len(signed)-len(b'~Module signature appended~\n')-12;n=struct.unpack_from('>I',signed,header+8)[0]
(root/'signed.ko').write_bytes(signed);(root/'unsigned.ko').write_bytes(signed[:header-n])
(root/'init').write_text('''#!/bin/busybox sh
/bin/busybox mount -t proc proc /proc
/bin/busybox mount -t sysfs sysfs /sys
/bin/busybox mount -t devtmpfs devtmpfs /dev
echo VERIFY_SIGNATURE_ENFORCEMENT
/bin/busybox cat /sys/module/module/parameters/sig_enforce
if /bin/busybox insmod /unsigned.ko; then
 echo FAIL_UNSIGNED_ACCEPTED
else
 echo PASS_UNSIGNED_REJECTED
fi
if /bin/busybox insmod /signed.ko; then
 echo PASS_SIGNED_ACCEPTED
else
 echo FAIL_SIGNED_REJECTED
fi
/bin/busybox cat /proc/modules
echo VERIFY_COMPLETE
/bin/busybox poweroff -f
''');(root/'init').chmod(0o755)
