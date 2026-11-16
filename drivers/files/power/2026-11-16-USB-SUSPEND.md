# USB tethering and deep-sleep follow-up — 2026-11-16

## USB: unresolved, work stopped at user request

- Before the 13:00 reboot, USB-A (`usb 1-2`) failed `SET_CONFIGURATION` twice at 12:57 with error `-110` (timeout). The phone later enumerated on both USB-C controllers. This is an actual communication error, not merely a missing NetworkManager profile.
- In the new boot, all three xHCI controllers registered. Samsung `04e8:6860` initially exposed one configuration with imaging/MTP and CDC-ACM interfaces only. No RNDIS/NCM network interface was advertised.
- `rndis_host`, `cdc_ncm`, `cdc_ether` and `usbnet` are installed with the local Secure Boot signature. Loading the first two succeeded at 13:06:39. No USB network interface appeared afterward.
- The user reported that USB tethering immediately disables itself. During the 13:06:37–13:08:38 sysfs transition capture and matching kernel journal, the retry produced no USB reconnection or descriptor change. This points to a failure before an Ethernet interface reaches Linux; it does not identify phone firmware, cable, or host negotiation as the unique cause.
- After moving to the other USB-C port, the user reported no charging. Linux enumerated `usb 5-1` at 13:11:09, then disconnected it at 13:11:10. USB-C still reported a partner and host/source roles, but there was no data device. Reported roles do not prove that power physically reaches the phone.
- Holding that port's USB2/USB3 root hubs (`usb5`, `usb6`) awake for 45 seconds did not restore enumeration. Both `power/control` values were restored to `auto` and read back. No PHY hot-unbind, role forcing or reboot was performed. Later recovery attempts are listed below.
- The user then confirmed this same cable and phone work on another PC. This shifts the investigation toward Surface host/port negotiation; it does not distinguish Linux, firmware, hardware or device-specific interoperability.
- With no USB data device or external display attached, re-registered only `xhci-hcd.3.auto` (the affected USB-C controller). The driver rebound and both root hubs returned, but no phone appeared.
- Then re-registered only the `pmic_glink.ucsi.0` auxiliary child with `ucsi_glink.pmic_glink_ucsi`. The driver and both Type-C ports returned; the affected connector still reported host/source and a partner without a USB data device. PMIC parent, PHY modules, Wi-Fi and audio were not reset.
- User reconnect/tethering verification after these operations is pending. If still failing, the next manufacturer-supported step is disconnect USB-C accessories, shut down normally, wait 10 seconds, then hold the power button about 20 seconds until the Surface logo reappears and reconnect. This physical reset has not been performed by the agent. [Microsoft USB-C recovery procedure](https://support.microsoft.com/en-us/surface/accessories/surface-dock/troubleshoot-problems-with-usb-c-on-surface).

Latest correction: the user confirms charging works. After reconnect at 13:24:04, Linux again enumerated Samsung MTP/ACM on `usb 5-1`, so this is no longer complete loss of USB device recognition. USB networking is still absent; ModemManager is inactive. The user declined phone debugging and explicitly requested battery-only work. Do not continue USB recovery or request phone access. The physical power-reset suggestion above is superseded as the immediate next step.

The existing `dwc3-qcom` replacement is the missing-HCD NULL guard (srcversion `8554A2970EC29806E65733C`). It changes suspend error handling; it is not a tethering-function patch. The driver filename and loaded srcversion match.

## Battery: sustained overnight drain confirmed

| Period (KST) | Duration | Charge | Estimated energy | Mean |
| --- | --- | --- | --- | --- |
| Nov 15 16:13 → Nov 16 08:40 | 16h 27m | 43 → 15% | 14.41 Wh | 0.88 W / 1.70 pp per hour |

The journal shows deep entry and exit without another kernel PM cycle between them. The pre-sleep charge sample is 213 seconds old and the gauge changes in approximately 1 pp steps. This is an estimate, not a power-meter measurement. Morning intervals involving charging are excluded. Yesterday's four intervals averaged about 0.77 W; different boundaries and conditions prevent assigning the difference to a regression.

USB phone connections first appear at 12:57, after the overnight period. Charging the attached phone cannot explain the overnight loss. This does not exclude the USB PHY/controller's own leakage while disconnected.

Current-boot Qualcomm AOSS/CX/DDR/APSS counts are zero, but this boot has not suspended yet. These zeros are not evidence that the previous night's deep sleep failed. Some firmware counters are empty/unimplemented; preserve that distinction.

## USB PHY candidate, not yet applied

The matching 7.3.0-31.31 source exposes only runtime PM callbacks in `qmp_combo_pm_ops` and calls `pm_runtime_forbid()` at probe. Qualcomm's proposed system-sleep callbacks address clocks left running during suspend; reviewers also discuss historically broken runtime PM and missing locking. No proven Surface-specific result or accepted replacement was established here. Do not enable blanket runtime PM or hot-reload these PHYs as a speculative fix.

- [Qualcomm patch review](https://lists.openwall.net/linux-kernel/2026/11/02/735)
- [Earlier Surface power-management issue](https://github.com/bryce-hoehn/linux-surface-laptop-7/issues/7): different old-kernel symptoms; its closed state does not prove this drain is fixed.
- [Samsung USB connection guidance](https://www.samsung.com/us/support/answer/ANS10002546/)
- Matching source archive already retained locally: `archive/hardware/source/linux-qcom-x1e_7.3.0-31.31.tar.gz`. Reviewed `drivers/phy/qualcomm/phy-qcom-qmp-combo.c`, `drivers/soc/qcom/qcom_stats.c`, and `drivers/usb/dwc3/dwc3-qcom.c`; no source patch applied today.

## Automatic measurements installed

Two files are included in the existing drivers `rootfs` restore, so both top-level and drivers SH/Python setup entry points reproduce them:

- `usr/local/libexec/surface-power-snapshot.py`: reads battery energy/status, USB presence/runtime state, suspend counts, and selected Qualcomm sleep counters. No battery/phone serial, account data or traffic is recorded.
- `usr/lib/systemd/system-sleep/95-surface-power-snapshot`: invokes the collector once before and once after sleep, with a 2-second timeout and a 1-second kill grace. It fails open and does not change power policy or initiate sleep.

Records: `/var/lib/surface-power/suspend.jsonl`; a previous file is retained after 2 MiB rotation. No resident daemon or periodic polling. Qualcomm durations remain raw architecture-counter ticks, not seconds. The manual root sample succeeded in about 22 ms and read AOSS/CX/DDR/APSS/ADSP counters. Actual sleep-boundary execution and before/after differences await the next normal suspend.

Read-only manual check:

```sh
sudo python3 -I /usr/local/libexec/surface-power-snapshot.py manual --stdout
```

Rollback: remove only the two installed files above. Existing measurements may be retained. No systemd enable operation or kernel/initramfs update is needed.

All workspace files are console-owned. No new commit or push was made for this follow-up.
