# JatayuOS · Ubuntu Cinnamon edition (development source)

A separate project for **Ubuntu 26.04 LTS Resolute Raccoon + Cinnamon**. Creator: **Anup Yadav, India**. Tagline: **Udaan Aapki, Shakti Bharat Ki**. Repository requested: https://github.com/jatayuos4u/jatayuos. This package does not contain files from the Debian/XFCE project.

## What works in this preview

- `jatayu-experience` is a separate, upgradeable Debian package. It keeps the original launcher, session, assets, and first-run choices in distinct paths; no system release file or Cinnamon binary is rewritten.
- In an Ubuntu **casper** live session, the `JatayuOS Cinnamon` session asks for language, keyboard and country before launching Cinnamon. The language must already be installed; the choice file reports whether it was available. The chosen country sets the live-session time zone. Installed sessions do not show the wizard.
- On first login, the Cinnamon panel gets left, center and right groups, with a bottom location and an original Dawn wallpaper. The marker in each user's config stops future upgrades from resetting later choices.
- Jatayu Settings, Aarambh, Bhasha Setu, Jatayu Update, Sanjeevani (Backup), Jatayu Software Center, Jatayu Help, About, Jaanch, Sarkar Setu, Utsav and web shortcuts have separate launchers. Web shortcuts open the real site with the user's browser; no site content or third-party logos are bundled.

## Build and try

On **Ubuntu Cinnamon 26.04**, run `./build-package.sh`, then `sudo apt install ./dist/jatayu-experience_0.1.0_all.deb`. At the LightDM login screen select **JatayuOS Cinnamon**. This is an add-on for an unmodified Ubuntu Cinnamon installation; its `.deb` can also be installed in a private remaster for testing. Run `python3 tests/check.py` to validate source wiring. For the live wizard, install the relevant language packs and generate the selected UTF-8 locales in the image. The keyboard layout is session-scoped and will need explicit installed-user persistence. The original image can be downloaded and verified from https://cdimage.ubuntu.com/ubuntucinnamon/releases/resolute/release/ .

## Release and ISO status

**No ISO is included or claimed to have been boot-tested.** The build script below produces a private test image on a Linux host with internet access, at least 40 GiB of free space, and `xorriso`, `squashfs-tools`, `curl` and `dpkg` installed. The official base ISO must be downloaded separately from the Canonical Ubuntu Cinnamon 26.04.1 release page; the script verifies it against the release SHA256SUMS before making changes. It replaces the installed standard squashfs layer with a flattened package-enabled layer and preserves the original boot entries using xorriso. The installed image and installer behavior have not been verified.

```bash
sudo ./scripts/build-private-test-iso.sh \
  /path/to/ubuntucinnamon-26.04.1-desktop-amd64.iso \
  /path/to/jatayuos-26.04.1-private-test-amd64.iso
```

This local build is for private validation. Boot-test BIOS, UEFI, live desktop, installer, installed system and Windows coexistence before using on real disks. The current execution environment cannot fetch Ubuntu mirrors or run QEMU. Consult `LEGAL.md` before sharing a modified ISO; use the official unmodified Ubuntu Cinnamon ISO for installation until the distribution requirements are addressed.

This preview does **not** yet implement a custom GRUB menu, Plymouth animation, Calamares integration, full desktop launcher renaming, a built-in Panchang calculation, or tested Windows dual boot. The Ubuntu Cinnamon 26.04 image uses `ubuntu-desktop-bootstrap` rather than Calamares. Do not claim these features are ready. Existing data belongs in `/home`; retain the home partition or restore a verified backup before any reinstall. LTS upgrades also need explicit testing and packaging updates, since no distribution can guarantee compatibility across every major release.
