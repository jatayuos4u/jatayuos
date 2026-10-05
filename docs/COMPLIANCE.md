# Source and license publication gate

Official website: https://jatayuos.in

This handoff is not legal clearance or permission to publicly redistribute every resulting binary.

- Preserve all upstream notices and licence files. The build collects installed copyright files and source package/version references, but does not itself download all corresponding source.
- Before sharing an ISO publicly or selling USB media, obtain the complete corresponding source and necessary build/patch material for covered components, and provide it through a licence-compliant distribution method. Generic upstream links and this project's source alone are insufficient.
- Keep Firefox's Debian package identity intact; review the applicable downstream redistribution/trademark route. No custom homepage, search changes, bundled extension or browser rebrand is configured.
- Review firmware and codec/backend licences individually. Do not infer unlimited redistribution rights from repository availability.
- Select a publication licence for original Jatayu code and artwork. No assumed adoption of the proposed GPL/Creative Commons choices is made here.
- Verify JatayuOS name/logo rights and ownership of production wallpaper. Supplied reference images are not embedded in this archive.
- Retain original creators' credits. Anup Yadav is the distribution creator/maintainer, not the author of all bundled components.
- Do not claim government affiliation, official approval, universal security, Secure Boot compatibility, universal Android support or guaranteed 2 GB performance.
- Audit keys, passwords, machine IDs, live accounts and logs before release. Keep production signing secrets outside the repository and ISO.

Primary references:

- https://www.debian.org/CD/vendors/legal
- https://www.debian.org/trademark
- https://www.mozilla.org/en-US/foundation/trademarks/distribution-policy/
- https://www.mozilla.org/en-US/MPL/2.0/
- https://www.debian.org/doc/manuals/debian-faq/ftparchives.en.html

The broader JatayuOS Blueprint v1.1 remains the product plan. This kit is a development implementation subset, with gaps explicitly recorded in STATUS.md.

## Audit preparation completed on 5 October 2026 UTC

- Existing Jatayu Tools and Wallpaper Changer licenses inspected and preserved.
- Missing shipped Creative Studio core.py recovered; complete source/payload
  archive and package assembly helper added. Rebuilt installed payload matched
  all 14 original files. The original ISO and packages remain unchanged.
- Full GPL text and component-scope/credit notices added without a blanket
  relicense of integration code or artwork.
- Exact-manifest source collector added and locally tested; it has not collected
  the full ISO source set because the Build 35 package manifest is still needed.

Publication remains pending the exact manifest/notices, source collection and
hosting, original licensing/rights decisions and the applicable Firefox branded
redistribution route. See [audit](legal/PUBLICATION-AUDIT.md),
[source procedure](legal/SOURCE-PUBLICATION.md), [copyright scope](../COPYRIGHT.md)
and [credits index](../THIRD-PARTY-NOTICES.md).
