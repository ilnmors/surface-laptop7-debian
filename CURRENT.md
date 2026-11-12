# Current state — promoted 2026-11-12, default boot verified 19:25

- Default boot verified: signed default image (not trial), CPUs 0-9 with three ondemand policies, Secure Boot, ath12k D044C56077CC5357DC3F5BF / ov02c10 08EF7452B0F555AA15FA25F (fast_video=Y), camera 720p 37.46 fps over 90 frames, Wi-Fi-bound HTTPS 200 (kernel log later read as root: no beacon loss; regulatory/L2/APM warnings listed in drivers/files/sleep/diagnostics/2026-11-12-192713), Open Bar 49 ACTIVE, dock click-action=previews. The IPASoft sensor-helper warning is expected (helper patch rolled back after flicker).
- Deep cycle 19:27 succeeded: kernel resume 4.76 s (spi_hid fixed 2 s wait 2.455 s, empty PCIe 1bd0000 1.07 s), Wi-Fi reconnect ~2.1 s, no audio errors. See drivers/files/sleep/diagnostics/2026-11-12-192713/README.md.
- Terminal tofu for U+23F5 fixed with the Debian fonts-symbola fallback (user font live; bundled for setup).

- Verified one-shot boot: CPUs 0-9 online, three ondemand policies, Secure Boot enabled, camera 37.5 fps / 90 frames / zero errors, Wi-Fi HTTPS 200, Open Bar ACTIVE.
- User approved promotion. CPU topology and preserved-metadata camera driver are now standard boot and offline installer inputs. Normal signed image/initramfs rebuilt; prior working image remains as fallback. Next reboot verifies the promoted default path.
- Neutral isolated camera color improved; noise/1080p/system color integration remain deferred. No CPU cap or panel refresh reduction was added.
- Latest promotion/report changes are local only. Obtain explicit final approval before any further GitHub push. Both repositories remain private.
- Read NEXT.md for remaining checks.
