# JatayuOS 1.0 Udaan release preparation status

Updated 5 October 2026 UTC. Website: https://jatayuos.in

## Accepted testing candidate

[Build #35](https://github.com/jatayuos4u/jatayuos/actions/runs/37208707920)
completed successfully on 4 October 2026 from `main` at
`95afcb80e3517d8930557d4fb1ba9a20a92b7f7f`.
The run finished at 14:44:19 UTC, approximately 27 minutes after starting.
The owner downloaded the ISO and reported: “i downloaded and cheeked all problem
solved and working properly”. This records owner acceptance of the observed
problems; it is not an itemized certification of every installation or hardware scenario.

Build #35 replaces Build #33 as the accepted testing candidate. No public final
release or permanent download has been published by this preparation.
Build #35 retains integration `1.0~rc3` and Calamares `3.3.14-1+jatayu3`.
Final-version source now prepares integration `1.0`; the installer pin remains
unchanged. No final ISO has been built, and Build #35 has not been relabeled.

## Corrections included in Build 35

- Explicit systemd-timesyncd package, service enablement and image validation.
- Dolphin preview backend packages, default previews and thumbnail cache initialization.
- Explicit `LANG=en_IN.UTF-8` and `LC_CTYPE=en_IN.UTF-8` in system/KDE defaults.
- The approved simple Fastfetch logo with normal system-information modules.
- Runtime asset packaging excludes reference/design subdirectories, fixing
  Build #34's early `cp assets/*` failure.
- Builds target main, verify checkout against the triggering SHA and record
  SOURCE-COMMIT.txt. The timeout is 50 minutes and artifact retention one day.
- Existing installer, Firefox pin/titlebar defaults, Places initialization,
  Aarambh, Jatayu Tools, Wallpaper Changer, LibreOffice and Waydroid integration retained.

The successful gated workflow establishes that its source/dependency prechecks,
build and configured assembled-image validations completed. It does not establish
a real-hardware test matrix by itself.

## Evidence and limits

Before the new ISO acceptance report, the owner supplied an installed-system
`timedatectl` result with synchronized clock and active NTP, followed by an
error-free APT refresh against trixie, trixie-security, trixie-updates and
trixie-backports reporting all packages up to date. This confirms the update
path on that tested installation. It is separate evidence, not a claim that
those terminal outputs came from a fresh Build #35 installation.

The owner later supplied ten VM screenshots for documentation: boot menu,
Plymouth, live welcome, desktop, menu, Creative Studio, Wallpaper Changer,
Kavach, Sarkar Setu and Utsav. Images show the captured interfaces and are not
evidence of unseen operations or other hardware. See [capture provenance](SCREENSHOTS.md).

## Final-version source preparation

Integration packaging and build output paths now agree on version `1.0`.
The build regenerates all three illustrated offline guides and About before
packaging, using the ten preserved owner VM captures. Edition 2 contains a
16-page User Manual, 6-page Installation Guide and 5-page FAQ, rendered and
visually checked. See [document inventory](DOCUMENTATION.md) and
[final preparation metadata](releases/1.0-udaan-final.json).
These files are committed as future runtime assets; the existing Build #35 ISO
still contains its earlier bundled documents.

GitHub release preparation comes first. The website remains the public entry
point, and SourceForge ISO launch is planned for 11 October 2026 after validation.
No workflow, tag, public release, repository visibility change or upload is
performed by this preparation.

## Remaining publication work

- Obtain and verify the ISO's SHA256SUMS and SOURCE-COMMIT.txt from the preserved
  downloaded bundle. The ISO digest is not yet independently recorded here.
- Provide permanent hosting for the exact ISO, checksum, guides, notices,
  package/source manifest and required corresponding source/build material.
- GPL-3.0-or-later is approved for original software. Resolve artwork/documentation
  publication permissions and upstream redistribution
  obligations; preserve the existing [compliance checklist](COMPLIANCE.md).
- Record which installation/hardware scenarios were actually tested before
  making specific compatibility claims. BIOS, Secure Boot, encryption,
  Windows dual boot and Android compatibility are not broadly certified.
- Run the privileged Debian dependency precheck, build the final-version ISO once,
  preserve its exact provenance/checksum, and validate that new artifact.
- Document the Jatayu app update delivery decision. Debian updates work through
  APT/Discover; a signed Jatayu repository is not configured.

See [draft release notes](RELEASE-1.0.md), [release checklist](RELEASE-CHECKLIST.md),
[testing](TESTING.md), [dual boot](DUAL-BOOT.md) and [update policy](UPDATES.md).

## Build history

- Build #33: earlier delivered candidate; missing the later NTP/preview/locale corrections.
- Build #34: failed before ISO assembly on copying a reference-assets directory;
  approximately 2 minutes 23 seconds. Packaging was corrected in `93694cb7`.
- Build #35: successful corrected candidate, downloaded and accepted by the owner.

This preparation changes source versions and documentation only. The build
trigger and installer logic remain unchanged; it does not certify a final ISO.
