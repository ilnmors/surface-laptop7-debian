# Fluent top bar

Fluent Light now uses an inset, rounded, translucent pale panel, dark text, blue hover accents and rounded buttons. Blur My Shell remains enabled with radius 14; forced light text and background overrides are disabled. The clock shows weekday and date. No extra extension was installed.

panel.css is appended to the bundled Fluent-Light Shell CSS. setup.sh installs that theme and restores the updated Blur My Shell and interface snapshots. The running Shell reloaded the theme without stylesheet errors. Visual appearance still needs user confirmation.

The previous CSS and panel settings are saved here. To restore, copy gnome-shell.before.css to ~/.themes/Fluent-Light/gnome-shell/gnome-shell.css, reset only /org/gnome/shell/extensions/blur-my-shell/panel/, then dconf load that path from panel.before.dconf. Toggle the User Themes setting to reload.

Additional widgets: Vitals 86 (CPU/memory, five-second polling), Caffeine 61 (manual only, automatic fullscreen/media activation disabled), AppIndicator 66 (tray icons). The reviewed GNOME 48 extension files and GTop dependencies are bundled. All three extensions are active; no per-extension RAM attribution was measured.
