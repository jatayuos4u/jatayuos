# JatayuOS 1.0 Udaan release checklist

This is a publication checklist for the accepted Build #35 candidate.
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

- [ ] Set permanent ISO hosting; do not use one-day Actions artifacts as the public download.
- [ ] Publish verified SHA256SUMS for that exact ISO.
- [ ] Publish the newer guides as separate downloads with versions and hashes.
- [ ] Link all artifacts and source/notices from jatayuos.in and test those links.
- [ ] Publish evidence-based requirements, supported scenarios and limitations.
- [ ] Define support/reporting instructions and Jatayu app update delivery policy.

## Final version decision

- [ ] Choose candidate publication or a later final-version ISO.
- [ ] If choosing a final-version build, explicitly authorize it, update versions,
      run prechecks, build once and validate the new artifact.
- [ ] Tag the exact artifact-producing commit rather than a later documentation-only commit.
- [ ] Publish the release only after the preceding required gates have evidence.

Integration remains `1.0~rc3`; no tag, final-version bump, ISO rebuild or public
release is created by this preparation. Preserve the working candidate and do
not spend additional Actions minutes solely to update documentation.
