# Build 35 source and notice evidence

Owner-supplied on 5 October 2026 UTC for accepted Build 35, expected source
commit `95afcb80e3517d8930557d4fb1ba9a20a92b7f7f`. The uploaded files did not
include SOURCE-COMMIT.txt or the ISO checksum, so this association is based on
the owner's handoff, not an independently checked ISO identity.

## Original uploaded files

| File | Bytes | SHA256 |
| --- | ---: | --- |
| package-manifest.tsv | 79,024 | `6f964ab87bc2969cf62cede0281e956a67e72b3e5b5e3b3cd6e9b02ae783c858` |
| third-party-notices.zip | 9,449,371 | `42cc525296c43aa4f21b1d145ff5d373d24f1d852a5bc3a3dcd07aa4d1751958` |

The manifest is preserved here byte-for-byte. The original ZIP remains in the
owner's upload/release bundle; it is not stored in this directory. Preserve and
publish its full notice texts with the release. The compressed notice index
records each member's name, uncompressed size and SHA256. It does not replace
the actual license notices.

## Verification result

- 1,474 binary package rows; no duplicate binary names.
- 808 source/version pairs: 803 Debian, two modified Debian and three local project.
- 1,475 notice files; 41,632,212 uncompressed bytes.
- ZIP CRC, safe path and non-symlink entry checks passed.
- Every manifest binary has a matching notice filename, after architecture suffix
  normalization where required; one additional notice, `wpa_supplicant`, is present.
- Modified Calamares/Fcitx and local Jatayu versions match the accepted candidate.
- All 805 required Debian base source versions located in current Trixie, updates,
  backports and security source catalogues. Referenced archives total
  6,741,476,731 bytes (about 6.74 GB), before extraction.

These are integrity, identity-planning and filename-coverage checks. They do not
establish complete license review, corresponding-source completeness, authenticated
archive provenance, public availability or publication clearance.

## Preserved records

- [package-manifest.tsv](package-manifest.tsv): original upload.
- [source-plan.tsv](source-plan.tsv): exact shipped and fetch versions, classification
  and patch/build-material references.
- [evidence-report.json](evidence-report.json): machine-readable coverage summary.
- [notice-index.tsv.gz](notice-index.tsv.gz): full SHA256 index of ZIP members.
- [source-availability.json.gz](source-availability.json.gz): catalogue URLs/hashes
  and exact source archive filenames, URLs, sizes and catalogue SHA256 values.

The catalogue lookup used HTTPS. Release signatures were not verified. Catalogue
hashes recorded here are observations, not a trusted signing root. Source archives
have not been downloaded by this lookup. URLs are availability observations and
may change; preserve verified source bundles before publishing the ISO.

## Next source collection

Use [the source procedure](../SOURCE-PUBLICATION.md) with authenticated Debian
deb-src indices and the original manifest. Never substitute newer versions.
Include exact project source/build/patch materials and full notices. Review
component-specific terms and original code/artwork rights. Provide accessible
source hosting alongside the ISO; this private repository is not that hosting.

No ISO rebuild, Actions artifact, public release or blanket license grant was
created while processing this upload.
