#!/bin/bash
# Explicit one-time cleanup requested by the user; normal setup never runs this.
set -euo pipefail
[[ ${1:-} == --remove-user-apps ]] || { echo 'Usage: reset-apps.sh --remove-user-apps (deletes Android user apps and their data)' >&2; exit 2; }
as_root() { if (( EUID == 0 )); then "$@"; else sudo "$@"; fi; }
mapfile -t packages < <(as_root waydroid shell -- pm list packages -3 | tr -d '\r' | sed -n 's/^package://p')
for package in "${packages[@]}"; do
 [[ $package =~ ^[A-Za-z0-9_.]+$ ]] || exit 1
 as_root waydroid shell -- pm uninstall --user 0 "$package"
done
# Optional factory apps only; retain settings, launcher, package installer, WebView and framework.
for package in com.android.calculator2 org.lineageos.jelly org.lineageos.recorder org.lineageos.etar org.lineageos.aperture com.android.deskclock com.android.gallery3d com.android.contacts org.lineageos.eleven; do
 as_root waydroid shell -- pm uninstall --user 0 "$package" || true
done
if (( EUID != 0 )); then python3 "$(dirname -- "$0")/files/integrate-apps.py"; else echo "Run files/integrate-apps.py as the desktop user to hide factory launchers."; fi
