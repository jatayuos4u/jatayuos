#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v dpkg-deb >/dev/null || { echo 'Install dpkg-dev' >&2; exit 1; }
mkdir -p dist
dpkg-deb --build --root-owner-group package dist/jatayu-experience_0.1.0_all.deb
echo "Package: $(pwd)/dist/jatayu-experience_0.1.0_all.deb"
