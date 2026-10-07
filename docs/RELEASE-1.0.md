# JatayuOS 1.0 Udaan release notes

[GitHub release: v1.0-udaan](https://github.com/jatayuos4u/jatayuos/releases/tag/v1.0-udaan) published in the private repository
on 6 October 2026; its existing tag records Build #37. The latest ISO,
**Build #38**, succeeded on 7 October 2026. Final boot/install validation and
public ISO distribution remain pending.
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
- Discover supports Debian APT packages and Flatpak apps from the signed Flathub remote.
- Info Center and its graphics, Wayland, audio and firmware helpers are included.
- RTKit is included for audio realtime scheduling.
- Waydroid starts on demand through authenticated Android Setup controls; Android images and initialization are separate.
- Baloo indexing and its KRunner file-search provider are disabled by default; launcher favourites contain installed applications.
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
| Build | [38](https://github.com/jatayuos4u/jatayuos/actions/runs/37589010270) — success |
| Exact source | `eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3` |
| Completed | 7 October 2026, 08:09:51 UTC |
| Base / architecture | Debian 13 Trixie / AMD64 |
| ISO filename | `JatayuOS-1.0-Udaan-amd64.iso` |
| ISO byte size | 2,373,058,560 (2.21 GiB) |
| Integration package | `1.0` |
| Calamares package | `3.3.14-1+jatayu3` |
| Private CI bundle | [Actions artifact](https://github.com/jatayuos4u/jatayuos/actions/runs/37589010270/artifacts/11468269941) |
| Artifact expiry | 8 October 2026, 08:09:32 UTC (13:39:32 IST) |
| ISO SHA256 | Pending independent verification of bundled SHA256SUMS |
| Permanent download | Pending publication |

Dependency/source prechecks, assembled-image checks and ISO structure validation
passed. CI ran 15 regression tests: 14 passed and one backup round-trip was skipped
because rsync is unavailable in the builder; all 15 passed locally. Final boot/install acceptance is still pending. Preserve the temporary
bundle before expiry; its ZIP digest is not the ISO checksum.
See [ISO checksum verification instructions](VERIFY-ISO.md) and
[final build metadata](releases/1.0-udaan-final.json).

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

Build #38 assembled integration `1.0`, updated About information and edition 2
offline guides from the merged main source. Its source commit and byte size are
recorded in [final build metadata](releases/1.0-udaan-final.json).
Independent ISO checksum verification and final boot/install evidence remain pending.
GitHub will hold the release record and source/docs; jatayuos.in will link users
to SourceForge for ISO downloads. SourceForge launch is planned for 11 October
2026, after the required checks. The existing private GitHub release tag records Build #37; it has not been moved.
Build #38's exact source is recorded above. Public ISO availability remains pending.
The download destination is [jatayuos.in](https://jatayuos.in).

## Using updates

Debian packages receive updates from the configured repositories via
APT/Discover. Flatpak applications receive updates through Flatpak/Discover.
This candidate does not enable a signed Jatayu application
repository; GitHub source commits do not automatically update installed apps.
Do not switch APT suites to another Debian release without a tested migration.

## Documentation

See [documentation inventory](DOCUMENTATION.md) for the committed edition 2
16-page User Manual, 6-page Installation Guide and 5-page FAQ. Build #38 regenerated and bundled these guides with updated Flatpak and
on-demand Android instructions; the existing
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
