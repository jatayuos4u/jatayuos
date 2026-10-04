#!/usr/bin/env python3
"""Inspect the assembled root before publishing a candidate artifact."""
from pathlib import Path
import sys, yaml, json
root=Path(sys.argv[1])
def read(name):return (root/name.lstrip('/')).read_text()
def config(name):return yaml.safe_load(read('/etc/calamares/'+name))
partition=config('modules/partition.conf')
assert partition['allowManualPartitioning'] is True
assert partition['initialPartitioningChoice']=='none'
assert partition['efi']['mountPoint']=='/boot/efi'
boot=config('modules/bootloader.conf')
assert boot['efiBootloaderId']=='JatayuOS'
assert boot['installEFIFallback'] is False
settings=config('settings.conf')
assert settings['branding']=='jatayu' and settings['prompt-install'] is True
assert 'GRUB_DISABLE_OS_PROBER=false' in read('/etc/default/grub.d/jatayu.cfg')
assert 'GRUB_TIMEOUT=8' in read('/etc/default/grub.d/jatayu.cfg')
for file in ('usr/bin/os-prober','usr/sbin/grub-install','usr/lib/grub/x86_64-efi/modinfo.sh','usr/lib/grub/i386-pc/modinfo.sh','usr/share/dbus-1/system-services/org.freedesktop.UPower.service','usr/share/xdg-desktop-portal/portals/kde.portal'):
    assert (root/file).is_file(), file
for name in ('USER-MANUAL.pdf','FAQ.pdf','INSTALLATION-GUIDE.pdf'):
    assert (root/'usr/share/jatayu'/name).read_bytes().startswith(b'%PDF-'),name
assert 'JatayuOS Installation Guide.pdf' in read('/usr/share/jatayu/app.py')
assert 'browser.tabs.inTitlebar", 0' in read('/usr/share/firefox-esr/browser/defaults/preferences/jatayu.js') or 'browser.tabs.inTitlebar",0' in read('/usr/share/firefox-esr/browser/defaults/preferences/jatayu.js')
ff=json.loads(read('/etc/skel/.config/fastfetch/config.jsonc'))
assert ff['logo']['source']=='/usr/share/jatayu/fastfetch-jatayu.txt' and ff['modules']
assert config('branding/jatayu/branding.desc')['slideshow']=='show.qml'
assert read('/etc/calamares/branding/jatayu/show.qml').count('    Slide {')==6
# The actual enabled unit must survive into the installed filesystem.
assert (root/'usr/lib/systemd/system/systemd-timesyncd.service').is_file()
link=root/'etc/systemd/system/sysinit.target.wants/systemd-timesyncd.service'
assert link.is_symlink(), 'Automatic time synchronization is not enabled'
assert str(link.readlink()).endswith('/systemd-timesyncd.service')
# Verify shipped KDE defaults and the generated system locale, not just source.
import configparser
regional=configparser.ConfigParser(interpolation=None)
regional.read(root/'etc/skel/.config/plasma-localerc')
assert regional['Formats']['LANG']=='en_IN.UTF-8'
assert regional['Formats']['LC_CTYPE']=='en_IN.UTF-8'
system_locale=read('/etc/default/locale')
for key in ('LANG','LC_CTYPE'):
    values=[line.split('=',1)[1].strip().strip('"') for line in system_locale.splitlines() if line.startswith(key+'=')]
    assert values==['en_IN.UTF-8'], 'Incorrect system locale: '+key
print('Assembled image installer, bootloader, desktop service, branding and help checks PASS.')
