# JatayuOS 1.0 (Udaan) testing status - 3 October 2026

Official website: https://jatayuos.in

## Delivered candidate

[Build #33](https://github.com/jatayuos4u/jatayuos/actions/runs/37128272039)
completed successfully from source `8dc7b0e40693b5b64b8c7c93ab7a8e2d16693689`.
One build took approximately 32 minutes, within its 50-minute cap and the
owner's 60-minute budget. No retry was needed.

[Download the ISO bundle](https://github.com/jatayuos4u/jatayuos/actions/runs/37128272039/artifacts/11276158606).
The ISO is 2,322,923,520 bytes (2.16 GiB). The bundle includes SHA256SUMS,
package reports and third-party notices. Artifact retention is one day;
the ISO bundle expires on 4 October 2026 at 14:34 UTC.

## Changes

- Removed build #32's overbroad Windows/EFI partition rejection job.
- Restored upstream Calamares partition and bootloader module code, retaining
  Debian Live sequencing, manual partitioning and an explicit partition choice.
- Retained Windows OS detection, the eight-second GRUB menu, JatayuOS EFI ID,
  and disabled firmware fallback replacement. Offline GRUB platform binaries
  remain preinstalled through the existing helper adaptation.
- Added a five-page installation PDF to the live desktop, Aarambh and menu.
  It covers Windows preparation, manual partitioning, EFI reuse, erase/reinstall
  and first-boot troubleshooting.
- Retained six installation slides, Firefox native titlebar defaults,
  Dolphin Places initialization and the gold Fastfetch eagle with default modules.
- Retained UPower/KDE portals and reduced animations for the reported responsiveness
  issue; these are not proof that all missed-click symptoms are resolved.
- Integration package is 1.0~rc3; Calamares is 3.3.14-1+jatayu3.

## Verified

- Source preflight and Debian package/dependency/source checks passed.
- All ten existing application and user-defaults regression tests passed locally.
- The new PDF rendered correctly as five pages. The actual live startup function
  copied it into a localized desktop path in a test using GUI substitutes; it
  did not create the file in the completed installed-session path.
- The UI patch applied to pinned upstream sources. Build-time hashes confirmed
  partition and bootloader module files were unchanged by that patch.
- Calamares compiled successfully and the rc3 package was installed in the image.
- Assembled-image checks passed for manual partitioning, bootloader settings,
  OS detection, GRUB binaries, UPower/KDE portal files, PDF help, Firefox defaults,
  Fastfetch configuration and slideshow files.
- Existing image smoke tests and BIOS/UEFI ISO structure checks passed.
- ISO and build-log artifacts uploaded successfully.

## Still required before a public release

1. Test offline blank-disk installation, explicit erase/reinstall, and manual
   Windows UEFI dual boot on disposable/backed-up media. Preserve Microsoft EFI
   files and Windows Boot Manager and boot both OSes. A successful build does not
   establish this. The earlier PC's missing Microsoft files need separate recovery.
2. Verify first-click menu/app response with mouse and touchpad on the affected PC.
3. Confirm Firefox controls, Dolphin Places, Fastfetch and slides in the live ISO.
4. Test installed updates, branding persistence, networking, audio, suspend and input.
5. Validate BIOS, Secure Boot, encryption and Waydroid separately before claiming support.
6. Complete Jatayu update delivery, licensing/corresponding-source arrangements,
   final screenshots and permanent download hosting before publication.

See [installation/dual boot](DUAL-BOOT.md), [testing](TESTING.md),
[updates](UPDATES.md), and [distribution checklist](COMPLIANCE.md).
No public release has been published.
