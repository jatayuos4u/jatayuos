#!/usr/bin/env python3
"""Compatibility entry point: regenerate the same illustrated offline guides."""
from pathlib import Path
import runpy
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'scripts/generate-illustrated-guides.py'),run_name='__main__')
