#!/bin/sh
set -eu
steam_root="$HOME/.local/share/Steam"
test -f "$steam_root/linux64/steamclient.so"
mkdir -p "$HOME/.steam/sdk64"
if [ ! -e "$HOME/.steam/sdk64/steamclient.so" ] && [ ! -L "$HOME/.steam/sdk64/steamclient.so" ]; then
    ln -s "$steam_root/linux64/steamclient.so" "$HOME/.steam/sdk64/steamclient.so"
fi
echo 'Steam x86-64 SDK library path is present. Relaunch the game from Steam.'
