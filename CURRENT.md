# Current Surface configuration

- Debian 13 ARM64, GNOME 48, kernel 7.3.0-31-qcom-x1e. Console UID 3000, primary group svadmins GID 2000.
- Secure Boot repair: the local public certificate is inserted into the existing kernel's reserved builtin certificate slot, then the inner kernel and Surface wrapper are signed. Original instructions and existing CA certificates are preserved. The update hooks repeat this automatically.
- Verification passed: Linux reference insertion tool comparison, inner/outer image signatures, and an isolated ARM64 boot with module signature enforcement. The unsigned module was rejected; the existing locally signed module loaded. Physical Surface boot verified on 2026-11-11: SecureBoot enabled, kernel lockdown integrity mode, and the local builtin certificate loaded. The MOK certificate is enrolled and trust permission is enabled.
- Bluetooth uses the persistent unique local-address recovery helper. Existing touchpad calibration remains installed.
- Touchscreen: overlay is active, but client 10-0034 does not answer HID probing. Touch input remains unresolved.
- Audio uses the physical speaker output directly, with no Windows EQ virtual sink. User confirmed continuous audible playback after this change. Earlier SoundWire/parity errors remain diagnostic evidence; this is not proof the underlying driver faults cannot recur.
- Fluent Light has a rounded translucent top bar. Vitals 86 shows CPU/memory every five seconds; Caffeine 61 is manual/off by default; AppIndicator 66 provides tray icons. All are active.
- Plymouth shows a Debian logo and spinner with quiet boot settings.
- Sleep remains deep. EFI pstore confirms a suspend-entry NULL dereference in dwc3_qcom_suspend after an xHCI probe timeout. Power-button/GPIO-key wakeup is enabled. The matching USB NULL-guard patch and five Qualcomm SoundWire fixes are installed for the next boot. Successful physical suspend/resume and audio reliability remain unverified. See files/sleep/diagnostics/2026-11-11/. The earlier user-session-freeze trial remains installed and is not a fix for this USB fault.
- files/ contains offline hardware, shell, theme and verification files. Site-specific CA, VPN and server access material is excluded. No signing private key is included.

- New modules: files/kernel-patches/ contains matching sources, upstream messages, backports, headers, unsigned reusable modules and build/install helpers. Local installed copies are signed. ARM64 signature-enforcement VM accepted both replacement drivers; physical devices still use old loaded modules until reboot.
- CPU: scmi-cpufreq was not loaded; it is now loaded and persisted. Policy0 exists; remaining cluster policies and the CPU9 PSCI failure remain unresolved.
- Android: Waydroid 1.6.3, Vanilla ARM64 images, Binder, hardware freedreno/Adreno X1-85 rendering and multiwindow apps verified. Individual app launchers are installed. No Google Play or x86 translation. Session starts on demand.
- Scrolling is unchanged by user decision. Samsung integration is not installed.
- setup.py and setup.sh use one offline installation path. PORTABILITY.md separates board-specific and portable Debian settings.
