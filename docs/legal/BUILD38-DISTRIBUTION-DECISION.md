# Build #38 distribution decision — 11 October 2026

The Build #38 ISO is technically accepted, its SHA256 was verified by the maintainer, and the GitHub Release is saved as a draft. This is a **distribution readiness record**, not a legal opinion or public download approval.

## Evidence available

- Project source and exact build commit: [Build #38 source](https://github.com/jatayuos4u/jatayuos/tree/eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3)
- Original software licensing and exclusions: [COPYRIGHT.md](../../COPYRIGHT.md)
- Input manifest: 1,507 binary packages, 829 source/version pairs.
- Third-party notice archive: 1,508 copyright files, all 1,507 manifest binary package names covered by matching notice filenames. This is filename coverage, not a license-by-license clearance.
- [Collection plan and exact versions](BUILD38-SOURCE-PUBLICATION.md).
- ISO `JatayuOS-1.0-Udaan-amd64.iso` SHA256: `5a5dbc79f724c8353f1173e55edde3f905d9ddb287272d492930e6730650e040`.
- Existing historical `v1.0-udaan` GitHub tag refers to Build #37. The Build #38 release should retain its distinct tag and remain a draft until conditions are met.

## Distributor's source options and limits

The ISO aggregates software governed by multiple licenses. The correct source-distribution arrangement must be assessed license by license.

For **GPLv3 online distribution**, section 6(d) generally allows equivalent network access to corresponding source from the binary download location; a different server can be used where clear directions are maintained and the distributor ensures continued availability. Merely naming Debian or publishing this project's own scripts is not automatically enough.

For **GPLv2**, corresponding-source distribution and written-offer alternatives have different conditions. Debian's guidance warns that simply linking to a third-party FTP server is insufficient and describes an up-front source-copy or an appropriate durable written offer, with its actual fulfillment responsibility. Do not issue a written offer unless the project has resources to honor it for the required duration and recipients.

Other license conditions, third-party rights (including non-free firmware/assets), modified Calamares/Fcitx and shipped Jatayu app sources must also be reviewed.

References:
- https://www.debian.org/CD/vendors/legal
- https://www.gnu.org/licenses/gpl-3.0.html
- https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

## Remaining steps before public binary download

1. Determine, for each covered component, whether corresponding source must be served, accompanied, or supported by a legally sufficient and fulfillable offer.
2. Collect and validate exact historical matching source files, modifications, complete build materials, and full license notices as applicable; classify and address any non-redistributable materials.
3. Host required source and notices durably, ensure anonymous access, and include clear locations next to the ISO download. Validate checksums from another machine.
4. Verify the public ISO file against the recorded checksum, publish final URLs and accurate release notes, then publish the Build #38 release.

**Until completion, do not claim complete corresponding-source delivery or blanket ISO redistribution clearance.** This documentation does not modify the ISO or trigger its build.
