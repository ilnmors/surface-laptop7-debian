#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
module=/usr/lib/aarch64-linux-gnu/libcamera/ipa_soft_simple.so
if [[ $EUID != 0 ]]; then
  exec sudo /bin/bash "$PWD/install.sh" "$@"
fi
case "${1:-install}" in
  install)
    test "$(dpkg-query -W -f='${Version}' libcamera-ipa:arm64)" = 0.4.0-7
    sha256sum --check --strict module.sha256
    dpkg-divert --local --rename --add "$module"
    install -m 644 ipa_soft_simple.so "$module"
    ;;
  rollback)
    test "$(dpkg-divert --listpackage "$module")" = LOCAL
    if [[ -e "$module" ]]; then
      cmp "$module" ipa_soft_simple.so
      unlink "$module"
    fi
    dpkg-divert --local --rename --remove "$module"
    ;;
  *)
    echo "Usage: $0 [install|rollback]" >&2
    exit 2
    ;;
esac
