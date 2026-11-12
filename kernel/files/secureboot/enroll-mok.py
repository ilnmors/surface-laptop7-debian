#!/usr/bin/python3
"""Queue certificate enrollment with a seven-character, whole-password prompt."""
import getpass
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import warnings

if os.geteuid()!=0:
    os.execvp('sudo',['sudo',sys.executable,str(Path(__file__).resolve()),*sys.argv[1:]])
certificate=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/var/lib/surface-secureboot/MOK.der')
subprocess.run(['openssl','x509','-inform','DER','-in',str(certificate),'-noout'],check=True)
result=subprocess.run(['mokutil','--test-key',str(certificate),'--ignore-keyring'],capture_output=True,text=True)
if 'is already enrolled' in result.stdout+result.stderr:
    print('Certificate is already enrolled. No password or new request is needed.')
    raise SystemExit(0)
if result.returncode!=0:
    raise SystemExit('Cannot verify certificate enrollment status.')
warnings.filterwarnings('error',category=getpass.GetPassWarning)
while True:
    password=getpass.getpass('Temporary MOK password (exactly 7 ASCII characters): ')
    if len(password)!=7 or not password.isascii() or not password.isprintable():
        print('Use exactly 7 printable ASCII characters.')
        continue
    if getpass.getpass('Confirm the 7-character password: ')!=password:
        print('Passwords do not match.')
        continue
    break
hashed=subprocess.check_output(['openssl','passwd','-6','-stdin'],input=(password+'\n').encode()).strip()
password=None
with tempfile.TemporaryDirectory(prefix='surface-mok-',dir='/run') as temporary:
    hash_file=Path(temporary)/'password.hash'
    descriptor=os.open(hash_file,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    with os.fdopen(descriptor,'wb') as stream:
        stream.write(hashed)
    subprocess.run(['mokutil','--import',str(certificate),'--hash-file',str(hash_file)],check=True)
subprocess.run(['mokutil','--timeout','-1'],check=True)
print('Enrollment requested. At MokManager choose Enroll MOK, Continue, Yes.')
print('Enter the complete 7-character password once when asked. Do not use Change MOK List Trusted State.')
