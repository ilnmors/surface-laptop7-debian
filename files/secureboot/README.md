# Secure Boot

Run sudo bash files/secureboot/install.sh after installing this bundle's kernel and DTB; setup.sh runs it too. The installer keeps the machine-specific private key under root-only /var/lib/surface-secureboot. Private keys are never included in this bundle.

## Boot chain

Surface UEFI → Microsoft-signed Debian shim → Debian-signed GRUB → locally signed Surface wrapper and kernel → locally signed drivers. The already enrolled MOK still authenticates the locally signed boot image. In Surface UEFI, the Secure Boot configuration must permit Microsoft and third-party CAs.

## Driver trust repair

The existing kernel already enables CONFIG_SYSTEM_EXTRA_CERTIFICATE with a 4096-byte reserve. kernel-certificate.py decompresses its EFI payload and uses the matching System.map to put the local public certificate into that reserved slot, updating the used-length and certificate-list length exactly as Linux's insert-sys-cert tool does. Existing certificates and kernel instructions are preserved. No kernel rebuild is required.

surface-secureboot-update signs modules, updates initramfs, inserts the public certificate, signs the inner kernel and its Surface wrapper with the embedded DTB, then refreshes /boot/secureboot. Kernel and initramfs hooks repeat this after updates. Unknown kernel layouts fail validation before replacing the active image. Run sudo surface-secureboot-update after manually replacing a module or DTB.

The original signed image is retained under /boot/secureboot/previous on this machine. The original packaged kernel at /boot/vmlinuz-7.3.0-31-qcom-x1e is unchanged.

## Enrollment

This machine's certificate is already enrolled and MokListTrustedRT=1 already permits kernel MOK trust. No further trust confirmation is needed. Repeating --trust-mok can produce "Failed to delete MokListTrusted state" because its opt-out variable is absent. retry-mok-trust.sh now skips that unnecessary request.

On a fresh installation, run sudo python3 files/secureboot/enroll-mok.py. For an unenrolled certificate it accepts exactly seven printable ASCII characters twice. On reboot choose Enroll MOK → Continue → Yes and enter the complete password. A temporary root-only password hash is removed after the request; no password is saved here. The signed MokManager's separate trust-state change UI remains unchanged and is unnecessary here.

## Verification

Linux reference insertion tool comparison and both PE signature checks passed. An isolated ARM64 boot with module.sig_enforce=1 loaded this builtin certificate, rejected the unsigned test module and accepted the existing locally signed module. See verification/.

Physical Surface boot verified on 2026-11-11, kernel 7.3.0-31-qcom-x1e: mokutil reports SecureBoot enabled, kernel lockdown is integrity, and the Surface Debian Local Secure Boot certificate loaded. This verifies boot and kernel trust; it does not establish touchscreen or suspend support.
