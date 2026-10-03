#!/usr/bin/env python3
"""Reject the withdrawn custom guard; upstream modules are hash-checked by build.sh."""
from pathlib import Path
import sys
root = Path(sys.argv[1]) / 'src/modules'
for module in ('partition', 'bootloader'):
    for file in (root / module).rglob('*'):
        if file.is_file():
            assert 'JatayuProtectedPartitionJob' not in file.read_text(errors='replace'), str(file)
print('Upstream partition/bootloader policy check PASS; actual disk tests remain required.')
