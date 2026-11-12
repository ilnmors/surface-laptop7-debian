# Current state — promoted 2026-11-12

- Verified one-shot boot: CPUs 0-9 online, three ondemand policies, Secure Boot enabled, camera 37.5 fps / 90 frames / zero errors, Wi-Fi HTTPS 200, Open Bar ACTIVE.
- User approved promotion. CPU topology and preserved-metadata camera driver are now standard boot and offline installer inputs. Normal signed image/initramfs rebuilt; prior working image remains as fallback. Next reboot verifies the promoted default path.
- Neutral isolated camera color improved; noise/1080p/system color integration remain deferred. No CPU cap or panel refresh reduction was added.
- Latest promotion/report changes are local only. Obtain explicit final approval before any further GitHub push. Both repositories remain private.
- Read NEXT.md for remaining checks.
