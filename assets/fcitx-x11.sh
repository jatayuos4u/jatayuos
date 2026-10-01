#!/bin/sh
[ "${XDG_SESSION_TYPE:-}" = x11 ] || exit 0
exec /usr/bin/fcitx5 -d
