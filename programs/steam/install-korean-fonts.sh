#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=${FEX_ROOTFS:-"$HOME/.local/share/fex-emu/RootFS/ArchLinux"}
[ -d "$root/etc/fonts" ] || { echo "FEX root filesystem not found: $root" >&2; exit 1; }
mkdir -p "$root/usr/share/fonts/noto-cjk"
cp "$here/files/fonts/"*.ttc "$root/usr/share/fonts/noto-cjk/"
echo "Korean fonts installed in FEX. Fully exit and reopen the game."
