#!/usr/bin/env python3
from pathlib import Path
import ast
import configparser
import subprocess
root=Path(__file__).resolve().parents[1]
for name in ('jatayu-app','jatayu-session','jatayu-first-run'):
    ast.parse((root/'package/usr/bin'/name).read_text())
ast.parse((root/'package/usr/lib/jatayu/wizard.py').read_text())
for file in (root/'package/usr/share/applications').glob('*.desktop'):
    p=configparser.ConfigParser(interpolation=None);p.read(file)
    assert p['Desktop Entry']['Exec'].startswith('/usr/bin/jatayu-app ')
subprocess.run(['bash','-n',str(root/'build-package.sh')],check=True)
assert 'user-session=jatayu' in (root/'package/etc/lightdm/lightdm.conf.d/70-jatayu.conf').read_text()
print('Syntax, launchers, and live-session wiring checked')
