# Current Surface configuration

- Debian 13 ARM64, GNOME 48, kernel 7.3.0-31-qcom-x1e. Console UID 3000, primary group svadmins GID 2000.
- Secure Boot repair: the local public certificate is inserted into the existing kernel's reserved builtin certificate slot, then the inner kernel and Surface wrapper are signed. Original instructions and existing CA certificates are preserved. The update hooks repeat this automatically.
- Verification passed: Linux reference insertion tool comparison, inner/outer image signatures, and an isolated ARM64 boot with module signature enforcement. The unsigned module was rejected; the existing locally signed module loaded. Physical Surface boot verified on 2026-11-11: SecureBoot enabled, kernel lockdown integrity mode, and the local builtin certificate loaded. The MOK certificate is enrolled and trust permission is enabled.
- Bluetooth uses the persistent unique local-address recovery helper. Existing touchpad calibration remains installed.
- Touchscreen: overlay is active, but client 10-0034 does not answer HID probing. Touch input remains unresolved.
- Audio uses the physical speaker output directly, with no Windows EQ virtual sink. User confirmed continuous audible playback after this change. Earlier SoundWire/parity errors remain diagnostic evidence; this is not proof the underlying driver faults cannot recur.
- Fluent Light has a rounded translucent top bar. Vitals 86 shows CPU/memory every five seconds; Caffeine 61 is manual/off by default; AppIndicator 66 provides tray icons. All are active.
- Plymouth shows a Debian logo and spinner with quiet boot settings.
- Sleep remains deep. EFI pstore confirms a suspend-entry NULL dereference in dwc3_qcom_suspend after an xHCI probe timeout. Power-button/GPIO-key wakeup is enabled. The matching USB NULL-guard patch and five Qualcomm SoundWire fixes are installed for the next boot. Successful physical suspend/resume and audio reliability remain unverified. See drivers/files/sleep/diagnostics/2026-11-11/. The earlier user-session-freeze trial remains installed and is not a fix for this USB fault.
- kernel/, drivers/, patches/, desktop/ and programs/ contain categorized offline payloads and component installers. Site-specific CA, VPN and server access material is excluded. No signing private key is included.

- New modules: patches/files/ contains matching sources, upstream messages, backports, headers, unsigned reusable modules and build/install helpers. Local installed copies are signed. ARM64 signature-enforcement VM accepted both replacement drivers; physical devices still use old loaded modules until reboot.
- CPU: scmi-cpufreq was not loaded; it is now loaded and persisted. Policy0 exists; remaining cluster policies and the CPU9 PSCI failure remain unresolved.
- Android: Waydroid 1.6.3, Vanilla ARM64 images, Binder, hardware freedreno/Adreno X1-85 rendering and multiwindow apps verified. Individual app launchers are installed. No Google Play or x86 translation. Session starts on demand.
- Scrolling is unchanged by user decision. Samsung integration is not installed.
- setup.py and setup.sh orchestrate the same component shell implementations. PORTABILITY.md separates board-specific and portable Debian settings.

## 2026-11-12 continuation

- Modular SH/Python entry points and payload directories are in place. No live full reinstallation was run during the refactor. Account migration/Console services remain in repository scope.
- Current boot still uses original loaded USB/SoundWire modules; replacement modules are present in initramfs and signed boot images. Five deep cycles succeeded, but callback delay remains under investigation. An isolated power-only trace captured the next user-initiated cycle and was saved.
- Steam SDK path repair is confirmed by SteamAPI initialization. FEX Korean fonts were added; visual confirmation and RimWorld-only touchpad click investigation are paused at the user's request.
- KakaoTalk: the initial APKPure ARMv7 candidate was rejected; an official-signer-verified ARM64 bundle was subsequently acquired and installed.

- Touchpad: the live 30-second edge test confirmed 26 libinput geometric palm exclusions and one jump warning. libinput10 1.28.1-1+deb13u1+surface1 now disables only edge exclusion for the exact virtual 045E:0C77 device; ABI/linkage and matching diagnostic context passed. GNOME needs logout/login; human improvement is pending.
- HTML is now tracked in Git, superseding the earlier untracked-report instruction. STATUS.json and tools/report.py regenerate it.

## Latest verified results

- KakaoTalk 26.9.2 ARM64 official-signer verification and split install passed. Tablet property is active; Secondary Device was selected and the empty email/password/QR login screen verified. No credentials entered.
- Waydroid storage now mounts after removing an orphan OMX HAL declaration whose service was absent. Only the vendor overlay changes; original images remain intact. Future vendor updates require overlay review.
- Five deep cycles succeeded. Recorded resume callback phases total ~4.77s: SPI-HID ~2.417s, PCIe noirq ~1.697s and Wi-Fi early ~0.522s dominate. This is not full screen-visible latency.
- Latest ~5.296h sleep lost ~6 percentage points (~3.046Wh, 0.575W). Awake sampled average ~7.64W. See drivers/files/power/ for calculation/Windows comparison limits.
- apt-get check and upgrade simulation pass; updates remain enabled. No actual apt upgrade was run.
