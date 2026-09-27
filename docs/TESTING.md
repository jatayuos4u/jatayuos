# First ISO test checklist

Use disposable virtual disks and snapshots. Never test partitioning against your only copy of Windows or personal files.

## Before build

- Run `python3 scripts/preflight.py`.
- Run `python3 -m unittest discover -s tests -v` with Pillow and rsync available.
- Read STATUS.md and COMPLIANCE.md.
- Ensure the chosen builder is Debian 13 with mount/chroot privileges and sufficient storage.

## After one successful build

1. Verify `sha256sum -c SHA256SUMS` in the output directory.
2. Boot the ISO in a VM using UEFI with Secure Boot off. Record VM CPU/RAM, boot time and memory.
3. At 4 GB RAM, check the live welcome, Try, keyboard settings, networking, Firefox, Discover, Settings, and all Jatayu app windows.
4. Disconnect network and install into an empty disposable virtual disk. Confirm Calamares does not require downloading a bootloader.
5. Reboot from that disk with ISO removed. Verify no live autologin, temporary password, installer-only account or stale boot entry remains. Verify login, unique machine-id and first-run Aarambh.
6. Finish Aarambh; log out and in; confirm it does not return. Reopen it from the menu.
7. Test software install, authentication cancellation, offline errors, package lock conflicts and updates.
8. Back up a test folder and restore it into a new folder; verify contents and permissions. Do not treat this as system rollback.
9. Convert image fixtures and documents. Ensure originals remain unchanged, unsafe SVG references fail, existing outputs are rejected and PDF compression shows actual results.
10. Repeat basic live/install tests at 2 GB RAM. Record peak memory and any out-of-memory errors separately from idle memory.
11. Only then test BIOS and disposable Windows dual boot images. Confirm the EFI System Partition and Windows recovery/BitLocker situation before real hardware tests.
12. Check suspend/resume, audio, Wi-Fi, external display, Indian typing and actual firewall/security-update behaviour on real hardware.

Secure Boot, full-disk encryption, Android and institutional compatibility require separate tests. No build checksum or successful VM boot certifies these features.
