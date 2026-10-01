#!/bin/bash
# Run inside a real Debian 13 VM, or a privileged Debian 13 build container.
set -euo pipefail
cd "$(dirname "$0")/.."
source /etc/os-release
[[ ${ID:-} == debian && ${VERSION_CODENAME:-} == trixie ]] || { echo 'Use Debian 13 Trixie for the builder.' >&2; exit 2; }
[[ $EUID == 0 ]] || { echo 'Run with sudo inside the dedicated builder.' >&2; exit 2; }
cap_hex=$(awk '/^CapEff:/{print $2}' /proc/self/status)
(( (16#$cap_hex & (1<<21)) && (16#$cap_hex & (1<<18)) )) || { echo 'Builder needs mount and chroot capabilities; stop before downloads.' >&2; exit 2; }
mkdir -p out
exec > >(tee -a out/build.log) 2>&1
echo "JatayuOS release candidate build started: $(date -u +%FT%TZ)"
precheck_only=false
case "${1:-}" in --precheck-only) precheck_only=true ;; "") ;; *) echo "Unknown build option" >&2; exit 2 ;; esac
export DEBIAN_FRONTEND=noninteractive
# Dedicated Debian builder: firmware candidates must be visible to preflight too.
# The official Trixie container already has a debian.sources file with its own
# Signed-By keyring. Extend its components instead of adding a duplicate source
# with a potentially conflicting Signed-By value.
if [[ -f /etc/apt/sources.list.d/debian.sources ]]; then
  awk '
    /^Components:/ {
      if ($0 !~ /(^|[[:space:]])contrib([[:space:]]|$)/) $0 = $0 " contrib"
      if ($0 !~ /(^|[[:space:]])non-free-firmware([[:space:]]|$)/) $0 = $0 " non-free-firmware"
    }
    { print }
  ' /etc/apt/sources.list.d/debian.sources > /etc/apt/sources.list.d/debian.sources.jatayu-tmp
  cat /etc/apt/sources.list.d/debian.sources.jatayu-tmp > /etc/apt/sources.list.d/debian.sources
  rm /etc/apt/sources.list.d/debian.sources.jatayu-tmp
else
  cat > /etc/apt/sources.list.d/jatayu-build-firmware.sources <<'EOF'
Types: deb
URIs: https://deb.debian.org/debian
Suites: trixie
Components: contrib non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
EOF
fi
cat > /etc/apt/sources.list.d/jatayu-build-backports.list <<'EOF'
deb http://deb.debian.org/debian trixie-backports main contrib non-free-firmware
EOF
# Rebuild only the distribution installer from Debian's source with the
# reviewable Jatayu UI patch. Its binary is included in the live filesystem.
# Reuse the container's Debian source stanza and its exact Signed-By keyring.
# A second stanza with a different path makes apt reject all sources.
test -f /etc/apt/sources.list.d/debian.sources
sed -i 's/^Types: deb$/Types: deb deb-src/' /etc/apt/sources.list.d/debian.sources
grep -q 'Types: deb deb-src' /etc/apt/sources.list.d/debian.sources
apt-get update
apt-get install -y --no-install-recommends live-build debootstrap squashfs-tools xorriso isolinux syslinux-common syslinux-utils grub-pc-bin grub-efi-amd64-bin mtools dosfstools python3 python3-yaml python3-pil poppler-utils fonts-dejavu-core dpkg-dev zstd ca-certificates
python3 scripts/prepare-wallpaper.py
python3 scripts/generate-files.py
python3 scripts/preflight.py --apt | tee out/precheck.txt
if $precheck_only; then echo "Precheck passed. ISO build was not requested."; exit 0; fi
printf '%s  %s\n' '1482544a10ec927187566396067d94009eff00b7c4866cf805d809b46f515235' jatayu-tools_2.0.2_all.deb | sha256sum -c -
bash scripts/package.sh
apt-get build-dep -y calamares
mkdir -p out/calamares-src
(cd out/calamares-src && apt-get source calamares=3.3.14-1)
calamares_src=out/calamares-src/calamares-3.3.14
test -f "$calamares_src/debian/changelog"
python3 scripts/patch-calamares.py "$calamares_src"
sed -i '1s/(3.3.14-1)/(3.3.14-1+jatayu1)/' "$calamares_src/debian/changelog"
(cd "$calamares_src" && DEB_BUILD_OPTIONS="nocheck parallel=2" dpkg-buildpackage -b -us -uc -j2)
test -s out/calamares-src/calamares_3.3.14-1+jatayu1_amd64.deb
mkdir -p build/auto build/config/package-lists build/config/packages.chroot build/config/hooks/live
cp auto-config.sh build/auto/config
chmod +x build/auto/config
cp packages.list build/config/package-lists/jatayu.list.chroot
cp out/jatayu-integration_*.deb jatayu-tools_2.0.2_all.deb out/jatayu-wallpaper_1.2.1_all.deb build/config/packages.chroot/
cp out/calamares-src/calamares_3.3.14-1+jatayu1_amd64.deb build/config/packages.chroot/
cp hooks/*.hook.chroot build/config/hooks/live/
chmod +x build/config/hooks/live/*
# The live-build bootloader templates carry Debian's default splash.
# Preserve their boot logic and replace only the shared artwork.
mkdir -p build/config/bootloaders
cp -a /usr/share/live/build/bootloaders/. build/config/bootloaders/
python3 scripts/prepare-boot-art.py
bash scripts/build-fcitx.sh
cd build
lb config
lb build
cd ..
iso=build/live-image-amd64.hybrid.iso
test -s "$iso"
test -x build/chroot/usr/bin/jatayu-wallpaper
test -s build/chroot/usr/share/jatayu/USER-MANUAL.pdf
test -s build/chroot/usr/share/jatayu/FAQ.pdf
chroot build/chroot /usr/bin/python3 -c "from PyQt6.QtWidgets import QApplication"
test -x build/chroot/usr/bin/libreoffice
test -x build/chroot/usr/bin/jatayu-tools
chroot build/chroot /usr/bin/python3 -c 'from PySide6.QtWebEngineWidgets import QWebEngineView'
for slug in kavach sarkar-setu utsav; do test -s "build/chroot/usr/share/jatayu/${slug}.html"; done
for slug in kavach sarkar-setu utsav; do grep -q "Exec=jatayu-webapp ${slug}" "build/chroot/usr/share/applications/org.jatayu.${slug}.desktop"; done
chroot build/chroot /usr/bin/env QT_QPA_PLATFORM=offscreen /usr/bin/jatayu-tools --smoke
test -s build/chroot/tmp/jatayu-tools-smoke.png
cp build/chroot/tmp/jatayu-tools-smoke.png out/jatayu-tools-smoke.png
test -x build/chroot/usr/libexec/jatayu-live-installer
cp "$iso" out/JatayuOS-0.1-rc-amd64.iso
find build -maxdepth 1 -name '*.packages' -exec cp '{}' out/ \;
cp build/chroot/usr/share/jatayu/build-package-manifest.tsv out/package-manifest.tsv
cp -a build/chroot/usr/share/jatayu/notices out/third-party-notices
python3 scripts/iso-check.py out/JatayuOS-0.1-rc-amd64.iso
(cd out && sha256sum JatayuOS-0.1-rc-amd64.iso > SHA256SUMS)
echo 'Release Candidate ISO assembled. It is NOT boot-tested or cleared for public redistribution.'
echo 'Run the VM/hardware checklist in docs/TESTING.md. See source obligations in docs/COMPLIANCE.md.'

