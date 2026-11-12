# Steam / native ARM64 client

The current client is ~/.local/share/Steam/steamrtarm64/steam and the user launcher is ~/.local/bin/steam. The launcher carries the FEX graphics-provider environment; a plain amd64 Steam .deb is not the working ARM64 setup.

RimWorld Player.log reported a missing ~/.steam/sdk64/steamclient.so, not an absent Steam process. fix-sdk.sh creates that absent path as a symlink to Steam's x86-64 linux64/steamclient.so. It never substitutes an ARM64 library for the x86 game and refuses to replace existing files. Restart the game from Steam to verify Steamworks initialization; no save data or game options were changed.

steam-launcher.sh is the current user launcher snapshot. Steam installation, runtime and FEX payload provenance still needs a complete export; this directory does not yet claim to reinstall the client offline. Games, saves, login tokens and userdata are not copied into this bundle.

## Architecture and incident evidence

Host/client: ARM64 Steam under steamrtarm64. RimWorldLinux and Steam's linux64/steamclient.so are x86-64. FEX runs the x86-64 game and its x86-64 SDK library; Steam IPC connects it to the native ARM64 client. This does not load an x86-64 library directly into an ARM64 process.

Observed Player.log: `dlopen failed ... ~/.steam/sdk64/steamclient.so`, `No such file or directory`, then `SteamAPI_Init(): Sys_LoadModule failed`. Steam itself was running. The missing SDK link was created on 2026-11-12. A fresh game launch and successful Steam API initialization are still required to confirm the outcome. No game save or user authentication state is stored here.

## RimWorld Korean rendering

2026-11-12: Host fontconfig resolves Korean to Noto Sans CJK KR, but the FEX ArchLinux root contained only Adwaita fonts. The game includes its Korean language archive. Bundled the Debian fonts-noto-cjk regular/bold TTC files and license in files/fonts; run ./install-korean-fonts.sh as the desktop user to install them inside the FEX root. Source: installed Debian fonts-noto-cjk package (/usr/share/fonts/opentype/noto). Restart the game to reload font discovery. Visual verification is pending; the stored game language was English when inspected. Intermittent clicks remain under investigation.
