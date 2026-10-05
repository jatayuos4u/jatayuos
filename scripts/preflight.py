#!/usr/bin/env python3
"""Fail before a long build for invalid syntax, missing files or unavailable packages."""
import argparse, ast, hashlib, pathlib, subprocess, sys, json, tempfile, tarfile, importlib.util, shlex, xml.etree.ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(); p.add_argument('--apt',action='store_true'); a=p.parse_args()
errors=[]
for name in ('apps/user-defaults.py','overlay/etc/skel/.config/plasma-workspace/env/00-jatayu-places.sh','overlay/usr/share/firefox-esr/browser/defaults/preferences/jatayu.js','assets/fastfetch-jatayu.txt'):
    if not (ROOT/name).is_file():errors.append('Missing desktop fix: '+name)
for f in ROOT.rglob('*.py'):
    if 'build' not in f.relative_to(ROOT).parts:
        try: ast.parse(f.read_text(), filename=str(f))
        except SyntaxError as e: errors.append(str(e))
for f in [*ROOT.glob('*.sh'),*ROOT.glob('scripts/*.sh'),*ROOT.glob('hooks/*')]:
    if subprocess.run(['bash','-n',str(f)],capture_output=True).returncode: errors.append(f'Shell syntax: {f}')
for f in ['apps/app.py','apps/engine.py','apps/webapp.py','scripts/jatayu-webapp','scripts/jatayu-admin','assets/wallpaper.jpg','assets/logo.png','assets/boot-splash.png','assets/plymouth-logo.png','assets/india-tricolor.png','scripts/prepare-boot-art.py','scripts/jatayu-live-installer','jatayu-tools_2.0.2_all.deb']:
    if not (ROOT/f).is_file(): errors.append(f'Missing {f}')
deb=ROOT/'jatayu-tools_2.0.2_all.deb'
if deb.is_file() and hashlib.sha256(deb.read_bytes()).hexdigest() != '1482544a10ec927187566396067d94009eff00b7c4866cf805d809b46f515235':
    errors.append('Jatayu Tools package checksum mismatch')
for slug in ('kavach','sarkar-setu','utsav'):
    if not (ROOT/f'assets/{slug}.html').is_file(): errors.append(f'Missing web app: {slug}')
    desktop=ROOT/f'overlay/usr/share/applications/org.jatayu.{slug}.desktop'
    if a.apt and (not desktop.is_file() or f'Exec=jatayu-webapp {slug}\n' not in desktop.read_text()):
        errors.append(f'Invalid web app launcher: {slug}')
branding=ROOT/'overlay/etc/calamares/branding/jatayu/branding.desc'
if a.apt and branding.is_file():
    import yaml
    settings=yaml.safe_load(branding.read_text())
    if settings.get('slideshow') != 'show.qml' or settings.get('slideshowAPI') != 2:
        errors.append('Invalid Jatayu installation slideshow configuration')
# Keep the six-slide presentation and its reusable card in every package.
show=ROOT/'overlay/etc/calamares/branding/jatayu/show.qml'
card=show.with_name('JatayuCard.qml')
if not show.is_file() or show.read_text().count('    Slide {') != 6:
    errors.append('Missing six-slide installer presentation')
if not card.is_file(): errors.append('Missing installer slide card')
# Wallpaper pieces and metadata are mandatory even for the fast source check.
layout=ROOT/'overlay/usr/share/plasma/look-and-feel/org.jatayu.desktop/contents/layouts/org.kde.plasma.desktop-layout.js'
if layout.is_file() and 'applications:firefox-esr.desktop' not in layout.read_text():errors.append('Firefox ESR dock launcher is missing')
manifest=json.loads((ROOT/'vendor/wallpaper-package.json').read_text())
digest=hashlib.sha256();total=0
for part in manifest['parts']:
    path=ROOT/part['file']
    if not path.is_file():errors.append('Missing wallpaper part: '+part['file']);continue
    data=path.read_bytes();digest.update(data);total+=len(data)
    if len(data)!=part['size'] or hashlib.sha256(data).hexdigest()!=part['sha256']:
        errors.append('Invalid wallpaper part: '+part['file'])
