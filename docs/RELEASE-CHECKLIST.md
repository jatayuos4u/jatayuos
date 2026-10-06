# JatayuOS 1.0 Udaan release checklist

This is a publication checklist after successful final ISO Build #37, with
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
- [ ] Verify and record ISO SHA256, byte size and SOURCE-COMMIT.txt from the preserved bundle.
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
- [ ] Record original documentation and artwork publication terms separately.
- [ ] Record logo/wallpaper rights or permission and relevant provenance.
- [ ] Complete corresponding-source and build/patch-material availability for covered shipped components.
- [x] Preserve exact manifest and notice integrity/coverage records; owner retains original notice ZIP.
- [ ] Publish the full third-party notice texts with the ISO.
- [ ] Complete firmware, codec and browser redistribution/trademark review using COMPLIANCE.md.
- [ ] Make required source/notices accessible alongside the published artifact.
- [ ] Review screenshots and reports for private data before publication.

## Delivery and website

- [x] Select SourceForge for ISO and corresponding-source hosting; jatayuos.in for the website.
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
- [x] Run the full dependency/source precheck on a privileged Debian 13 builder (Builds #36 and #37).
- [x] Merge PR #4 and build the final ISO successfully in [Build #37](https://github.com/jatayuos4u/jatayuos/actions/runs/37406898100).
- [x] Record artifact-producing source `45b7d1f76dea0184b0fcf7dd1c900f4edf139552` and ISO byte size 2,354,036,736.
- [x] Upload the private CI bundle containing checksums, provenance, manifests and notices.
- [ ] Preserve the bundle before its 7 October 2026, 03:23:38 UTC expiry; independently verify and record the ISO checksum.
- [ ] Boot and install-test the final artifact; record the actual tested scenarios.
- [ ] Review private repository contents and arrange public access to required source and release documents.
- [ ] Tag the exact artifact-producing commit.
- [ ] Publish the GitHub release after required gates have evidence.
- [ ] Verify SourceForge files and website links before the planned launch.

The final ISO has been assembled successfully. No tag or public release has
been published. Final boot/install validation and permanent download delivery
remain pending. Website creation can proceed using the verified build record.
