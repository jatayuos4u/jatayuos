# JatayuOS 1.0 (Udaan) — Build #38

> **GitHub release draft — not a published ISO download.** Use this text for a **draft** release record. Do not publish the binary download until matching third-party source and distribution conditions are met and the hosted ISO is verified.

## Release summary

JatayuOS 1.0 (Udaan) is an independent, India-focused AMD64 desktop Linux distribution based on Debian 13 (Trixie), with KDE Plasma 6.3.6.

**Udaan Aapki. Shakti Bharat Ki.**

Build #38 is the final ISO tested and approved by the maintainer following boot and installation testing. It includes a graphical Calamares installer, Firefox ESR, LibreOffice, Dolphin, Aarambh welcome application, Jatayu Tools Creative Studio, Wallpaper Changer, Kavach, Sarkar Setu, Utsav, APT and Flatpak. Offline installation is supported. The stated minimum RAM is 4 GB, with 8 GB recommended.

## Verified Build #38 identity

| Field | Value |
| --- | --- |
| Build | [GitHub Actions #38](https://github.com/jatayuos4u/jatayuos/actions/runs/37589010270) |
| Original build source commit | [`eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3`](https://github.com/jatayuos4u/jatayuos/tree/eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3) |
| ISO file | `JatayuOS-1.0-Udaan-amd64.iso` |
| ISO size | 2,373,058,560 bytes (2.21 GiB) |
| SHA256 | `5a5dbc79f724c8353f1173e55edde3f905d9ddb287272d492930e6730650e040` |
| Website | https://jatayuos.in |
| Binary download | **Pending** — no verified public URL yet |

**Tag selection:** The existing `v1.0-udaan` tag refers to the earlier Build #37 revision and must not be reused as the Build #38 source identity. When creating a new tag for the Build #38 release record, use `v1.0-udaan-build38` and set its target to the exact original build commit above. Verify the target before saving. Do not retag or delete `v1.0-udaan`.

## Documentation and source

- [User Manual](https://github.com/jatayuos4u/jatayuos/blob/main/assets/USER-MANUAL.pdf)
- [Installation Guide](https://github.com/jatayuos4u/jatayuos/blob/main/assets/INSTALLATION-GUIDE.pdf)
- [FAQ](https://github.com/jatayuos4u/jatayuos/blob/main/assets/FAQ.pdf)
- [Source code and exact Build #38 snapshot](https://github.com/jatayuos4u/jatayuos/blob/main/docs/SOURCE-CODE.md)
- [Third-party notices index](https://github.com/jatayuos4u/jatayuos/blob/main/THIRD-PARTY-NOTICES.md)
- [Build #38 source publication plan](https://github.com/jatayuos4u/jatayuos/blob/main/docs/legal/BUILD38-SOURCE-PUBLICATION.md)
- [License and copyright information](https://github.com/jatayuos4u/jatayuos/blob/main/COPYRIGHT.md)

### Installation and verification

Write the ISO to a USB using a reliable image writer (the USB will be erased), boot the AMD64 computer from the USB, and use Calamares for installation. Back up important data before partitioning. No internet connection is required during installation. Verify the downloaded ISO against the SHA256 above before use.

### Release and licensing note

The final Build #38 ISO is **technically accepted**, but a public ISO download is **not yet announced**. The project source code is public. The Build #38 package manifest enumerates 1,507 binary packages with matching notice filenames, but the complete corresponding-source archives and applicable redistribution checks remain outstanding. Third-party packages and assets retain their respective licenses. JatayuOS is not affiliated with or endorsed by the Government of India.

The documented Utsav greeting-handler security correction merged after Build #38 was generated. The public repository contains the patch; this does not mean the same correction is present in the unchanged ISO. Review this difference before binary publication.

**Maintainer publication checklist:** confirm source and redistribution terms, stable binary URL and downloaded ISO hash, verified source/notice URLs, release tag pointing at the correct commit, and accurate website links. Until then, keep the GitHub release in **Draft** state.
