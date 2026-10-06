# JatayuOS 1.0 Udaan release notes — final draft

Draft for publication review. Final ISO Build #37 succeeded on 6 October 2026;
final boot/install validation and public publication remain pending.
Website: https://jatayuos.in

## Overview

JatayuOS is an independent AMD64 desktop distribution by Anup Yadav, made in
India and based on Debian 13 Trixie with KDE Plasma.
“Udaan Aapki. Shakti Bharat Ki.” is the project tagline.

The owner downloaded Build #35 and reported the previously observed problems
resolved and the OS working properly. The candidate is accepted for release
preparation; this document does not announce a public final release.

## Included desktop and applications

- Aarambh provides a starting point for help, settings and applications.
- Firefox ESR, LibreOffice and Dolphin cover browsing, documents and files.
- Jatayu Tools Creative Studio provides local image and PDF workflows.
- Wallpaper Changer provides the offline collection and desktop wallpaper controls.
- Kavach provides safety information and shortcuts to system tools.
- Sarkar Setu is a directory of external service links, without government affiliation.
- Utsav provides festival/calendar information; important dates need local verification.
- Waydroid packages are included; Android images and initialization remain on demand.
- Fastfetch uses the approved compact Jatayu design with system information.

## Corrections established in Build 35

Time synchronization is installed and enabled automatically. Dolphin thumbnail
backends, default previews and cache initialization are included. UTF-8 India
locale defaults are explicit in the system and KDE session. The asset packaging
failure from Build #34 is fixed.

The installer uses the restored upstream partition/bootloader module code with
Debian Live sequencing. Alongside choices depend on the detected layout; manual
UEFI dual boot requires preserving the existing EFI filesystem and Windows
partitions. Read the Installation Guide before changing disks.

## Final ISO build identity

| Field | Value |
| --- | --- |
| Build | [37](https://github.com/jatayuos4u/jatayuos/actions/runs/37406898100) — success |
| Exact source | `45b7d1f76dea0184b0fcf7dd1c900f4edf139552` |
| Completed | 6 October 2026, 03:24:06 UTC |
| Base / architecture | Debian 13 Trixie / AMD64 |
| ISO filename | `JatayuOS-1.0-Udaan-amd64.iso` |
| ISO byte size | 2,354,036,736 (2.19 GiB) |
| Integration package | `1.0` |
| Calamares package | `3.3.14-1+jatayu3` |
| Private CI bundle | [Actions artifact](https://github.com/jatayuos4u/jatayuos/actions/runs/37406898100/artifacts/11388251943) |
| Artifact expiry | 7 October 2026, 03:23:38 UTC (08:53:38 IST) |
| ISO SHA256 | Pending independent verification of bundled SHA256SUMS |
| Permanent download | Pending publication |

Dependency/source prechecks, assembled-image checks and ISO structure validation
passed. Final boot/install acceptance is still pending. Preserve the temporary
bundle before expiry; its ZIP digest is not the ISO checksum.
See [final build metadata](releases/1.0-udaan-final.json).

## Earlier testing reference identity

| Field | Value |
| --- | --- |
| Build | [35](https://github.com/jatayuos4u/jatayuos/actions/runs/37208707920) |
| Exact source | `95afcb80e3517d8930557d4fb1ba9a20a92b7f7f` |
| Base | Debian 13 Trixie |
| Architecture | AMD64 |
| ISO filename | `JatayuOS-1.0-Udaan-amd64.iso` |
| Integration package | `1.0~rc3` |
| Calamares package | `3.3.14-1+jatayu3` |
| Permanent download | Pending publication |
| ISO SHA256 | Pending verification from preserved SHA256SUMS |

Do not use the Actions artifact ZIP digest as the ISO checksum. Exact build
provenance and document hashes are recorded in
[the candidate metadata](releases/1.0-udaan-candidate.json).
The historical run link is not permanent download hosting.

## Final-version preparation

Build #37 assembled integration `1.0`, updated About information and edition 2
offline guides from the merged main source. Its source commit and byte size are
recorded in [final build metadata](releases/1.0-udaan-final.json).
Independent ISO checksum verification and final boot/install evidence remain pending.
GitHub will hold the release record and source/docs; jatayuos.in will link users
to SourceForge for ISO downloads. SourceForge launch is planned for 11 October
2026, after the required checks. This draft does not announce availability.

## Using updates

Debian packages receive updates from the configured repositories via
APT/Discover. This candidate does not enable a signed Jatayu application
repository; GitHub source commits do not automatically update installed apps.
Do not switch APT suites to another Debian release without a tested migration.

## Documentation

See [documentation inventory](DOCUMENTATION.md) for the committed edition 2
16-page User Manual, 6-page Installation Guide and 5-page FAQ. Build #37 regenerated and bundled these guides; the existing
Build #35 ISO retains its earlier documents. Repository hashes describe the
committed PDFs; regenerated document hashes are in the final build bundle. The [quick user guide](USER-GUIDE.md) provides repository-readable instructions.

## Known limits

The successful build and owner's acceptance do not certify every device,
Windows disk layout, Secure Boot, encryption or Android application. Waydroid
requires setup and compatible session/kernel/graphics support. No Google apps
or ARM translation are bundled. Dashboard labels in Kavach are not a complete
live security audit, and third-party portal links can change.

## Credits and publication status

Debian, Linux, KDE, Mozilla, LibreOffice, Qt, Calamares, Fcitx, Waydroid and other
upstream projects retain their authorship, licenses and marks. Anup Yadav is the
distribution maintainer, not the author of every component.

Public distribution remains subject to completing the project's existing
[license/source checklist](COMPLIANCE.md), checksum verification, permanent
hosting and final metadata decision. See [release checklist](RELEASE-CHECKLIST.md).
Original software is licensed GPL-3.0-or-later. Separate artwork/documentation
permissions and third-party distribution requirements remain under review.