if total!=manifest['size'] or digest.hexdigest()!=manifest['sha256']:
    errors.append('Wallpaper complete-package checksum mismatch')
for name in ('USER-MANUAL.pdf','FAQ.pdf','INSTALLATION-GUIDE.pdf'):
    path=ROOT/'assets'/name
    if not path.is_file() or not path.read_bytes().startswith(b'%PDF-'):
        errors.append('Missing or invalid offline PDF: '+name)
# Final-version integration and regenerated illustrated guides must agree.
package_script=(ROOT/'scripts/package.sh').read_text()
build_script=(ROOT/'scripts/build.sh').read_text()
if 'Version: 1.0\n' not in package_script:
    errors.append('Final integration package version must be 1.0')
if 'out/jatayu-integration_1.0_all.deb' not in package_script or 'out/jatayu-integration_1.0_all.deb' not in build_script:
    errors.append('Integration package output/copy paths must match version 1.0')
if 'python3 scripts/generate-documentation.py' not in build_script:
    errors.append('Offline guides must regenerate before packaging')
if 'python3-reportlab' not in build_script:
    errors.append('Offline guide generator dependency is missing')
for name in ('GPL-3','copyright'):
    if not (ROOT/'overlay/usr/share/doc/jatayu-integration'/name).is_file():
        errors.append('Missing integration license material: '+name)
for name in ('boot-menu.png','plymouth-screen.png','Welcome-screen.png','desktop.png','Menu(1).png','jatayu-tools.png','walpaper-changer.png','kavach-app.png','sarkar-setu.png','utsav-app.png'):
    if not (ROOT/'docs/screenshots/build35'/name).is_file():
        errors.append('Missing illustrated guide capture: '+name)
# package.sh installs assets/* into /usr/share/jatayu. Validate the smoke-test
# input before source compilation or live-build can spend runner minutes.
for hook in (ROOT/'hooks').glob('*.hook.chroot'):
    for line in hook.read_text().splitlines():
        words=shlex.split(line, comments=True)
        if words and words[0]=='mksquashfs':
            sources=words[1:words.index(next(w for w in words[1:] if w.endswith('.squashfs')))]
            for source in sources:
                if source.startswith('/usr/share/jatayu/'):
                    asset=ROOT/'assets'/source.removeprefix('/usr/share/jatayu/')
                    if not asset.is_file():errors.append(f'Missing hook input: {source} ({hook.name})')
for name in ('ABOUT.html','kavach.svg','sarkar-setu.svg','utsav.svg'):
    if not (ROOT/'assets'/name).is_file():errors.append('Missing '+name)
for path in (ROOT/'overlay').rglob('*.desktop'):
    if not path.is_file():continue
    text=path.read_text()
    if '[Desktop Entry]' not in text or 'Type=' not in text or 'Name=' not in text:
        errors.append('Invalid desktop entry: '+str(path))
for path in (ROOT/'overlay/etc/xdg/menus').rglob('*.menu'):
    try:ET.parse(path)
    except ET.ParseError:errors.append('Invalid menu XML: '+str(path))
for path in ('apps/app.py','apps/configure-image.py','auto-config.sh','scripts/generate-files.py'):
    if 'Development Preview' in (ROOT/path).read_text() or 'development preview' in (ROOT/path).read_text():
        errors.append('Outdated user-facing branding: '+path)
packages=[s.strip() for s in (ROOT/'packages.list').read_text().splitlines() if s.strip() and not s.startswith('#')]
for name in ('user-setup','sddm-theme-breeze','papirus-icon-theme','libreoffice','python3-pyqt6','waydroid','xdg-user-dirs','upower','systemd-timesyncd','xdg-desktop-portal','xdg-desktop-portal-kde','os-prober','ntfs-3g','kio-extras','kimageformat6-plugins','kdegraphics-thumbnailers','ffmpegthumbs','qt6-image-formats-plugins'):
    if name not in packages: errors.append(f'Missing live-login package: {name}')
