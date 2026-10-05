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
Keep the integration package at `1.0~rc3` and Calamares at
`3.3.14-1+jatayu3`; the tested ISO has not been rebuilt or relabeled internally.

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

## Release documents prepared after the ISO

The owner-facing User Manual (16 pages), Installation Guide (6 pages) and FAQ
(5 pages) were created and visually checked after Build #35. Their filenames,
page counts and exact hashes are recorded in [the documentation inventory](DOCUMENTATION.md)
and [candidate metadata](releases/1.0-udaan-candidate.json).
They have been delivered separately; they are not newly embedded in the existing ISO.
The older bundled PDFs in assets remain unchanged.

## Remaining publication work

- Obtain and verify the ISO's SHA256SUMS and SOURCE-COMMIT.txt from the preserved
  downloaded bundle. The ISO digest is not yet independently recorded here.
- Provide permanent hosting for the exact ISO, checksum, guides, notices,
  package/source manifest and required corresponding source/build material.
- Resolve original-code/artwork licensing, rights and upstream redistribution
  obligations; preserve the existing [compliance checklist](COMPLIANCE.md).
- Record which installation/hardware scenarios were actually tested before
  making specific compatibility claims. BIOS, Secure Boot, encryption,
  Windows dual boot and Android compatibility are not broadly certified.
- Decide whether to release the accepted candidate as a candidate or schedule
  an explicitly authorized final-version build. Version changes require a new
  artifact and validation; no rebuild is scheduled by this commit.
- Document the Jatayu app update delivery decision. Debian updates work through
  APT/Discover; a signed Jatayu repository is not configured.

See [draft release notes](RELEASE-1.0.md), [release checklist](RELEASE-CHECKLIST.md),
[testing](TESTING.md), [dual boot](DUAL-BOOT.md) and [update policy](UPDATES.md).

## Build history

- Build #33: earlier delivered candidate; missing the later NTP/preview/locale corrections.
- Build #34: failed before ISO assembly on copying a reference-assets directory;
  approximately 2 minutes 23 seconds. Packaging was corrected in `93694cb7`.
- Build #35: successful corrected candidate, downloaded and accepted by the owner.

This documentation-only preparation leaves the build trigger, workflow, runtime
assets, package versions and installer code unchanged.
