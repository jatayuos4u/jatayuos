var panel = new Panel;
panel.location = "bottom";
panel.height = 48;
panel.floating = true;
var launcher = panel.addWidget("org.kde.plasma.kicker");
launcher.currentConfigGroup = ["General"];
launcher.writeConfig("icon", "/usr/share/jatayu/logo.svg");
panel.addWidget("org.kde.plasma.icontasks");
panel.addWidget("org.kde.plasma.systemtray");
panel.addWidget("org.kde.plasma.digitalclock");
panel.addWidget("org.kde.plasma.showdesktop");
var ds = desktops();
for (var i=0; i<ds.length; i++) {
  ds[i].wallpaperPlugin="org.kde.image";
  ds[i].currentConfigGroup=["Wallpaper","org.kde.image","General"];
  ds[i].writeConfig("Image","file:///usr/share/jatayu/wallpaper.svg");
}
