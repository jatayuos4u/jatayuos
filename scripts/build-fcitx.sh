#!/bin/bash
# Rebuild Debian's Fcitx with a longer startup diagnostic grace period.
set -euo pipefail
apt-get build-dep -y fcitx5
mkdir -p out/fcitx-src
(cd out/fcitx-src && apt-get source fcitx5=5.1.12-2)
fcitx_source=out/fcitx-src/fcitx5-5.1.12
python3 - "$fcitx_source" <<'PY'
from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'src/modules/wayland/waylandmodule.cpp'
s=p.read_text()
old='CLOCK_MONOTONIC, now(CLOCK_MONOTONIC) + 7000000, 0,'
assert s.count(old)==1, 'Unexpected Fcitx diagnostic timer source'
p.write_text(s.replace(old, 'CLOCK_MONOTONIC, now(CLOCK_MONOTONIC) + 30000000, 0,'))
p=root/'debian/changelog'
s=p.read_text()
assert s.startswith('fcitx5 (5.1.12-2)')
p.write_text(s.replace('fcitx5 (5.1.12-2)', 'fcitx5 (5.1.12-2+jatayu1)', 1))
print('Fcitx diagnostic grace: 30 seconds; diagnostic conditions and warnings retained.')
PY
(cd "$fcitx_source" && DEB_BUILD_OPTIONS="nocheck parallel=2" dpkg-buildpackage -b -us -uc -j2)
mkdir -p build/config/packages.chroot
# Exact-version runtime dependencies must travel together; development/debug packages are excluded.
for package in out/fcitx-src/*.deb; do
  case "$package" in *-dev_*|*-dbgsym_*) continue ;; esac
  cp "$package" build/config/packages.chroot/
done
test -s build/config/packages.chroot/fcitx5_5.1.12-2+jatayu1_amd64.deb
