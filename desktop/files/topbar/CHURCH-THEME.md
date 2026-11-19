# Cross in the Wilderness / Fluent Orange Light (2026-11-19)

Matches the wallpaper `church-cross-in-the-wilderness.jpg` (Frederic Edwin Church, 1857): amber sunset sky, olive-brown mountains.

- GTK3/GTK4: `Fluent-orange-Light` (accent #F57C00), built offline exactly like the teal variant in [ALPINE-THEME.md](ALPINE-THEME.md) with `install.sh -d OUTPUT -t orange -c light -s standard`; `COPYING` kept and `desktop/files/dock/dock.css` appended to its Shell CSS. GTK4 is linked to `~/.themes/Fluent-orange-Light/gtk-4.0`.
- GNOME accent: orange.
- Shell: stays `Fluent-Light` (the generated Shell variants lack the Surface panel additions; see ALPINE-THEME.md, Panel recovery).
- Open Bar (`settings/openbar.dconf`, light/dark/current keys alike): parchment bar #faf5e8, tan border, dark brown text, amber highlight and accent.
- Dock (`settings/dash-to-dock.dconf`): background #faf5e8, amber running dots #F57C00.
- Papirus icons, cursor and the terminal palette are unchanged.

Rollback: `archive/church-theme-before-2026-11-19/restore.sh` (Open Bar, dock and interface dconf dumps plus the previous GTK4 link). The teal theme stays installed.
