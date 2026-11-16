# USB PHY system-sleep trial — 2026-11-16

Goal: reduce Linux `deep` sleep drain (0.77–0.88 W measured 11/15–16) by gating Qualcomm QMP USB PHY clocks during system suspend.

## Change

- `patches/01-qmp-combo-system-sleep.patch`, `patches/02-qmp-usb-system-sleep.patch`: Qualcomm v1 proposal (not merged), applied without fuzz to the matching 7.3.0-31.31 source.
- Why it can matter here: both drivers call `pm_runtime_forbid()` at probe, so their runtime-suspend path never runs and, without system-sleep callbacks, PHY clocks stay enabled across suspend. The patch calls the existing runtime suspend/resume (autonomous mode + clock gating) from system sleep when the device is runtime-active.
- Review notes: system suspend runs after the dwc3 consumers suspend; the callbacks do not take the PHY mutex (upstream reviewers raised locking). Treat this as a trial, not a verified fix.

## State

- Built and signed by the earlier session (`build.py`, `verify.py`, `verification.json`): QEMU guest with `module.sig_enforce=1` accepted signed and rejected unsigned modules; offline rebuild matched srcversions.
- Installed 2026-11-16 13:53 KST with `setup.py` (pkexec): modules in `/lib/modules/7.3.0-31-qcom-x1e/updates/surface/`, initramfs and signed image refreshed, `sbverify` OK. Backups and manifest under `/var/lib/surface-power/phy-sleep-20261116/backup/`.
- Next boot loads `41E45FA66B29B5A2C416CBE` (combo) and `601E8F5D83837191C8575E9` (usb). The boot that installed them still runs `63A1B2708C9E05A81BA565D` / `8ABB3B604DFD01F79E2AD77`.

## Validation after reboot

1. `cat /sys/module/phy_qcom_qmp_{combo,usb}/srcversion` shows the new values; USB-A/USB-C devices, charging and external display still work.
2. Let the machine sleep naturally on battery for 2 h or more (matched brightness/120Hz/apps). Compare pre/post energy and Qualcomm counters in `/var/lib/surface-power/suspend.jsonl`.
3. Check the journal for PHY/dwc3 errors around suspend/resume and that USB devices work after resume.

## Rollback

- Boot menu (hold Esc/Shift during the 1-second hidden menu): `Surface before PHY sleep patch (2026-11-16)` boots the exact previous signed image and initramfs.
- Permanent: `python3 -I patches/files/phy-sleep/setup.py --restore` (pkexec) restores modules, initramfs hook, image and GRUB config from the checksummed backup, then reboot.
