# JatayuOS 1.0 Udaan release status

Updated 6 October 2026 UTC. Website: https://jatayuos.in

## Successful final-version ISO build

[Build #37](https://github.com/jatayuos4u/jatayuos/actions/runs/37406898100) completed successfully on `main` from
`45b7d1f76dea0184b0fcf7dd1c900f4edf139552`. It started at 03:00:23 UTC and
completed at 03:24:06 UTC on 6 October 2026, approximately 23 minutes 43 seconds later.

- ISO: `JatayuOS-1.0-Udaan-amd64.iso`.
- ISO size: **2,354,036,736 bytes (2.19 GiB)**.
- Integration: `1.0`; Calamares: `3.3.14-1+jatayu3`.
- Static and privileged Debian dependency/source prechecks passed.
- Assembled installer, bootloader, desktop service, branding and help checks passed.
- ISO structure check passed.
- ISO bundle and build log uploaded to private Actions artifacts.

The [ISO bundle](https://github.com/jatayuos4u/jatayuos/actions/runs/37406898100/artifacts/11388251943) expires on
**7 October 2026 at 03:23:38 UTC (08:53:38 IST)** under the one-day retention policy.
Preserve the bundle before expiry. It contains checksum and provenance files,
package manifests and notices. Its ZIP digest is not the ISO SHA256.
The ISO checksum has not yet been independently recorded in the repository.

PR #4 was merged into main before this build. The separate privileged precheck
[Build #36](https://github.com/jatayuos4u/jatayuos/actions/runs/37406502297)
also passed. See [final build metadata](releases/1.0-udaan-final.json).

## Earlier accepted testing reference

[Build #35](https://github.com/jatayuos4u/jatayuos/actions/runs/37208707920)
completed on 4 October 2026 from `95afcb80e3517d8930557d4fb1ba9a20a92b7f7f`,
with integration `1.0~rc3`. The owner downloaded it and reported the observed
problems solved and the OS working properly. That acceptance belongs to Build #35;
final Build #37 still needs its own boot/install evidence.

Corrections carried forward include automatic time synchronization, Dolphin
preview backends/defaults, explicit India UTF-8 locale defaults, the approved
Fastfetch logo and the asset-copy fix after Build #34. Existing installer and
desktop application integration remain included.

Earlier owner-supplied clock/APT outputs confirmed synchronization and updates
on the tested installation. Ten VM screenshots preserve the captured interfaces;
they do not establish unseen operations or other hardware compatibility.
See [capture provenance](SCREENSHOTS.md).

## Documentation and website handoff

Edition 2 guides were committed and regenerated during the final build:
16-page User Manual, 6-page Installation Guide and 5-page FAQ, together with
updated About information. Repository document hashes describe the committed
PDFs; build-generated document hashes are supplied in the artifact.
See [document inventory](DOCUMENTATION.md).

GitHub now records the successful final ISO build, source and documents.
Website creation is the next project step. https://jatayuos.in will be the public
entry point linking to SourceForge. SourceForge launch remains planned for
**11 October 2026**, subject to final validation and publication requirements.
The repository remains private; no tag, public release or permanent download
has been published.

## Remaining validation and publication work

- Preserve the Build #37 bundle and independently verify/record the exact ISO
  SHA256 against SHA256SUMS and SOURCE-COMMIT.txt.
- Boot and install-test this final artifact and record the actual VM/hardware
  configurations and scenarios tested.
- Provide permanent hosting for the ISO, checksum, guides, notices,
  package/source manifests and required corresponding source/build material.
- Complete the existing [compliance checklist](COMPLIANCE.md), including
  artwork/documentation permissions and upstream redistribution requirements.
- Build the website with verified release information; connect permanent
  downloads after their upload and verification.
- Document Jatayu app update delivery. Debian updates use APT/Discover;
  a signed Jatayu repository is not configured.

BIOS, Secure Boot, encryption, Windows dual boot and Android compatibility are
not broadly certified by CI assembly. See [release notes](RELEASE-1.0.md),
[release checklist](RELEASE-CHECKLIST.md), [testing](TESTING.md),
[dual boot](DUAL-BOOT.md) and [update policy](UPDATES.md).

## Build history

- Build #33: earlier candidate before the NTP/preview/locale corrections.
- Build #34: failed during asset copying; fixed in `93694cb7`.
- Build #35: successful corrected candidate, downloaded and accepted by the owner.
- Build #36: successful privileged dependency/source precheck for final preparation.
- Build #37: successful final-version ISO assembly from the merged main source.
