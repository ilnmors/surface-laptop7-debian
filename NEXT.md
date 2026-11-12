# Continue investigation

When the user says "계속", read CURRENT.md and this file, inspect the current boot, then continue unfinished investigation. Do not repeat completed installations. Keep documentation, installer inputs, checksums and Git commits synchronized. Do not copy infrastructure credentials into this bundle.

## Pending hardware verification

0. After GNOME logout/login, repeat the edge test for the newly installed libinput geometric-palm exception. Retain diagnosis logs and compare against 26 edge exclusions / one jump warning; do not claim upstream contact fragmentation fixed.

1. After a user-controlled reboot, confirm Secure Boot enabled and the new dwc3_qcom / soundwire_qcom modules loaded from updates/surface. Test one user-initiated deep sleep/wake cycle and sustained/interrupted speaker playback. Do not force suspend during active work.
2. If audio fails, capture timestamped SoundWire/WSA884x errors before changing routes. The five installed SoundWire patches improve error/IRQ handling but are not proven to fix parity faults.
3. CPU: current online CPUs 0-8; CPU9 failed PSCI with -22. scmi-cpufreq now loads and provides policy0 only. Investigate X1P64100 SCMI sustained-frequency/turbo classification and the CPU DT topology without inventing firmware values. SCMI perf is builtin, so its source patch needs a proper matched kernel build.
4. Touchscreen: Romulus13 I2C 0x34 does not acknowledge; v2 GPIO38 overlay is active. Compare v1 reset GPIO31 evidence and exact hardware variant before further GPIO/power changes. Do not substitute 15-inch QSPI wiring.
5. Review the Romulus USB PHY reinit-on-resume series separately from the fixed NULL crash; missing initial xHCI probe must not be conflated with PHY state loss after resume.
6. Touchpad QSPI v3 RFC has controller/board prerequisites; compare it to existing downstream GPI/GENI/SPI-HID before replacing working input.
7. Camera quality, battery/runtime and Bluetooth startup remain separate checks; retain previous rejected camera/overshoot trials as history rather than reapplying them.

## User decisions

- Scroll injection was declined; do not install it.
- Samsung integration is deferred; describe capabilities only.
- Android apps should appear individually in GNOME, not as a full Android desktop.
- hardware-report.html is now tracked by the latest user instruction.
- Kopia Console changes belong to repository only; do not deploy them on the current Surface.

## Infrastructure follow-up (outside this bundle)

Console Caddy/code-server roles were applied successfully. The old operational SSH certificate was renewed with the old CA for one year, preserving key and principals. Both old and renewed certificates were rejected in the VMM login test; investigate server trust/principals when authorized. Never replace the operational certificate with the new repository CA before server redeployment.

## Installation and program follow-up

- Modular setup is implemented. Use --plan before installation and --verify-only to check payloads. Do not run a full live reinstall merely to validate refactoring. Console UID/GID and infrastructure services belong to repository, not this hardware installer.
- Steam runtime/FEX root and games are not fully bundled. Existing Steam helpers are reproducible, not a complete offline Steam installation. Game-only click and Korean rendering verification are paused by user request.
- KakaoTalk ARM64 is installed and official-signer verified. Secondary Device login screen has been verified; account login remains the user’s action. Android core components are retained.
- The next manual deep sleep was captured and saved under drivers/files/sleep/diagnostics/2026-11-12-090205/. SPI-HID ~2.417s and PCIe/Wi-Fi ~2.219s dominate resume. Re-arm only if another comparison is needed. No automatic forced sleep.

## Resume in this same conversation

The user will type "계속" in this session. Read this file and CURRENT.md, check the latest Git commits and current boot, then resume unresolved hardware investigations. At the 5% limit notification, new investigation was stopped; documentation, verification and commits were completed/recorded separately. Kopia was not deployed.
