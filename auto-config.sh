#!/bin/bash
set -euo pipefail
lb config noauto \
  --mode debian --distribution trixie --architectures amd64 \
  --binary-image iso-hybrid --bootloaders 'syslinux grub-efi' \
  --archive-areas 'main contrib non-free-firmware' \
  --mirror-bootstrap https://deb.debian.org/debian/ \
  --mirror-chroot https://deb.debian.org/debian/ \
  --mirror-binary https://deb.debian.org/debian/ \
  --mirror-chroot-security https://security.debian.org/debian-security/ \
  --mirror-binary-security https://security.debian.org/debian-security/ \
  --debian-installer none --apt-recommends false \
  --firmware-chroot true --firmware-binary true \
  --security true --updates true --backports false \
  --memtest none --iso-volume JATAYUOS_DEV \
  --iso-application 'JatayuOS Development Live' \
  --iso-publisher 'JatayuOS - Anup Yadav - Independent project' \
  --bootappend-live 'boot=live components quiet splash username=jatayu hostname=jatayuos locales=en_IN.UTF-8 keyboard-layouts=us timezone=Asia/Kolkata' \
  --chroot-squashfs-compression-type zstd \
  --chroot-squashfs-compression-level 6 \
  --cache true --cache-packages true --checksums sha256 "$@"

