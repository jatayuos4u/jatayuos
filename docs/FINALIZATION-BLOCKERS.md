# Final-version upload and build status

## Upload completed — 5 October 2026

All five previously blocked files were committed to prepare/final-1.0-udaan in e05f585c419a2095d906d8db52f3a12902cb7358 after the owner's explicit authorization. Their committed Git blob hashes were read back and verified against the preparation manifest:

- `assets/INSTALLATION-GUIDE.pdf` (Git blob SHA 0681d0e19b0f715ef8ee17d208e2914516ea38eb)
- `assets/USER-MANUAL.pdf` (Git blob SHA e4915b698cbecedebbaf29e30106422422d2d53d)
- `docs/screenshots/build35/Menu(1).png` (Git blob SHA 4e0c0e39eccd312b296698f8f504ab2792b636f8)
- `docs/screenshots/build35/desktop.png` (Git blob SHA 472988a702c5b975c09964b08d26c3e00c45f57e)
- `docs/screenshots/build35/utsav-app.png` (Git blob SHA 62d16bf67c28d4d4d3d1e75aead6c79d3e253874)

The manual and installation guide were regenerated from the unchanged branch generator and all ten supplied VM captures. Both match the prepared final-version hashes exactly. The earlier Library PDF editions were not substituted. All ten captures are now present on the branch.

## Final build completed — 6 October 2026

The full source tree was verified, local preflight and ten regression tests
passed, and privileged Debian precheck Build #36 succeeded. PR #4 was merged
into main. [Build #37](https://github.com/jatayuos4u/jatayuos/actions/runs/37406898100) then assembled the final-version ISO successfully
from `45b7d1f76dea0184b0fcf7dd1c900f4edf139552`.

The ISO is 2,354,036,736 bytes (2.19 GiB), with integration `1.0`.
Dependency/source, assembled-image and ISO structure checks passed.
The [private ISO bundle](https://github.com/jatayuos4u/jatayuos/actions/runs/37406898100/artifacts/11388251943) expires on
7 October 2026 at 03:23:38 UTC (08:53:38 IST).

## Remaining validation and publication

Preserve the final bundle, independently verify its ISO checksum/provenance,
and boot/install-test this exact artifact. Complete corresponding-source
delivery and artwork/documentation publication review before public launch.
The successful build does not establish final installation acceptance.

Website creation is the next project step. SourceForge launch remains planned
for 11 October 2026; https://jatayuos.in is the planned download entry point.
The repository remains private. The GitHub release record and `v1.0-udaan`
tag are published, pointing downloads to https://jatayuos.in. No public ISO
delivery or repository visibility change has occurred. See [current status](STATUS.md) and
[final build metadata](releases/1.0-udaan-final.json).
