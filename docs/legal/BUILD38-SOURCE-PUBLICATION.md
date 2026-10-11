# Build #38 corresponding-source publication plan — 11 October 2026

**Status: preparation and input verification only; NOT confirmation of source collection, hosted source, or ISO redistribution compliance.** No ISO rebuild is required.

## Exact release identity

- ISO: `JatayuOS-1.0-Udaan-amd64.iso`
- Build: **#38**, maintainer-tested and accepted
- ISO SHA256: `5a5dbc79f724c8353f1173e55edde3f905d9ddb287272d492930e6730650e040`
- SOURCE-COMMIT.txt: `eb7d73a1b1b7ea55174a9caeda2ff2824ec259a3`
- Build #38 owner-supplied manifest: `package-manifest(1).tsv`, SHA256 `4b9a6753ff0819cf0d9374eb30b3a5339094d09a124b600a5e772e9e89795b4f`
- Build #38 owner-supplied notice archive: `third-party-notices(1).zip`, SHA256 `c1a0c9fb6fd3f0742e4f963a63fd7b6a2d0381505e196206d7fe288a3f598ab4`

**These Build #38 input files are held by the maintainer and were inspected in the release conversation; they are not automatically published by this document.** Keep original names/hashes in the public handoff rather than substituting Build #35 evidence.

## Input inventory and coverage

- 1,507 binary-package manifest rows (four columns each).
- 829 distinct source/version pairs.
- 824 ordinary Debian source/version pairs; 2 locally modified Debian pairs; 3 local Jatayu project pairs.
- Modified Debian: `calamares=3.3.14-1+jatayu3` (base `3.3.14-1`, patch `scripts/patch-calamares.py`); `fcitx5=5.1.12-2+jatayu1` (base `5.1.12-2`, build/patch `scripts/build-fcitx.sh`).
- Local: `jatayu-integration=1.0`, `jatayu-tools=2.0.2`, `jatayu-wallpaper=1.2.1`.
- 1,508 copyright files in the notice ZIP; 1,507 named package matches and one extra `wpa_supplicant`. This is **filename coverage, not legal evaluation**.

## Collect precise source and verify provenance

Use the repository's existing `scripts/collect-release-sources.py`; see [procedure](SOURCE-PUBLICATION.md). Do this on a Linux machine with Python 3, `apt-get`, `dpkg-source` and authenticated Debian 13 deb-src indexes for relevant Trixie suites. A Windows host can use a Debian VM. Do **not** use an updated installation's dpkg manifest in place of the ISO-provided Build #38 manifest.

1. Preserve the original Build #38 manifest and notice ZIP, source commit, ISO SHA256, and document their hashes. Publish the actual full notice ZIP, not only the repository's summary.
2. Plan without downloading:

   ```bash
   python3 scripts/collect-release-sources.py package-manifest.tsv --output source-plan-build38
   ```

   Inspect `source-plan-build38/source-plan.json`; confirm 1,507 binaries / 829 sources and the manifest SHA256 above.
3. Set up authenticated Debian source repositories (Trixie, updates/security and relevant backports) and perform exact-version source collection into a **new empty** directory:

   ```bash
   python3 scripts/collect-release-sources.py package-manifest.tsv --output source-download-build38 --download
   ```

   Collect exact `.dsc` files and all referenced source archives, check `.dsc` SHA256 values and successful extraction. Record the authenticated indices / Debian archive provenance. Missing versions require authenticated snapshots with matching versions; **do not substitute newer versions**. The source collector may take several GB and considerable time; the earlier ~6.74 GB Build #35 estimate is **not** a validated Build #38 size.
4. Supplement modified source bundles with the exact Build #38 scripts and build/install instructions, including `scripts/patch-calamares.py` and `scripts/build-fcitx.sh`; preserve the original base source and differences.
5. Supply all local Jatayu sources, including `vendor/jatayu-tools-2.0.2-source.tar.gz`, the Wallpaper Changer source/build inputs and any missing original masters, and the exact Build #38 repository snapshot.
6. Review upstream license obligations component by component, including firmware, codecs, Firefox branded redistribution, source and notices, plus applicable required offers/availability periods. Do not infer universal ISO distribution clearance from the package name match or this procedure.

## Publish and audit

- Host the Build #38 ISO, `SHA256SUMS`, `SOURCE-COMMIT.txt`, exact manifest, actual third-party notice ZIP, complete matching source bundles and checksums at stable public locations. Internet Archive and/or another host may be used if download terms and capacity permit.
- From a separate, anonymous browser or machine, download samples and verify the ISO, notice archive and source archive hashes; verify that the source URLs are not merely links to generic Debian homepages.
- Record publication URLs, hashes, incomplete components and specific license/rights decisions in the release checklist and `docs/COMPLIANCE.md`. Avoid saying the ISO is redistribution-cleared until these gates are satisfied.
- Do not move `v1.0-udaan` (which points to historical Build #37) without a separate documented release identity decision.

This plan and accompanying git commit are **documentation-only**. They do not trigger, modify or replace the tested Build #38 ISO.
