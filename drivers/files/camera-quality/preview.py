#!/usr/bin/env python3
"""Run the isolated offline libcamera color trial; does not replace system libraries."""
import argparse, os, shutil, subprocess
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--low-gain', action='store_true', help='Neutral colors with the community exposure target')
p.add_argument('--neutral', action='store_true', help='Neutral color without community CCM')
p.add_argument('--capture', type=int, help='Headless frame count instead of a preview window')
a = p.parse_args()
here = Path(__file__).resolve().parent
cache = Path.home() / '.cache/surface-camera-0.7'
cache.mkdir(parents=True, exist_ok=True)
if not (cache / '.extracted').exists():
    for package in sorted((here / 'backports/packages').glob('*.deb')):
        subprocess.run(['dpkg-deb', '-x', str(package), str(cache)], check=True)
    (cache / '.extracted').touch()
ipa = cache / 'trial-ipa'
config = cache / 'trial-config/simple'
ipa.mkdir(exist_ok=True)
config.mkdir(parents=True, exist_ok=True)
shutil.copy2(here / ('backports/ipa/ipa_soft_simple-gain-step-candidate.so' if a.low_gain else 'backports/ipa/ipa_soft_simple-balanced-candidate.so'), ipa / 'ipa_soft_simple.so')
shutil.copy2(here / ('preview/ov02c10-neutral-low-gain.yaml' if a.low_gain else 'preview/ov02c10-neutral-candidate.yaml'), config / 'ov02c10.yaml')
env = dict(os.environ,
    LD_LIBRARY_PATH=str(cache / 'usr/lib/aarch64-linux-gnu'),
    LIBCAMERA_IPA_MODULE_PATH=str(ipa),
    LIBCAMERA_IPA_PROXY_PATH=str(cache / 'usr/libexec/aarch64-linux-gnu/libcamera'),
    LIBCAMERA_IPA_CONFIG_PATH=str(config.parent),
    LIBCAMERA_PIPELINES_MATCH_LIST='simple', LIBCAMERA_SOFTISP_MODE='cpu',
    LIBCAMERA_IPA_FORCE_ISOLATION='1', QT_QPA_PLATFORM='xcb')
stream = '--stream=role=viewfinder,width=1280,height=720'
if a.capture:
    cmd = [str(cache / 'usr/bin/cam'), '-c', '1', '--capture=' + str(a.capture), stream]
else:
    cmd = [str(cache / 'usr/bin/qcam'), '--renderer=qt', '-c',
        '/base/soc@0/cci@ac16000/i2c-bus@1/camera@36', stream]
os.execve(cmd[0], cmd, env)
