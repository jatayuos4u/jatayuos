# Jatayu Wallpaper Changer 1.2.1

For Debian 13 / JatayuOS with KDE Plasma 6. One architecture-independent .deb now contains both the app and 24 wallpapers: 12 nature/space scenes and 12 Indian destinations.

## Install or upgrade

Turn off Auto change in the old app, wait 10 seconds and close it before upgrading.

```sh
sudo apt install ./jatayu-wallpaper_1.2.1_all.deb
```

APT removes the old `jatayu-wallpapers-india` package because this release replaces that collection. The uploaded ZIP and your external image folders are not modified. Existing favourites and settings remain; favourites pointing to old removed images no longer appear. Re-enable Auto change after opening the upgraded app.

Open Jatayu Wallpaper Changer from the menu or run `jatayu-wallpaper` as your normal logged-in KDE user. Do not launch it with sudo. APT may need internet access for missing Python/PyQt6 dependencies; the installed app works offline.

## Collection

24 PNG wallpapers, all exactly 1920 × 1080:

- Crystal Alpine Lake, Himalayan River, Alpine Blossoms
- Emerald Waterfall, Autumn Mirror
- Turquoise Paradise, Sunset Tide
- Sapphire Galaxy, Cosmic River, Aurora Reflections, Milky Way Sanctuary
- Golden Dunes
- Taj Mahal, Golden Temple, Hawa Mahal, Varanasi Ghats
- Gateway of India, Mysore Palace, Konark Sun Temple, Meenakshi Temple
- Kedarnath, Hampi Stone Chariot, Pangong Lake, Kerala Backwaters

The built-in image generator produced masters at 1672 × 941. Those masters were resized with Lanczos resampling into lossless 1920 × 1080 PNG exports. These are Full HD file exports, not native Full HD captures or native 4K images. Resizing does not invent genuine extra detail. The scenes are AI-generated artistic depictions, not verified travel photographs or scientific telescope images. No third-party source photographs were used. Masters and exact prompts are included in the source archive.

## Use

Browse all three gallery pages with Previous and Next. Search scans the entire collection. Select a wallpaper, display and layout, then Apply Wallpaper. The app passes the installed full-size file to Plasma; gallery thumbnails are never applied to the desktop.

Favourites use the heart button. Add folder references your images without altering them. Supported formats: JPEG/JFIF, PNG, WebP and BMP. Scans are nonrecursive.

Enable Auto change for background rotation after closing the window and at login. Choose shuffle, interval, favourites-only and change-at-login. Turn it off to remove its login entry and stop the agent within a few seconds.

Wallpaper changes affect the current KDE Activity, not the lock/login screen. Refresh screens after connecting or disconnecting a monitor. Fill covers the display with cropping; Fit keeps the whole image; Centre uses the file's original pixel size; Stretch can alter proportions.

## Troubleshooting and remove

If APT reports a lock, close Discover and wait for active updates to finish. Do not delete lock files. If Plasma is unavailable, log into a KDE Plasma session and retry.

Disable Auto change before removing the package:

```sh
sudo apt remove jatayu-wallpaper
```

Personal settings in `~/.config/jatayu-wallpaper/` and external images remain. The app source is GPL-3.0-or-later. Debian, KDE Plasma, Python, Qt and PyQt6 are independent upstream projects. Package/developer metadata is included; standalone software-centre displays may still vary.

## Changes in 1.2.0

Add folder now uses a consistently light Qt folder dialog, including file lists, buttons and headers. Automatic rotation uses a systemd user service when available, with a detached background fallback. The panel shows a countdown or an actionable error and includes Restart auto changer. Empty favourites and disconnected displays are reported instead of failing silently.

If rotation stalls, use Restart auto changer. For diagnostics, inspect `~/.config/jatayu-wallpaper/service-status.json`, `service.log`, and `service-launch.log`. For the supervised service use `systemctl --user status jatayu-wallpaper.service` and `journalctl --user -u jatayu-wallpaper.service`.

## Changes in 1.2.1

Fix preview flicker when navigating to page 3. The preview uses a cached image without changing layout size hints; gallery width and page selection remain stable. All 24 wallpapers and rotation settings are retained.
