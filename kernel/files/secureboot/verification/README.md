# Verification

vm-module-test.log records an isolated QEMU ARM64 boot of the repaired kernel with module.sig_enforce=1. It loaded the Surface certificate, rejected an unsigned dummy module and accepted the installed, locally signed copy. The VM had no host disks or network.

verify-vm.sh reproduces that test. Run it as root on the configured machine. Optional QEMU packages are under packages/; setup.sh does not install them. The test initramfs is temporary and does not change the host kernel or modules.

insert-sys-cert.c and its ARM64 binary are the Linux reference tool used to compare the certificate slot and length fields. The original source is Linux 7.3.0's scripts/insert-sys-cert.c (GPL).
