# Windows dual boot and desktop responsiveness

Website: https://jatayuos.in

## Installer policy

The pending release keeps GRUB Windows detection enabled, uses the JatayuOS
EFI directory, and leaves the firmware fallback loader alone. The partition
page requires an explicit choice. Existing EFI partitions as small as 32 MiB
are accepted, subject to sufficient free space for the bootloader.

The patched Calamares checks its complete partition job plan against the
original disk model before executing partition operations. Formatting or
deleting an existing NTFS, BitLocker or EFI partition, or replacing the partition table
of a disk containing one, stops installation. This intentionally also blocks
erase-disk installation on such disks and formatting NTFS data volumes.
Shrinking NTFS through the supported alongside workflow remains possible.

For Windows dual boot, back up files and the BitLocker recovery key first.
Shrink Windows from Windows Disk Management and leave unallocated space.
Boot the USB in the same firmware mode as Windows (normally UEFI).
Install the Linux root in that space. Reuse the existing EFI partition at
`/boot/efi` with formatting disabled. Preserve Windows, Microsoft reserved,
and recovery partitions. Review the final summary before installing.

Windows must be fully shut down; avoid modifying hibernated NTFS volumes.
An encrypted or unbootable Windows installation may require separate recovery.
GRUB detection cannot recreate missing Microsoft EFI files.

## Desktop changes

The package list explicitly includes UPower, xdg-desktop-portal, and its KDE
backend because recommended packages are disabled during image construction.
These address missing D-Bus services observed in the hardware logs.
New accounts use half-duration KDE animations. Blur, contrast effects, and
Baloo indexing remain disabled. These changes do not establish that missing
services or animations caused all repeated-click symptoms.

## Required validation before public release

- Compile the pinned Calamares source with the asserted safety patch.
- UEFI Windows test disk: install in unallocated space, verify Microsoft EFI
  file hashes remain unchanged, retain Windows Boot Manager, and boot both OSes.
- Verify GRUB shows Windows when a valid Microsoft loader exists, including
  a loader on a different EFI partition.
- Confirm unsafe NTFS/BitLocker/EFI format, delete, and erase plans stop before disk writes.
- Confirm a blank-disk installation and NTFS alongside shrink still work.
- Test multiple disks and NVMe naming; repeat the protection tests.
- Test Secure Boot separately; support is not established by these changes.
- On the reported Acer machine, compare mouse and touchpad input, check menu
  opening on the first click, and inspect fresh KWin/Plasma logs.
- Check UPower and desktop portal D-Bus activation in live and installed sessions.

Source patch application against upstream 3.3.14 and static preflight passed.
Thirteen isolated C++ plan fixtures passed, including protected partition format
and deletion, changed preview filesystem type, alongside root creation, blank
disk, and multiple disks. Reproduce after applying the patch with
`python3 tests/partition-plan-check.py /path/to/calamares-3.3.14`.
This harness uses lightweight API substitutes and does not compile Calamares
or write disks. The integration package also assembled locally as `1.0~rc2`.
Build #32 compiled the patched Calamares package successfully and assembled
the ISO with its automated structure checks passing. Windows boot preservation
and hardware responsiveness tests are still pending. Do not label
this a tested public release until these checks pass.
