#!/usr/bin/env python3
"""Generate Jatayu desktop configuration from committed owner-approved assets."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def put(name,text):
    p=R/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
# The owner-supplied shield is committed as assets/logo.png.
# The approved 1920x1080 eagle wallpaper is committed as assets/wallpaper.jpg.
# Bootloader artwork is committed as assets/boot-splash.png.
# Nine-part Plasma frame, using original simple vector shapes.
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="140" height="100">','<rect id="center" x="20" y="20" width="60" height="40" fill="#10212d"/>']
for name,x,y,w,h in [('top',20,10,60,10),('bottom',20,60,60,10),('left',10,20,10,40),('right',80,20,10,40),('topleft',10,10,10,10),('topright',80,10,10,10),('bottomleft',10,60,10,10),('bottomright',80,60,10,10)]:
    parts.append(f'<rect id="{name}" x="{x}" y="{y}" width="{w}" height="{h}" fill="#10212d" stroke="#bc9652" stroke-width="1"/>')
parts.extend(['<rect id="hint-top-margin" width="1" height="8"/><rect id="hint-bottom-margin" width="1" height="8"/><rect id="hint-left-margin" width="8" height="1"/><rect id="hint-right-margin" width="8" height="1"/>','</svg>'])
put('assets/panel-background.svg',''.join(parts))
apps=[('welcome','Aarambh - JatayuOS Welcome','/usr/share/jatayu/logo.png','System;'),('tools','Jatayu Editing Tools','jatayu-tools','X-Jatayu-Tools;System;'),('about','About JatayuOS','/usr/share/jatayu/logo.png','System;')]
for mode,title,icon,categories in apps:
    command='jatayu-tools' if mode=='tools' else f'jatayu {mode}'
    put(f'overlay/usr/share/applications/org.jatayu.{mode}.desktop',f'[Desktop Entry]\nType=Application\nName={title}\nComment=JatayuOS {title}\nExec={command}\nIcon={icon}\nTerminal=false\nCategories={categories}\nStartupNotify=true\n')
for mode in ('update','backup','check','language','portals','android'):
    (R/f'overlay/usr/share/applications/org.jatayu.{mode}.desktop').unlink(missing_ok=True)
for name,title,command,icon in (
    ('installer','Install JatayuOS','pkexec /usr/libexec/jatayu-live-installer','/usr/share/jatayu/logo.png'),
    ('faq','JatayuOS FAQ','xdg-open /usr/share/jatayu/FAQ.pdf','help-faq'),
    ('manual','JatayuOS User Manual','xdg-open /usr/share/jatayu/USER-MANUAL.pdf','help-contents')):
    put(f'overlay/usr/share/applications/org.jatayu.{name}.desktop',
        f'[Desktop Entry]\nType=Application\nName={title}\nExec={command}\nIcon={icon}\nTerminal=false\nCategories=System;\n')
put('overlay/etc/xdg/autostart/org.jatayu.welcome.desktop','[Desktop Entry]\nType=Application\nName=JatayuOS Welcome\nExec=jatayu autostart\nOnlyShowIn=KDE;\nX-KDE-autostart-phase=2\n')
put('overlay/usr/share/polkit-1/actions/org.jatayu.admin.policy',"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE policyconfig PUBLIC \"-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN\" \"http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd\">\n<policyconfig>\n  <action id=\"org.jatayu.live-layout\">\n    <description>Set live-session language and keyboard</description>\n    <message>Set JatayuOS live-session language and keyboard</message>\n    <defaults><allow_any>no</allow_any><allow_inactive>no</allow_inactive><allow_active>yes</allow_active></defaults>\n    <annotate key=\"org.freedesktop.policykit.exec.path\">/usr/libexec/jatayu-admin</annotate>\n    <annotate key=\"org.freedesktop.policykit.exec.argv1\">live-layout</annotate>\n  </action>\n  <action id=\"org.jatayu.install\">\n    <description>Install selected software</description>\n    <message>Administrator authentication is required to install software</message>\n    <defaults><allow_any>no</allow_any><allow_inactive>no</allow_inactive><allow_active>auth_admin</allow_active></defaults>\n    <annotate key=\"org.freedesktop.policykit.exec.path\">/usr/libexec/jatayu-admin</annotate>\n    <annotate key=\"org.freedesktop.policykit.exec.argv1\">install</annotate>\n  </action>\n  <action id=\"org.jatayu.refresh\">\n    <description>Refresh package information</description>\n    <message>Administrator authentication is required to refresh packages</message>\n    <defaults><allow_any>no</allow_any><allow_inactive>no</allow_inactive><allow_active>auth_admin</allow_active></defaults>\n    <annotate key=\"org.freedesktop.policykit.exec.path\">/usr/libexec/jatayu-admin</annotate>\n    <annotate key=\"org.freedesktop.policykit.exec.argv1\">refresh</annotate>\n  </action>\n  <action id=\"org.jatayu.live-installer\">\n    <description>Start Calamares in the JatayuOS live session</description>\n    <message>Start the JatayuOS installer</message>\n    <defaults><allow_any>no</allow_any><allow_inactive>no</allow_inactive><allow_active>yes</allow_active></defaults>\n    <annotate key=\"org.freedesktop.policykit.exec.path\">/usr/libexec/jatayu-live-installer</annotate>\n    <annotate key=\"org.freedesktop.policykit.exec.allow_gui\">true</annotate>\n  </action>\n</policyconfig>\n")
put('overlay/etc/skel/.config/kdeglobals','''[General]
ColorScheme=BreezeDark
BrowserApplication=firefox-esr.desktop
[KDE]
LookAndFeelPackage=org.jatayu.desktop
SingleClick=true
[Icons]
Theme=Papirus-Dark
''')
put('overlay/etc/skel/.config/plasmarc','[Theme]\nname=default\n')
put('overlay/etc/skel/.config/baloofilerc','[Basic Settings]\nIndexing-Enabled=false\n')
put('overlay/etc/skel/.config/kwinrc','[Plugins]\nblurEnabled=false\ncontrastEnabled=false\n[Wayland]\nInputMethod=/usr/share/applications/org.fcitx.Fcitx5.desktop\n')
put('overlay/etc/skel/.config/mimeapps.list','[Default Applications]\nx-scheme-handler/http=firefox-esr.desktop\nx-scheme-handler/https=firefox-esr.desktop\ntext/html=firefox-esr.desktop\n')
base='overlay/usr/share/plasma/look-and-feel/org.jatayu.desktop/'
put(base+'metadata.json',json.dumps({'KPlugin':{'Id':'org.jatayu.desktop','Name':'JatayuOS','Description':'JatayuOS Udaan desktop layout','Version':'1.0','Authors':[{'Name':'Anup Yadav'}]},'KPackageStructure':'Plasma/LookAndFeel'},indent=2))
put(base+'contents/defaults','[kdeglobals][General]\nColorScheme=BreezeDark\n[kdeglobals][KDE]\nwidgetStyle=Breeze\n[kdeglobals][Icons]\nTheme=Papirus-Dark\n[plasmarc][Theme]\nname=default\n')
put(base+'contents/layouts/org.kde.plasma.desktop-layout.js',"var panel = new Panel;\npanel.location = \"bottom\";\npanel.height = 54;\npanel.floating = false;\nvar launcher = panel.addWidget(\"org.kde.plasma.kickoff\");\nlauncher.currentConfigGroup = [\"General\"];\nlauncher.writeConfig(\"icon\", \"/usr/share/jatayu/logo.png\");\nvar tasks = panel.addWidget(\"org.kde.plasma.icontasks\");\ntasks.currentConfigGroup = [\"General\"];\ntasks.writeConfig(\"launchers\", [\"applications:org.kde.dolphin.desktop\", \"applications:firefox-esr.desktop\", \"applications:systemsettings.desktop\"]);\npanel.addWidget(\"org.kde.plasma.systemtray\");\npanel.addWidget(\"org.kde.plasma.digitalclock\");\npanel.addWidget(\"org.kde.plasma.showdesktop\");\nvar ds = desktops();\nfor (var i=0; i<ds.length; i++) {\n  ds[i].wallpaperPlugin=\"org.kde.image\";\n  ds[i].currentConfigGroup=[\"Wallpaper\",\"org.kde.image\",\"General\"];\n  ds[i].writeConfig(\"Image\",\"file:///usr/share/jatayu/wallpaper.jpg\");\nds[i].writeConfig(\"FillMode\",\"2\");\n}\n")
brand='overlay/etc/calamares/branding/jatayu/'
put(brand+'branding.desc','''componentName: jatayu
welcomeStyleCalamares: true
welcomeExpandingLogo: false
windowExpanding: normal
windowSize: 900px,650px
windowPlacement: center
strings:
  productName: JatayuOS
  shortProductName: JatayuOS
  version: "1.0 (Udaan)"
  shortVersion: "1.0"
  versionedName: JatayuOS 1.0 (Udaan)
  shortVersionedName: JatayuOS 1.0
  bootloaderEntryName: JatayuOS
  productUrl: https://jatayuos.in
images:
  productLogo: logo.png
  productIcon: logo.png
  productWelcome: logo.png
slideshow: [ "/etc/calamares/branding/jatayu/logo.png" ]
style:
  SidebarBackground: "#10212d"
  SidebarText: "#ffffff"
  SidebarTextCurrent: "#10212d"
''')

# Opaque animated dots avoid font glyph sizing and remain clear at low resolutions.
from PIL import Image, ImageDraw
for color,name in [('#ff9933','saffron'),('#f5f5f5','white'),('#13884d','green')]:
    im=Image.new('RGBA',(36,36),(0,0,0,0));ImageDraw.Draw(im).ellipse((2,2,33,33),fill=color)
    im.save(R/f'assets/plymouth-dot-{name}.png')
put('overlay/usr/share/plymouth/themes/jatayu/jatayu.plymouth','[Plymouth Theme]\nName=JatayuOS\nDescription=JatayuOS development boot theme\nModuleName=script\n[script]\nImageDir=/usr/share/plymouth/themes/jatayu\nScriptFile=/usr/share/plymouth/themes/jatayu/jatayu.script\n')
put('overlay/usr/share/plymouth/themes/jatayu/jatayu.script','''Window.SetBackgroundTopColor(0.025,0.055,0.09);
Window.SetBackgroundBottomColor(0.025,0.055,0.09);
logo.image = Image("logo.png");
logo.sprite = Sprite(logo.image);
logo.sprite.SetPosition(Window.GetWidth()/2-logo.image.GetWidth()/2, Window.GetHeight()/2-logo.image.GetHeight()/2-47, 10);
saffron.image = Image("plymouth-dot-saffron.png");
white.image = Image("plymouth-dot-white.png");
green.image = Image("plymouth-dot-green.png");
saffron.sprite = Sprite(saffron.image);
white.sprite = Sprite(white.image);
green.sprite = Sprite(green.image);
saffron.sprite.SetPosition(Window.GetWidth()/2-54, Window.GetHeight()/2+105, 10);
white.sprite.SetPosition(Window.GetWidth()/2-18, Window.GetHeight()/2+105, 10);
green.sprite.SetPosition(Window.GetWidth()/2+18, Window.GetHeight()/2+105, 10);
message.sprite = Sprite();
tick = 0;
fun animate() {
  tick += 1;
  phase = tick % 80;
  if (phase < 40) opacity = 0.72 + phase * 0.007;
  else opacity = 1 - (phase - 40) * 0.007;
  logo.sprite.SetOpacity(opacity);
  saffron.sprite.SetOpacity(0.45 + (tick % 45) / 82);
  white.sprite.SetOpacity(0.45 + ((tick + 15) % 45) / 82);
  green.sprite.SetOpacity(0.45 + ((tick + 30) % 45) / 82);
}
fun show_message(text) {
  message.image = Image.Text(text, 1, 1, 1);
  message.sprite.SetImage(message.image);
  message.sprite.SetPosition(Window.GetWidth()/2-message.image.GetWidth()/2, Window.GetHeight()/2+165, 10);
}
fun password(prompt, bullets) {
  text = prompt + " ";
  for (i=0; i<bullets; i++) text += "*";
  show_message(text);
}
fun question(prompt, entry) { show_message(prompt + " " + entry); }
Plymouth.SetRefreshFunction(animate);
Plymouth.SetDisplayPasswordFunction(password);
Plymouth.SetDisplayQuestionFunction(question);
Plymouth.SetMessageFunction(show_message);
''')
put('overlay/etc/xdg/menus/applications-merged/jatayu-tools.menu','''<!DOCTYPE Menu PUBLIC "-//freedesktop//DTD Menu 1.0//EN" "http://www.freedesktop.org/standards/menu-spec/menu-1.0.dtd">
<Menu><Name>Applications</Name><Menu><Name>Jatayu Tools</Name><Directory>jatayu-tools.directory</Directory><Include><Category>X-Jatayu-Tools</Category></Include></Menu></Menu>
''')
put('overlay/usr/share/desktop-directories/jatayu-tools.directory','''[Desktop Entry]
Type=Directory
Name=Jatayu Tools
Icon=/usr/share/jatayu/logo.png
''')

for slug,title in [('kavach','Kavach'),('sarkar-setu','Sarkar Setu'),('utsav','Utsav')]:
    put(f'overlay/usr/share/applications/org.jatayu.{slug}.desktop',f'[Desktop Entry]\nType=Application\nName={title}\nExec=jatayu-webapp {slug}\nIcon=/usr/share/jatayu/{slug}.svg\nTerminal=false\nCategories=X-Jatayu-Tools;Network;\n')
put('overlay/etc/skel/.xinputrc','# Let KDE Wayland start Fcitx 5 from Virtual Keyboard.\nrun_im none\n')
# KWin launches Fcitx directly with its input-method socket on Wayland.
# Prevent the independent XDG autostart from racing it; keep an X11 fallback.
put('assets/fcitx-x11.sh','#!/bin/sh\n[ "${XDG_SESSION_TYPE:-}" = x11 ] || exit 0\nexec /usr/bin/fcitx5 -d\n')
put('overlay/etc/skel/.config/autostart/org.fcitx.Fcitx5.desktop','[Desktop Entry]\nType=Application\nName=Fcitx 5 (X11 fallback)\nExec=/bin/sh /usr/share/jatayu/fcitx-x11.sh\nOnlyShowIn=KDE;\n')

put('overlay/usr/share/doc/jatayu-integration/copyright','''JatayuOS integration development source
Project maintainer: Anup Yadav <jatayuos4u@gmail.com>
Original integration code and owner-provided Jatayu visual references were prepared for this project.
The owner's final publication licence has not yet been selected. This is a private
development handoff, not a blanket licence for upstream components.
Debian, KDE, Qt, Calamares, Firefox and all dependencies retain their own licences
and notices under /usr/share/doc. The image build preserves those notices.
Do not publicly redistribute before completing docs/COMPLIANCE.md.
''')
print('Generated original assets, desktop integration, policies and installer branding.')

# Offer Hindi alongside the default US physical keyboard without switching input.
put('overlay/etc/skel/.config/fcitx5/profile','[Groups/0]\nName=Default\nDefault Layout=us\nDefaultIM=keyboard-us\n[Groups/0/Items/0]\nName=keyboard-us\nLayout=\n[Groups/0/Items/1]\nName=m17n_hi_itrans\nLayout=\n[GroupOrder]\n0=Default\n')


# A local override adds the owner's unchanged package to the custom menu.
put('overlay/usr/local/share/applications/org.jatayuos.WallpaperChanger.desktop','[Desktop Entry]\nType=Application\nName=Jatayu Wallpaper Changer\nExec=jatayu-wallpaper\nIcon=org.jatayuos.WallpaperChanger\nTerminal=false\nCategories=X-Jatayu-Tools;Utility;Graphics;Qt;\nStartupWMClass=org.jatayuos.WallpaperChanger\n')
put('overlay/etc/skel/.config/dolphinrc','[General]\nShowFullPath=false\n[MainWindow]\nMenuBar=Enabled\n')

# Initialize standard folders/Places before Plasma or Dolphin creates its model.
put('overlay/etc/skel/.config/plasma-workspace/env/00-jatayu-places.sh','#!/bin/sh\nmkdir -p "${XDG_STATE_HOME:-$HOME/.local/state}"\npython3 /usr/share/jatayu/user-defaults.py >>"${XDG_STATE_HOME:-$HOME/.local/state}/jatayu-places.log" 2>&1\n')
# Native KDE title bar defaults; preferences remain editable by the user.
# Firefox uses an integer preference: 0 shows the native window title bar.
# drawInTitlebar is obsolete and has no effect in current Firefox ESR.
put('overlay/usr/share/firefox-esr/browser/defaults/preferences/jatayu.js','pref("browser.tabs.inTitlebar", 0);\n')
put('overlay/etc/skel/.config/gtk-3.0/settings.ini','[Settings]\ngtk-decoration-layout=:minimize,maximize,close\n')
put('overlay/etc/skel/.config/gtk-4.0/settings.ini','[Settings]\ngtk-decoration-layout=:minimize,maximize,close\n')
# The approved text-logo asset is maintained in assets/fastfetch-jatayu.txt.
put('overlay/etc/skel/.config/fastfetch/config.jsonc',json.dumps({'logo':{'type':'file','source':'/usr/share/jatayu/fastfetch-jatayu.txt','color':{'1':'yellow'}}},indent=2)+'\n')
put('overlay/etc/default/grub.d/jatayu.cfg','GRUB_DISTRIBUTOR="JatayuOS"\nGRUB_DISABLE_OS_PROBER=false\nGRUB_CMDLINE_LINUX_DEFAULT="quiet splash"\nGRUB_THEME="/usr/share/grub/themes/jatayu/theme.txt"\nGRUB_TERMINAL_OUTPUT="gfxterm"\nGRUB_GFXMODE="auto"\nGRUB_TIMEOUT_STYLE="menu"\nGRUB_TIMEOUT=8\n')
put('overlay/etc/sddm.conf.d/20-jatayu.conf','[Theme]\nCurrent=breeze\n[General]\nInputMethod=\n')
