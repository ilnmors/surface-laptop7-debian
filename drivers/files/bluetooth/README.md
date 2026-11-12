# Bluetooth address initialization

The Qualcomm controller downloaded firmware but reported a missing public address. BlueZ hid it as an unconfigured controller.

surface-bluetooth-address assigns a stable locally administered address derived from the installed machine-id only when a Qualcomm controller reports that its public address is the sole missing setting. Configured adapters are preserved.

The udev rule starts surface-bluetooth-address@hciN.service at device creation. The helper waits for initialization before checking the controller. setup.sh installs the script, rule and service.

Current machine validation completed with the adapter powered and Bluetooth discovery working. Pairing with a physical accessory and a cold boot remain untested.
