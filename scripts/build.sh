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
echo "JatayuOS development build started: $(date -u +%FT%TZ)"
export DEBIAN_FRONTEND=noninteractive
# Dedicated Debian builder: firmware candidates must be visible to preflight too.
cat > /etc/apt/sources.list.d/jatayu-build-firmware.sources <<'EOF'
Types: deb
URIs: https://deb.debian.org/debian
Suites: trixie
Components: contrib non-free-firmware
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
EOF
apt-get update
apt-get install -y --no-install-recommends live-build debootstrap squashfs-tools xorriso isolinux syslinux-common syslinux-utils grub-pc-bin grub-efi-amd64-bin mtools dosfstools python3 python3-yaml dpkg-dev zstd ca-certificates
python3 scripts/preflight.py --apt
bash scripts/package.sh
mkdir -p build/auto build/config/package-lists build/config/packages.chroot build/config/hooks/live
cp auto-config.sh build/auto/config
chmod +x build/auto/config
cp packages.list build/config/package-lists/jatayu.list.chroot
cp out/jatayu-integration_*.deb build/config/packages.chroot/
cp hooks/*.hook.chroot build/config/hooks/live/
chmod +x build/config/hooks/live/*
cd build
lb config
lb build
cd ..
iso=build/live-image-amd64.hybrid.iso
test -s "$iso"
cp "$iso" out/JatayuOS-0.1-dev-amd64.iso
find build -maxdepth 1 -name '*.packages' -exec cp '{}' out/ \;
cp build/chroot/usr/share/jatayu/build-package-manifest.tsv out/package-manifest.tsv
cp -a build/chroot/usr/share/jatayu/notices out/third-party-notices
python3 scripts/iso-check.py out/JatayuOS-0.1-dev-amd64.iso
(cd out && sha256sum JatayuOS-0.1-dev-amd64.iso > SHA256SUMS)
echo 'Development ISO assembled. It is NOT boot-tested or cleared for public redistribution.'
echo 'Run the VM/hardware checklist in docs/TESTING.md. See source obligations in docs/COMPLIANCE.md.'
