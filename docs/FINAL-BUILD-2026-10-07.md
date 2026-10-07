# JatayuOS 1.0 Udaan — final-build changes, 7 October 2026

This candidate incorporates the installed-system checks from the Acer Aspire
R3-131T. A successful Actions run verifies assembly; hardware acceptance below
must be completed on the resulting ISO before public release.

## Changes

- Explicitly include RTKit for audio scheduling.
- Include Flatpak, Discover's Flatpak backend and the signed system Flathub
  remote alongside Debian APT. Android images and Flatpak applications are not
  bundled; their installation requires internet access.
- Include Info Center and its optional diagnostic helpers: aha, clinfo,
  dmidecode, iproute2, libdisplay-info-bin, mesa-utils, pciutils,
  pulseaudio-utils, vulkan-tools, wayland-utils and fwupd. Include rfkill.
- Display the approved JatayuOS logo and os-release identity in Info Center.
- Disable Waydroid container autostart without masking its service. Android
  Setup provides authenticated start/stop controls; initial Android setup is
  still performed using the official Waydroid documentation.
- Retain disabled Baloo indexing and disable its KRunner provider by default.
  Application search remains available. Indexed file search can be enabled
  later by enabling indexing and the File Search provider in System Settings.
- Seed new-user Kickoff favourites with installed applications, excluding the
  uninstalled Kontact entry. Existing users' favourites are not reset.
- Add source checks, early image checks and assembled-root assertions.

## Retained settings

Calamares's RAM threshold remains **1.5 GB**, as requested by the owner. Product
requirements remain **4 GB minimum, 8 GB recommended** for usable performance.
Partitioning, GRUB, kernel/graphics stack, approved desktop artwork, lighter
desktop effects, zram configuration and automatic time synchronisation are
unchanged. Firmware security limitations are reported rather than hidden.

## Acceptance on the new ISO

1. Boot the live USB and install to a spare disk or disposable VM. Verify
   offline installation, first login, correct branding and no failed services.
2. Compare boot timing and idle desktop responsiveness on the Acer with the
   browser closed. Verify Waydroid is inactive after boot and starts through
   Android Setup after initialisation. Confirm reboot leaves it inactive.
3. In Discover, verify Debian and Flathub sources; install, open and remove a
   small application from each source. Confirm signed remote configuration.
4. Play and record sound; inspect realtime data-loop threads during playback.
   Pair Bluetooth headphones and test playback/reconnection after reboot.
5. Inspect Info Center's graphics, Wayland, audio, network and firmware pages.
   Check `upower -d` and whether a battery is detected before treating the
   Energy page as a software defect. Missing hardware data is not fabricated.
6. Test Wi-Fi reconnection, Ethernet with a cable, webcam preview, keyboard,
   touchpad/touchscreen, brightness, suspend/resume and shutdown.
7. Check APT dependencies, package audit, system/user failed units and kernel
   errors. Verify clock synchronisation and installer/default language choices.
8. Test every supported boot/install mode before advertising support, including
   any claimed Secure Boot, BIOS, UEFI, encryption and Windows dual-boot modes.

Publish the actual ISO checksum and package manifest from this Actions run.
Do not reuse an older image's checksum or claim that assembly alone proves all
hardware compatibility.
