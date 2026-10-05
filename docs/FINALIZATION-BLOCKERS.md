# Final-version upload status

The final-version preparation is staged on this draft branch, not merged to main. Ten regression tests passed locally. The prior session visually checked all 27 guide pages.

Automatic approval review blocked binary uploads because exact payload/destination authorization was not accepted. Do not merge or trigger the ISO workflow until the following files have been uploaded and verified:

- `assets/INSTALLATION-GUIDE.pdf` (Git blob SHA 0681d0e19b0f715ef8ee17d208e2914516ea38eb)
- `assets/USER-MANUAL.pdf` (Git blob SHA e4915b698cbecedebbaf29e30106422422d2d53d)
- `docs/screenshots/build35/Menu(1).png` (Git blob SHA 4e0c0e39eccd312b296698f8f504ab2792b636f8)
- `docs/screenshots/build35/desktop.png` (Git blob SHA 472988a702c5b975c09964b08d26c3e00c45f57e)
- `docs/screenshots/build35/utsav-app.png` (Git blob SHA 62d16bf67c28d4d4d3d1e75aead6c79d3e253874)

The guide generator requires all ten supplied VM captures. The current branch retains the older manual and installation-guide PDFs until approved replacement uploads finish. Listed final documentation hashes describe the prepared local files, not those older branch PDFs.

After upload approval: verify the full source tree, run the gated build once, preserve ISO provenance/checksums, validate the new ISO and complete corresponding-source and artwork/documentation publication permissions. SourceForge launch remains planned for 11 October 2026; website https://jatayuos.in is the download entry point. No final release, tag or visibility change has occurred.
