# Owner-supplied Jatayu Wallpaper 1.2.1

The ISO uses the original uploaded Debian package unchanged. The split files are
transport pieces only; scripts/prepare-wallpaper.py checks each piece and the
complete package against vendor/wallpaper-package.json.

The supplied application source, build script, tests, licence, documentation,
metadata and generation prompts are preserved here. The complete original source
ZIP, including generated masters, remains in the owner's uploaded release bundle.
Exported wallpapers are preserved in the original Debian package. To reconstruct
the build inputs locally, extract that package with dpkg-deb -x and copy the files
from usr/share/wallpapers/Jatayu-Collection into this directory's wallpapers/.

The menu category override is packaged separately by jatayu-integration and does
not change the original wallpaper package, application logic or licence.
