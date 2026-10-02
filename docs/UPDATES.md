# Updates and last testing candidate

Official website: https://jatayuos.in

This candidate keeps Debian 13 (trixie) as its supported base. Do not change
APT suites to a future Debian release without a tested migration.

Jatayu assets use project-specific paths. The integration package now records
its /etc files as dpkg conffiles so Jatayu upgrades preserve administrator edits.
Existing branding diversions remain; test base-files upgrades explicitly.
Plasma compatibility, generated GRUB/initramfs artwork and upstream patched
Calamares/Fcitx versions must be checked when their dependencies change.
Configuration created only by configure-image.py is not yet a complete
package-managed migration system. This candidate does not guarantee major
Debian or Plasma upgrades.

New users receive a pre-Plasma initializer for standard user directories and
Dolphin Places. It adds missing entries once, backs up existing bookmarks, and
does not reset later user removals or change icons/themes. Firefox defaults to
a native title bar; GTK buttons are minimize, maximize and close. Fastfetch
uses a portable Jatayu text wordmark. KWallet remains with libpam-kwallet5;
verify wallet unlocking with password login and matching wallet password.
Live/autologin sessions have no password available for automatic unlocking.

Future app updates need a separately hosted, signed APT repository. None is
enabled in this image because the repository URL and signing key are not yet
provided. Maintain separate testing and stable channels, publish higher
versions of the same package names, and scope the key using Signed-By.
Do not distribute a private signing key to clients. Users can then update via
APT/Discover without reinstalling. Keep app data under users' home directories,
and use explicit, versioned migrations rather than resetting their settings.

## Required before public release

- Fresh live VM and real-hardware boots: requested Places entries, unchanged
  icons/theme, Firefox buttons in restored/maximized state, Jatayu Fastfetch.
- Offline install and first boot, BIOS and UEFI; previous installer/input tests.
- Password login: configure kdewallet with the login password, verify unlock
  and Wi-Fi credential persistence; also test autologin separately.
- On an installed test system, apply Debian 13 package updates including
  base-files, GRUB, kernel and available KDE updates; reboot and inspect branding.
- Upgrade the integration package with one edited conffile and customized
  bookmarks: verify both survive and no duplicate Places entries appear.
- Complete signed repository setup and legal/source publication checks.
