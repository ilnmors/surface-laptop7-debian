# Console UID

The repository expects Console UID 3000. The migration from UID 1001 to 3000 completed successfully before login. The primary group was subsequently changed to svadmins (GID 2000).

The helper refuses a live UID change, backs up account databases under root-only /var/lib/surface-uid-migration, runs usermod and updates files owned by the old UID on the root filesystem. These account backups are excluded from this bundle.

Offline copies: migrate.py and surface-console-uid.service. To reinstall this machine-specific migration, place migrate.py under /var/lib/surface-uid-migration with root ownership and mode 0700, install the unit under /etc/systemd/system, and enable it. Do not start it in an active Console session.

After reboot, check id -u console (3000) and journalctl -u surface-console-uid.service.

Current account: UID 3000, primary group svadmins (GID 2000). Existing supplementary groups, including sudo, are retained. apply-group.sh reproduces the group assignment and updates files belonging to the former private Console group; setup.sh runs it. Running processes obtain the new groups after a fresh login.
