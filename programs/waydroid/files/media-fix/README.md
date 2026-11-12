# Shared storage / orphan OMX declaration

The installed MAINLINE vendor image declared android.hardware.media.omx but shipped no matching service binary. hwservicemanager repeatedly tried and failed to start IOmx/IOmxStore; MediaProvider/StorageManager hit 20-second timeouts and emulated;0 became unmountable. KakaoTalk remained on its splash screen.

A matching failure mechanism and resolution was documented on a different Qualcomm device: https://gist.github.com/jstockdale/36c4b6a858726d08dc6b1e93f6b37473 . The hardware-specific Codec2 import from that report is NOT used here. Local missing-service and timeout evidence was checked before applying the small manifest adaptation.

apply.py requires a mounted MAINLINE vendor and refuses automatic modification when an OMX service binary exists. It removes only android.hardware.media.omx from a copy of the vendor manifest in /var/lib/waydroid/overlay/vendor/etc/vintf/manifest.xml, then runs waydroid upgrade -o to restart with regenerated configuration. Original Android images are unchanged. It does not disable a working codec or promise hardware decode.

Run as root after the desktop user's Waydroid session starts. The Waydroid setup component calls this helper. The original manifest is saved under /var/lib/waydroid/surface-media-fix; the inspected version is also included here. Verify sm list-volumes all and the actual app login screen after restart.

Rollback: restore /var/lib/waydroid/surface-media-fix/original-vendor-manifest.xml to /var/lib/waydroid/overlay/vendor/etc/vintf/manifest.xml and run sudo waydroid upgrade -o. Future vendor-image updates need a manifest comparison; do not preserve stale full manifests without review.
