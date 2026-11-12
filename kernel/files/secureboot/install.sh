#!/bin/bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if (( EUID != 0 )); then exec sudo /bin/bash "$PWD/install.sh"; fi
state=/var/lib/surface-secureboot
install -d -m700 "$state"
if [[ ! -f $state/MOK.key && ! -f $state/MOK.pem ]]; then
  openssl req -new -x509 -newkey rsa:3072 -noenc -days 3650 \
    -subj '/CN=Surface Secure Boot/' \
    -addext subjectKeyIdentifier=hash -addext extendedKeyUsage=codeSigning \
    -keyout "$state/MOK.key" -out "$state/MOK.pem"
fi
test -f "$state/MOK.key"
test -f "$state/MOK.pem"
chmod 600 "$state/MOK.key"
openssl x509 -in "$state/MOK.pem" -outform DER -out "$state/MOK.der"
install -m755 sign-file "$state/sign-file"
install -d /usr/local/lib/surface-secureboot
install -m644 kernel-certificate.py /usr/local/lib/surface-secureboot/kernel_certificate.py
install -m755 surface-secureboot-update /usr/local/sbin/
install -d /etc/initramfs/post-update.d
install -m755 hooks/kernel-postinst /etc/kernel/postinst.d/zz-surface-secureboot
install -m755 hooks/initramfs-post-update /etc/initramfs/post-update.d/zz-surface-secureboot
temporary=$(mktemp -d)
trap 'rm -rf "$temporary"' EXIT
for package in packages/{shim-signed,shim-unsigned,shim-helpers-arm64-signed,shim-signed-common,grub-efi-arm64-signed}_*.deb; do
  dpkg-deb -x "$package" "$temporary"
done
install -d /boot/efi/EFI/debian
install -m644 "$temporary/usr/lib/shim/shimaa64.efi.signed" /boot/efi/EFI/debian/shimaa64.efi
install -m644 "$temporary/usr/lib/shim/mmaa64.efi.signed" /boot/efi/EFI/debian/mmaa64.efi
install -m644 "$temporary/usr/lib/grub/arm64-efi-signed/grubaa64.efi.signed" /boot/efi/EFI/debian/grubaa64.efi
/usr/local/sbin/surface-secureboot-update
efi_device=$(findmnt -n -o SOURCE -T /boot/efi)
efi_uuid=$(blkid -s PARTUUID -o value "$efi_device")
parent=$(lsblk -ndo PKNAME "$efi_device")
partition=$(cat "/sys/class/block/${efi_device##*/}/partition")
if ! efibootmgr -v | grep -Fi "$efi_uuid" | grep -Fq '\EFI\debian\shimaa64.efi'; then
  efibootmgr --create --disk "/dev/$parent" --part "$partition" \
    --label 'Debian Surface' --loader '\EFI\debian\shimaa64.efi'
fi
printf '%s\n' 'Enroll this machine-specific key before enabling Secure Boot:' \
  "sudo mokutil --import $state/MOK.der"
