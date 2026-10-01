#!/usr/bin/env python3
"""Build architecture-independent .deb packages with dpkg-deb."""
import gzip
import io
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'dist'; OUT.mkdir(exist_ok=True)
BUILD=ROOT/'build'; BUILD.mkdir(exist_ok=True)
VERSION='1.2.1'

def put(root,path,text):
    p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);return p

def control(root,name,description,depends=None):
    size=sum(p.stat().st_size for p in root.rglob('*') if p.is_file())//1024
    text=f'Package: {name}\nVersion: {VERSION}\nArchitecture: all\nMaintainer: JatayuOS Project <jatayu-os-project@users.noreply.github.com>\nSection: graphics\nPriority: optional\nInstalled-Size: {size}\nHomepage: https://github.com/jatayu-os-project/JatayuOS\n'
    if depends:text+='Depends: '+depends+'\nConflicts: jatayu-wallpapers-india\n'
    text+='Description: '+description+'\n'
    put(root,'DEBIAN/control',text)

app=BUILD/'app'; images=BUILD/'images'
for p in (app,images):
    if p.exists():shutil.rmtree(p)
    p.mkdir()
for name in ('app.py','core.py','plasma.py','service.py'):
    dest=app/'usr/share/jatayu-wallpaper'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'src'/name,dest)
launcher=put(app,'usr/bin/jatayu-wallpaper','#!/bin/sh\nexec /usr/bin/python3 /usr/share/jatayu-wallpaper/app.py "$@"\n');launcher.chmod(0o755)
put(app,'usr/share/applications/org.jatayuos.WallpaperChanger.desktop','''[Desktop Entry]
Type=Application
Name=Jatayu Wallpaper Changer
Name[hi]=जटायु वॉलपेपर चेंजर
Comment=Explore India, nature and space wallpapers offline
Exec=jatayu-wallpaper
Icon=org.jatayuos.WallpaperChanger
Terminal=false
Categories=Utility;Graphics;Qt;
Keywords=Wallpaper;Background;India;Jatayu;Slideshow;
StartupWMClass=org.jatayuos.WallpaperChanger
''')
put(app,'usr/lib/systemd/user/jatayu-wallpaper.service',"""[Unit]
Description=Jatayu wallpaper rotation
PartOf=graphical-session.target
After=graphical-session-pre.target
[Service]
Type=simple
ExecStart=/usr/bin/jatayu-wallpaper --service
Restart=on-failure
RestartSec=3
TimeoutStopSec=5
""")
icon=app/'usr/share/icons/hicolor/scalable/apps/org.jatayuos.WallpaperChanger.svg';icon.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'assets/jatayu-wallpaper.svg',icon)
put(app,'usr/share/metainfo/org.jatayuos.WallpaperChanger.metainfo.xml','''<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
<id>org.jatayuos.WallpaperChanger</id>
<metadata_license>CC0-1.0</metadata_license>
<project_license>GPL-3.0-or-later</project_license>
<name>Jatayu Wallpaper Changer</name>
<summary>Explore India, nature and space wallpapers offline</summary>
<developer id="org.jatayuos"><name>JatayuOS Project</name></developer>
<description><p>A local wallpaper gallery for JatayuOS and Debian with KDE Plasma. Browse, search, mark favourites, add folders, choose screens and schedule offline wallpaper rotation.</p></description>
<launchable type="desktop-id">org.jatayuos.WallpaperChanger.desktop</launchable>
<url type="homepage">https://github.com/jatayu-os-project/JatayuOS</url>
<provides><binary>jatayu-wallpaper</binary></provides>
<releases><release version="1.2.1" date="2026-10-01"/></releases>
<content_rating type="oars-1.1"/>
</component>
''')
manifest=json.loads((ROOT/'wallpapers/collection.json').read_text())
assert len(manifest)==24
for e in manifest:
    source=ROOT/'wallpapers'/e['file']
    with Image.open(source) as im:
        im.load();assert im.size==(1920,1080);assert im.format=='PNG'
    target=app/'usr/share/wallpapers/Jatayu-Collection'/e['file']
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
put(app,'usr/share/wallpapers/Jatayu-Collection/collection.json',json.dumps(manifest,indent=2))
for document in ROOT.glob('docs/*'):
    dest=app/'usr/share/doc/jatayu-wallpaper'/document.name
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(document,dest)
with gzip.open(app/'usr/share/doc/jatayu-wallpaper/changelog.gz','wb') as f:
    f.write(b'Jatayu Wallpaper Changer 1.2.1 (2026-10-01)\nFix preview layout feedback and page selection flicker. Keep 24 Full HD PNG wallpapers.\n')
control(app,'jatayu-wallpaper','offline wallpaper gallery with 24 bundled India, nature and space scenes\n Full HD PNG exports, favourites and automatic wallpaper rotation for Plasma.','python3 (>= 3.11), python3-pyqt6, plasma-workspace (>= 6.0)')
subprocess.run(['dpkg-deb','--root-owner-group','--build',str(app),str(OUT/f'jatayu-wallpaper_{VERSION}_all.deb')],check=True)
print('Built one package with',len(manifest),'Full HD wallpapers.')
