# JatayuOS finishing status — 30 September 2026

Official website: https://jatayuos.in

## Confirmed
- Development ISO build #22 completed and passed automated image-structure checks.
- The owner reports successful installation and supplied installed-system desktop screenshots.
- The missing unsquashfs dependency was added; the build reads a small SquashFS image before image creation.
- Simple matching passwords are permitted with quality guidance; the patched installer includes a show-password option.

## Prepared after build #22, not yet delivered in a new ISO
- Persistent installed-system GRUB theme using the approved tricolor artwork, logo and countdown.
- Explicit xdg-user-dirs package to initialize Documents, Downloads, Pictures, Music and other standard folders.
- Dolphin and System Settings launchers in the default Plasma panel.
- Locale names rendered together with their English labels instead of distant columns.
- Non-expanding Calamares welcome logo and readable selected sidebar text.
- Fixed Aarambh header-logo dimensions and a Wayland desktop-file identity.

Validation: Python syntax checks, desktop-file generation, and applying the full source patch to upstream Calamares 3.3.14 passed. The patched Calamares and Fcitx packages compiled successfully in build #23; the image did not complete and runtime changes remain untested. Default panel changes apply to new user profiles; existing profiles are not forcibly reset.

## Build #23 and current blocker
- Both patched packages compiled and installed into the image chroot.
- Image configuration failed because Debian did not supply /etc/calamares/modules/locale.conf. Commit 0454b0e creates it when absent; syntax and isolated missing/existing configuration checks passed.
- GitHub also rejected artifact upload because Actions artifact storage quota is full. No new ISO was delivered. Do not spend another full build until upload capacity is available.
- Only runs #22 and #23 remain visible in the repository; #22 retains the last successful ISO (artifact 11076812929, 2,096,318,502 bytes). Preserve or download it before any cleanup.
- GitHub's upload error states quota usage is recalculated every 6–12 hours.

## Fcitx and India defaults prepared
The supplied diagnostic report shows one working Fcitx process, the KWin launcher and active Wayland input contexts. The early warning is consistent with a startup timing issue, but its root cause is not conclusively established.
The custom Fcitx package delays its diagnostic from 7 to 30 seconds while retaining the warning conditions. User boot/input validation is still required.
The next image also sets the initial timezone to Asia/Kolkata and adds optional Hindi ITRANS input alongside the default US keyboard. These defaults are not yet runtime-tested.

## Remaining release work
1. Confirm the installed theme, locale layout, standard folders, dock and Fcitx/input behavior on the next test image.
2. Validate both BIOS and UEFI installation/reboot paths and at least one real PC. Successful installation in the reported VM does not establish all hardware paths.
3. Measure startup time, idle CPU/RAM and Jatayu Tools launch time on known hardware; performance is not yet benchmarked.
4. Build the signed Jatayu APT repository and versioned packages for Tools/branding/configuration updates to installed systems. Debian package updates alone do not deliver project updates.
5. Exercise Jatayu Tools document/image operations, Kavach system links and all three web apps.
6. Initialize and test Waydroid on supported hardware; bundled packages do not imply Android is ready without its separate image.
7. Verify effective firewall, unattended security updates, backup/restore and installer cleanup on an installed system.
8. Complete corresponding-source delivery and project artwork/licence records before a public release.

Full-system backup/recovery, automated snapshots and complete Hindi UI localization remain unfinished. Secure Boot and Windows dual-boot have not been validated.
