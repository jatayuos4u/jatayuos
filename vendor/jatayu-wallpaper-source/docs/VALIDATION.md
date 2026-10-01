# Validation — Jatayu Wallpaper Changer 1.2.1

Checks cover all 24 Full HD PNG exports, packaged-file integrity, complete gallery navigation, search, favourites, dark palette readability, settings persistence, safe filenames, per-screen and all-screen Plasma scripts, service-unavailable errors and background rotation start/stop, non-native folder dialog contrast, and a real 60-second rotation after closing the GUI. D-Bus scripts are executed against a simulated Plasma service.

No real KDE desktop is running in this environment. Final desktop rendering, compositor behaviour and login timing still need a check on Debian 13 / JatayuOS Plasma 6.

Developer checks: `python tests/run_tests.py` (PyQt6 and dbus-daemon required). Build: `python build.py` (Pillow and dpkg-deb required). Export PNGs and generated masters are included in `wallpapers/`. Exact generation prompts are in `wallpapers/prompts.json` and `wallpapers/india-prompts.json`.

To reproduce a Full HD export from a master:

```sh
convert master.png -filter Lanczos -resize '1920x1080^' -gravity center -extent 1920x1080 export.png
```

Full HD refers to the exported file dimensions; generated masters are 1672 × 941. App runtime applies the exported file directly without another resize or recompression.

The timed test exercises the detached agent with a simulated Plasma D-Bus service. This environment has no running systemd user manager or real KDE session; service supervision and login must be verified on the target desktop.

1.2.1: cached preview painting is independent of layout size hints. Page selection updates atomically, and a reserved gallery scrollbar prevents column-width changes on the shorter final page. Regression checks repeatedly navigate all pages at several window sizes and check that preview resize events settle.
