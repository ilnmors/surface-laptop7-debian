# Deep-suspend crash, 2026-11-11

## Confirmed cause

Previous boot, kernel 7.3.0-31-qcom-x1e, Secure Boot disabled:
1. At boot xhci-hcd.1.auto under a400000.usb failed setup with -110 (timeout), leaving the host platform device present without driver data.
2. At 21:12:35 deep suspend began. Filesystem sync and task freezing completed; the persistent journal stopped before later kernel messages were flushed.
3. At uptime 5702.007565 the CPU hit a NULL dereference at address 0x58 in dwc3_qcom_suspend.part.0+0x1d0/0x380. This occurred during device suspend, before successful entry into deep sleep.
4. Disassembly of the installed dwc3-qcom.ko confirms that this offset reads hcd->self.root_hub after platform_get_drvdata(dwc->xhci) returned NULL. The source has no hcd check in dwc3_qcom_read_usb2_speed().

The power button is not the cause established by these logs: both PMIC power-button and GPIO-key wakeup are enabled. A failed suspend callback prevents normal completion of the sleep/wake cycle. Both deep and s2idle use device suspend, so switching sleep modes alone is not a demonstrated fix.

Current boot: Secure Boot enabled; all three xHCI host devices are bound, including a400000.usb. No sleep was forced. Successful resume remains untested and the missing NULL guard remains in the installed driver.

## Matching upstream work

[PATCH RESEND v3] usb: dwc3: qcom: check for hcd in dwc3_qcom_read_usb2_speed, 2026-11-06:
https://lists.openwall.net/linux-kernel/2026/11/06/466

The proposed change initializes udev to NULL and only calls usb_hub_find_child when hcd is non-NULL. It matches the observed fault. This report does not claim the patch is installed. The initial xHCI timeout also deserves investigation; preventing this Oops does not itself repair a failed USB port.

## Evidence

The three text files alongside this report are EFI pstore records recovered by systemd under /var/lib/systemd/pstore, not ordinary journal excerpts. /sys/fs/pstore was empty because the records had already been archived. Other archived fragments are continuations of the same module list. Audio parity errors and a Wi-Fi regulatory timeout precede the crash but the faulting instruction is in the USB driver.
