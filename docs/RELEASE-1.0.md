# JatayuOS 1.0 Udaan candidate release notes

Draft for publication review. Accepted testing candidate: Build #35.
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

## Corrections in this candidate

Time synchronization is installed and enabled automatically. Dolphin thumbnail
backends, default previews and cache initialization are included. UTF-8 India
locale defaults are explicit in the system and KDE session. The asset packaging
failure from Build #34 is fixed.

The installer uses the restored upstream partition/bootloader module code with
Debian Live sequencing. Alongside choices depend on the detected layout; manual
UEFI dual boot requires preserving the existing EFI filesystem and Windows
partitions. Read the Installation Guide before changing disks.

## Artifact identity

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

## Using updates

Debian packages receive updates from the configured repositories via
APT/Discover. This candidate does not enable a signed Jatayu application
repository; GitHub source commits do not automatically update installed apps.
Do not switch APT suites to another Debian release without a tested migration.

## Documentation

See [documentation inventory](DOCUMENTATION.md) for the separately delivered
16-page User Manual, 6-page Installation Guide and 5-page FAQ. These newer guides
were prepared after the ISO; the PDFs inside that ISO remain the earlier editions.
The [quick user guide](USER-GUIDE.md) provides repository-readable instructions.

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
No license choice or rights clearance is implied by these draft notes.
