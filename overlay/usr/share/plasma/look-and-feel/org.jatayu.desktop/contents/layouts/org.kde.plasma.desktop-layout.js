var panel = new Panel;
panel.location = "bottom";
panel.height = 54;
panel.floating = false;
var launcher = panel.addWidget("org.kde.plasma.kickoff");
launcher.currentConfigGroup = ["General"];
launcher.writeConfig("icon", "/usr/share/jatayu/logo.png");
var tasks = panel.addWidget("org.kde.plasma.icontasks");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", ["applications:org.kde.dolphin.desktop", "applications:systemsettings.desktop"]);
panel.addWidget("org.kde.plasma.systemtray");
panel.addWidget("org.kde.plasma.digitalclock");
panel.addWidget("org.kde.plasma.showdesktop");
var ds = desktops();
for (var i=0; i<ds.length; i++) {
  ds[i].wallpaperPlugin="org.kde.image";
  ds[i].currentConfigGroup=["Wallpaper","org.kde.image","General"];
  ds[i].writeConfig("Image","file:///usr/share/jatayu/wallpaper.jpg");
ds[i].writeConfig("FillMode","2");
}
