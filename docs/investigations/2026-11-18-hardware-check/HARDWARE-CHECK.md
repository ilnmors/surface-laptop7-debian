# Hardware check — 2026-11-18

Phase 1 of the goals (every component usable, awake battery, sleep battery). Normal boot 74a7f298 (PHY-only reference, no sync_state). Automatic checks by the agent; physical checks done by the user on request.

## Results

| Component | Result | Evidence |
| --- | --- | --- |
| CPU | OK | 10 cores, 3 policies 710 MHz–3.42 GHz, ondemand (unchanged) |
| Memory / swap | OK | 16 GB, 4 GB /swapfile |
| Thermal sensors | OK | 60+ zones, idle 36–41 °C |
| Fan | Works, late | SAM-controlled. 60 s full load: 85 °C at 0 rpm, fan started (2,861–3,007 rpm) only after the load ended; user heard nothing. CPU stayed at 3.42 GHz |
| NVMe | OK (no SMART tool) | SK hynix 256 GB, 38 °C |
| Display / GPU | OK | eDP 2304x1536 120 Hz, backlight, Adreno X1-85 Mesa 25 GL 4.6, turnip ICD present |
| Video decoder | Missing | DT `video-codec@aa00000` (iris) disabled; firmware present |
| Keyboard | OK | All keys, Fn row (brightness, volume, mute), Caps Lock LED, backlight (user). Unnamed events BTN_MISC 0x100e1 and KEY_UNKNOWN 0xc0515 come from EC-handled keys |
| Touchpad | OK | Motion, physical/tap clicks, drag, two-finger scroll, 3-finger swipe, pinch (user + libinput log) |
| Touchscreen | OK (user) | Surface Laptop 7 has no pen support |
| Lid switch | OK | SW_LID closed/open twice, display back on |
| Speakers / internal mics | OK | 1 kHz speaker→mic loopback; left/right tones correct (user) |
| Headphone jack | Not tested | No headphones |
| Front camera | OK, quality below Windows | OV02C10, 37 fps capture; Snapshot preview fine (user), low-light quality known issue |
| Camera privacy LED | LED works, not linked | `white:camera-indicator` lights when written manually (user saw it); stays 0 while the camera streams, trigger `none`. Sensor node lacks the privacy-led link |
| IR camera (Windows Hello) | Not available | Only one sensor in DT; CCI ac15000 disabled; no IR sensor/emitter support |
| Wi-Fi | OK | Wi-Fi 7 AP ch 36, 270 Mbit/s, 5/6 GHz capable |
| Bluetooth | OK | 27 devices in a scan; left soft-blocked as before |
| Battery / charge limit | OK | 98% of design; 80% end threshold active |
| USB-C port 1 / 2 | OK, slow display | Data, hub, PD source/sink, charging, DP alt mode on both. Monitor: port 1 HPD after 39 s; port 2 HPD 2 s but GNOME re-modeset for 13 s; port 2 SS hub reset once (`set hub depth failed`) |
| Surface Connect charging | OK | ac online, 29.7 W then held at limit; unplug/replug detected twice within 1 s polling |
| USB controller a400000 / USB-A | Intermittent boot failure; port OK | `xhci-hcd.1.auto: can't setup: -110` in this boot and 7eaa4187; USB-A did not react. One diagnostic `dwc3-qcom` unbind/bind (12:32:58) brought up bus 1 (2×USB2) and bus 6 (2×USB3). USB-A = port 2: Samsung FIT stick at 5 Gbps (replug clean), Logitech G102 mouse and CHERRY keyboard full-speed on USB2, both used by the user. A one-time -71 on 1-2 happened only at bind time with the stick already inserted. Port 1 is probably Surface Connect data |
| TPM | Missing | No /dev/tpm* (Pluton) |
| Ambient light sensor | Missing | No IIO light sensor |
| Time sync | Missing service | No NTP client installed; clock not synchronized |
| Secure Boot | OK | enabled |

## Deferred checks

- Surface Connect dock (USB data, Ethernet, display): no dock available. Expect power OK, USB data via a400000 (only when it initializes), display probably unavailable because DP controller `ae9a000` (DP2) is disabled in DT.
- Headphone jack and headset microphone: no headphones.

## Phase 2: awake power survey (2026-11-18, battery, backlight 1581/4095, 120 Hz, idle desktop)

One variable at a time, restored before the next. Average of `power_now` over 150 s after a 30 s settle. Run 1 (12:44) and run 2 (13:19); run 1 was cut by GNOME's 15-minute battery idle suspend at 12:58:57, and its ASPM phase did not apply the policy (script bug), so both are discarded.

| Phase | Avg W | vs. baseline | ADSP LPM entries/s | Speaker PCM |
| --- | --- | --- | --- | --- |
| Baseline (run 1) | 4.20 | – | 0 | open |
| Waydroid + KakaoTalk stopped | 4.17 | −0.02 | 0 | open |
| Speaker PCM suspended | 3.62 | **−0.58** | 102 | suspended |
| Baseline (run 2) | 4.31 | – | 0 | open |
| GNOME extensions off (7) | 3.97 | **≈ −0.27** | 0 | open |
| PCIe ASPM powersupersave | 4.17 | ≈ 0 | 0 | open |
| Baseline end (run 2) | 4.17 | – | 0 | open |

- Baseline drift within a run ±0.07 W; between runs 4.17–4.31 W.
- The always-open speaker PCM (`51-surface-speaker-no-idle.conf`, the 2026-11-15 speaker failure workaround) keeps the ADSP out of its low-power state entirely (0 entries/s); closing it lets the ADSP idle (~102/s, the rate Codex had seen) and saves about 14%.
- Waydroid idle cost is negligible. ASPM is already L1.2 on both links; `powersupersave` changes nothing.
- Not measured: Wi-Fi power save (`iw` not installed), per-extension breakdown, video decoder.

