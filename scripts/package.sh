#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
stage=build/package-root
# A repeated local assembly must not retain deleted files from an older package.
rm -rf -- "$stage"
mkdir -p "$stage/DEBIAN" "$stage/usr/share/jatayu" "$stage/usr/bin" "$stage/usr/libexec"
cp -a overlay/. "$stage/"
cp apps/*.py "$stage/usr/share/jatayu/"
# Install runtime assets only; design/reference subdirectories are not shipped.
find assets -maxdepth 1 -type f -exec cp -- {} "$stage/usr/share/jatayu/" \;
cp assets/logo.png "$stage/etc/calamares/branding/jatayu/logo.png"
cp assets/plymouth-logo.png "$stage/usr/share/plymouth/themes/jatayu/logo.png"
cp assets/plymouth-dot-*.png "$stage/usr/share/plymouth/themes/jatayu/"
cp scripts/jatayu "$stage/usr/bin/jatayu"
cp scripts/jatayu-webapp "$stage/usr/bin/jatayu-webapp"
cp scripts/jatayu-admin "$stage/usr/libexec/jatayu-admin"
cp scripts/jatayu-live-installer "$stage/usr/libexec/jatayu-live-installer"
cp scripts/postinst "$stage/DEBIAN/postinst"
chmod 755 "$stage/usr/bin/jatayu" "$stage/usr/bin/jatayu-webapp" "$stage/usr/libexec/jatayu-admin" "$stage/usr/libexec/jatayu-live-installer" "$stage/DEBIAN/postinst"
cat > "$stage/DEBIAN/control" <<'EOF'
Package: jatayu-integration
Version: 1.0~rc3
Architecture: all
Maintainer: Anup Yadav <jatayuos4u@gmail.com>
Depends: python3, python3-pyside6.qtwidgets, python3-pyside6.qtwebenginewidgets, python3-pil, python3-yaml, rsync, poppler-utils, qpdf, ghostscript, librsvg2-bin, pkexec, plasma-workspace, xdg-utils, upower, xdg-desktop-portal, xdg-desktop-portal-kde, os-prober, ntfs-3g
Section: misc
Priority: optional
Description: JatayuOS release candidate desktop integration and offline utility suite
 Original Jatayu interfaces using established Debian utilities.
 Release Candidate; see bundled limitations and compliance notes.
EOF
mkdir -p out
# Preserve administrator edits during future Jatayu package upgrades.
find "$stage/etc" -type f -printf '/etc/%P\n' | sort > "$stage/DEBIAN/conffiles"
dpkg-deb --root-owner-group --build "$stage" out/jatayu-integration_1.0~rc3_all.deb
