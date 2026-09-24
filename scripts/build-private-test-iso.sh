#!/usr/bin/env bash
# Build a local test image only. Distribution needs the review in LEGAL.md.
set -euo pipefail
[[ $# -eq 2 ]] || { echo "Usage: $0 OFFICIAL_UBUNTUCINNAMON_26.04.1_ISO OUTPUT_ISO" >&2; exit 2; }
base=$(realpath "$1")
out=$(realpath -m "$2")
name=ubuntucinnamon-26.04.1-desktop-amd64.iso
[[ $(basename "$base") == "$name" && -f "$base" && ! -e "$out" ]] || { echo 'Use the named official ISO and a new output path.' >&2; exit 2; }
[[ $EUID -eq 0 ]] || { echo 'Run with sudo on a Linux build machine.' >&2; exit 2; }
for tool in xorriso unsquashfs mksquashfs dpkg-deb curl sha256sum chroot dpkg-query; do
    command -v "$tool" >/dev/null || { echo "Missing: $tool" >&2; exit 2; }
done
available=$(df -Pk "$(dirname "$out")" | awk 'NR==2 {print $4}')
((available > 40 * 1024 * 1024)) || { echo 'At least 40 GiB free disk space is required.' >&2; exit 2; }
project=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
work=$(mktemp -d "$(dirname "$out")/jatayu-iso.XXXXXXXX")
cleanup() { mountpoint -q "$work/root/dev" && umount -l "$work/root/dev" || :; mountpoint -q "$work/root/proc" && umount -l "$work/root/proc" || :; mountpoint -q "$work/root/sys" && umount -l "$work/root/sys" || :; rm -rf "$work"; }
trap cleanup EXIT
url=https://cdimage.ubuntu.com/ubuntucinnamon/releases/26.04.1/release
curl -fsSL "$url/SHA256SUMS" -o "$work/SHA256SUMS"
expected=$(awk -v n="$name" '$2==n || $2=="*"n {print $1}' "$work/SHA256SUMS")
[[ $expected =~ ^[0-9a-f]{64}$ ]] || { echo 'Official checksum entry missing.' >&2; exit 1; }
echo "$expected  $base" | sha256sum -c -
"$project/build-package.sh"
deb="$project/dist/jatayu-experience_0.1.0_all.deb"
mkdir -p "$work/root" "$work/layers"
xorriso -osirrox on -indev "$base" \
    -extract /casper/minimal.squashfs "$work/layers/minimal.squashfs" \
    -extract /casper/minimal.standard.squashfs "$work/layers/standard.squashfs" \
    -extract /md5sum.txt "$work/md5sum.txt"
unsquashfs -no-progress -d "$work/root" "$work/layers/minimal.squashfs"
unsquashfs -no-progress -f -d "$work/root" "$work/layers/standard.squashfs"
mkdir -p "$work/root/tmp" "$work/root/dev" "$work/root/proc" "$work/root/sys" "$work/root/etc"
cp "$deb" "$work/root/tmp/jatayu.deb"
cp -L "$work/root/etc/resolv.conf" "$work/resolv.original" 2>/dev/null || :
cp --remove-destination -L /etc/resolv.conf "$work/root/etc/resolv.conf"
printf '#!/bin/sh\nexit 101\n' > "$work/root/usr/sbin/policy-rc.d"
chmod 755 "$work/root/usr/sbin/policy-rc.d"
mount --bind /dev "$work/root/dev"
mount -t proc proc "$work/root/proc"
mount --bind /sys "$work/root/sys"
chroot "$work/root" apt-get update
chroot "$work/root" env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-tk
chroot "$work/root" dpkg -i /tmp/jatayu.deb
chroot "$work/root" dpkg-query -W -f='${Package}\t${Version}\n' | sort > "$work/manifest"
chroot "$work/root" dpkg-query -W -f='${Status}\n' jatayu-experience | grep -Fx 'install ok installed'
rm -f "$work/root/tmp/jatayu.deb" "$work/root/usr/sbin/policy-rc.d"
rm -rf "$work/root/var/lib/apt/lists/"*
if [[ -f "$work/resolv.original" ]]; then cp --remove-destination "$work/resolv.original" "$work/root/etc/resolv.conf"; fi
umount "$work/root/sys" "$work/root/proc" "$work/root/dev"
size=$(du -sx --block-size=1 "$work/root" | awk '{print $1}')
printf '%s\n' "$size" > "$work/minimal.standard.size"
cp "$work/manifest" "$work/minimal.standard.manifest"
cp "$work/manifest" "$work/minimal.standard.manifest.full"
mksquashfs "$work/root" "$work/minimal.standard.squashfs" -noappend -comp xz -b 1M -processors 4 -no-progress
# Retain checksums for unchanged ISO files and replace only modified entries.
python3 - "$work" <<'PY'
import hashlib, pathlib, sys
w=pathlib.Path(sys.argv[1]); md5=w/'md5sum.txt'
changes={'casper/minimal.standard.squashfs':'minimal.standard.squashfs',
         'casper/minimal.standard.size':'minimal.standard.size',
         'casper/minimal.standard.manifest':'minimal.standard.manifest',
         'casper/minimal.standard.manifest.full':'minimal.standard.manifest.full'}
lines=[]
for line in md5.read_text().splitlines():
    if len(line.split(maxsplit=1))==2:
        key=line.split(maxsplit=1)[1].lstrip('*./')
        if key in changes:continue
    lines.append(line)
for path,local in changes.items():
    digest=hashlib.md5((w/local).read_bytes()).hexdigest()
    lines.append(f'{digest}  ./{path}')
md5.write_text('\n'.join(lines)+'\n')
PY
xorriso -indev "$base" -outdev "$out" \
    -map "$work/minimal.standard.squashfs" /casper/minimal.standard.squashfs \
    -map "$work/minimal.standard.size" /casper/minimal.standard.size \
    -map "$work/minimal.standard.manifest" /casper/minimal.standard.manifest \
    -map "$work/minimal.standard.manifest.full" /casper/minimal.standard.manifest.full \
    -map "$work/md5sum.txt" /md5sum.txt \
    -boot_image any replay -commit
xorriso -indev "$out" -report_el_torito plain > "$out.boot-report.txt"
sha256sum "$out" > "$out.sha256"
echo "Private test image created: $out"
echo 'Boot-test BIOS, UEFI, live session, installer and installed system before use.'
