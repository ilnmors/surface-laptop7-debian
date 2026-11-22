# External contributions

Issues, pull requests and comments posted in other projects from the work in this bundle.
Rules for new posts are in AGENT.md ("External contributions"). Open promises are tracked in
[NEXT.md](../NEXT.md) ("External commitments") until the result is posted; this file is the record.

| Date (UTC) | Where | Kind | Subject | State |
| --- | --- | --- | --- | --- |
| 2026-11-20 | [bryce-hoehn/linux-surface-laptop-7 #28](https://github.com/bryce-hoehn/linux-surface-laptop-7/pull/28) | PR | README: the 13.8-inch (romulus13) GTCH SPI touchscreen works | Merged 2026-11-21 |
| 2026-11-20 | [qBitnaut/omarchy-dragon-sl7 #39](https://github.com/qBitnaut/omarchy-dragon-sl7/issues/39) | Issue | Deep suspend aborts from an `ss_phy_irq` storm when the USB PHYs power-collapse: dwc3-qcom fix | Open, no reply yet |
| 2026-11-20 | [omacom/omarchy #18970](https://github.com/omacom/omarchy/issues/18970#issuecomment-7041712388) | Comment | 13.8-inch data point for "wakes from suspend by itself": the SuperSpeed PHY wake line | Issue open |

## bryce-hoehn/linux-surface-laptop-7 #28

- Added a README row for the 13.8-inch touchscreen (GTCH over SPI/QSPI, same CouchLiteOS description as the 15-inch overlay in #24).
- Review (OliW07): does the unchanged ELLX `alex-lentz/iptsd` package work, and please mention the iptsd dependency.
  Answered 2026-11-20: iptsd dependency added to the row; touchscreen tested with the locally patched daemon,
  an unpatched build of the same source and the unchanged ELLX package (`iptsd_3.1.0-1_arm64.deb`; its binary exits
  with SIGILL on stop under Debian 13).
- Merged 2026-11-21 22:00 UTC. Promise closed. The fork `ilnmors/linux-surface-laptop-7` was deleted 2026-11-22 (no unmerged work).

## qBitnaut/omarchy-dragon-sl7 #39

- Shares the `ss_phy_irq` storm finding (82,847 / 26,542 interrupts per suspend with nothing attached on a
  `fw_devlink.sync_state=timeout` boot; receiver detection `ARCVR_DTCT_EN` keeps the SuperSpeed wake line asserted)
  and the fix in [patches/files/dwc3-ss-wake](../patches/files/dwc3-ss-wake/).
- Promise: test their patch 0124 (geni UART keeps the engine clocked in suspend) on 7.3 against the SSAM -110 after
  back-to-back suspends, and report back. Needs a module build and an approved reboot.

## omacom/omarchy #18970

- Same finding as #39, written as a data point for the 15-inch self-wake report.
- Promise: if the D+ (`dp_hs_phy`) wake or the lid-line wake reproduces on the 13.8-inch model, add the numbers.
