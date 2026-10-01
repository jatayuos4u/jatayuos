"""Jatayu Wallpaper Changer. SPDX-License-Identifier: GPL-3.0-or-later."""
import json
import os
import random
import tempfile
from pathlib import Path

VERSION = '1.2.1'
APP_ID = 'org.jatayuos.WallpaperChanger'
DATA = Path(os.environ.get('JATAYU_WALLPAPER_DATA', '/usr/share/wallpapers/Jatayu-Collection'))
CONFIG = Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home()/'.config'))) / 'jatayu-wallpaper'
DEFAULTS = dict(folders=[], favourites=[], enabled=False, interval=1800, shuffle=True,
                favourites_only=False, at_login=True, screen=-1, layout=2, last='')
EXTENSIONS = {'.jpg', '.jpeg', '.jfif', '.png', '.webp', '.bmp'}
LAYOUTS = {'Fill': 2, 'Fit': 1, 'Stretch': 0, 'Centre': 6}

def read_json(path, default):
    try:
        data = json.loads(path.read_text())
        return data if isinstance(data, type(default)) else default
    except (OSError, ValueError):
        return default

def settings():
    c = DEFAULTS.copy()
    c.update(read_json(CONFIG/'settings.json', {}))
    for key in ('folders', 'favourites'):
        c[key] = [x for x in c.get(key, []) if isinstance(x, str)] if isinstance(c.get(key), list) else []
    for key in ('enabled', 'shuffle', 'favourites_only', 'at_login'):
        c[key] = bool(c.get(key, DEFAULTS[key]))
    try:
        c['interval'] = max(60, min(86400, int(c['interval'])))
        c['screen'] = max(-1, int(c['screen']))
        c['layout'] = int(c['layout']) if int(c['layout']) in LAYOUTS.values() else 2
    except (ValueError, TypeError):
        c.update(interval=1800, screen=-1, layout=2)
    return c

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                     prefix=path.name+'.', delete=False) as stream:
        temp=Path(stream.name)
        json.dump(data,stream,ensure_ascii=False,indent=2)
    try:temp.replace(path)
    finally:
        if temp.exists():temp.unlink()

def save(c):
    write_json(CONFIG/'settings.json', c)

def collection(c):
    manifest = read_json(DATA/'collection.json', [])
    meta = {x['file']: x for x in manifest if isinstance(x, dict) and 'file' in x}
    found = {}
    for root in [DATA] + [Path(x) for x in c['folders']]:
        if not root.is_dir():
            continue
        # Folder scan is intentionally nonrecursive and never follows directory symlinks.
        try:
            paths = list(root.iterdir())
        except OSError:
            continue
        for p in paths:
            if p.suffix.lower() not in EXTENSIONS or not p.is_file():
                continue
            from PyQt6.QtGui import QImageReader
            if not QImageReader(str(p)).canRead():
                continue
            p = p.resolve()
            entry = meta.get(p.name, {}) if root == DATA else {}
            name = entry.get('title', p.stem.replace('_', ' ').replace('-', ' ').title())
            found[str(p)] = dict(path=str(p), title=name, place=entry.get('place', ''),
                                bundled=root == DATA, category=entry.get('category', ''), generated=entry.get('generated', False))
    return sorted(found.values(), key=lambda e: e['title'].casefold())

def next_image(entries, c, previous):
    paths = [e['path'] for e in entries if not c['favourites_only'] or e['path'] in c['favourites']]
    if not paths:
        return None
    if c['shuffle']:
        return random.choice([p for p in paths if p != previous] or paths)
    return paths[(paths.index(previous)+1) % len(paths)] if previous in paths else paths[0]

def wallpaper_script(path, screen=-1, layout=2):
    p = Path(path).resolve()
    if not p.is_file() or p.suffix.lower() not in EXTENSIONS:
        raise ValueError('The image is missing or its format is unsupported.')
    # JSON quoting prevents filenames from being interpreted as JavaScript.
    uri = json.dumps(p.as_uri())
    screen, layout = int(screen), int(layout)
    if screen < -1 or layout not in LAYOUTS.values():
        raise ValueError('Invalid screen or layout.')
    return '''(function(){var ds=desktopsForActivity(currentActivity());var count=0;
for(var i=0;i<ds.length;i++){var d=ds[i];if(d.screen<0)continue;
if(SCREEN<0||d.screen===SCREEN){d.wallpaperPlugin="org.kde.image";
d.currentConfigGroup=["Wallpaper","org.kde.image","General"];
d.writeConfig("Image",URI);d.writeConfig("FillMode",LAYOUT);count++;}}
print("JATAYU_OK:"+count);})();'''.replace('SCREEN', str(screen)).replace('URI', uri).replace('LAYOUT', str(layout))

SCREENS_SCRIPT = '''(function(){var ds=desktopsForActivity(currentActivity());var r=[];var seen={};
for(var i=0;i<ds.length;i++){var n=ds[i].screen;if(n>=0&&!seen[n]){seen[n]=true;r.push(n);}}
print("JATAYU_SCREENS:"+JSON.stringify(r));})();'''

HELP = '''<h2>Jatayu Wallpaper Changer</h2>
<p>Select an image and choose <b>Apply Wallpaper</b>. Use the display selector for all screens or one screen in your current KDE Activity. This changes the desktop, not the lock screen or login screen.</p>
<p><b>Gallery:</b> Use Previous and Next below the gallery to browse all pages. Search checks the entire collection, not just the current page. Nine cards appear on each page.</p>
<p><b>Favourites:</b> Select an image and press the heart button. Search matches place names and filenames. Add folder imports a folder by reference, without moving or changing its files.</p>
<p><b>Auto change:</b> Enable automatic rotation and select an interval. A small background process continues after closing the window. Turn Auto change off to stop it and remove its login startup entry. It does not run as root.</p>
<p><b>Slideshow:</b> Choose shuffle, favourites only, and change at login. Shuffle avoids the previous image when more than one is available. Missing files are skipped. With no valid favourites, favourites-only rotation pauses.</p>
<p><b>Layouts:</b> Fill crops to cover the screen. Fit may add borders. Stretch changes proportions. Centre shows the original size. The preview is an image preview; the final crop depends on your monitor.</p>
<p><b>Requirements:</b> Debian 13 with KDE Plasma 6, Python 3 and PyQt6. Run in your normal logged-in Plasma session. Other desktops are not supported in this release. First installation may download missing dependencies; operation is offline.</p>
<p><b>Troubleshooting:</b> If Plasma is unavailable, log into a KDE Plasma session and retry. If a monitor is unplugged, click Refresh screens. For package-manager lock errors, close Discover and wait for updates to finish; never delete lock files.</p>
<p><b>Your collection:</b> 24 AI-generated Indian destination, nature, mountain, coast, desert and space scenes. All bundled PNG files are 1920 × 1080 Full HD exports resized from 1672 × 941 generated masters. These are artistic scenes, not photographs of verified locations. The complete generation prompts and original masters are supplied in the source bundle.</p>
<p><b>Privacy:</b> No accounts, downloads, telemetry or network requests. Settings are stored under ~/.config/jatayu-wallpaper. Removing the app preserves personal settings and external images.</p>'''
