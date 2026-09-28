#!/usr/bin/env python3
"""Generate original configuration/artwork; no downloaded artwork is embedded."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def put(name,text):
    p=R/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
put('assets/logo.svg',"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"256\" height=\"256\" viewBox=\"0 0 256 256\"><rect width=\"256\" height=\"256\" rx=\"48\" fill=\"#10212d\"/><path d=\"M38 111 Q84 43 138 82 Q170 56 220 74 L179 97 L205 114 Q174 145 144 134 Q112 171 56 157 L96 132 Q66 134 38 111Z\" fill=\"#e9b75b\"/><path d=\"M49 174 Q115 205 207 157\" fill=\"none\" stroke=\"#e9b75b\" stroke-width=\"9\" stroke-linecap=\"round\"/><circle cx=\"166\" cy=\"89\" r=\"5\" fill=\"#10212d\"/></svg>")
put('assets/wallpaper.svg',"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"1920\" height=\"1080\" viewBox=\"0 0 1920 1080\"><defs><linearGradient id=\"sky\" x2=\"0\" y2=\"1\"><stop stop-color=\"#102c40\"/><stop offset=\".7\" stop-color=\"#112334\"/><stop offset=\"1\" stop-color=\"#071522\"/></linearGradient></defs><rect width=\"1920\" height=\"1080\" fill=\"url(#sky)\"/><circle cx=\"1500\" cy=\"390\" r=\"230\" fill=\"#d79b54\" opacity=\".8\"/><path d=\"M0 830 Q450 680 780 840 T1920 770 V1080 H0Z\" fill=\"#091923\"/><path d=\"M0 980 Q510 780 1000 925 T1920 850 V1080 H0Z\" fill=\"#0b1c29\"/><path d=\"M910 520 Q1020 465 1115 485 Q1215 415 1330 440 Q1220 470 1170 515 Q1070 570 910 520Z\" fill=\"#0a1b28\" opacity=\".8\"/></svg>")
# Nine-part Plasma frame, using original simple vector shapes.
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="140" height="100">','<rect id="center" x="20" y="20" width="60" height="40" fill="#10212d"/>']
for name,x,y,w,h in [('top',20,10,60,10),('bottom',20,60,60,10),('left',10,20,10,40),('right',80,20,10,40),('topleft',10,10,10,10),('topright',80,10,10,10),('bottomleft',10,60,10,10),('bottomright',80,60,10,10)]:
    parts.append(f'<rect id="{name}" x="{x}" y="{y}" width="{w}" height="{h}" fill="#10212d" stroke="#bc9652" stroke-width="1"/>')
parts.extend(['<rect id="hint-top-margin" width="1" height="8"/><rect id="hint-bottom-margin" width="1" height="8"/><rect id="hint-left-margin" width="8" height="1"/><rect id="hint-right-margin" width="8" height="1"/>','</svg>'])
put('assets/panel-background.svg',''.join(parts))
apps=[('welcome','Jatayu Welcome','/usr/share/jatayu/logo.svg','System;'),('tools','Jatayu Tools','/usr/share/jatayu/logo.svg','System;'),('about','About JatayuOS','/usr/share/jatayu/logo.svg','System;')]
for mode,title,icon,categories in apps:
    put(f'overlay/usr/share/applications/org.jatayu.{mode}.desktop',f'[Desktop Entry]\nType=Application\nName={title}\nComment=JatayuOS {title}\nExec=jatayu {mode}\nIcon={icon}\nTerminal=false\nCategories={categories}\nStartupNotify=true\n')
put('overlay/etc/xdg/autostart/org.jatayu.welcome.desktop','[Desktop Entry]\nType=Application\nName=JatayuOS Welcome\nExec=jatayu autostart\nOnlyShowIn=KDE;\nX-KDE-autostart-phase=2\n')
put('overlay/usr/share/polkit-1/actions/org.jatayu.admin.policy',"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE policyconfig PUBLIC \"-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN\" \"http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd\">\n<policyconfig>\n  <action id=\"org.jatayu.live-layout\">\n    <description>Set live-session language and keyboard</description>\n    <message>Set JatayuOS live-session language and keyboard</message>\n    <defaults><allow_any>no</allow_any><allow_inactive>no</allow_inactive><allow_active>yes</allow_active></defaults>\n    <annotate key=\"org.freedesktop.policykit.exec.path\">/usr/libexec/jatayu-admin</annotate>\n    <annotate key=\"org.freedesktop.policykit.exec.argv1\">live-layout</annotate>\n  </action>\n  <action id=\"org.jatayu.install\">\n    <description>Install selected software</description>\n    <message>Administrator authentication is required to install software</message>\n    <defaults><allow_any>no</allow_any><allow_inactive>no</allow_inactive><allow_active>auth_admin</allow_active></defaults>\n    <annotate key=\"org.freedesktop.policykit.exec.path\">/usr/libexec/jatayu-admin</annotate>\n    <annotate key=\"org.freedesktop.policykit.exec.argv1\">install</annotate>\n  </action>\n  <action id=\"org.jatayu.refresh\">\n    <description>Refresh package information</description>\n    <message>Administrator authentication is required to refresh packages</message>\n    <defaults><allow_any>no</allow_any><allow_inactive>no</allow_inactive><allow_active>auth_admin</allow_active></defaults>\n    <annotate key=\"org.freedesktop.policykit.exec.path\">/usr/libexec/jatayu-admin</annotate>\n    <annotate key=\"org.freedesktop.policykit.exec.argv1\">refresh</annotate>\n  </action>\n</policyconfig>\n")
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
put(base+'contents/layouts/org.kde.plasma.desktop-layout.js',"var panel = new Panel;\npanel.location = \"bottom\";\npanel.height = 48;\npanel.floating = true;\nvar launcher = panel.addWidget(\"org.kde.plasma.kicker\");\nlauncher.currentConfigGroup = [\"General\"];\nlauncher.writeConfig(\"icon\", \"/usr/share/jatayu/logo.svg\");\npanel.addWidget(\"org.kde.plasma.icontasks\");\npanel.addWidget(\"org.kde.plasma.systemtray\");\npanel.addWidget(\"org.kde.plasma.digitalclock\");\npanel.addWidget(\"org.kde.plasma.showdesktop\");\nvar ds = desktops();\nfor (var i=0; i<ds.length; i++) {\n  ds[i].wallpaperPlugin=\"org.kde.image\";\n  ds[i].currentConfigGroup=[\"Wallpaper\",\"org.kde.image\",\"General\"];\n  ds[i].writeConfig(\"Image\",\"file:///usr/share/jatayu/wallpaper.svg\");\n}\n")
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
