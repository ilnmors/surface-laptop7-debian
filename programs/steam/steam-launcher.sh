#!/bin/sh
set -eu
root="$HOME/.local/share/Steam"
if [ -z "${XAUTHORITY:-}" ] || [ ! -f "$XAUTHORITY" ]; then
  authority=$(systemctl --user show-environment | sed -n 's/^XAUTHORITY=//p')
  if [ -n "$authority" ] && [ -f "$authority" ]; then export XAUTHORITY="$authority"; fi
fi
provider="$HOME/.local/share/fex-emu/RootFS/ArchLinux/graphics_provider.json"
if [ -f "$provider" ]; then export STEAM_COMPAT_GRAPHICS_PROVIDER="$provider"; fi
cd "$root"
exec "$root/steamrtarm64/steam" "$@"
