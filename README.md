# JatayuOS 1.0 (Udaan)

**Made in India. Udaan Aapki. Shakti Bharat Ki.**

Official website: [jatayuos.in](https://jatayuos.in) · Maintainer: Anup Yadav · Contact: jatayuos4u@gmail.com

JatayuOS is an independent AMD64 desktop distribution based on Debian 13 (Trixie) and KDE Plasma. It includes Firefox ESR, LibreOffice, Dolphin, Aarambh, Jatayu Editing Tools, Wallpaper Changer, and Waydroid packages. Android images and setup are separate.

## Release status

1.0 (Udaan) is the approved first official release name. This repository is preparing its release candidate; a final 1.0 ISO has not yet been validated or published. Previous testing images have been built and used in VM and real-PC testing. The owner confirmed the corrected Firefox native-title-bar setting. Approved Fastfetch artwork, complete release testing and source/licensing publication checks remain pending.

## Documentation

- [User Manual](assets/USER-MANUAL.pdf)
- [Frequently Asked Questions](assets/FAQ.pdf)
- [Screenshots and capture provenance](docs/SCREENSHOTS.md)
- [Testing checklist](docs/TESTING.md)
- [Windows dual boot, protection policy and responsiveness validation](docs/DUAL-BOOT.md)
- [Six-slide installation presentation](docs/INSTALLER-SLIDES.md)
- [Update policy](docs/UPDATES.md)
- [Credits and distribution checklist](docs/COMPLIANCE.md)

## Build

Use a dedicated privileged Debian 13 builder with mount/chroot support and sufficient disk space.

```sh
python3 scripts/preflight.py
sudo bash scripts/build.sh --precheck-only
sudo bash scripts/build.sh
```

The full build also runs the dependency/source precheck before compilation. Output: `out/JatayuOS-1.0-Udaan-amd64.iso`, `SHA256SUMS`, package manifest and notices. Documentation can be regenerated with `python3 scripts/generate-documentation.py` (ReportLab and DejaVu fonts required).

GitHub Actions builds require the BUILD confirmation and retain the 60-minute job cap. Normal source edits do not trigger an ISO build. No release is automatically published. Testing remains required after successful assembly.

## Updates and support

Debian 13 package updates are available through APT/Discover. A signed Jatayu application repository is not yet enabled. A new ISO does not automatically upgrade installed systems. Major Debian upgrades, Secure Boot, dual-boot and universal Waydroid compatibility are not claimed.

Report issues with the ISO checksum, boot mode, hardware/VM details, reproduction steps and relevant logs. Remove private data before sharing.

## Credits

JatayuOS builds on Debian, Linux, KDE, Mozilla, Qt, LibreOffice, Calamares, Fcitx, Waydroid and other upstream contributors. Third-party components retain their licences and marks. Installed licence files and package/source manifests remain part of the image. See the compliance checklist for outstanding publication obligations.
