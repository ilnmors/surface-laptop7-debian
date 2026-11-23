# USB tethering failure and recovery — 2026-11-16

Phone: Samsung Galaxy S25 (SM-S931N), Android 17, build CP2A.260605.016 (build date 2026-10-19, patch 2026-10-05). USB tethering function: RNDIS. Times are Surface KST; the phone clock ran about 1.5 s behind.

## Result

Resolved at 14:29. After a phone restart, enabling USB tethering switched the phone to `04e8:6864` (RNDIS+ADB), `rndis_host` bound, NetworkManager activated `Wired connection 1` with a DHCP lease and set it as the default route. After USB debugging was disabled the phone re-enumerated as `04e8:6863` (RNDIS only) and tethering stayed up.

## Root cause

The phone rejected every USB tethering request on its own side:

```
TetheringRequestTracker: Cannot add pending request due to existing fuzzy-matched request: TetheringRequest[ TETHERING_USB ... ]
UsbDetailsCtrlFunction: onTetheringFailed() error : 18      (TETHER_ERROR_DUPLICATE_REQUEST)
UsbDeviceManager: setCurrentFunctions(sec_charging)
```

A USB tethering request from an earlier, interrupted attempt was still pending in the phone's Tethering service (it predates the oldest retained log line, 13:28). Every new toggle was treated as a duplicate and turned off immediately, and the phone never switched its USB function, so the Surface saw no re-enumeration. `cmd tethering` has no shell implementation and the service cannot be restarted without root; a normal phone restart cleared it.

## Contributing Surface-side fault (unresolved)

The interrupted attempts are linked to a Surface USB2 fault on the USB-C ports:

- When the phone's USB data drops abruptly (function switch, or Samsung's `block_usb_lock=1` "block USB while locked" feature cutting data when the screen locks), the next attach on that port can come up as full-speed with `device descriptor read/64, error -71`, `device not accepting address`, `unable to enumerate USB device` and repeated `attempt power cycle` (seen as charging toggling on/off), or not be detected at all (`usbN-port1 state=not attached` while Type-C reports a partner).
- The port then stays dead, including after re-plugging, until the PHY is re-initialised. Re-registering only `xhci-hcd.N.auto` (earlier session) did not help; rebinding the dwc3-qcom glue does.
- USB2 path: dwc3 (`a600000.usb` = Type-C port0/bus 3, `a800000.usb` = port1/bus 5) → `qcom,x1e80100-snps-eusb2-phy` → PMIC `qcom,smb2360-eusb2-repeater` (no tuning properties in the DTB).

Recovery used today (root; affects only that controller's port):

```sh
echo a800000.usb > /sys/bus/platform/drivers/dwc3-qcom/unbind
echo a800000.usb > /sys/bus/platform/drivers/dwc3-qcom/bind     # a600000.usb for the other port
```

After rebinding `a800000.usb` the attached phone enumerated at high speed without re-plugging.

## Ruled out

| Hypothesis | Evidence |
| --- | --- |
| `cma=0` | The last good boot (11/13 trial-touch, `cma=512M`) failed to reserve CMA and also ran with CmaTotal=0. |
| DTB change | Current embedded DTB and the 11/13 trial DTB are identical (sha256 `ab97dca3…`). |
| dwc3-qcom replacement | Unchanged since 11/11 (srcversion `8554A2970EC29806E65733C`); the 11/12 successes used it. |
| Device autosuspend | Phone device `power/control=on`, runtime active. |
| Root-hub autosuspend (`autosuspend_delay_ms=0`) | Failed with all root hubs forced `on` after a clean controller re-init. Restored to `auto`. |
| GNOME MTP mount | Unmounted for the tests; no change. |

Journal history: tethering worked on 11/12 (boots -13, -12) and 11/13 10:29/11:50 (boot -6); the first recorded failure is 11/16 12:57.

## Changes made

- Phone: developer options, wireless debugging and USB debugging disabled again after the investigation (`development_settings_enabled=0`, `adb_wifi_enabled=0`, `adb_enabled=0`). `block_usb_lock` was left unchanged at the user's choice.
- Surface: `adb` (Debian 1:34.0.5-12) installed for the investigation. Root hubs back on `auto`; the temporary restore timer was stopped. Both USB-C controllers were rebound once during testing.
- No kernel, DTB, module or boot change was made for this issue.

## If it recurs

1. Unlock the phone before plugging in and before enabling USB tethering.
2. If the toggle turns off instantly, restart the phone (stale pending request).
3. If the Surface shows charging only / no USB device, rebind the dwc3-qcom controller for that port (above) or reboot.

Open item: make the Surface USB2 path survive abrupt data loss (repeater/PHY handling or an automatic re-init), instead of relying on manual rebinding.

## WireGuard MTU over tethering (added 15:20)

With the default route on USB tethering, the homelab tunnel `wg0` (default MTU 1420) passed ping but stalled SSH and HTTPS: larger packets were black-holed. Measured inside the tunnel with DF set: inner IPv4 packets up to 1360 bytes pass (10/10), 1370 fails (0/5); IPv6 results were inconsistent above 1360. 1360 is therefore the largest working value on this path and is also fine on Wi-Fi.

- System: NetworkManager connection `home-vpn` now has `wireguard.mtu=1360`; verified after `nmcli connection up home-vpn` (link MTU 1360, Forgejo HTTPS 200, SSH transfer OK).
- Bundle: `drivers/files/rootfs/etc/NetworkManager/dispatcher.d/90-surface-wg-mtu` sets MTU 1360 when `wg0` comes up, so a recreated connection gets the same value without storing WireGuard keys in Git.
- Rollback: `nmcli connection modify home-vpn wireguard.mtu 0` (default 1420) and remove the dispatcher file.
