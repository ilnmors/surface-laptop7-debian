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

## Urgent display recovery after the next reboot

The early GPU hook included gen70500 SQE/GMU but omitted the Microsoft qcdxkmsuc8380.mbn zap shader. The new boot logged zap_shader_load_mdt ENOENT, GPU hardware init failure and GMU OOB timeouts. Root firmware existed but was absent from initramfs. The earlier partial inclusion was insufficient.

Fixed the installed/bundled hook to include both actual Microsoft shader paths, rebuilt initramfs and refreshed the signed kernel. Verified all four firmware entries and kernel signature. Kept 120Hz and original scale; performed temporary scale modeset and panel DPMS cycle. Disabled Night Light and Blur My Shell for recovery. Stopped Waydroid/container and temporarily disabled Kakao autostart (backup beside its desktop file). No session logout/reboot forced because unsaved work may exist. Visual recovery is not confirmed; a clean reboot is needed to verify GPU initialization. Do not restart Android automatically before that verification.
