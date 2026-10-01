# JatayuOS 0.1 Release Candidate integration

Prepared on 2026-10-01 on the existing `codex/aarambh-waydroid-finalize` test branch.

## Changes

- Preserve previous installer, Fcitx startup and BIOS/UEFI tricolour fixes.
- Include the owner's original Wallpaper Changer 1.2.1 Debian package; verify
  every transport piece and the complete original SHA256 before use.
- Add its menu-category override and preserve the GPL application source/notices.
- Include LibreOffice and its KDE integration.
- Provide a seven-page offline User Manual and three-page FAQ; retire stale text
  help and desktop Development Preview wording.
- Add Aarambh shortcuts and startup checkbox; expand About with naming story,
  Made in India attribution, applications, credits and legal links.
- Give Kavach, Sarkar Setu and Utsav distinct icons and desktop-window identities.
- Create standard user folders before welcome opens and retain native Dolphin
  Places rather than replacing user bookmarks.
- Keep Firefox ESR pinned in the existing Plasma panel layout.
- Add mandatory package/dependency/source-version checks before compilation.
  `sudo bash scripts/build.sh --precheck-only` runs these without ISO assembly.

## Local verification

- Static precheck: PASS, 107 distinct declared package names.
- Original wallpaper complete-package hash:
  `b278fd3f4a032baf9c8b547423c793c73c70ae1c8b37a82c7c4b9d220b5277a9`.
- Wallpaper source tests: PASS, including 24 exported images, mock Plasma D-Bus,
  GUI navigation, missing-service handling and timed rotation after closing GUI.
- Wallpaper preview regression: PASS at three window sizes.
- Existing file-safety and backup/restore suite: seven tests PASS.
- Aarambh live/installed and About: offscreen smoke renders inspected.
- PDFs: rendered and inspected; 7 manual pages and 3 FAQ pages.
- Integration Debian package assembled and required file paths inspected.

These checks run outside a real KDE session. APT resolution must run in the
Debian 13 builder. The local environment lacks mount/chroot capabilities, so it
cannot assemble or boot the ISO. The workflow must pass the builder precheck
before compilation or live-build begins. Boot/install/hardware testing follows
successful ISO assembly. No final-release or public-redistribution claim is made.
