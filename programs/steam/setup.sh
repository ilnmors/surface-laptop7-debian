#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ ! -f "$HOME/.local/share/Steam/steamrtarm64/steam" ]; then
 echo 'Steam ARM64 runtime is not bundled; existing native Steam installation is required.'; exit 0
fi
install -D -m755 "$here/steam-launcher.sh" "$HOME/.local/bin/steam"
sh "$here/fix-sdk.sh"
if [ -d "$HOME/.local/share/fex-emu/RootFS/ArchLinux/etc/fonts" ]; then sh "$here/install-korean-fonts.sh"; fi
