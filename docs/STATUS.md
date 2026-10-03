# JatayuOS 1.0 (Udaan) testing status — 3 October 2026

Official website: https://jatayuos.in

## Delivered candidate

[Build #32](https://github.com/jatayuos4u/jatayuos/actions/runs/37115177183)
completed successfully on 3 October 2026. Source revision:
`ac51f8d37989a049e72e010aa79721472006978f`.
The ISO is 2,322,923,520 bytes (2.16 GiB). Its bundle includes SHA256SUMS,
package reports and third-party notices. Actions artifacts have one-day
retention; this is a testing delivery, not a permanent public release.

Included changes:
- Six local JatayuOS installation slides, advancing every 14 seconds.
- Windows/BitLocker/EFI destructive-plan protection before partition writes,
  explicit partition selection, and reuse of existing EFI partitions.
- UPower and KDE desktop portal services, plus shorter animations for new accounts.
- A revised gold eagle/shield text asset with Fastfetch's default modules.
- Existing Firefox native title-bar fix, Dolphin folder initialization,
  Jatayu applications, offline manuals, LibreOffice and Waydroid packages.

## Verified

- Static syntax/assets checks and Debian dependency/source precheck passed.
- Patched Calamares 3.3.14-1+jatayu2 compiled and was installed into the image.
- Thirteen isolated partition-plan fixtures passed. These use API substitutes,
  not real disks; the harness also rejects the earlier const-pointer regression.
- Six slides rendered locally with Qt Quick and upstream Calamares components;
  slide count, wraparound and exit lifecycle passed.
- Ten existing app/defaults unit tests passed locally.
- Integration-package assembly, build smoke checks and ISO structure checks passed.
- ISO and log artifacts uploaded successfully.

Build #31 stopped at a const-pointer compilation error before ISO construction.
It was corrected in #32. The two attempts used about 43 minutes of runner time,
within the 60-minute budget; #32 had a 50-minute cap.

## Required before final release

1. Follow [dual-boot validation](DUAL-BOOT.md) on disposable disks, then a backed-up
   Windows PC. Verify Microsoft EFI files and Windows Boot Manager are preserved,
   and boot Windows and JatayuOS. The affected PC's missing Microsoft EFI files
   require separate recovery first.
2. Test menus and app launch on the first click with both a mouse and touchpad.
   Missing-service and animation changes do not prove the input issue is solved.
3. Confirm all six slides in the real installer, Firefox window buttons,
   Dolphin Places, and Fastfetch appearance in Konsole.
4. Test live/installed networking, audio, sleep, graphics and Indian typing.
5. Validate BIOS, Secure Boot, encryption and Waydroid separately; support is
   not established by successful ISO assembly.
6. Finish signed Jatayu update repository setup, corresponding-source delivery,
   artwork/licence records and the [distribution checklist](COMPLIANCE.md).

No final public release has been published. See [testing](TESTING.md),
[update policy](UPDATES.md), and [approved Fastfetch target](APPROVED-FASTFETCH.md).
