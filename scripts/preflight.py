#!/usr/bin/env python3
"""Fail before a long build for invalid syntax, missing files or unavailable packages."""
import argparse, ast, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument('--apt',action='store_true'); a=p.parse_args()
errors=[]
for f in ROOT.rglob('*.py'):
    if 'build' not in f.relative_to(ROOT).parts:
        try: ast.parse(f.read_text(), filename=str(f))
        except SyntaxError as e: errors.append(str(e))
for f in [*ROOT.glob('*.sh'),*ROOT.glob('scripts/*.sh'),*ROOT.glob('hooks/*')]:
    if subprocess.run(['bash','-n',str(f)],capture_output=True).returncode: errors.append(f'Shell syntax: {f}')
for f in ['apps/app.py','apps/engine.py','scripts/jatayu-admin','assets/wallpaper.svg','assets/logo.svg']:
    if not (ROOT/f).is_file(): errors.append(f'Missing {f}')
packages=[s.strip() for s in (ROOT/'packages.list').read_text().splitlines() if s.strip() and not s.startswith('#')]
for name in ('user-setup','sddm-theme-breeze'):
    if name not in packages: errors.append(f'Missing live-login package: {name}')
if a.apt:
    for name in packages:
        r=subprocess.run(['apt-cache','policy',name],text=True,capture_output=True)
        if 'Candidate:' not in r.stdout or 'Candidate: (none)' in r.stdout: errors.append(f'Unavailable package: {name}')
print(f'Checked Python/shell syntax, required assets and {len(packages)} package declarations.')
if errors: print('\n'.join(errors),file=sys.stderr); sys.exit(1)
print('Static preflight PASS; this does not boot-test an ISO.')
