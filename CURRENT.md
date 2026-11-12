# Current state — 2026-11-13 maintenance pass

- Next boot is a one-shot trial (GRUB next_entry=surface-touch-trial): signed image with the GTCH HID-over-SPI touchscreen on spi10 and cma=512M. It clears itself before booting; the default image also carries cma=512M. Restore: drivers/files/touchscreen/spi-gtch/restore.sh; GRUB backup /boot/secureboot/grub.cfg.before-cma512.
- Camera: capture failures were CMA exhaustion (128 MB, ~112 MB held by drivers); 720p and 1080p run at 37.5 fps with the system heap. cma=512M fixes it from the next boot.
- Done today: Symbola installed system-wide (user confirmed), leftover Nextcloud token 124 revoked, Wi-Fi/audio/Bluetooth stable across deep cycles, USB runtime PM tested (no effect, reverted), root-owned bundle files returned to console.
- Waiting on the user: touchscreen/CMA trial result, camera 37.5 vs 18.8 fps noise choice, a real KakaoTalk message, boot-screen appearance, Fn-lock daemon go-ahead. Steam game checks and Samsung integration stay held by earlier decision.


- v2 boot and lid cycle verified: kernel resume 1.41 s (v1 1.62 s, originally 4.76 s), touchpad restarted 2.3 s after wake, Wi-Fi connected 2.1 s after wake, KakaoTalk running in the background, sleep drain roughly ≤ 0.7 W (1 % over 43 min). See drivers/files/sleep/diagnostics/2026-11-12-231657/README.md.

- Next boot: spi-hid v2 (0923360D0DE94E631C945EE) defers reset+settle entirely; GRUB fallback = verified v1 image (21:16). Old boot images deleted. KakaoTalk login autostart now boots only the Waydroid session (MessengerService runs, no window). Brightness lowered to ~25 % for the sleep-drain test.

## Verified 21:22 (v1)

- Verified 21:16 boot + 21:22 lid cycle: kernel resume 1.62 s (was 4.76 s), CPU 0-9, Secure Boot, spi_hid F78320E76D9CB9AFF42A4E8, no pcie3 device, Wi-Fi HTTPS 200 and reconnect ~2.0 s, touchpad back after wake. Installer now uses the PCIe3-off DTB and this module. Boot-time panel-edp "unknown panel" WARN noted (unrelated driver; not yet compared with earlier boots). Battery comparison pending (was charging).
- Installed: deferred-resume spi-hid.ko (F78320E76D9CB9AFF42A4E8) and DTB with unused pcie3 (1bd0000) disabled; signed image/initramfs rebuilt. The 19:25 verified image is GRUB "Surface previous working image" (/boot/secureboot/rollback-20261112); the pre-CPU image moved to rollback-20261112-pre-cpu (no menu entry).

## Verified before the trial

- Default boot verified: signed default image (not trial), CPUs 0-9 with three ondemand policies, Secure Boot, ath12k D044C56077CC5357DC3F5BF / ov02c10 08EF7452B0F555AA15FA25F (fast_video=Y), camera 720p 37.46 fps over 90 frames, Wi-Fi-bound HTTPS 200 (kernel log later read as root: no beacon loss; regulatory/L2/APM warnings listed in drivers/files/sleep/diagnostics/2026-11-12-192713), Open Bar 49 ACTIVE, dock click-action=previews. The IPASoft sensor-helper warning is expected (helper patch rolled back after flicker).
- Deep cycle 19:27 succeeded: kernel resume 4.76 s (spi_hid fixed 2 s wait 2.455 s, empty PCIe 1bd0000 1.07 s), Wi-Fi reconnect ~2.1 s, no audio errors. See drivers/files/sleep/diagnostics/2026-11-12-192713/README.md.
- Terminal tofu for U+23F5 fixed with the Debian fonts-symbola fallback (user font live; bundled for setup).

- Verified one-shot boot: CPUs 0-9 online, three ondemand policies, Secure Boot enabled, camera 37.5 fps / 90 frames / zero errors, Wi-Fi HTTPS 200, Open Bar ACTIVE.
- User approved promotion. CPU topology and preserved-metadata camera driver are now standard boot and offline installer inputs. Normal signed image/initramfs rebuilt; prior working image remains as fallback. Next reboot verifies the promoted default path.
- Neutral isolated camera color improved; noise/1080p/system color integration remain deferred. No CPU cap or panel refresh reduction was added.
- Latest promotion/report changes are local only. Obtain explicit final approval before any further GitHub push. Both repositories remain private.
- Read NEXT.md for remaining checks.
