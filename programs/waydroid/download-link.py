#!/usr/bin/env python3
"""Expose only Waydroid shared Downloads to the invoking desktop user."""
import argparse, os, pwd, shutil, subprocess
from pathlib import Path

def storage(home):
    return home / '.local/share/waydroid/data/media/0/Download'

def has_access(target, uid):
    if not os.access(target, os.R_OK | os.W_OK | os.X_OK):
        return False
    result = subprocess.run(['getfacl', '-cpn', str(target)], capture_output=True, text=True)
    return result.returncode == 0 and f'default:user:{uid}:rwx' in result.stdout.splitlines()

def grant_access(uid):
    if os.geteuid() != 0 or uid == 0:
        raise SystemExit('The ACL helper requires root and a non-root desktop UID.')
    home = Path(pwd.getpwuid(uid).pw_dir)
    base = home / '.local/share/waydroid/data'
    parents = [base, base / 'media', base / 'media/0']
    if not all(p.is_dir() and not p.is_symlink() for p in parents):
        raise SystemExit('Start Waydroid once to create the Android shared storage.')
    target = storage(home)
    if not target.exists():
        parent = target.parent.stat()
        target.mkdir(mode=0o770)
        os.chown(target, parent.st_uid, parent.st_gid)
    if not target.is_dir() or target.is_symlink():
        raise SystemExit('Refusing an unexpected Download storage path.')
    for parent in parents:
        subprocess.run(['setfacl', '-m', f'u:{uid}:--x', str(parent)], check=True)
    subprocess.run(['setfacl', '-R', '-P', '-m', f'u:{uid}:rwX', str(target)], check=True)
    directories = [directory for directory, _, _ in os.walk(target, followlinks=False)]
    for offset in range(0, len(directories), 100):
        subprocess.run(['setfacl', '-m', f'd:u:{uid}:rwx', *directories[offset:offset + 100]], check=True)
    print('Waydroid Download ACLs applied; existing Android owners preserved.')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify the link and access without changing anything.')
    parser.add_argument('--apply-acl', type=int, metavar='UID', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.apply_acl is not None:
        grant_access(args.apply_acl)
        return
    if os.geteuid() == 0:
        raise SystemExit('Run as the Waydroid desktop user, not root.')
    if not shutil.which('getfacl') or not shutil.which('setfacl'):
        raise SystemExit('Install the bundled acl package through programs/waydroid/setup.sh first.')
    from gi.repository import GLib
    home = Path.home()
    folder = Path(GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD) or home / 'Downloads')
    link, target = folder / 'waydroid', storage(home)
    if os.path.lexists(link) and (not link.is_symlink() or os.readlink(link) != str(target)):
        raise SystemExit(f'Refusing to replace the existing path: {link}')
    if args.check:
        if not link.is_symlink() or not has_access(target, os.getuid()):
            raise SystemExit('Waydroid download link or access is not configured.')
        print(f'Verified: {link} -> {target}; user read/write access and inherited ACL present.')
        return
    if not has_access(target, os.getuid()):
        subprocess.run(['sudo', 'python3', str(Path(__file__).resolve()), '--apply-acl', str(os.getuid())], check=True)
    if not has_access(target, os.getuid()):
        raise SystemExit('Download access verification failed.')
    folder.mkdir(parents=True, exist_ok=True)
    if not os.path.lexists(link):
        link.symlink_to(target, target_is_directory=True)
    print(f'Configured: {link} -> {target}')

if __name__ == '__main__':
    main()
