# Continue investigation

When the user says "계속", read CURRENT.md and this file, inspect the current boot, then continue unfinished investigation. Do not repeat completed installations. Keep documentation, installer inputs, checksums and Git commits synchronized. Do not copy infrastructure credentials into this bundle.

## Pending hardware verification

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
- hardware-report.html is an untracked local report and must not be staged.
- Kopia Console changes belong to repository only; do not deploy them on the current Surface.

## Infrastructure follow-up (outside this bundle)

Console Caddy/code-server roles were applied successfully. The old operational SSH certificate was renewed with the old CA for one year, preserving key and principals. Both old and renewed certificates were rejected in the VMM login test; investigate server trust/principals when authorized. Never replace the operational certificate with the new repository CA before server redeployment.
