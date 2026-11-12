#!/bin/bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib.sh"
surface_init programs "$@"
bash programs/waydroid/setup.sh
bash programs/steam/setup.sh
if [[ -f programs/kakaotalk/files/manifest.json ]]; then bash programs/kakaotalk/setup.sh; else echo 'KakaoTalk: verified ARM64 package is not yet available; skipped.'; fi
