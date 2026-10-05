# JatayuOS final-candidate test checklist

Official website: https://jatayuos.in

Use disposable virtual disks and snapshots. Never test partitioning against your only copy of Windows or personal files.

## Build 35 acceptance record

Build #35 completed successfully and the owner downloaded it and reported the
observed problems solved. See [STATUS.md](STATUS.md) for the exact source SHA
and evidence limits. The checklist below remains the per-scenario test matrix;
blank items must not be assumed passed from the broad acceptance report.

The newer separately delivered Installation Guide has six pages. The ISO still
contains the earlier five-page guide; documentation-only preparation does not
replace files in the already-built ISO.

## Per-scenario verification

- Open the five-page Installation Guide PDF from the live desktop while offline.
- Check all six installation slides rotate and stop when installation finishes.
- Confirm explicit erase/reinstall and manual partitioning complete without the withdrawn protection error.
- Follow [Windows dual-boot validation](DUAL-BOOT.md), including preserved EFI
  file hashes, Windows Boot Manager, and booting both systems.
- Test menu response on the first click with both mouse and touchpad; capture
  fresh KWin/Plasma logs if repeated clicks are still needed.
- Check Firefox minimize/maximize, Dolphin Places and the revised Fastfetch logo.
- Verify UPower and KDE desktop portal D-Bus activation after login.

- On fresh live and installed boots with internet, verify `timedatectl status`,
  `systemctl is-enabled systemd-timesyncd` and `systemctl is-active systemd-timesyncd`.
  Confirm synchronization and successful `sudo apt update` / Discover refresh
  without manually correcting the clock. Repeat after Windows/Linux reboots.
- Verify `locale` reports `LANG=en_IN.UTF-8` and `LC_CTYPE=en_IN.UTF-8` in a
  new user's terminal, with no locale/input-method warnings.
- Open image/video folders in Dolphin: check default previews, Places, removable
  drives and thumbnail persistence after logout/login.
- Test the physical touchpad button separately from tap-to-click; record results
  separately. A working tap does not establish that the button issue is resolved.

## Before build

- Build from `main` only; record its exact SHA. Keep the trigger file unchanged
  during preparation. Dispatch one build only when source checks are complete.
- Run `python3 scripts/preflight.py`.
- Run `python3 -m unittest discover -s tests -v` with Pillow and rsync available.
- Read STATUS.md and COMPLIANCE.md.
- Ensure the chosen builder is Debian 13 with mount/chroot privileges and sufficient storage.

## After one successful build

1. Verify `sha256sum -c SHA256SUMS` in the output directory and confirm
   `SOURCE-COMMIT.txt` matches the intended `main` commit and workflow run SHA.
2. Boot the ISO in a VM using UEFI with Secure Boot off. Record VM CPU/RAM, boot time and memory.
3. At 4 GB RAM, check the live welcome, Try, keyboard settings, networking, Firefox, Discover, Settings, and all Jatayu app windows. Record `free -h`, `uptime`, `systemd-analyze blame`, `journalctl -b -p warning` and `ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head` after the desktop is idle for three minutes and while reproducing any lag. Record VirtualBox graphics controller, 3D acceleration, video RAM, host hypervisor status, and VM CPU/RAM separately; compare with a native boot before attributing lag to Jatayu services.
4. Disconnect network and install into an empty disposable virtual disk. On Calamares Users, confirm a unique password of 12+ characters is accepted and Next becomes enabled; verify that weak-password guidance appears without blocking the explicitly allowed choice. Confirm Calamares does not require downloading a bootloader.
5. Reboot from that disk with ISO removed. Verify no live autologin, temporary password, installer-only account or stale boot entry remains. Verify login, unique machine-id and first-run Aarambh.
6. Finish Aarambh; log out and in; confirm it does not return. Reopen it from the menu.
7. Test software install, authentication cancellation, offline errors, package lock conflicts and updates.
8. Back up a test folder and restore it into a new folder; verify contents and permissions. Do not treat this as system rollback.
9. Convert image fixtures and documents. Ensure originals remain unchanged, unsafe SVG references fail, existing outputs are rejected and PDF compression shows actual results.
10. Repeat basic live/install tests at 2 GB RAM. Record peak memory and any out-of-memory errors separately from idle memory.
11. Only then test BIOS and disposable Windows dual boot images. Confirm the EFI System Partition and Windows recovery/BitLocker situation before real hardware tests.
12. Check suspend/resume, audio, Wi-Fi, external display, Indian typing and actual firewall/security-update behaviour on real hardware.

Secure Boot, full-disk encryption, Android and institutional compatibility require separate tests. No build checksum or successful VM boot certifies these features.
