#!/bin/bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib.sh"
surface_init patches "$@"
test -x /usr/local/sbin/surface-secureboot-update || { echo 'Apply kernel/setup.sh first.' >&2; exit 1; }
sudo bash patches/files/install.sh
