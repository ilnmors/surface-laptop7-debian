-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Format: 3.0 (quilt)
Source: libinput
Binary: libinput10, libinput-bin, libinput10-udeb, libinput-dev, libinput-tools
Architecture: any
Version: 1.28.1-1+deb13u1
Maintainer: Debian X Strike Force <debian-x@lists.debian.org>
Uploaders: Emilio Pozuelo Monfort <pochu@debian.org>, Héctor Orón Martínez <zumbi@debian.org>, Marius Gripsgard <marius@ubports.com>
Homepage: https://www.freedesktop.org/wiki/Software/libinput/
Standards-Version: 4.6.2
Vcs-Browser: https://salsa.debian.org/xorg-team/lib/libinput
Vcs-Git: https://salsa.debian.org/xorg-team/lib/libinput.git
Testsuite: autopkgtest
Testsuite-Triggers: build-essential
Build-Depends: debhelper-compat (= 13), meson, pkgconf, check, libgtk-3-dev, libmtdev-dev (>= 1.1.0), libudev-dev, libevdev-dev (>= 1.10.0), libwacom-dev (>= 0.20)
Package-List:
 libinput-bin deb libs optional arch=any
 libinput-dev deb libdevel optional arch=any
 libinput-tools deb libdevel optional arch=any
 libinput10 deb libs optional arch=any
 libinput10-udeb udeb debian-installer optional arch=any profile=!noudeb profile:v1=!noudeb
Checksums-Sha1:
 463c3c6269c128cb24060ecf5a3ec6195ed94ad6 1074349 libinput_1.28.1.orig.tar.gz
 9ecd51ce68d125b05ccca48ad433c3de04806d9b 13404 libinput_1.28.1-1+deb13u1.debian.tar.xz
Checksums-Sha256:
 a13f8c9a7d93df3c85c66afd135f0296701d8d32f911991b7aa4273fdd6a42a3 1074349 libinput_1.28.1.orig.tar.gz
 413b1238c335cced8f2698fc0bc8c0c6605034324a9528d841726ba1d3575f56 13404 libinput_1.28.1-1+deb13u1.debian.tar.xz
Files:
 34988f66b52814647c01fa72f2c5210d 1074349 libinput_1.28.1.orig.tar.gz
 b0f23b9704d8b9878fb1b7eabaac07fa 13404 libinput_1.28.1-1+deb13u1.debian.tar.xz

-----BEGIN PGP SIGNATURE-----

iQKmBAEBCgCQFiEERkRAmAjBceBVMd3uBUy48xNDz0QFAmooD3VfFIAAAAAALgAo
aXNzdWVyLWZwckBub3RhdGlvbnMub3BlbnBncC5maWZ0aGhvcnNlbWFuLm5ldDQ2
NDQ0MDk4MDhDMTcxRTA1NTMxRERFRTA1NENCOEYzMTM0M0NGNDQSHGNhcm5pbEBk
ZWJpYW4ub3JnAAoJEAVMuPMTQ89EFPMP/21smLWZdY5FNqMjtIhGeMBzUA4gxVRB
6U/W7h1oQXWdda3WpfyVqrXH2/4uiw2emfJflzaMfuEv9uO0+cwrdQUQLiIE5cPX
EfL6lm33sCXpOX4YV+C+XigDHmxnaHGwTmnE5fC7Jb9PcY+0ktHQfdGpIQLHTzSK
1znFbDnJeW9bPrTcHb6Hj3oKhbxRZwM6zT5KuGk/ftoSiMWmH041frttwzjI93ZD
IadFEfBoem/ahTe7XVTEqzNKRTQvjEHSQQ51nHqfC0qA6o55fqRvMjiJIDglMtQL
1mKPGWWf2shd3tH2ZwClSo2a8RZVMEEFVbectG9wlcPE0mLWJWkeREoRWweGmVOX
1/l38QzOPuyZaTZ+uaQTR2q51akMDt64YmuoPNBLPUsdECASDi0wriDe3Kd8BhVv
FYDBLKgaeMUhE6WRvyfPz1LojwWf9yE0xTD16/dPfiCDZbgsWk8kAmOBR9e1oBRB
zkjafqKNHP5lvWfOgr5k1ubLWLoL/1TsxfX/8lanyz7zkqkmDjWvZkzNgYpO4STJ
okBkzRTSQcj4WaR+1Tr5ONpI85PSDK27fM5ByDLy+TUygzLlbVqnYKKLN5g5zRbS
hFtMHQK8KoQGWKN0faQauqrZNS0iJYRHo9WgKAzCannIYw+zAxlzaqHMt8BlbMF9
5JineC0f+D0U
=pEIG
-----END PGP SIGNATURE-----
