#!/bin/bash
# Match the repository's Console administrator group without changing other groups.
set -euo pipefail
(( EUID == 0 )) || { echo 'Run as root.' >&2; exit 1; }
old_gid=$(id -g console)
old_group=$(id -gn console)
if getent group svadmins >/dev/null; then
    [[ $(getent group svadmins | cut -d: -f3) == 2000 ]] || { echo 'svadmins has an unexpected GID.' >&2; exit 1; }
else
    ! getent group 2000 >/dev/null || { echo 'GID 2000 is already in use.' >&2; exit 1; }
    [[ $old_group == console ]] || { echo 'Unexpected Console primary group.' >&2; exit 1; }
    groupmod --gid 2000 --new-name svadmins console
fi
usermod --gid svadmins console
if [[ $old_gid != 2000 ]]; then
    [[ $old_group == console ]] || { echo 'Refusing to remap a shared group.' >&2; exit 1; }
    find / -xdev -gid "$old_gid" -exec chgrp -h 2000 {} +
    runtime=/run/user/$(id -u console)
    if [[ -d $runtime ]]; then
        find "$runtime" -xdev \( -path "$runtime/doc" -o -path "$runtime/gvfs" \) -prune -o -gid "$old_gid" -exec chgrp -h 2000 {} +
    fi
fi
id console
