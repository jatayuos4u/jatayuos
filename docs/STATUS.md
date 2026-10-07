# JatayuOS 1.0 Udaan build and release status

Updated 7 October 2026. Website: https://jatayuos.in

## Latest successful ISO: Build #38

[Build #38](https://github.com/jatayuos4u/jatayuos/actions/runs/37589010270)
completed successfully on main from
`eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3`.
The run started at 07:42:39 UTC and completed at 08:09:51 UTC on 7 October 2026.

| Detail | Verified value |
| --- | --- |
| ISO filename | `JatayuOS-1.0-Udaan-amd64.iso` |
| ISO size | 2,373,058,560 bytes (2.21 GiB) |
| Base / desktop / architecture | Debian 13 Trixie / KDE Plasma 6.3.6 / AMD64 |
| Integration / installer | 1.0 / Calamares 3.3.14-1+jatayu3 |
| ISO SHA256 | `5a5dbc79f724c8353f1173e55edde3f905d9ddb287272d492930e6730650e040` |
| Artifact expiry | 8 October 2026 at 08:09:32 UTC (13:39:32 IST) |

## Checks confirmed in the build log

- Source syntax, required assets and 134 package declarations: pass.
- Privileged Debian APT dependency and pinned-source precheck: pass.
- Regression suite: 15 tests, 14 passed and one backup round-trip skipped
  because rsync was unavailable in the builder. All 15 passed locally before
  committing the build source.
- Upstream partition/bootloader policy check: pass.
- Assembled image checks: pass, including installed Info Center helpers, RTKit,
  Flatpak/Discover backend, signed Flathub configuration, logo path, disabled
  Waydroid boot autostart, Android launcher and disabled indexing defaults.
- Desktop runtime import checks and Creative Studio offscreen smoke check: pass.
- ISO structure: pass; BIOS and UEFI boot entries present.
- ISO bundle and build log uploads: successful.

Boot entries and image assembly checks do not by themselves establish successful
installation on every supported disk layout or hardware platform.

The owner-supplied Info Center screenshot received on 7 October displays the
JatayuOS shield, JatayuOS 1.0 Udaan, Plasma 6.3.6, Frameworks 6.13.0, Qt 6.8.2
and a Wayland session on an Acer Aspire R3-131T. This confirms the visible
branding on that machine; it is not a checksum or a record of every runtime test.

See [the build changes and hardware acceptance checklist](FINAL-BUILD-2026-10-07.md).

## Preserve and verify this artifact

The [Build #38 ISO bundle](https://github.com/jatayuos4u/jatayuos/actions/runs/37589010270/artifacts/11468269941)
contains SHA256SUMS, SOURCE-COMMIT.txt, package manifests, document checksums,
notices and the smoke capture. Preserve it before expiry and follow
[ISO verification](VERIFY-ISO.md).

The maintainer independently hashed the downloaded ISO outside the CI builder
on 7 October 2026. The supplied terminal output shows SHA256SUMS verification
returned OK and SOURCE-COMMIT.txt matched the Build #38 commit. The exact ISO
hash is recorded above and in [the checksum file](releases/1.0-udaan-build38.SHA256SUMS).
See [the verification evidence](VERIFY-ISO.md#recorded-build-38-verification).
The ISO byte size was recorded by CI; no separate local stat output was supplied.
The ZIP digest remains separately recorded in [build metadata](releases/1.0-udaan-final.json).

## Source, tag and publication

The existing private `v1.0-udaan` tag and
[GitHub release](https://github.com/jatayuos4u/jatayuos/releases/tag/v1.0-udaan)
record Build #37's source
`45b7d1f76dea0184b0fcf7dd1c900f4edf139552`.
They have not been moved to Build #38. Use the exact Build #38 source SHA above
for this latest ISO; README/documentation commits are not new ISO builds.

The current repository remains private. Permanent public ISO delivery through
SourceForge and https://jatayuos.in remains planned for 11 October 2026.
Edition 2 guides were regenerated in Build #38 with Flatpak and on-demand
Android instructions. Committed PDF hashes and build-generated document hashes
have separate scopes; use DOCUMENT-SHA256SUMS from the latest bundle for its PDFs.

## Next evidence to record

- Live boot, installation, first-login and hardware runtime tests on this ISO,
  including Discover app installation, audio/Bluetooth, webcam and suspend.
- Supported boot and installation scenarios before advertising compatibility.
- Permanent artifact hosting and verification after download.
- Existing source, notice and publication requirements from
  [the release checklist](RELEASE-CHECKLIST.md) and [compliance record](COMPLIANCE.md).

APT/Discover supplies Debian package updates. Flatpak/Discover supplies updates
from configured Flatpak remotes. A separate signed Jatayu application repository
is not configured; GitHub commits do not automatically update installed systems.

## Build history

- #35: corrected earlier candidate, downloaded and accepted by the owner.
- #36: privileged precheck for final-version preparation.
- #37: successful ISO on 6 October; source retained by the existing release tag.
- #38: latest successful ISO on 7 October with the desktop integration fixes.
