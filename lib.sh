#!/bin/bash
# Shared helpers; setup entry points always run as the desktop user.
surface_init() {
  component=$1; shift
  bundle=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
  cd "$bundle"
  case "${1:-}" in
    --plan) echo "$component: $(cat "$bundle/$component/PLAN.txt")"; exit 0;;
    --verify-only) exec python3 "$bundle/setup.py" --verify-only;;
    '') ;;
    *) echo "Usage: $component/setup.sh [--plan|--verify-only]" >&2; exit 2;;
  esac
  . /etc/os-release
  [[ $ID == debian && $VERSION_CODENAME == trixie && $EUID != 0 ]] || {
    echo 'Run as the desktop user on Debian 13.' >&2; exit 1;
  }
  if [[ $component != desktop ]]; then
    [[ $(dpkg --print-architecture) == arm64 ]] || { echo 'Bundled hardware/program packages require ARM64.' >&2; exit 1; }
  fi
  if [[ $component == kernel || $component == drivers || $component == patches ]]; then
    grep -azq 'microsoft,romulus13' /sys/firmware/devicetree/base/compatible || {
      echo 'Hardware components support Surface Laptop 7 Romulus13 only.' >&2; exit 1;
    }
  fi
  if [[ ${SURFACE_PAYLOADS_VERIFIED:-} != 1 ]]; then python3 "$bundle/setup.py" --verify-only; fi
  sudo -v
  kernel=7.3.0-31-qcom-x1e
}
offline_apt() {
  local packages=() pattern file
  for pattern in "$@"; do
    while IFS= read -r file; do packages+=("$file"); done < <(compgen -G "$pattern" || true)
  done
  (( ${#packages[@]} )) || { echo 'No offline packages found.' >&2; return 1; }
  sudo apt-get --no-download -o Dir::Etc::sourcelist=/dev/null -o Dir::Etc::sourceparts=- --no-install-recommends install "${packages[@]}"
}
restore_tree() { tar -C "$1" -cf - . | sudo tar --no-overwrite-dir --no-same-owner -C / -xf -; }