# Default previews and cache initialization must survive future build edits.
preview=ROOT/'overlay/etc/skel/.local/share/dolphin/view_properties/global/.directory'
if not preview.is_file() or 'PreviewsShown=true' not in preview.read_text():
    errors.append('Dolphin default image previews are missing')
defaults=(ROOT/'apps/user-defaults.py').read_text()
if "cache/'thumbnails'/name" not in defaults or defaults.index("cache/'thumbnails'/name") > defaults.index('if marker.exists():return'):
    errors.append('Thumbnail cache must initialize before the Places marker check')
if (ROOT/'overlay/etc/skel/.cache').exists():
    errors.append('Do not ship runtime caches in the default user skeleton')
if a.apt:
    for name in packages:
        r=subprocess.run(['apt-cache','policy',name],text=True,capture_output=True)
        if 'Candidate:' not in r.stdout or 'Candidate: (none)' in r.stdout: errors.append(f'Unavailable package: {name}')
if a.apt and not errors:
    spec=importlib.util.spec_from_file_location('prepare_wallpaper',ROOT/'scripts/prepare-wallpaper.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    deb=module.prepare()
    for field,expected in [('Package','jatayu-wallpaper'),('Version','1.2.1'),('Architecture','all')]:
        value=subprocess.check_output(['dpkg-deb','-f',str(deb),field],text=True).strip()
        if value!=expected:errors.append('Wallpaper metadata mismatch: '+field)
    result=subprocess.run(['apt-get','--simulate','--no-install-recommends','install',*packages,str(deb),str(ROOT/'jatayu-tools_2.0.2_all.deb')],text=True,capture_output=True)
    report=ROOT/'out/precheck-dependencies.txt';report.parent.mkdir(exist_ok=True);report.write_text(result.stdout+result.stderr)
    if result.returncode:errors.append('APT dependency simulation failed; see out/precheck-dependencies.txt')
    for package,version in [('calamares','3.3.14-1'),('fcitx5','5.1.12-2')]:
        result=subprocess.run(['apt-cache','showsrc',package],text=True,capture_output=True)
        if 'Version: '+version+'\n' not in result.stdout:errors.append('Missing pinned source version: '+package+'='+version)
    for name in ('USER-MANUAL.pdf','FAQ.pdf','INSTALLATION-GUIDE.pdf'):
        if subprocess.run(['pdfinfo',str(ROOT/'assets'/name)],capture_output=True).returncode:
            errors.append('Unreadable PDF: '+name)
# Keep the validated UTF-8 session defaults in both KDE and the image hook.
locale_defaults=ROOT/'overlay/etc/skel/.config/plasma-localerc'
if not locale_defaults.is_file() or any(value not in locale_defaults.read_text().splitlines() for value in ('LANG=en_IN.UTF-8','LC_CTYPE=en_IN.UTF-8')):
    errors.append('Missing explicit UTF-8 KDE session defaults')
if 'update-locale LANG=en_IN.UTF-8 LC_CTYPE=en_IN.UTF-8' not in (ROOT/'hooks/0900-jatayu.hook.chroot').read_text():
    errors.append('Missing explicit UTF-8 system locale defaults')
# Lock the automatic time provider and approved Fastfetch configuration.
image_hook=(ROOT/'hooks/0900-jatayu.hook.chroot').read_text()
if not any(line.startswith('systemctl enable ') and 'systemd-timesyncd' in shlex.split(line)[2:] for line in image_hook.splitlines()):
    errors.append('Automatic time synchronization must be enabled in the image hook')
if not any(line.startswith('test -f ') and line.endswith('/systemd-timesyncd.service') for line in image_hook.splitlines()):
    errors.append('Image hook must verify the time synchronization service exists')
for value in ("assert data.get('modules')", "'source':'/usr/share/jatayu/fastfetch-jatayu.txt'"):
    if value not in image_hook:
        errors.append('Missing locked Fastfetch default modules or logo: '+value)
print(f'Checked Python/shell syntax, required assets and {len(packages)} package declarations.')
if errors: print('\n'.join(errors),file=sys.stderr); sys.exit(1)
print(('APT dependency and source precheck PASS' if a.apt else 'Static precheck PASS') + '; boot/install testing remains required.')
