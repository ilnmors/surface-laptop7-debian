#!/usr/bin/python3
"""Mount the GNOME Online Accounts WebDAV (Files) volumes after login.

GNOME lists these volumes but mounts them only when Files opens them. Retry
for a while so the mount also succeeds when the network comes up late after
login (the shares use the public domain, so no VPN is needed).
"""
import gi
gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib

RETRY_SECONDS = 15
GIVE_UP_AFTER = 600

loop = GLib.MainLoop()
monitor = Gio.VolumeMonitor.get()
elapsed = 0
pending = set()


def webdav_volumes():
    for volume in monitor.get_volumes():
        uuid = volume.get_uuid() or ""
        if uuid.startswith(("davs://", "dav://")) and volume.can_mount():
            yield volume


def mounted(volume, result):
    pending.discard(volume.get_uuid())
    try:
        volume.mount_finish(result)
    except GLib.Error as error:
        print(f"goa-webdav-mount: {volume.get_name()}: {error.message}", flush=True)


def attempt():
    global elapsed
    volumes = list(webdav_volumes())
    waiting = [v for v in volumes if v.get_mount() is None]
    # The volume list fills in shortly after login; finish only once shares were found and all are mounted.
    if volumes and not waiting:
        loop.quit()
        return False
    for volume in waiting:
        if volume.get_uuid() not in pending:
            pending.add(volume.get_uuid())
            volume.mount(Gio.MountMountFlags.NONE, Gio.MountOperation(), None, mounted)
    elapsed += RETRY_SECONDS
    if elapsed > GIVE_UP_AFTER:
        loop.quit()
        return False
    return True


GLib.idle_add(lambda: attempt() and False)
GLib.timeout_add_seconds(RETRY_SECONDS, attempt)
loop.run()
