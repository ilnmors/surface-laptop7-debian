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

The top bar uses three rounded light groups instead of concentrating every indicator on the right. Left: Activities and fixed-width CPU/RAM. Center: clock/date. Right: notification bell, native English/Korean indicator, tray and system controls. Open Bar Trilands, 34px height, 6px margin, 14px corners. The legacy IBus tray icon is hidden; input sources and switch shortcuts are unchanged. The existing bottom taskbar remains. Settings were applied and refreshed without logout, read back, and saved for offline setup. Appearance awaits user feedback. Targeted rollback: `archive/topbar-before-balanced-*/restore.sh`.
