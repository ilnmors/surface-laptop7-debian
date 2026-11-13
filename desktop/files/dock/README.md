# Fluent floating dock

Existing Dash to Dock: bottom, centered compact 40px icons, pale background, rounded border, blue running indicators. Clicking an application with several windows opens window previews instead of cycling. One window activates normally. Auto-hide/intellihide are retained.

The Fluent theme contains dock.css; desktop/setup.sh restores the saved dash-to-dock.dconf. Settings were applied live. Before-settings are in before.dconf; remove the Surface Fluent dock CSS block and load that snapshot to undo this change.

## Taskbar layout (2026-11-13)

With autohide + intellihide + pressure reveal, a finger on the GTCH touchscreen could never bring the dock back (only pointer pressure at the edge reveals it; Dash to Dock has no touch-edge reveal). The dock is therefore always visible, and because a permanently floating pill looked out of place it is laid out like the Windows 11 taskbar:

- `dock-fixed=true`, `autohide=false`, `intellihide=false`: always shown; maximized windows are sized above it.
- `extend-height=true`, `force-straight-corner=true`: full screen width, flush with the bottom edge.
- `always-center-icons=true`, `show-apps-at-top=true`: centered icons, the app grid button at the left end like Start.
- `running-indicator-style='DASHES'`, `dash-max-icon-size=36`, background `#f3f3f3` at 0.94.
- `dock.css` (appended to the Fluent-Light shell theme): flat bar, 1 px top border, no radius/margin/shadow.

Settings are in `settings/dash-to-dock.dconf`. To go back to the floating auto-hide dock, load `before.dconf` and restore the previous CSS block from git history.
