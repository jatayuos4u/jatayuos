# Source and license publication audit

Audit prepared 5 October 2026 UTC for JatayuOS Build #35,
source `95afcb80e3517d8930557d4fb1ba9a20a92b7f7f`.

## Current result

Publication requirements are not yet complete. This audit records verified
licenses and recovered source, provides exact-source collection tooling, and
keeps remaining approvals and evidence explicit. It does not grant licenses
for assets the maintainer does not own or declare an ISO legally cleared.

| Component | Verified evidence | Remaining requirement |
| --- | --- | --- |
| Jatayu integration 1.0~rc3 | Source/config/build scripts at the Build 35 commit | Maintainer license and provenance confirmation; accessible source snapshot |
| Jatayu Tools 2.0.2 | Shipped copyright says GPL-3.0-or-later; Python sources in package | Publish recovered complete payload/source bundle alongside binary |
| Wallpaper Changer 1.2.1 | Preserved source, GPL-3.0-or-later text, separate artwork/CC0 metadata notices | Publish complete source/build inputs; resolve artwork permission scope |
| Calamares 3.3.14-1+jatayu3 | Pinned Debian 3.3.14-1 plus scripts/patch-calamares.py and build.sh | Publish exact Debian source archives and applicable notices plus modifications |
| Fcitx5 5.1.12-2+jatayu1 family | Pinned Debian 5.1.12-2 plus scripts/build-fcitx.sh | Publish exact Debian sources and modification/build materials |
| Other installed Debian packages | Owner supplied manifest: 1,474 binaries / 808 source-version pairs; matching notice names for every binary | Authenticate and collect exact source archives; review license/source completeness |
| Logo and OS artwork | Owner supplied inputs, but final permission record absent | Origin/ownership/terms confirmation; keep separate from code licenses |
| Firefox ESR | Debian package retained; titlebar preference override present | Verify the applicable downstream distribution/trademark route |
| New guides and captures | Prepared separately after Build 35 | Confirm publication rights/terms; host the guides and record URLs |

## Recovered Creative Studio source

The shipped `jatayu-tools_2.0.2_all.deb` contains GPL-3.0-or-later notices.
The repository already had an exact match for the packaged qt_app.py, but not
the packaged core.py. That missing source is now preserved in
[apps/jatayu-tools/core.py](../../apps/jatayu-tools/core.py).

[The source archive](../../vendor/jatayu-tools-2.0.2-source.tar.gz) preserves all
installed payload files, Debian control files, Python sources, SVG/PNG assets,
notices, metadata and launchers. It includes GPL text and a package assembly
helper. SHA256: `4a43b459300464c3c07f576a04cd5a3510b6bbe80e0a358facf80f08c02bb42f`.

A local rebuild and extraction matched all 14 installed files against the
shipped package. This is a payload-equivalence check, not a bit-for-bit archive
reproducibility claim. The helper is newly supplied reconstruction material;
unavailable historical build tooling is not invented.

Existing package hash:
`1482544a10ec927187566396067d94009eff00b7c4866cf805d809b46f515235`.

## Uploaded Build 35 evidence

The owner supplied package-manifest.tsv and third-party-notices.zip on 5 October
2026 UTC. [The evidence record](build35/README.md) preserves their SHA256 hashes,
the exact manifest, source plan and an index of every notice.

The manifest has 1,474 unique binary package rows and 808 source/version pairs:
803 Debian sources, two patched Debian sources and three local project sources.
The ZIP passes CRC and entry-path checks. Every manifest binary has a matching
copyright-notice filename; one additional notice is present. Filename coverage
does not mean that every notice's terms have been reviewed.

All 805 required upstream source versions were found in the current Trixie,
updates, security and backports source catalogues. The archive files total
6,741,476,731 bytes. This was an HTTPS catalogue lookup, without Release-signature
authentication; no full source archive collection or public hosting is claimed.
The owner has not attached SOURCE-COMMIT.txt or the ISO SHA256 in this upload,
so association with Build 35 remains owner-provided evidence.

The [source collector](../../scripts/collect-release-sources.py) has generated
an exact-version plan from the uploaded manifest. It maps patched Calamares and
Fcitx to their pinned Debian bases, preserves patch references, and rejects
unknown patched versions. Its download mode verifies .dsc SHA256 entries and
extraction. Use authenticated Debian source indices for the actual collection.
Package license, firmware and required build-input review remains necessary.

## Publication decisions still needed

1. Confirm the maintainer's authority to license the original integration code,
   HTML apps, custom shapes, docs and other project-authored material.
   Recommended software license: GPL-3.0-or-later, consistent with the two
   existing Jatayu application packages. This is a recommendation, not a grant.
2. Record origin and permission for the logo, main wallpaper, tricolor art and
   any third-party inputs. AI generation descriptions alone do not establish
   rights for every input or a trademark clearance.
3. Clarify permission for the wallpaper collection. Its existing generated-artwork
   notice says included for use with JatayuOS; it is not silently relicensed.
4. Publish the preserved exact manifest/notices and collect/publish the covered source/build material
   via accessible hosting with the ISO. A private GitHub repository is not a public
   source-download route.
5. Verify the branded Firefox distribution route, including the project's
   `browser.tabs.inTitlebar` preference override. The unaltered Mozilla.org
   distribution policy restricts default-setting changes; do not assume its route
   automatically covers Debian packages or this downstream configuration.

No contact message, license grant, written source offer, repo visibility change,
public release or ISO rebuild was issued during this audit.

## Primary references reviewed

- [Debian distribution/source guidance](https://www.debian.org/CD/vendors/legal):
  corresponding source and modifications must be available for covered binaries;
  generic third-party links alone do not establish the distributor's compliance.
- [Mozilla distribution policy](https://www.mozilla.org/en-US/foundation/trademarks/distribution-policy/):
  code licensing and permission to use trademarks are distinct.
- Preserved package copyright notices and full GPL-3 text:
  [Wallpaper Changer](../../vendor/jatayu-wallpaper-source/docs/copyright),
  [full GPL text](../../LICENSES/GPL-3.0.txt).
- [Debian copyright format](https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/).

Specific compliance choices must follow the actual applicable package licenses,
not a single blanket rule for every component.
