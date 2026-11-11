#!/usr/bin/env python3
"""Python entry point for the same offline installer used by setup.sh."""
import argparse,hashlib,os,sys
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--verify-only',action='store_true',help='Verify bundled payloads without changing the system')
args=parser.parse_args();folder=Path(__file__).resolve().parent
if args.verify_only:
    failed=[]
    for line in (folder/'files/SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);path=folder/name;h=hashlib.sha256()
        try:
            with path.open('rb') as f:
                for data in iter(lambda:f.read(4*1024*1024),b''):h.update(data)
            if h.hexdigest()!=digest:failed.append(name)
        except OSError:failed.append(name)
    if failed:
        print('Verification failed: '+', '.join(failed),file=sys.stderr);sys.exit(1)
    print('All offline payload checksums match.');sys.exit(0)
if not sys.platform.startswith('linux'):parser.error('Installation requires Debian Linux.')
os.execv('/bin/bash',['bash',str(folder/'setup.sh')])
