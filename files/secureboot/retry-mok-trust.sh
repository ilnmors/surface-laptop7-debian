#!/bin/bash
# Reopen MokManager for kernel MOK trust confirmation; keep existing keys.
set -euo pipefail
if (( EUID != 0 )); then
    exec sudo /bin/bash "$0"
fi
state=/var/lib/surface-secureboot
[[ -f "$state/MOK.der" ]]
mkdir -p "$state"
# Shim exports 1 when kernel MOK trust is already permitted.
# A redundant --trust-mok can fail deleting the absent opt-out variable.
if /usr/bin/python3 - <<'CHECK_TRUST'
from pathlib import Path
p=Path('/sys/firmware/efi/mok-variables/MokListTrustedRT')
raise SystemExit(0 if p.is_file() and p.read_bytes()==b'\x01' else 1)
CHECK_TRUST
then
    printf 'already-trusted; no new request\n' > "$state/mok-retry.status"
    printf 'Kernel MOK trust is already permitted. No MokManager request was queued.\n'
    printf 'Missing kernel keys require kernel-side investigation, not repeated trust confirmation.\n'
    exit 0
fi
printf 'pending\n' > "$state/mok-retry.status"
trap 'result=$?; if (( result != 0 )); then printf "failed %s\n" "$result" > "$state/mok-retry.status"; fi' EXIT
printf '\nReconfirm kernel trust of enrolled Surface MOK. Existing keys are retained.\n'
printf 'Choose a temporary 8-16 character ASCII password. Input is hidden.\n'
printf 'MokManager will ask for THREE INDIVIDUAL CHARACTERS by position.\n\n'
# mokutil 0.7.2 returns 1 for an already enrolled key.
set +e
/usr/bin/mokutil --test-key "$state/MOK.der"
key_status=$?
set -e
if (( key_status != 0 && key_status != 1 )); then
    printf 'Cannot inspect MOK certificate.
' >&2
    exit 1
fi
/usr/bin/mokutil --timeout -1
/usr/bin/mokutil --trust-mok
/usr/bin/efibootmgr --bootnext 0004
/usr/bin/python3 - <<'PY'
from pathlib import Path
import struct
base=Path('/sys/firmware/efi/efivars')
guid='605dab50-e046-4300-abb6-3dd810dd8b23'
request=(base/f'MokListTrustedNew-{guid}').read_bytes()[4:]
assert len(request)>=8 and struct.unpack_from('<I',request)[0]==0, 'Trust request missing or incorrect'
timeout=(base/f'MokTimeout-{guid}').read_bytes()[4:]
assert struct.unpack('<i',timeout)[0]==-1, 'MokManager timeout not disabled'
PY
printf 'ready\n' > "$state/mok-retry.status"
printf '\nREADY: next boot uses Debian Surface, and MokManager waits for input.\n'
printf 'Choose Change MOK List Trusted State, enter the requested password characters, then confirm trusting MOK.\n'
printf 'The kernel Secure Boot boot failure is still under investigation; this request alone does not guarantee boot.\n'
printf '\nPress Enter to close this window.\n'
read -r unused || true
