# JatayuOS public repository / ISO publication gate — 10 October 2026

This document separates making project source public from distributing the finished 2.21 GiB ISO. Neither is authorized merely by creating this checklist.

## Verified from repository records

- Accepted ISO: Build #38, source commit `eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3`.
- SHA256: `5a5dbc79f724c8353f1173e55edde3f905d9ddb287272d492930e6730650e040`.
- Existing `v1.0-udaan` release/tag points at earlier Build #37 source. Do not silently move a published historical tag. Prefer a separate Build #38-specific source tag/release or an explicitly explained migration after confirmation.
- Maintainer reported final Build #38 boot/install acceptance on 9 October; independently documented platform coverage remains outstanding.
- SourceForge project restoration is pending. No public download host is verified.
- Build #38 ISO need not be rebuilt for source documentation changes.

## Repository visibility gate

- [ ] Run full-history secret scanning on every branch and tag with an appropriate local scanner, including large/binary files; review findings securely and rotate exposed credentials before publication.
- [ ] Review Actions logs, uploaded artifacts and prior screenshots for identifiers, access tokens, private host details, personal data and live credentials.
- [ ] Confirm collaborator access, GitHub Apps/tokens, 2FA, branch/tag protection and Actions default permissions.
- [ ] Confirm licensing/redistribution permissions for all original software, documentation, screenshots, logo and wallpaper sources.
- [ ] Review historical commits for content the owner does not intend to publish. Removing a file from HEAD does not remove it from history.
- [ ] Perform a second-person/manual review of the above and explicitly authorize visibility change.

## Separate ISO distribution gate

- [ ] Resolve every open obligation in `docs/COMPLIANCE.md`, `docs/RELEASE-CHECKLIST.md` and `docs/legal/PUBLICATION-AUDIT.md`.
- [ ] Obtain and make available the corresponding upstream source/build/patch material and notices under applicable licenses. The Linux distribution includes multiple distinct licenses: project GPL-3.0-or-later is not a blanket license for the ISO.
- [ ] Resolve Firefox redistribution/trademark, firmware/codec and original artwork provenance questions.
- [ ] Document tested configurations and limitations.
- [ ] Publish the exact checksum with the full ISO and verify a fresh download from the public host.
- [ ] Ensure public landing page and release record describe the accepted Build #38 ISO without misattributing Build #37.

## Current decision

Not yet cleared for automatic repository visibility change or public ISO distribution. Complete checks and record evidence; do not mark them complete based solely on source availability or keyword searches.
