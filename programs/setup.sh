#!/bin/bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib.sh"
surface_init programs "$@"
bash programs/waydroid/setup.sh
bash programs/steam/setup.sh
if compgen -G 'programs/kakaotalk/files/apk/*.apk' >/dev/null; then bash programs/kakaotalk/setup.sh; else echo 'KakaoTalk: no APKs in programs/kakaotalk/files/apk (see programs/kakaotalk/README.md); skipped.'; fi
