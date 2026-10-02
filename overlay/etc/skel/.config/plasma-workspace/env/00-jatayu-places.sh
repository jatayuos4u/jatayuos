#!/bin/sh
mkdir -p "${XDG_STATE_HOME:-$HOME/.local/state}"
python3 /usr/share/jatayu/user-defaults.py >>"${XDG_STATE_HOME:-$HOME/.local/state}/jatayu-places.log" 2>&1
