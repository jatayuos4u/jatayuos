<div align="center">

<img src="assets/logo.png" alt="JatayuOS logo" width="160">

# JatayuOS 1.0 (Udaan)

**India’s Own Digital Experience**

*Udaan Aapki. Shakti Bharat Ki.*

Made in India · Debian 13 (Trixie) · KDE Plasma · amd64

### [Download JatayuOS 1.0 (Udaan)](https://jatayuos.in/download/)

[Official Website](https://jatayuos.in/) · [User Documentation](https://jatayuos.in/docs/) · [Installation Guide](https://jatayuos.in/docs/installation/) · [Support](https://jatayuos.in/support/)

</div>

---

JatayuOS is a free desktop Linux distribution made in India for everyday work, learning and creativity. Maintained by **Anup Yadav**, it combines Debian 13 (Trixie), KDE Plasma and Jatayu applications in a familiar desktop environment.

![JatayuOS desktop](docs/screenshots/build35/desktop.png)

*Desktop overview from an earlier test installation. See [screenshot provenance](docs/SCREENSHOTS.md) for capture details.*

## Download and verify

**JatayuOS 1.0 (Udaan) is available now.** Download the final tested ISO through the [official download page](https://jatayuos.in/download/), which links to [SourceForge](https://sourceforge.net/projects/jatayuos/files/1.0-Udaan/JatayuOS-1.0-Udaan-amd64.iso/download).

| Release detail | Value |
| --- | --- |
| Version | JatayuOS 1.0 (Udaan) |
| Architecture | amd64 / x86-64 — 64-bit Intel and AMD PCs |
| ISO filename | `JatayuOS-1.0-Udaan-amd64.iso` |
| ISO size | 2,373,058,560 bytes (2.37 GB / 2.21 GiB) |
| Installation | No internet required to install from the ISO |
| Availability | Free to download and use |

The maintainer tested the final ISO for boot and installation and verified downloaded copies against its SHA256 on **13 October 2026**. This is maintainer verification, not certification for every hardware configuration.

Expected ISO SHA256:

```text
5a5dbc79f724c8353f1173e55edde3f905d9ddb287272d492930e6730650e040
```

Linux:

```bash
sha256sum JatayuOS-1.0-Udaan-amd64.iso
```

Windows PowerShell:

```powershell
Get-FileHash .\JatayuOS-1.0-Udaan-amd64.iso -Algorithm SHA256
```

Compare the complete result before using the ISO. Uppercase and lowercase letters are equivalent. The checksum applies to the ISO, not a ZIP containing it. You can also [download SHA256SUMS directly from the website](https://jatayuos.in/SHA256SUMS).

If a SourceForge download is slow or pauses, use **Problems Downloading?** on its download page to choose another mirror.

## Your desktop, ready for everyday work

| Experience | Included tools |
| --- | --- |
| Desktop and files | KDE Plasma and Dolphin |
| Browsing and productivity | Firefox ESR and LibreOffice |
| Welcome and shortcuts | Aarambh |
| Image and PDF workflows | Jatayu Tools Creative Studio |
| Personalization | Wallpaper Changer |
| Information and guidance | Kavach, Sarkar Setu and Utsav |
| Software management | APT and Flatpak support through Discover |
| Installation | Calamares graphical installer |

Sarkar Setu links to external services and does not imply government affiliation. Kavach provides guidance and security shortcuts. Optional Android setup uses Waydroid; images and initialization require separate setup and compatible hardware/session support.

## System requirements

| Component | Minimum | Recommended |
| --- | --- | --- |
| Processor | 64-bit Intel / AMD (x86-64) | Modern 64-bit Intel / AMD |
| Memory | **4 GB RAM** | 8 GB RAM or more |
| Free storage | 25 GB | 40 GB or more |
| Display | 1024 × 768 | Full HD (1920 × 1080) |

Allow extra storage for your files and applications. Internet is needed to download the ISO, install additional software, receive updates and use online services.

Try the live USB to check your display, Wi-Fi, audio and input devices before installation. Back up important files before changing disk partitions.

## Documentation and support

Read the guides on the official website:

- [User Manual and documentation](https://jatayuos.in/docs/)
- [Installation Guide](https://jatayuos.in/docs/installation/)
- [Support and contact](https://jatayuos.in/support/)
- [Community Discussions](https://github.com/jatayuos4u/jatayuos/discussions)
- [Report a bug](https://github.com/jatayuos4u/jatayuos/issues)

When reporting a problem, include your release version, ISO checksum, hardware details, boot mode, steps to reproduce it and the exact error message. Remove private information from logs and screenshots.

Debian packages receive updates through APT/Discover. Flatpak applications receive updates through their configured remote. A signed Jatayu application repository is not yet configured; a new ISO does not automatically upgrade an installed system.

## Source code

- [Archived release sources — Internet Archive](https://archive.org/details/jatayuos-1-0-udaan-build38-sources)
- [Exact source revision for the downloadable ISO](https://github.com/jatayuos4u/jatayuos/tree/eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3)
- [Source documentation](docs/SOURCE-CODE.md)
- [Third-party notices](THIRD-PARTY-NOTICES.md)

Release source commit:

```text
eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3
```

The archive URL retains its original internal identifier. The public product name is **JatayuOS 1.0 (Udaan)**.

<details>
<summary>Source tags and developer build records</summary>

The existing `v1.0-udaan` tag remains at the earlier revision `45b7d1f76dea0184b0fcf7dd1c900f4edf139552`. Its automatic GitHub source archives do not represent the current downloadable ISO. Use the exact source revision and archived release collection above.

The final ISO was produced by [Actions run #38](https://github.com/jatayuos4u/jatayuos/actions/runs/37589010270). The `v1.0-udaan-build38` release record remains a draft.

[Build and acceptance record](docs/FINAL-BUILD-2026-10-07.md) · [ISO verification](docs/VERIFY-ISO.md) · [Release checklist](docs/RELEASE-CHECKLIST.md)

</details>

## Known limitations

The Utsav greeting-handler security correction merged after the final ISO was generated. It is present in the current repository, but the unchanged ISO does not include that later patch.

Secure Boot, encryption, every Windows partition layout and universal Android compatibility have not been certified. Review the installation guidance and [testing checklist](docs/TESTING.md) for your setup.

## Build from source

Use a dedicated privileged Debian 13 builder with mount/chroot support and sufficient disk space:

```sh
python3 scripts/preflight.py
sudo bash scripts/build.sh --precheck-only
sudo bash scripts/build.sh
```

The build runs dependency/source prechecks before compilation. Output includes the ISO, `SHA256SUMS`, package manifests and notices.

[Build documentation](docs/FINAL-BUILD-2026-10-07.md) · [Source publication procedure](docs/legal/SOURCE-PUBLICATION.md)

## Credits and licensing

Created and maintained by **Anup Yadav**. JatayuOS builds on Debian, Linux, KDE, Mozilla, LibreOffice, Qt, Calamares, Fcitx, Waydroid and many other upstream projects.

Original Jatayu software uses **GPL-3.0-or-later** within the scope recorded in [COPYRIGHT.md](COPYRIGHT.md); see [LICENSE](LICENSE). Third-party software, documentation and artwork retain their respective licenses and attribution requirements.

The release source archive is linked above. Its completeness and all redistribution conditions have not been independently audited in this update. Consult the [publication checklist](docs/COMPLIANCE.md) and [source audit](docs/legal/PUBLICATION-AUDIT.md) for the recorded review status.

JatayuOS is an independent project made in India. It is not affiliated with, funded by or endorsed by the Government of India. Software is provided without warranty, subject to its applicable licenses.

---

<div align="center">

**JatayuOS 1.0 (Udaan) · Made in India**

[Download](https://jatayuos.in/download/) · [Documentation](https://jatayuos.in/docs/) · [Support](https://jatayuos.in/support/)

</div>
