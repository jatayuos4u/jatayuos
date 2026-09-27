#!/usr/bin/env python3
"""Generate original configuration/artwork; no downloaded artwork is embedded."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def put(name,text):
    p=R/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
put('assets/logo.svg','''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256"><rect width="256" height="256" rx="52" fill="#10212d"/><path d="M45 62h166L128 217z" fill="none" stroke="#e5b866" stroke-width="9"/><text x="128" y="151" text-anchor="middle" font-family="sans-serif" font-size="96" fill="#e5b866">J</text></svg>''')
put('assets/wallpaper.svg','''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#10293c"/><stop offset="1" stop-color="#050e18"/></linearGradient><linearGradient id="gold"><stop stop-color="#a86f26"/><stop offset="1" stop-color="#ffd88b"/></linearGradient></defs><rect width="1920" height="1080" fill="url(#bg)"/><path d="M0 850 Q600 550 1920 900 M0 910 Q650 600 1920 960" fill="none" stroke="url(#gold)" stroke-width="2" opacity=".5"/><text x="1140" y="435" text-anchor="middle" fill="#fff" font-family="sans-serif" font-size="108">JatayuOS</text><text x="1140" y="505" text-anchor="middle" fill="#e5b866" font-family="sans-serif" font-size="30">Udaan Aapki. Shakti Bharat Ki.</text><text x="70" y="1000" fill="#8096a7" font-family="sans-serif" font-size="20">Development artwork • Approved eagle wallpaper awaiting clean source and rights verification</text></svg>''')
# Nine-part Plasma frame, using original simple vector shapes.
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="140" height="100">','<rect id="center" x="20" y="20" width="60" height="40" fill="#10212d"/>']
for name,x,y,w,h in [('top',20,10,60,10),('bottom',20,60,60,10),('left',10,20,10,40),('right',80,20,10,40),('topleft',10,10,10,10),('topright',80,10,10,10),('bottomleft',10,60,10,10),('bottomright',80,60,10,10)]:
    parts.append(f'<rect id="{name}" x="{x}" y="{y}" width="{w}" height="{h}" fill="#10212d" stroke="#bc9652" stroke-width="1"/>')
parts.extend(['<rect id="hint-top-margin" width="1" height="8"/><rect id="hint-bottom-margin" width="1" height="8"/><rect id="hint-left-margin" width="8" height="1"/><rect id="hint-right-margin" width="8" height="1"/>','</svg>'])
put('assets/panel-background.svg',''.join(parts))
apps=[('welcome','Aarambh','Start-here','System;'),('update','Jatayu Update','system-software-update','System;'),('backup','Jatayu Sanjeevani','document-save','System;'),('check','Jaanch','dialog-information','System;'),('language','Bhasa Setu','preferences-desktop-locale','Settings;'),('portals','Sarkar Setu','internet-web-browser','Network;'),('tools','Jatayu Tools','applications-graphics','Graphics;'),('android','Android Setup','phone','System;'),('about','About JatayuOS','help-about','System;')]
for mode,title,icon,categories in apps:
    put(f'overlay/usr/share/applications/org.jatayu.{mode}.desktop',f'[Desktop Entry]\nType=Application\nName={title}\nComment=JatayuOS {title}\nExec=jatayu {mode}\nIcon={icon.lower()}\nTerminal=false\nCategories={categories}\nStartupNotify=true\n')
put('overlay/etc/xdg/autostart/org.jatayu.welcome.desktop','[Desktop Entry]\nType=Application\nName=JatayuOS Welcome\nExec=jatayu autostart\nOnlyShowIn=KDE;\nX-KDE-autostart-phase=2\n')
put('overlay/usr/share/polkit-1/actions/org.jatayu.admin.policy','''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE policyconfig PUBLIC "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN" "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd"><policyconfig><action id="org.jatayu.admin"><description>Manage selected Jatayu software and live-session settings</description><message>Authentication is required for this Jatayu action</message><defaults><allow_any>no</allow_any><allow_inactive>no</allow_inactive><allow_active>auth_admin</allow_active></defaults><annotate key="org.freedesktop.policykit.exec.path">/usr/libexec/jatayu-admin</annotate></action></policyconfig>''')
put('overlay/etc/skel/.config/kdeglobals','''[General]
ColorScheme=BreezeDark
BrowserApplication=firefox-esr.desktop
[KDE]
LookAndFeelPackage=org.jatayu.desktop
SingleClick=false
[Icons]
Theme=breeze-dark
''')
put('overlay/etc/skel/.config/plasmarc','[Theme]\nname=jatayu\n')
put('overlay/etc/skel/.config/baloofilerc','[Basic Settings]\nIndexing-Enabled=false\n')
put('overlay/etc/skel/.config/kwinrc','[Plugins]\nblurEnabled=false\ncontrastEnabled=false\n')
put('overlay/etc/skel/.config/mimeapps.list','[Default Applications]\nx-scheme-handler/http=firefox-esr.desktop\nx-scheme-handler/https=firefox-esr.desktop\ntext/html=firefox-esr.desktop\n')
base='overlay/usr/share/plasma/look-and-feel/org.jatayu.desktop/'
put(base+'metadata.json',json.dumps({'KPlugin':{'Id':'org.jatayu.desktop','Name':'JatayuOS','Description':'JatayuOS development layout','Version':'0.1','Authors':[{'Name':'Anup Yadav'}]},'KPackageStructure':'Plasma/LookAndFeel'},indent=2))
put(base+'contents/defaults','[kdeglobals][General]\nColorScheme=BreezeDark\n[kdeglobals][KDE]\nwidgetStyle=Breeze\n[plasmarc][Theme]\nname=jatayu\n')
put(base+'contents/layouts/org.kde.plasma.desktop-layout.js','''var panel = new Panel;
panel.location = "bottom";
panel.height = 52;
panel.floating = true;
var launcher = panel.addWidget("org.kde.plasma.kickoff");
launcher.currentConfigGroup = ["General"];
launcher.writeConfig("icon", "/usr/share/jatayu/logo.svg");
launcher.writeConfig("favorites", "org.jatayu.welcome.desktop,org.kde.discover.desktop,systemsettings.desktop,org.jatayu.tools.desktop,firefox-esr.desktop,org.kde.dolphin.desktop");
var tasks = panel.addWidget("org.kde.plasma.icontasks");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", "applications:org.kde.dolphin.desktop,applications:firefox-esr.desktop,applications:org.kde.konsole.desktop,applications:org.jatayu.tools.desktop,applications:systemsettings.desktop");
panel.addWidget("org.kde.plasma.systemtray");
panel.addWidget("org.kde.plasma.digitalclock");
panel.addWidget("org.kde.plasma.showdesktop");
var ds = desktops();
for (var i=0; i<ds.length; i++) {
  ds[i].wallpaperPlugin="org.kde.image";
  ds[i].currentConfigGroup=["Wallpaper","org.kde.image","General"];
  ds[i].writeConfig("Image","file:///usr/share/jatayu/wallpaper.svg");
}
''')
brand='overlay/etc/calamares/branding/jatayu/'
put(brand+'branding.desc','''componentName: jatayu
welcomeStyleCalamares: true
welcomeExpandingLogo: true
windowExpanding: normal
windowSize: 900px,650px
windowPlacement: center
strings:
  productName: JatayuOS
  shortProductName: JatayuOS
  version: "0.1 Development"
  shortVersion: "0.1"
  versionedName: JatayuOS 0.1 Development
  shortVersionedName: JatayuOS 0.1
  bootloaderEntryName: JatayuOS
images:
  productLogo: logo.svg
  productIcon: logo.svg
  productWelcome: logo.svg
style:
  SidebarBackground: "#10212d"
  SidebarText: "#ffffff"
  SidebarTextCurrent: "#ffd17b"
''')
put(brand+'logo.svg',(R/'assets/logo.svg').read_text())
put('overlay/usr/share/plymouth/themes/jatayu/jatayu.plymouth','[Plymouth Theme]\nName=JatayuOS\nDescription=JatayuOS development boot theme\nModuleName=script\n[script]\nImageDir=/usr/share/plymouth/themes/jatayu\nScriptFile=/usr/share/plymouth/themes/jatayu/jatayu.script\n')
put('overlay/usr/share/plymouth/themes/jatayu/jatayu.script','''Window.SetBackgroundTopColor(0.025,0.055,0.09);
Window.SetBackgroundBottomColor(0.025,0.055,0.09);
title.image = Image.Text("JatayuOS", 1, 0.8, 0.45);
title.sprite = Sprite(title.image);
title.sprite.SetPosition(Window.GetWidth()/2-title.image.GetWidth()/2,Window.GetHeight()/2-55,10);
message.sprite = Sprite();
fun show_message(text) {
  message.image = Image.Text(text, 1, 1, 1);
  message.sprite.SetImage(message.image);
  message.sprite.SetPosition(Window.GetWidth()/2-message.image.GetWidth()/2,Window.GetHeight()/2+20,10);
}
fun normal() { show_message("Udaan Aapki. Shakti Bharat Ki."); }
fun password(prompt, bullets) {
  text = prompt + " ";
  for (i=0; i<bullets; i++) text += "*";
  show_message(text);
}
fun question(prompt, entry) { show_message(prompt + " " + entry); }
Plymouth.SetDisplayNormalFunction(normal);
Plymouth.SetDisplayPasswordFunction(password);
Plymouth.SetDisplayQuestionFunction(question);
Plymouth.SetMessageFunction(show_message);
normal();
''')
put('assets/README.txt','''JatayuOS 0.1 development preview
Created for Anup Yadav. Based on Debian and KDE; Firefox retains Mozilla identity.
This integrated source kit is not a tested ISO or production release.
The original code-drawn placeholder artwork is deliberate: approved eagle artwork needs clean source files and rights verification.
The desktop uses standard Kickoff and a themed panel. Pixel-identical custom menu and angled sections remain pending.
All seven Jatayu app entry points are supplied, but scope limits are shown inside each app.
See README.md, docs/STATUS.md and docs/COMPLIANCE.md in the build kit.
''')
put('overlay/usr/share/doc/jatayu-integration/copyright','''JatayuOS integration development source
Project maintainer: Anup Yadav <jatayuos4u@gmail.com>
Original code and original placeholder artwork were prepared for this project.
The owner's final publication licence has not yet been selected. This is a private
development handoff, not a blanket licence for upstream components.
Debian, KDE, Qt, Calamares, Firefox and all dependencies retain their own licences
and notices under /usr/share/doc. The image build preserves those notices.
Do not publicly redistribute before completing docs/COMPLIANCE.md.
''')
print('Generated original assets, desktop integration, policies and installer branding.')
