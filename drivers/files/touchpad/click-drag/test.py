#!/usr/bin/env python3
"""Compile the actual TouchDevice header against a uinput event sink; no device access."""
from pathlib import Path
from zipfile import ZipFile
import shutil, subprocess, tempfile
HERE = Path(__file__).resolve().parent
EDGE = HERE.parent / 'edge-fix'

def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, text=True, **kwargs)

with tempfile.TemporaryDirectory(prefix='surface-button-tests-') as tmp:
    work = Path(tmp)
    source = work / 'source'
    with ZipFile(EDGE / 'source.zip') as archive:
        for name in archive.namelist():
            if '/vendor/iptsd/' not in name or name.endswith('/'):
                continue
            rel = Path(name.split('/vendor/iptsd/', 1)[1])
            if rel.is_absolute() or '..' in rel.parts:
                raise ValueError('Unsafe source archive path')
            target = source / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(name))
    deps = work / 'deps'
    for package in sorted((EDGE / 'build-debs').glob('*.deb')):
        run(['dpkg-deb', '-x', str(package), str(deps)])
    run(['patch', '-p1', '-i', str(EDGE / 'edge-contact.patch')], cwd=source)
    header = source / 'src/apps/daemon/touch.hpp'
    baseline = header.read_bytes()
    run(['patch', '-p1', '-i', str(HERE / 'physical-button-state.patch')], cwd=source)
    for name, content, expected in [('before', baseline, 1), ('after', header.read_bytes(), 0)]:
        stage = work / name
        stage.mkdir()
        (stage / 'touch.hpp').write_bytes(content)
        for fixture in (HERE / 'tests').iterdir():
            shutil.copy2(fixture, stage / fixture.name)
        run(['g++', '-std=c++20', '-O1', '-DFMT_HEADER_ONLY',
             '-I' + str(deps / 'usr/include'), '-I' + str(deps / 'usr/include/eigen3'),
             '-I' + str(source / 'src'), str(stage / 'button-state.cpp'), '-o', str(stage / 'test')])
        result = subprocess.run([str(stage / 'test')], capture_output=True, text=True, timeout=10)
        print(name.upper(), result.stdout, sep='\n')
        if result.returncode != expected:
            raise SystemExit(f'{name}: unexpected result {result.returncode}')
print('Original reproduces failure; patched header passes. No physical input was injected.')
