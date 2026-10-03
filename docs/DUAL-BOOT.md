# Windows dual boot and standard partitioning

Website: https://jatayuos.in

## Installer policy

JatayuOS uses Debian Live's Calamares installer and Debian's module sequence.
The custom NTFS/BitLocker/EFI rejection job from build #32 was withdrawn:
it incorrectly blocked valid erase-disk and manual installations.
Partition and bootloader module source now remains unchanged by our UI patch;
the builder verifies this with hashes before compiling.

Manual partitioning is enabled. No partitioning method is preselected.
Erase disk is available with Calamares confirmation and deletes the selected
disk's contents. Alongside is available when supported by the detected layout.
There is no custom promise that an explicitly destructive choice preserves data.

GRUB OS detection is enabled, the menu is shown for eight seconds, and the
bootloader uses EFI/JatayuOS. Firmware fallback replacement is disabled.
Debian's bootloader package-selection helper is adapted only to use the two
preinstalled GRUB platform binary sets for offline installation.

## Windows preparation

Back up files and save the BitLocker recovery key. Use Windows Disk Management
to prepare unallocated space; fully shut down Windows and disable Fast Startup.
Boot USB in the same firmware mode as Windows, normally UEFI. Create ext4 root
in unallocated space. Reuse the existing EFI partition at /boot/efi without
formatting. Keep NTFS, Microsoft reserved and recovery partitions unchanged.
Review the final summary. Missing Microsoft EFI files require separate recovery;
a fresh ISO or os-prober cannot recreate them.

See the five-page [installation PDF](../assets/INSTALLATION-GUIDE.pdf), available
on the live desktop, in Aarambh and the application menu.

## Release validation

Use disposable disks and record the exact ISO checksum:
- Blank-disk offline UEFI install and first installed boot.
- Explicit erase/reinstall: normal confirmation and completion without the old error.
- Windows UEFI manual install in unallocated space: preserve Microsoft EFI hashes,
  Windows Boot Manager, Windows/recovery partitions, then boot both systems.
- Supported alongside workflow; encrypted/hibernated volumes must not be forced.
- Multiple disks and NVMe names; verify the intended EFI partition and target disk.
- Linux reinstall with a separate /home retained without formatting.
- Check all six slides and open the live desktop PDF while offline.
- Test first-click response using mouse and touchpad; capture fresh logs.
- Test Firefox controls, Dolphin Places, Fastfetch and UPower/KDE portals.

The UPower/portal additions and reduced animation duration address observed
missing services and visual delay. They do not prove the hardware input issue
is fixed. Secure Boot, BIOS and encryption require their own tests.
