# Publishing corresponding source for Build 35

This procedure implements source collection and delivery, not a legal clearance.
Read [the audit](PUBLICATION-AUDIT.md) and [copyright scope](../../COPYRIGHT.md).

## Preserved manifest and notice evidence

The uploaded manifest is now preserved at
[build35/package-manifest.tsv](build35/package-manifest.tsv). See
[the verification record](build35/README.md) for notice coverage, input hashes
and the exact source plan. Keep the original notice ZIP for publication; the
repository's notice index is not a replacement for its full copyright texts.

## Complete the release evidence

From the already downloaded Build 35 ZIP, preserve the remaining evidence and
retain these original files:

- package-manifest.tsv
- third-party-notices/ (all files)
- SHA256SUMS
- SOURCE-COMMIT.txt

The source commit must be
`95afcb80e3517d8930557d4fb1ba9a20a92b7f7f`.
Do not create the release manifest from an installed system that has since been
updated: its versions may differ from the ISO.

## Plan without downloads

On a machine with Python 3:

```sh
python3 scripts/collect-release-sources.py package-manifest.tsv --output source-release
```

A plan generated from the supplied manifest is preserved in
build35/source-plan.tsv. All 805 upstream versions were found in current source
catalogues, requiring about 6.74 GB of archive downloads, before extraction.
That lookup is not signature authentication or source publication.

Review source-release/source-plan.json. It lists exact Debian sources and local
project packages separately. Unknown `+jatayu` versions are rejected.

## Download Debian source archives

Use a dedicated Debian environment with apt-get and dpkg-source installed and
trusted deb-src indices for the appropriate Trixie, security, updates and
backports archives. The collector does not alter APT sources or install packages.

```sh
python3 scripts/collect-release-sources.py package-manifest.tsv --output source-download --download
```

Use a new empty output directory. Inspect source-download-report.json and each
download.log. If an exact version is no longer in current repositories, retrieve
that same version from a verified archive/snapshot; do not replace it with the
current candidate. Retain source archive checksums and publisher verification.

The collector verifies archives against the downloaded .dsc SHA256 list and
extracts them using dpkg-source. Retain .dsc and every referenced archive.
Review packages containing firmware or prebuilt data individually: downloading
a Debian source archive does not establish permissions beyond its actual terms.

## Add the project and modified-source materials

- Export the exact Build 35 repository tree, including scripts, configuration,
  source, packaging, tests and source asset inputs. Include the approved LICENSE
  and COPYRIGHT.md as a licensing supplement to the original Build 35 export;
  preserve historical source bytes. Original software is now GPL-3.0-or-later;
  resolve separate asset rights and retain existing third-party terms before
  publishing the full mixed source bundle.
- Include vendor/jatayu-tools-2.0.2-source.tar.gz as a recovered source supplement.
- Include Wallpaper Changer application source/build metadata, existing notices
  and required collection input assets. The original source ZIP with masters is
  held by the owner; do not claim it is already uploaded here.
- Include the pinned Debian Calamares and Fcitx source archives together with
  the exact patch and build scripts from Build 35.
- Preserve all relevant upstream license texts, modified-file notices and
  build/install instructions.

Project GitHub files alone are not the complete source for the ISO's dependencies.

## Publish and verify

Host the ISO, checksum, exact manifest, third-party notices and source bundles
through durable, accessible download URLs. Link those URLs together on the
release page. Check anonymous access and hash the delivered bytes.
Do not publish a written multi-year source offer unless you can fulfill its
actual terms; this preparation does not create such a commitment.

Complete the per-component review, record license/rights decisions, then update
COMPLIANCE.md and the release checklist with verified URLs and evidence.

## Selected hosting

The maintainer selected SourceForge for the ISO and corresponding-source delivery,
with https://jatayuos.in as the website. See
[the upload procedure](../releases/SOURCEFORGE-PUBLICATION.md). Project access,
exact ISO checksum verification, source collection and public URL checks remain
pending. No public upload has occurred.
