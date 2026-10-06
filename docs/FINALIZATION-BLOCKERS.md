# Final-version upload status

## Upload completed — 5 October 2026

All five previously blocked files were committed to prepare/final-1.0-udaan in e05f585c419a2095d906d8db52f3a12902cb7358 after the owner's explicit authorization. Their committed Git blob hashes were read back and verified against the preparation manifest:

- `assets/INSTALLATION-GUIDE.pdf` (Git blob SHA 0681d0e19b0f715ef8ee17d208e2914516ea38eb)
- `assets/USER-MANUAL.pdf` (Git blob SHA e4915b698cbecedebbaf29e30106422422d2d53d)
- `docs/screenshots/build35/Menu(1).png` (Git blob SHA 4e0c0e39eccd312b296698f8f504ab2792b636f8)
- `docs/screenshots/build35/desktop.png` (Git blob SHA 472988a702c5b975c09964b08d26c3e00c45f57e)
- `docs/screenshots/build35/utsav-app.png` (Git blob SHA 62d16bf67c28d4d4d3d1e75aead6c79d3e253874)

The manual and installation guide were regenerated from the unchanged branch generator and all ten supplied VM captures. Both match the prepared final-version hashes exactly. The earlier Library PDF editions were not substituted. All ten captures are now present on the branch.

## Remaining release preparation

The final-version preparation remains on draft PR #4, not merged to main. The earlier session reported ten regression tests passed and visually checked all 27 guide pages. This upload recovery verified file hashes; it did not rerun the full precheck or assemble a new ISO.

Next: verify the full source tree and complete the precheck, run the gated build once, preserve ISO provenance/checksums, validate the new ISO and complete corresponding-source delivery and artwork/documentation publication review. SourceForge launch remains planned for 11 October 2026; website https://jatayuos.in is the download entry point. The repository remains private. No final release, tag or visibility change has occurred.
