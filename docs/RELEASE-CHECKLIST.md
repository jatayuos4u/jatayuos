# JatayuOS 1.0 Udaan release checklist

This is a publication checklist after successful latest ISO Build #38, with
Build #35 retained as the earlier accepted testing reference.
Checked entries describe completed work; unchecked entries are not assertions
that the work failed, only that evidence or a decision is still needed.

## Candidate and acceptance

- [x] GitHub Build #35 completed successfully.
- [x] Exact source recorded as `95afcb80e3517d8930557d4fb1ba9a20a92b7f7f`.
- [x] Owner downloaded the ISO and reported observed problems resolved.
- [x] Ten owner-supplied VM captures recorded for documentation.
- [x] User Manual, Installation Guide and FAQ prepared and visually checked.
- [x] Current release status, draft notes and document hashes recorded in source.
- [x] Record Build #38 ISO SHA256 and source commit from the maintainer's downloaded-copy verification; byte size is recorded from CI.
- [ ] Record hardware/VM configurations and individually tested scenarios where compatibility will be advertised.

## Source audit preparation

- [x] Inspect existing Creative Studio and Wallpaper Changer license notices.
- [x] Recover missing Creative Studio core source and preserve the complete source/payload archive.
- [x] Rebuild Creative Studio package and compare its installed payload with the shipped package.
- [x] Add component credit/license-scope notices and exact-source collection tooling.
- [x] Receive the owner-supplied Build 35 manifest and third-party-notices ZIP; verify integrity and notice-name coverage.
- [x] Preserve exact manifest/source plan; locate all 805 upstream source versions in current catalogues (signature authentication pending).
- [ ] Run exact-source collection and review covered package/source completeness.
- [ ] Verify the Firefox downstream redistribution route, including the titlebar preference override.

See [source/license audit](legal/PUBLICATION-AUDIT.md). The completed preparation
items do not mark public distribution cleared.

## Public distribution

- [x] Record maintainer approval and apply GPL-3.0-or-later to original Jatayu software, including preserved Build 35 sources.
- [x] Record maintainer's CC BY-SA 4.0 permission for original documentation and project-owned artwork, with logo/brand excluded; see `ARTWORK-AND-DOCS-LICENSE.md`.
- [ ] Verify ownership and embedded third-party rights for each published document, screenshot, wallpaper and icon.
- [ ] Record logo/wallpaper rights or permission and relevant provenance.
- [ ] Complete corresponding-source and build/patch-material availability for covered shipped components.
- [x] Preserve exact manifest and notice integrity/coverage records; owner retains original notice ZIP.
- [ ] Publish the full third-party notice texts with the ISO.
- [ ] Complete firmware, codec and browser redistribution/trademark review using COMPLIANCE.md.
- [ ] Make required source/notices accessible alongside the published artifact.
- [ ] Review screenshots and reports for private data before publication.

## Delivery and website

- [x] Originally select SourceForge for ISO hosting and jatayuos.in for the website; SourceForge restoration is pending and a replacement public host has not been verified.
- [x] Record the existing SourceForge project: https://sourceforge.net/projects/jatayuos.
- [ ] Authenticate project access and upload/verify permanent downloads.
- [ ] Connect the website's source repository and add verified release URLs.
- [ ] Publish verified SHA256SUMS for that exact ISO.
- [ ] Publish the newer guides as separate downloads with versions and hashes.
- [ ] Link all artifacts and source/notices from jatayuos.in and test those links.
- [ ] Publish evidence-based requirements, supported scenarios and limitations.
- [ ] Define support/reporting instructions and Jatayu app update delivery policy.

## Final version and release

- [x] Choose a final-version ISO with GitHub release preparation before the planned SourceForge launch on 11 October 2026.
- [x] Prepare integration version `1.0` and matching package paths.
- [x] Commit edition 2 guides and preserve the ten original VM captures.
- [x] Regenerate guides and About before packaging; require their source inputs in preflight.
- [x] Run the full dependency/source precheck on a privileged Debian 13 builder (Builds #36, #37 and #38).
- [x] Merge PR #4 and build the final ISO successfully in [Build #37](https://github.com/jatayuos4u/jatayuos/actions/runs/37406898100).
- [x] Record artifact-producing source `45b7d1f76dea0184b0fcf7dd1c900f4edf139552` and ISO byte size 2,354,036,736.
- [x] Build #38 succeeded from `eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3`, with ISO byte size 2,373,058,560.
- [x] Build #38 image assertions verified desktop helpers, RTKit, Flatpak/Flathub, branding and on-demand Android defaults.
- [x] Upload the private CI bundle containing checksums, provenance, manifests and notices.
- [x] Maintainer downloaded the Build #38 bundle and verified the ISO against bundled SHA256SUMS on 7 October 2026; source commit matches. See [verification evidence](VERIFY-ISO.md#recorded-build-38-verification).
- [ ] Retain a backup of the full downloaded bundle before its 8 October 2026, 08:09:32 UTC (13:39:32 IST) expiry.
- [x] Maintainer reported Build #38 boot/install testing passed on 9 October 2026.
- [ ] Record the exact tested hardware/VM scenarios and evidence before claiming broad compatibility.
- [ ] Complete Git history/Actions artifact secret scanning and public visibility review before switching repository visibility.
- [ ] Arrange public access to required corresponding source and release documents (repository build scripts alone may not meet all obligations).
- [x] Tag the exact artifact-producing commit `45b7d1f76dea0184b0fcf7dd1c900f4edf139552` as `v1.0-udaan`.
- [x] Publish the private [GitHub release record](https://github.com/jatayuos4u/jatayuos/releases/tag/v1.0-udaan) with jatayuos.in as the download destination.
- [ ] Complete remaining validation/source/rights gates before public ISO distribution.
- [ ] Verify SourceForge files and website links before the planned launch.

The final ISO has been assembled successfully and the private GitHub release
record/tag published for Build #37. The latest Build #38 source is recorded separately;
the existing tag has not moved. The [downloaded ISO checksum verification](VERIFY-ISO.md#recorded-build-38-verification)
is complete and recorded. Final boot/install validation and public permanent download
delivery remain pending. Website creation can proceed using the verified build record.
