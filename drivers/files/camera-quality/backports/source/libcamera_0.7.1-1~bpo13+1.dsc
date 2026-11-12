-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 3.0 (quilt)
Source: libcamera
Binary: libcamera-dev, libcamera-doc, libcamera0.7, libcamera-ipa, libcamera-tools, libcamera-v4l2, gstreamer1.0-libcamera, python3-libcamera
Architecture: linux-any all
Version: 0.7.1-1~bpo13+1
Maintainer: Debian Multimedia Maintainers <debian-multimedia@lists.debian.org>
Uploaders: Emmanuel Arias <emmanuelarias30@gmail.com>, IOhannes m zmölnig (Debian/GNU) <umlaeute@debian.org>, Andrej Shadura <andrewsh@debian.org>, Dylan Aïssi <daissi@debian.org>
Homepage: https://libcamera.org/
Standards-Version: 4.7.4
Vcs-Browser: https://salsa.debian.org/multimedia-team/libcamera
Vcs-Git: https://salsa.debian.org/multimedia-team/libcamera.git
Testsuite: autopkgtest
Testsuite-Triggers: @builddeps@, gstreamer1.0-tools
Build-Depends: debhelper-compat (= 13), dh-sequence-python3, libdrm-dev <!pkg.libcamera.nosdl>, libdw-dev <!pkg.libcamera.notrace>, libevent-dev, libgnutls28-dev | gnutls-dev, libgstreamer-plugins-base1.0-dev, libgstreamer1.0-dev, libgtest-dev <!nocheck>, libjpeg-dev <!pkg.libcamera.nosdl>, liblttng-ust-dev [!hurd-any !i386], libpisp-dev [arm64 armel armhf], libpython3-dev <!pkg.libcamera.nopython>, libsdl2-dev <!pkg.libcamera.nosdl>, libtiff-dev, libudev-dev [linux-any], libyaml-dev, libyuv-dev, meson (>= 0.63), openssl, pkgconf, python3-jinja2:native, python3-ply, python3-pybind11 <!pkg.libcamera.nopython>, python3-yaml:native, qt6-base-dev [!i386] <!pkg.libcamera.noqt>
Build-Depends-Indep: doxygen <!nodoc>, doxygen-latex <!nodoc>, graphviz <!nodoc>, libjs-jquery <!nodoc>, libjs-sphinxdoc <!nodoc>, libjs-underscore <!nodoc>, python3-sphinx:native <!nodoc>, python3-sphinx-book-theme:native <!nodoc>, python3-sphinxcontrib.doxylink:native <!nodoc>
Package-List:
 gstreamer1.0-libcamera deb libs optional arch=linux-any
 libcamera-dev deb libdevel optional arch=linux-any
 libcamera-doc deb doc optional arch=all profile=!nodoc
 libcamera-ipa deb libs optional arch=linux-any
 libcamera-tools deb video optional arch=linux-any
 libcamera-v4l2 deb libs optional arch=linux-any
 libcamera0.7 deb libs optional arch=linux-any
 python3-libcamera deb python optional arch=linux-any
Checksums-Sha1:
 1d9fbe1a24891fce55285d97ba7b6887911718f8 2147991 libcamera_0.7.1.orig.tar.gz
 22e04f295f9424ea755e20ecdfe94f807c6b7a4b 23912 libcamera_0.7.1-1~bpo13+1.debian.tar.xz
Checksums-Sha256:
 7e55515764f168b36450dfd9c15cac87956bc286c7e34d73a19f13454186bb64 2147991 libcamera_0.7.1.orig.tar.gz
 c99836f121b5d0eacc04cf046fbfd8c943d3bd90b2026bd10a6a34a63669be4a 23912 libcamera_0.7.1-1~bpo13+1.debian.tar.xz
Files:
 674e11e408578147512a586603ed9c20 2147991 libcamera_0.7.1.orig.tar.gz
 c4afc57b22e2368633afd8e1d167c6c9 23912 libcamera_0.7.1-1~bpo13+1.debian.tar.xz

-----BEGIN PGP SIGNATURE-----

iQJCBAEBCgAsFiEE6nIe6ZnTE18IYOVF8RQITAhhEREFAmn6GTAOHGxvb2xAZG9v
ei5vcmcACgkQ8RQITAhhERHOeg/6A9YV+r4TpKLSpE7tCzyELXuTzka1YIDHKS5I
CMMWJ6E95DM1XoebBsJmmlbS5VdBzOP6vWEyqYRJ69YnWOBPT5SxcemhDYIvnKsD
2I5twYmnv9K9aArFc6V961/VzOpMMNpccaJFXjlMe9zPXk4tS+TORFWgtaGSENVy
h4h6RrdgZn9FV8cPn4MVg8oDhIPeMaF1JGHGuoLsT6hEnXQD2RL7n4XOcBwEKR71
HAGALm6RJ6u1ow/KWyKKjpbiAqEnF2JOMK2W46isrXBzXHb4kJ9Zoq6woMAmT1+7
jqqo7bFHSd2lzyYm10ZS7KzWk9czNId3NbNHjFfYGbkMk9meeabPe3IgKUQs4EUT
f7HnfnI2GTjLvaLzQfQD9x8OEUJhlghQ3Cv4YGzamSktEKVBX7NOKy3YU5sJxDaS
869wkgAtsoGqttZujz/IbO/RFfE7szRjp5WYHjURYh30ZNpvqf9IWiFEotMnii5x
q8C99eBbOXBjeRQ0zwySgOqAwHf5BoPi6S560fJmhtN9F98ZVpmF7y/neoTNs1eE
r/tZLAdnf4tq8tJICO/S0Wz33uRlMW6d4CFEq3ZBq/qpdjorVFikxo+DGP0nQDQA
+kCnbx8FQCVYHyuGbn8Im64jG8QUrY85DftUap+mbKCeqfNG0HO8tytL7Ths1In4
/BbwJ60=
=OKj3
-----END PGP SIGNATURE-----
