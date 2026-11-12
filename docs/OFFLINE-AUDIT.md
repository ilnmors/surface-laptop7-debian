# Offline bundle audit — 2026-11-11

- All 115 bundled rootfs files match installed content. Three files use cleaned Surface names in the bundle instead of installed sl7 names; their contents match.
- Secure Boot updater, builtin-certificate helper and merged boot DTB match installed copies.
- Fluent-Light theme and bundled GNOME extensions match installed files. Desktop dconf snapshots were refreshed; the current background snapshot changed.
- Both checksum manifests passed before this audit. Manifests were refreshed after documentation and snapshot updates.
- Secure Boot physical boot is now verified; touchscreen probing still fails. Deep suspend crashes in the USB driver; saved evidence and an upstream patch reference are under sleep/diagnostics/.
- Signing private keys, site-specific CA/VPN/server credentials and repository project secrets are excluded.

Keep CURRENT.md, installation files, concise procedures and checksums synchronized after each Surface configuration change. A saved configuration is not a claim of hardware functionality.
