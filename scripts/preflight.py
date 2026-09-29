#!/usr/bin/env python3
"""Fail before a long build for invalid syntax, missing files or unavailable packages."""
import argparse, ast, hashlib, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument('--apt',action='store_true'); a=p.parse_args()
errors=[]
for f in ROOT.rglob('*.py'):
    if 'build' not in f.relative_to(ROOT).parts:
        try: ast.parse(f.read_text(), filename=str(f))
        except SyntaxError as e: errors.append(str(e))
for f in [*ROOT.glob('*.sh'),*ROOT.glob('scripts/*.sh'),*ROOT.glob('hooks/*')]:
    if subprocess.run(['bash','-n',str(f)],capture_output=True).returncode: errors.append(f'Shell syntax: {f}')
for f in ['apps/app.py','apps/engine.py','scripts/jatayu-admin','assets/wallpaper.jpg','assets/logo.png','assets/boot-splash.png','assets/plymouth-logo.png','assets/india-tricolor.png','scripts/prepare-boot-art.py','scripts/jatayu-live-installer','jatayu-tools_2.0.0_all.deb']:
    if not (ROOT/f).is_file(): errors.append(f'Missing {f}')
deb=ROOT/'jatayu-tools_2.0.0_all.deb'
if deb.is_file() and hashlib.sha256(deb.read_bytes()).hexdigest() != '4634514e641b851369b9cd276f573f68fa75128a38394a6e1722a32b87bd489b':
    errors.append('Jatayu Tools package checksum mismatch')
packages=[s.strip() for s in (ROOT/'packages.list').read_text().splitlines() if s.strip() and not s.startswith('#')]
for name in ('user-setup','sddm-theme-breeze','papirus-icon-theme'):
    if name not in packages: errors.append(f'Missing live-login package: {name}')
if a.apt:
    for name in packages:
        r=subprocess.run(['apt-cache','policy',name],text=True,capture_output=True)
        if 'Candidate:' not in r.stdout or 'Candidate: (none)' in r.stdout: errors.append(f'Unavailable package: {name}')
print(f'Checked Python/shell syntax, required assets and {len(packages)} package declarations.')
if errors: print('\n'.join(errors),file=sys.stderr); sys.exit(1)
print('Static preflight PASS; this does not boot-test an ISO.')
