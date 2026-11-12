-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 3.0 (quilt)
Source: libcamera
Binary: libcamera-dev, libcamera-doc, libcamera0.4, libcamera-ipa, libcamera-tools, libcamera-v4l2, gstreamer1.0-libcamera, python3-libcamera
Architecture: linux-any all
Version: 0.4.0-7
Maintainer: Debian Multimedia Maintainers <debian-multimedia@lists.debian.org>
Uploaders: Emmanuel Arias <emmanuelarias30@gmail.com>, IOhannes m zmölnig (Debian/GNU) <umlaeute@debian.org>, Andrej Shadura <andrewsh@debian.org>, Dylan Aïssi <daissi@debian.org>
Homepage: https://libcamera.org/
Standards-Version: 4.7.2
Vcs-Browser: https://salsa.debian.org/multimedia-team/libcamera
Vcs-Git: https://salsa.debian.org/multimedia-team/libcamera.git
Testsuite: autopkgtest
Testsuite-Triggers: @builddeps@, gstreamer1.0-tools
Build-Depends: debhelper-compat (= 13), dh-sequence-python3, libdrm-dev <!pkg.libcamera.nosdl>, libdw-dev <!pkg.libcamera.notrace>, libevent-dev, libgnutls28-dev | gnutls-dev, libgstreamer-plugins-base1.0-dev, libgstreamer1.0-dev, libgtest-dev <!nocheck>, libjpeg-dev <!pkg.libcamera.nosdl>, liblttng-ust-dev [!hurd-any !i386], libpython3-dev <!pkg.libcamera.nopython>, libsdl2-dev <!pkg.libcamera.nosdl>, libtiff-dev, libudev-dev [linux-any], libyaml-dev, libyuv-dev, meson (>= 0.63), openssl, pkgconf, python3-jinja2, python3-ply, python3-pybind11 <!pkg.libcamera.nopython>, python3-yaml, qt6-base-dev [!i386] <!pkg.libcamera.noqt>
Build-Depends-Indep: doxygen <!nodoc>, doxygen-latex <!nodoc>, graphviz <!nodoc>, libjs-jquery <!nodoc>, libjs-sphinxdoc <!nodoc>, libjs-underscore <!nodoc>, python3-sphinx <!nodoc>
Package-List:
 gstreamer1.0-libcamera deb libs optional arch=linux-any
 libcamera-dev deb libdevel optional arch=linux-any
 libcamera-doc deb doc optional arch=all profile=!nodoc
 libcamera-ipa deb libs optional arch=linux-any
 libcamera-tools deb video optional arch=linux-any
 libcamera-v4l2 deb libs optional arch=linux-any
 libcamera0.4 deb libs optional arch=linux-any
 python3-libcamera deb python optional arch=linux-any
Checksums-Sha1:
 1b03222a4f73ad7a410ac80897c10660ba27d340 1315742 libcamera_0.4.0.orig.tar.bz2
 85addbc024a72b57a9faeb7ac5b03ee6bc4fb63b 24448 libcamera_0.4.0-7.debian.tar.xz
Checksums-Sha256:
 32a0a2b91f03f16a191b8fbe48fdcf886e8153c367569301bfd1bf70ebb4dcc0 1315742 libcamera_0.4.0.orig.tar.bz2
 e1e1a9a0726cf7e446926ac849018a02f9b497951062e1982be761a039ce6271 24448 libcamera_0.4.0-7.debian.tar.xz
Files:
 b20f54559e80c1c4fd79e95774e8e98a 1315742 libcamera_0.4.0.orig.tar.bz2
 e023bf69c14c03d6b3b089b77381e0ab 24448 libcamera_0.4.0-7.debian.tar.xz

-----BEGIN PGP SIGNATURE-----

iQIzBAEBCgAdFiEEmjwHvQbeL0FugTpdYS7xYT4FD1QFAmff75YACgkQYS7xYT4F
D1SqixAAhx75EdZI88pSRzc9isMLc6grsUgFIXyKSt+n0Mof26h+dNAno4ft8khb
F+UMirr4BD6jFwDsOTa7gkensdp4e+EzR64atexbZI9twKpfJ2SSM+wTITTtQgPN
hqIH5mouIccBPn93K8FwxxOq057Cst6YRpIKM2p4s1RToFtZoiPA+BHiM2YGmmpk
a+ndiZP29vHx9csyArkySTel6bNup+s8YvW0zadlETEpeiZQ4yNOHntmh4dxZ8Hs
zn3mRyYO8Q1AeCmwT0dCT9FsAJsoXrrIjuMF8qQxezodQPXxbWXeVkQV+8K2nxaO
yARpjq+GINMwQzFvKLo8Q9gx2uVl0VaOA//iacSeDt8sFNeNHQMpFLntNXUo79Ar
KEXYT4UvLibiQh3PFPJx8wuRFgNvbcO+/Cq4sqzDISFPYfLmFqAGkTkjUds/EsZ0
7y+4lIhcqkGo2Hu/QQSYUTlULDkrvEnL3XCeL4puBbuKwRtkmBO4XC4AkNSIbB4R
OSlq+EmfRA1CTUuB1gsAR0bC5+ZA2clt8yaY7ItskMnJ/Mg3+o6KX5OZRtTuXLku
kau4J2mT6dtK6exN6OD8yXfk2vtxQz0Ho1+stBvNJzrLExnaVmMn7L2iDf0lg1Ol
oouHnlqf+20ZGYSVtA1sYmIXJg29qnndT5pQjM6+tcYgMH66tbs=
=AUPH
-----END PGP SIGNATURE-----
