# JatayuOS quick user guide

For JatayuOS 1.0 Udaan Build #35. The illustrated PDFs are tracked in
[documentation inventory](DOCUMENTATION.md).

## Start and explore

Boot the ISO's normal Live system entry. Use Try JatayuOS in the live welcome
to explore, or read the Installation Guide before choosing Install JatayuOS.
An ordinary live session is not permanent storage for personal files.

Aarambh offers help and application/settings shortcuts. In the installed view,
uncheck Show Aarambh when I sign in to disable future automatic opening; it
remains available from the menu.

## Desktop and files

Meta opens the application menu, Meta+E opens Dolphin, Alt+Space opens KRunner
and Ctrl+Alt+T opens Konsole. These shortcuts are configurable in System Settings.
Use the panel for network, audio and clean shutdown controls.

Dolphin Places provides folder shortcuts and mounted devices. Enable previews
when needed, and check file type/size settings if thumbnails are absent. Eject
removable storage before unplugging it. Firefox ESR and LibreOffice provide
browsing and office tools; Discover reviews software and updates.

## Jatayu Tools

Open Creative Studio from the Jatayu Tools menu category. Add files, select a
queued item, choose its operation/settings and output folder, then run the
selected jobs. Inspect output quality and retain originals. Image Studio
provides image workflows; PDF Studio provides PDF merge/compression/export
and extraction workflows. Local compression may reduce quality and does not
always make a smaller file.

Wallpaper Changer: select a bundled image or personal folder, choose display
and layout, and Apply Wallpaper. The current KDE Activity and selected display
matter. The bundled collection works offline.

Kavach supplies guidance and shortcuts; verify actual firewall/update settings
rather than treating dashboard labels as a live security audit.
Sarkar Setu links to independently operated services; verify destinations before
signing in. Utsav calendar information depends on region/data; verify important
observances against a trusted local source.

## Check updates and time

Run these commands one at a time:

```sh
timedatectl status
sudo apt update
apt list --upgradable
```

A correct clock with active, synchronized NTP and an error-free refresh confirms
the update path for that session. No pending upgrades can be normal. Discover
also offers Updates and Refresh. To apply upgrades in Konsole:

```sh
sudo apt update
sudo apt upgrade
```

Review the changes before accepting. Do not run simultaneous Discover/APT
transactions, delete lock files to force an operation or bypass signature checks.
Debian repositories do not deliver arbitrary Jatayu GitHub commits; a signed
Jatayu app repository is not configured. See [update policy](UPDATES.md).

## Android is optional

The Waydroid package is included; Android images require initial setup/download.
Wayland, binder and graphics compatibility matter. No Google apps or ARM
translation are bundled. Use the official
[Waydroid setup instructions](https://docs.waydro.id/usage/install-on-desktops);
avoid adding a duplicate repository to this image just to reinstall its package.

## Installation and Windows

Back up first. Erase disk deletes the selected disk's contents. Alongside options
depend on the detected layout. For Windows UEFI manual dual boot, prepare
unallocated space from Windows, save the BitLocker recovery key, fully shut down
Windows and boot the ISO in the same firmware mode. Create ext4 root in free
space and reuse the correct EFI partition at /boot/efi without formatting.
Preserve Windows, reserved and recovery partitions and review the final summary.
See [dual boot policy](DUAL-BOOT.md).

## Reporting problems

Include the ISO source/checksum, live or installed session, hardware/VM details,
steps, expected behavior and actual errors. Review shared logs for private data.
Compare physical touchpad clicks with tapping or an external mouse before
diagnosing missed launcher clicks.

Useful read-only checks:

```sh
cat /etc/os-release
uname -r
free -h
df -h /
timedatectl status
journalctl -b -p warning --no-pager -n 80
```

Keep personal-file backups on another device. Jatayu Sanjeevani folder backups
are not bootable full-system recovery.

## Credits and scope

JatayuOS is an independent India-made project by Anup Yadav using Debian 13
and KDE Plasma. Upstream projects retain their authorship and licenses.
Installed notices are under /usr/share/doc and /usr/share/jatayu/notices.
Package/source-version references are included in build-package-manifest.tsv.

The owner's acceptance report does not broadly certify Secure Boot, encryption,
Windows disk layouts or Android compatibility. See [status](STATUS.md) for
evidence and [release checklist](RELEASE-CHECKLIST.md) for publication work.
