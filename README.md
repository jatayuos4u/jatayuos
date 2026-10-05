# JatayuOS 1.0 (Udaan)

**Made in India. Udaan Aapki. Shakti Bharat Ki.**

Official website: [jatayuos.in](https://jatayuos.in) · Maintainer: Anup Yadav · Contact: jatayuos4u@gmail.com

JatayuOS is an independent AMD64 desktop distribution based on Debian 13 (Trixie) and KDE Plasma. It includes Firefox ESR, LibreOffice, Dolphin, Aarambh, Jatayu Editing Tools, Wallpaper Changer, and Waydroid packages. Android images and setup are separate.

## Release status

[Build #35](https://github.com/jatayuos4u/jatayuos/actions/runs/37208707920) completed successfully from `95afcb80e3517d8930557d4fb1ba9a20a92b7f7f`. The owner downloaded it and reported the observed problems solved and the OS working properly. This is the accepted testing candidate; public final publication is still pending checksum preservation, hosting and the existing source/license gates. Runtime integration remains `1.0~rc3`.

See [current status](docs/STATUS.md), [draft release notes](docs/RELEASE-1.0.md) and [publication checklist](docs/RELEASE-CHECKLIST.md). Specific hardware and installation scenarios should only be advertised when individually verified.

## Documentation

- [Repository quick user guide](docs/USER-GUIDE.md)
- [New illustrated documentation inventory and hashes](docs/DOCUMENTATION.md)
- [Earlier ISO-bundled User Manual](assets/USER-MANUAL.pdf)
- [Earlier ISO-bundled Frequently Asked Questions](assets/FAQ.pdf)
- [Earlier ISO-bundled Installation Guide](assets/INSTALLATION-GUIDE.pdf)
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

Manual GitHub Actions builds require the BUILD confirmation and target main. A push changing the dedicated trigger file on main also starts a build. The job cap is 50 minutes and artifact retention is one day. Normal source edits do not trigger an ISO build. No release is automatically published. Testing remains required after successful assembly.

## Updates and support

Debian 13 package updates are available through APT/Discover. A signed Jatayu application repository is not yet enabled. A new ISO does not automatically upgrade installed systems. Major Debian upgrades, Secure Boot, dual-boot and universal Waydroid compatibility are not claimed.

Report issues with the ISO checksum, boot mode, hardware/VM details, reproduction steps and relevant logs. Remove private data before sharing.

## Credits

JatayuOS builds on Debian, Linux, KDE, Mozilla, Qt, LibreOffice, Calamares, Fcitx, Waydroid and other upstream contributors. Third-party components retain their licences and marks. Installed licence files and package/source manifests remain part of the image. See the compliance checklist for outstanding publication obligations.

## Source and license publication

See [component copyright scope](COPYRIGHT.md), [third-party credit index](THIRD-PARTY-NOTICES.md), [verified audit and remaining work](docs/legal/PUBLICATION-AUDIT.md) and [exact source collection procedure](docs/legal/SOURCE-PUBLICATION.md).

The [Creative Studio 2.0.2 source bundle](vendor/jatayu-tools-2.0.2-source.tar.gz) preserves the shipped source/assets/notices and includes package assembly material. Its rebuilt installed payload matches the original package. The maintainer has approved **GPL-3.0-or-later** for original JatayuOS software; see [LICENSE](LICENSE) and [copyright scope](COPYRIGHT.md). Artwork/documentation permissions, full-ISO source publication and permanent source hosting remain pending.