### Run 3 (13:36–14:07): per-extension and video

| Phase | Avg W |
| --- | --- |
| Baseline / mid / end | 4.39 / 4.45 / 4.71 |
| Vitals off | 4.44 |
| caffeine off | 4.46 |
| appindicatorsupport off | 4.39 |
| openbar off | 4.34 |
| surface-notifications off | 4.37 |
| dash-to-dock off | 4.55 |
| user-theme off | 4.58 |
| 1080p30 VP9 6 Mbit/s, software decode (gst playbin, waylandsink) | **8.88** (CPU 11% of 10 cores; decoder ~1.6 cores) |

- No single extension is outside the baseline drift (4.39 → 4.71 W during this run). The −0.27 W of "all extensions off" in run 2 is not attributable to one extension and may be drift.
- Video playback roughly doubles awake power (+4.3 W) without the hardware decoder (`iris` disabled in DT).

## Investigation D (2026-11-18)

### a400000 boot failure

- Good boots (17f25aba, 8e4ebc98, 128f390f, 67d21b94): `xhci-hcd.1.auto` starts about 7 s on the kernel clock, no "deferred probe pending" messages.
- Failing boots (74a7f298, 1a9b4911, 7eaa4187): the kernel clock already reads 19–25 s at "Booting Linux" (12–18 s more spent before Linux, firmware/GRUB stage); `xhci-hcd.1.auto` starts at the same instant the deferred-probe timeout prints its pending list (LPASS pinctrl/codec chain), while `phy_qcom_eusb2_repeater` is just being loaded, and fails 12–14 ms later with `-110`.
- Hypothesis: when the deferred-probe timeout fires during module loading, fw_devlink stops waiting for optional suppliers and the multiport controller is set up before its eUSB2 repeater/PHY chain is ready. `phy-qcom-eusb2-repeater`, `phy-snps-eusb2` and `xhci-plat-hcd` are in the initramfs only as stock modules; the bundle's own `dwc3-qcom`/`phy-qcom-qmp-*` copies are present.
- Not yet explained: why some boots spend 12–18 s longer before Linux (all three failing boots; cold power-on and warm reboot both appear).
- Candidate fixes to evaluate later (one at a time): load order/softdep so the repeater binds before dwc3-qcom; `deferred_probe_timeout=` raised; then re-check a400000 on several cold and warm boots.
- During today's two deep sleeps a400000 also logged `port-1/port-2 HS-PHY not in L2` (same message as the USB-C failure on 11/17).

### Camera privacy LED

LED hardware works when written manually; the OV02C10 DT node has no `leds`/`led-names = "privacy-led"` link, so V4L2 never drives it.

### Not analysed yet

USB-C monitor hot-plug delay; Wi-Fi power save (`iw` absent); sleep wake source (phase 3, needs the attended trial boot).

## Collected fix list (to be ordered after the investigation)

- Speaker PCM always open — done 2026-11-18: root cause reproduced (speaker SoundWire controller resume clash); only that controller is held on, the no-idle rule is removed. Driver root fix deferred.
- Sleep: idle USB-C SuperSpeed PHY wake IRQs (a600000 PDC 17, a800000 PDC 47) storm once CXSD is reachable; then sync_state can be enabled.
- a400000 boot failure (deferred-probe timeout race; every trial boot so far). 2026-11-19: softdep installed (drivers/files/boot-trials/install-a400000-trial.sh); cold boot 1 OK, more boots needed.
- Video hardware decoder (`iris`) — enabled 2026-11-19 with the device-signed `qcvss8380.mbn` (generic firmware rejected); 1080p H.264: 2.5 W with iris vs 6.75 W software (idle 3.9 W). Was: disabled, +4.3 W during 1080p playback. 2026-11-19: node, driver and `qcom/vpu/vpu30_p4_s6.mbn` are present; a trial DTB with `status = "okay"` is in drivers/files/boot-trials/ (one attended boot; the VPU may still reject the generic firmware signature).
- Camera privacy LED — done 2026-11-19 (`led-names = "privacy"`; this kernel does not use `privacy-led`). Was: not linked to the sensor. 2026-11-19: the same trial DTB gives the LED a phandle and adds `leds`/`led-names = "privacy-led"` to camera@36.
- USB-C external monitor hot-plug delay. 2026-11-19: the normal kernel log has no HPD or link-training timestamps; measure attended with `drm.debug` enabled (plug in, then time HPD, link training and modeset).
- No NTP client — done 2026-11-18: managed by the repository (timesyncd), applied directly.
- Wi-Fi power save — checked 2026-11-19: `iw` is installed (`/usr/sbin`, outside the user PATH) and reports `Power save: on`, set by NetworkManager `20-sl7-wifi.conf` (`wifi.powersave=3`). The power difference can only be measured on battery.
- Waydroid shows an Android "physical keyboard" notification (user request, low priority). 2026-11-19: it is Android's blockable system channel `PHYSICAL_KEYBOARD` ("Configure physical keyboard"). Long-press the notification and turn that channel off; an automated change means editing the ABX `/data/system/notification_policy.xml` (abx2xml/xml2abx) and restarting the Waydroid session.
- Waydroid start shows a black window for display calibration (~29 ms at login); hide it if possible (user request). 2026-11-19: `persist.waydroid.width`/`height` are unset, so multi-window mode measures the output with a temporary surface; setting them (waydroid.cfg [properties], `waydroid upgrade -o`, session restart) should skip it. Try while watching the screen.
