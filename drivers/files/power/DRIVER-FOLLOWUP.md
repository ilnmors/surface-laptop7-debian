# Remaining driver follow-up, 2026-11-12

- Nextcloud HTTPS remains unreachable; approved infra SSH timed out before authentication. This is outside the Surface driver installer.
- Current suspend success/failure counters remain 0/0. A manual cycle with the replacement USB/SoundWire modules has not yet occurred. Do not force suspend during user work; the power trace remains armed.
- No failed system services were reported. CPU limits/topology remain unchanged by request.
- PCIe broken-L1SS-resume mitigation is already present in the matching kernel source (`pp->bridge->broken_l1ss_resume = true`); do not reapply that patch as a new fix.
- Romulus13 touchscreen v2 enablement is already present but this unit still has no bound driver at 8-0034. Upstream v2 deliberately removed reset GPIO31 and uses interrupt GPIO38 pull-up. Reapplying v2 does not address the observed address NACK; no guessed reset wiring was applied.
- A newer qmp-combo PHY system-sleep clock-gating proposal may reduce suspend leakage, but the review still discusses broken historical runtime PM and locking. The matching source currently has runtime callbacks and pm_runtime_forbid, without the new system-sleep callbacks. This is a candidate requiring exact module/board validation, not a proven fix for this Surface. No experimental PHY replacement was installed in this pass.

References:
- https://lists.openwall.net/linux-kernel/2026/09/30/627 (touchscreen v2 rationale)
- https://lists.openwall.net/linux-kernel/2026/11/02/735 (qmp-combo review)
- matching local source drivers/pci/controller/dwc/pcie-qcom.c and drivers/phy/qualcomm/phy-qcom-qmp-combo.c
