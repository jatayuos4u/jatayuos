#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
stage=build/package-root
mkdir -p "$stage/DEBIAN" "$stage/usr/share/jatayu" "$stage/usr/bin" "$stage/usr/libexec"
cp -a overlay/. "$stage/"
cp apps/*.py "$stage/usr/share/jatayu/"
cp assets/* "$stage/usr/share/jatayu/"
cp assets/logo.png "$stage/etc/calamares/branding/jatayu/logo.png"
cp assets/plymouth-logo.png "$stage/usr/share/plymouth/themes/jatayu/logo.png"
cp scripts/jatayu "$stage/usr/bin/jatayu"
cp scripts/jatayu-admin "$stage/usr/libexec/jatayu-admin"
cp scripts/jatayu-live-installer "$stage/usr/libexec/jatayu-live-installer"
cp scripts/postinst "$stage/DEBIAN/postinst"
chmod 755 "$stage/usr/bin/jatayu" "$stage/usr/libexec/jatayu-admin" "$stage/usr/libexec/jatayu-live-installer" "$stage/DEBIAN/postinst"
cat > "$stage/DEBIAN/control" <<'EOF'
Package: jatayu-integration
Version: 0.1.0
Architecture: all
Maintainer: Anup Yadav <jatayuos4u@gmail.com>
Depends: python3, python3-pyside6.qtwidgets, python3-pil, python3-yaml, rsync, poppler-utils, qpdf, ghostscript, librsvg2-bin, pkexec, plasma-workspace, xdg-utils
Section: misc
Priority: optional
Description: JatayuOS development desktop integration and offline utility suite
 Original Jatayu interfaces using established Debian utilities.
 Development preview; see bundled limitations and compliance notes.
EOF
mkdir -p out
dpkg-deb --root-owner-group --build "$stage" out/jatayu-integration_0.1.0_all.deb

