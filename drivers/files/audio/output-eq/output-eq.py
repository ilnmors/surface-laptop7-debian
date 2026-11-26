#!/usr/bin/env python3
"""Per-output parametric EQ for PipeWire, from an AutoEq "ParametricEQ.txt" file.

Each EQ is a WirePlumber smart filter run by the user's filter-chain.service:
it is inserted only in front of its target sink (for example one Bluetooth
headset) and is skipped for every other output.

  output-eq.py list                                  audio sinks and installed EQs
  output-eq.py set NAME --sink NODE --file EQ.txt    install or replace one EQ
  output-eq.py remove NAME                           remove one EQ

Run as the desktop user. Nothing outside ~/.config/pipewire is changed.
"""
import argparse, json, re, shutil, subprocess, sys, time
from pathlib import Path

CONF_DIR = Path.home() / '.config/pipewire/filter-chain.conf.d'
EQ_DIR = Path.home() / '.config/pipewire/eq'
PREFIX = '60-output-eq-'
NAME_RE = re.compile(r'^[a-z0-9][a-z0-9-]{0,40}$')
PREAMP_RE = re.compile(r'^Preamp:\s*-?\d+(\.\d+)?\s*dB$')
FILTER_RE = re.compile(r'^Filter\s+\d+:\s+(ON|OFF)\s+(PK|LSC|HSC|LS|HS|LP|HP|LPQ|HPQ|NO)\s+Fc\s+\d+(\.\d+)?\s*Hz'
                       r'(\s+Gain\s+-?\d+(\.\d+)?\s*dB)?(\s+Q\s+\d+(\.\d+)?)?$')

TEMPLATE = '''# Output EQ "{name}", written by output-eq.py (surface-laptop7-debian).
# Smart filter: used only in front of {sink}.
context.modules = [
  {{ name = libpipewire-module-filter-chain
    # A broken chain must not take the filter-chain daemon down with it.
    flags = [ nofail ]
    args = {{
      node.description = "{name} EQ"
      media.name       = "{name} EQ"
      filter.graph = {{
        nodes = [
          {{ type = builtin name = eq label = param_eq
            config = {{ filename = "{eq_file}" }} }}
        ]
        inputs  = [ "eq:In 1" "eq:In 2" ]
        outputs = [ "eq:Out 1" "eq:Out 2" ]
      }}
      audio.channels = 2
      audio.position = [ FL FR ]
      capture.props = {{
        node.name   = "effect_input.output_eq_{key}"
        media.class = Audio/Sink
        filter.smart = true
        filter.smart.name = "output-eq-{name}"
        filter.smart.target = {{ node.name = "{sink}" }}
      }}
      playback.props = {{
        node.name    = "effect_output.output_eq_{key}"
        node.passive = true
      }}
    }}
  }}
]
'''


def die(msg):
    print(f'output-eq: {msg}', file=sys.stderr)
    sys.exit(1)


def pw_nodes():
    out = subprocess.run(['pw-dump'], capture_output=True, text=True, check=True).stdout
    for obj in json.loads(out):
        props = (obj.get('info') or {}).get('props') or {}
        if obj.get('type') == 'PipeWire:Interface:Node':
            yield props


def sinks():
    return [(p.get('node.name', ''), p.get('node.description', ''))
            for p in pw_nodes()
            if p.get('media.class') == 'Audio/Sink' and not p.get('filter.smart')
            and not str(p.get('node.name', '')).startswith('effect_input.')]


def check_eq_file(path):
    lines = [l.strip() for l in path.read_text().splitlines() if l.strip()]
    if not lines:
        die(f'{path} is empty')
    bad = [l for l in lines if not (PREAMP_RE.match(l) or FILTER_RE.match(l))]
    if bad:
        die(f'{path}: not AutoEq ParametricEQ lines: {bad[:3]}')
    if not any(FILTER_RE.match(l) for l in lines):
        die(f'{path}: no Filter lines')
    if not lines[0].startswith('Preamp:'):
        print('output-eq: warning: no Preamp line; loud bands may clip', file=sys.stderr)


def restart():
    subprocess.run(['systemctl', '--user', 'enable', 'filter-chain.service'], check=True,
                   capture_output=True)
    subprocess.run(['systemctl', '--user', 'restart', 'filter-chain.service'], check=True)


def cmd_list(_):
    print('Audio sinks (use the node name with --sink):')
    for name, desc in sinks():
        print(f'  {name}    {desc}')
    confs = sorted(CONF_DIR.glob(f'{PREFIX}*.conf'))
    print('Installed output EQs:' if confs else 'Installed output EQs: none')
    for conf in confs:
        target = re.search(r'filter\.smart\.target = \{ node\.name = "([^"]+)"', conf.read_text())
        print(f'  {conf.stem[len(PREFIX):]}  ->  {target.group(1) if target else "?"}')


def cmd_set(a):
    if not NAME_RE.match(a.name):
        die('NAME: lowercase letters, digits and "-" only')
    src = Path(a.file).expanduser().resolve()
    if not src.is_file():
        die(f'{src} not found')
    check_eq_file(src)
    known = [n for n, _ in sinks()]
    if a.sink not in known and not a.force:
        die(f'sink {a.sink!r} is not present now (see "list"); use --force for a device '
            'that is currently disconnected')
    EQ_DIR.mkdir(parents=True, exist_ok=True)
    CONF_DIR.mkdir(parents=True, exist_ok=True)
    eq_file = EQ_DIR / f'{a.name}.txt'
    if src != eq_file:
        shutil.copyfile(src, eq_file)
    key = a.name.replace('-', '_')
    conf = CONF_DIR / f'{PREFIX}{a.name}.conf'
    conf.write_text(TEMPLATE.format(name=a.name, sink=a.sink, eq_file=eq_file, key=key))
    restart()
    for _ in range(20):
        if any(p.get('node.name') == f'effect_input.output_eq_{key}' for p in pw_nodes()):
            print(f'EQ "{a.name}" active in front of {a.sink}.')
            print('The Preamp lowers the level; raise the volume if it sounds quieter.')
            return
        time.sleep(0.5)
    die(f'filter-chain restarted but the EQ node did not appear; check '
        f'"journalctl --user -u filter-chain" and remove {conf} to roll back')


def cmd_remove(a):
    conf = CONF_DIR / f'{PREFIX}{a.name}.conf'
    eq_file = EQ_DIR / f'{a.name}.txt'
    if not conf.exists():
        die(f'no EQ named {a.name!r} (see "list")')
    conf.unlink()
    eq_file.unlink(missing_ok=True)
    restart()
    print(f'EQ "{a.name}" removed.')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('list', help='audio sinks and installed EQs').set_defaults(func=cmd_list)
    s = sub.add_parser('set', help='install or replace one EQ')
    s.add_argument('name', help='short name, e.g. wh-ch720n')
    s.add_argument('--sink', required=True, help='target sink node.name (see "list")')
    s.add_argument('--file', required=True, help='AutoEq ParametricEQ.txt')
    s.add_argument('--force', action='store_true', help='allow a sink that is not connected now')
    s.set_defaults(func=cmd_set)
    r = sub.add_parser('remove', help='remove one EQ')
    r.add_argument('name')
    r.set_defaults(func=cmd_remove)
    a = p.parse_args()
    a.func(a)


if __name__ == '__main__':
    main()
