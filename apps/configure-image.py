#!/usr/bin/env python3
"""One-time image configuration. Upstream installer sequencing is preserved."""
from pathlib import Path
import shutil, subprocess, yaml, json
def write(p,s):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
def edit_yaml(p,fn):
    p=Path(p);d=yaml.safe_load(p.read_text());fn(d);p.write_text(yaml.safe_dump(d,sort_keys=False))

if not Path('/etc/calamares/settings.conf').exists():raise SystemExit('Missing Debian Calamares configuration')
edit_yaml('/etc/calamares/settings.conf',lambda d:d.update({'branding':'jatayu','prompt-install':True}))
def welcome(d):
    d['requirements']['requiredStorage']=25
    d['requirements']['requiredRam']=1.5
    d['requirements']['required']=[x for x in d['requirements']['required'] if x!='internet']
    d['showSupportUrl']=False;d['showKnownIssuesUrl']=False;d['showReleaseNotesUrl']=False
edit_yaml('/etc/calamares/modules/welcome.conf',welcome)
edit_yaml('/etc/calamares/modules/bootloader.conf',lambda d:d.update({'efiBootloaderId':'JatayuOS','installEFIFallback':False}))
# Debian's helper apt-installs mutually exclusive grub metapackages during install.
# Our ISO already includes grub2-common and BOTH platform binary sets, so this
# independent helper avoids needing network or a local apt medium to fetch them.
helper='/usr/share/calamares/helpers/calamares-bootloader-config'
subprocess.run(['dpkg-divert','--local','--add','--rename',helper],check=True)
write(helper,'#!/bin/sh\nset -e\ntest -x /usr/sbin/grub-install\ntest -d /usr/lib/grub/x86_64-efi\ntest -d /usr/lib/grub/i386-pc\necho "JatayuOS: platform GRUB binaries are already included for offline installation."\n')
Path(helper).chmod(0o755)
# Identity: explicitly divert base-files entries rather than unmanaged overwrites.
identity='NAME="JatayuOS"\nPRETTY_NAME="JatayuOS 0.1 Development (Debian 13)"\nID=jatayuos\nID_LIKE=debian\nVERSION_ID="0.1"\nVERSION="0.1 Development"\nVERSION_CODENAME=trixie\nDEBIAN_CODENAME=trixie\n'
for p in ['/etc/os-release','/usr/lib/os-release']:
    # live-build/debootstrap already diverts /etc/os-release to its own
    # .debootstrap path. Preserve that registered diversion; dpkg rejects a
    # second one with a different target.
    existing=subprocess.run(['dpkg-divert','--list',p],check=True,capture_output=True,text=True).stdout
    if not existing.strip():
        subprocess.run(['dpkg-divert','--local','--add','--rename',p],check=True)
    write(p,identity)
write('/etc/default/grub.d/jatayu.cfg','GRUB_DISTRIBUTOR="JatayuOS"\nGRUB_DISABLE_OS_PROBER=false\nGRUB_CMDLINE_LINUX_DEFAULT="quiet splash"\n')
# Live-only installer shortcut creation is delegated to our autostart.
write('/etc/xdg/autostart/calamares-desktop-icon.desktop','[Desktop Entry]\nType=Application\nName=Installer shortcut\nHidden=true\n')
for name in ['org.kde.plasma-welcome.desktop','plasma-welcome.desktop']:
    write('/etc/xdg/autostart/'+name,'[Desktop Entry]\nType=Application\nName=Welcome\nHidden=true\n')
write('/etc/sddm.conf.d/20-jatayu.conf','[Theme]\nCurrent=breeze\n[General]\nInputMethod=\n')
# The selected greeter must exist. SDDM silently falls back to its built-in
# theme when Recommends are disabled and sddm-theme-breeze is omitted.
if not Path('/usr/share/sddm/themes/breeze/theme.conf').exists():
    raise SystemExit('Breeze SDDM theme missing; install sddm-theme-breeze')
write('/usr/share/sddm/themes/breeze/theme.conf.user','[General]\nbackground=/usr/share/jatayu/wallpaper.svg\nshowlogo=hidden\n')
write('/etc/default/zramswap','ALGO=lz4\nPERCENT=50\nPRIORITY=100\n')
write('/etc/sysctl.d/80-jatayu.conf','vm.swappiness=100\n')
write('/etc/apt/apt.conf.d/20auto-upgrades','APT::Periodic::Update-Package-Lists "1";\nAPT::Periodic::Unattended-Upgrade "1";\n')
write('/etc/apt/apt.conf.d/52jatayu-unattended','Unattended-Upgrade::Origins-Pattern { "origin=Debian,codename=trixie-security,label=Debian-Security"; };\nUnattended-Upgrade::Automatic-Reboot "false";\n')
# Build-time configuration only; activation applies on subsequent boot.
subprocess.run(['ufw','default','deny','incoming'],check=True)
subprocess.run(['ufw','default','allow','outgoing'],check=True)
p=Path('/etc/ufw/ufw.conf');p.write_text(p.read_text().replace('ENABLED=no','ENABLED=yes'))
subprocess.run(['systemctl','enable','ufw','zramswap'],check=True)
# A custom theme inherits a complete shipped Breeze style; modifications are
# limited to the original panel artwork and metadata supplied by Jatayu.
dst=Path('/usr/share/plasma/desktoptheme/jatayu')
src=Path('/usr/share/plasma/desktoptheme/default')
if not src.exists():raise SystemExit('Breeze theme not found; inspect plasma-desktoptheme packaging')
shutil.copytree(src,dst,dirs_exist_ok=True)
shutil.copyfile('/usr/share/jatayu/panel-background.svg',dst/'widgets/panel-background.svg')
old=dst/'widgets/panel-background.svgz'
if old.exists():old.unlink()
meta=dst/'metadata.json'
if meta.exists():
    d=json.loads(meta.read_text());d.setdefault('KPlugin',{}).update({'Id':'jatayu','Name':'JatayuOS (Breeze-derived)'});meta.write_text(json.dumps(d,indent=2))
print('Jatayu image integration configured. VM installation tests remain required.')
