# JatayuOS 1.0 Udaan — Build 35 candidate

**Udaan Aapki. Shakti Bharat Ki. — Made in India**

JatayuOS is an independent AMD64 desktop distribution based on Debian 13
(Trixie) and KDE Plasma. It includes Aarambh, Jatayu Editing Tools, Wallpaper
Changer, Kavach, Sarkar Setu, Utsav, Firefox ESR and LibreOffice. Waydroid
packages are included; Android images and configuration are separate.

Build 35 is the owner-accepted testing candidate. Integration version is
`1.0~rc3`; this artifact has not been rebuilt or relabeled as a new final build.
Source commit: `95afcb80e3517d8930557d4fb1ba9a20a92b7f7f`.

## Preparation status

This README is staged for a future SourceForge upload. The ISO checksum,
corresponding-source delivery, applicable artwork/documentation permissions
and component review must be completed before public ISO publication.

## Verify a downloaded ISO

Compare the ISO's SHA256 with the ISO entry in SHA256SUMS.

Windows PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath ".\JatayuOS-1.0-Udaan-amd64.iso"
```

Linux:

```sh
sha256sum JatayuOS-1.0-Udaan-amd64.iso
```

The GitHub artifact ZIP checksum is different from the ISO checksum.

Back up important data before installation. First test boot and installation in
a disposable VM. BIOS/UEFI support depends on tested hardware; Secure Boot,
universal Android compatibility and automatic upgrades of Jatayu applications
are not claimed.

## Licenses, source and support

Original Jatayu software is GPL-3.0-or-later under COPYRIGHT.md. Upstream
software retains its individual licenses and credits; artwork and documentation
have separate terms. Preserve the full third-party-notices.zip and exact
package-manifest.tsv. Dependency source bundles and exact project/patch/build
materials must be published alongside this release before the ISO is made public.

Website: https://jatayuos.in
Maintainer: Anup Yadav — jatayuos4u@gmail.com

Reports should include the ISO checksum, boot mode, device or VM details,
reproduction steps and reviewed logs. Remove private data before sharing.
