#!/bin/bash
# Rebuild alpine_2.26+dfsg-3+maildir1: Debian trixie's alpine 2.26+dfsg-3 source plus Eduardo Chappa's
# alpine-2.26 Maildir patch (Debian builds Alpine without it, so it cannot open ~/workspace/mails).
# Build dependencies: aspell debhelper fakeroot libkrb5-dev libldap2-dev libncurses-dev libpam0g-dev libssl-dev.
set -euo pipefail
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
dpkg-source -x "$here/alpine_2.26+dfsg-3.dsc" "$work/alpine"
cp "$here/maildir.patch" "$work/alpine/debian/patches/maildir.patch"
echo maildir.patch >> "$work/alpine/debian/patches/series"
cd "$work/alpine"
{ printf 'alpine (2.26+dfsg-3+maildir1) trixie; urgency=medium\n\n'
  printf '  * Local build: add Eduardo Chappa'"'"'s alpine-2.26 Maildir patch (debian/patches/maildir.patch).\n\n'
  printf ' -- il <il@ilnmors.internal>  %s\n\n' "$(LC_ALL=C date -R)"
  cat debian/changelog; } > debian/changelog.new
mv debian/changelog.new debian/changelog
DEB_BUILD_OPTIONS="parallel=$(nproc)" dpkg-buildpackage -b -us -uc -rfakeroot
cp "$work"/alpine_2.26+dfsg-3+maildir1_arm64.deb "$here/../packages/"
