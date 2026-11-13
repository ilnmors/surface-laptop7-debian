# Current state — reviewed 2026-11-13

## Observed in the running system

- Booted at 08:56 through `/secureboot/trial-touch/vmlinuz-surface-signed.efi` with `cma=512M`. The 512 MiB reservation failed; `/proc/meminfo` reports CmaTotal=0. The current boot is not proof that the new default command line has been used.
- CPU online 0-9, Secure Boot enabled, spi-hid v2 srcversion 0923360D0DE94E631C945EE. The physical 045E:0C6E touchscreen and IPTSD virtual touchscreen/stylus exist.
- The saved default image uses the promoted GTCH SPI DTB, PCIe3-off and explicit `cma=0`; a previous working image remains in GRUB. Reboot into the default image is a remaining check, not required for this read-only handoff review.

## Claude changes reviewed

- Touchscreen: GTCH SPI panel trial succeeded and was promoted to the default/offline DTB pipeline.
- Resume: spi-hid defers hardware restart; recorded kernel resume 4.76 → 1.41 s. Touchpad readiness still occurs about 2.3 s after wake; Wi-Fi about 2.1 s. These are different measurements.
- Camera: no-CMA/system-heap path, dma-heap udev access and user black-level tuning support GNOME/PipeWire. Recorded 720p/1080p 37.5fps; user reported better color. Low-light grain remains; the rejected sensor-helper IPA is still not a production fix.
- Desktop: full-width always-visible taskbar with window previews, Open Bar, Symbola fallback. Boot-screen appearance confirmed in the handoff record. Native Fn toggle retained by user choice; experimental normalizer removed.
- KakaoTalk: background-only login launch and notifications recorded as working. Steam game checks and Samsung integration remain held.
- Repository: reviewed OxiCloud binding/OIDC provisioning, retired-stack archive, release pins, Authelia-only application login settings, Sure UI-based LLM configuration and `.agent-workspace` rename. This is local change review, not validation of a fresh server deployment.

## Ownership and validation

- Workspace generation/editing/checks run as console. Root-owned entries in repository (47) were returned to console:svadmins; Surface already had console ownership. System-installed files retain required root ownership.
- `console` ran the installer plan and offline checksum verification. Raw upstream data/offline payloads remain local as before.
- No push or reboot was performed by this handoff review. Future pushes require final user confirmation; local AGENT.md files carry the workflow and ownership rule.

## Desktop refresh (2026-11-13)

Use one continuous opaque Mainland top bar: 34px high, zero outer margin/radius/border, 100% background opacity. Trilands was removed after the user reported the transparent gaps between white component groups. Keep CPU/RAM on the left, clock in the center and notification/input/system controls on the right. The alpine photo and teal GTK3/GTK4 app theme remain; Shell stays Fluent-Light. Settings were refreshed live; appearance awaits user confirmation. The wallpaper, app theme and panel settings are documented separately in `desktop/files/topbar/ALPINE-THEME.md`.

## Waydroid downloads

Waydroid setup creates `<XDG Downloads>/waydroid` after Android boot readiness, using the shared SH/Python helper in `programs/waydroid/download-link.*`. It grants narrowly scoped ACL access with the current desktop UID while preserving Android owners. The ACL package is bundled for offline installation. Existing correct setup is idempotent; `--check` is read-only. The current `~/Downloads/waydroid` link and inherited ACLs passed live verification.
