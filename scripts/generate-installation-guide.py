#!/usr/bin/env python3
"""Build the offline installation guide shipped on the live desktop."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parents[1]
for name, file in [('Guide','DejaVuSans.ttf'),('GuideBold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('Guide',normal='Guide',bold='GuideBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text',fontName='Guide',fontSize=10,leading=15,spaceAfter=10,textColor=colors.HexColor('#263746')))
styles.add(ParagraphStyle(name='TitleJ',fontName='GuideBold',fontSize=25,leading=31,spaceAfter=20,textColor=colors.HexColor('#122938')))
styles.add(ParagraphStyle(name='HeadingJ',fontName='GuideBold',fontSize=12,leading=17,spaceBefore=9,spaceAfter=6))
def p(text):return Paragraph(text,styles['Text'])
def h(text):return Paragraph(text,styles['HeadingJ'])
def table(rows):
    t=Table([[p(c) for c in row] for row in rows],colWidths=[140,355])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5edf1')),('LINEBELOW',(0,0),(-1,-1),.5,colors.HexColor('#c9d4dc')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7)]))
    return t
pages=[('Installation Guide',[
 p('<b>JatayuOS 1.0 (Udaan)</b><br/>Udaan Aapki. Shakti Bharat Ki.<br/>Made in India | Guide edition: 3 October 2026'),
 h('Read before installing'),p('This guide covers the Debian Live Calamares workflow used by JatayuOS. Choose an installation method, review the proposed changes, and confirm before disk operations begin. The installer does not automatically protect a disk you explicitly choose to erase.'),
 table([['Your goal','Choose this path'],['Keep Windows','Prepare unallocated space in Windows, then use manual partitioning (page 3), or review an available alongside option (page 4).'],['Use the entire disk','Erase disk, only when every file and operating system on that disk can be removed (page 4).'],['Reinstall Linux','Manual partitioning. Identify Linux root and any separate home partition carefully (page 4).']]),
 h('Before changing partitions'),p('Back up important files to another physical device and verify the backup. Save the Windows BitLocker/device-encryption recovery key somewhere accessible without this PC. Record the existing partitions and firmware settings. Keep Windows recovery media available.'),
 p('This is a testing candidate. A successful build is not proof of Windows dual boot or hardware compatibility. Test on a disposable disk or VM before using important data.'),
 p('Offline help: this PDF opens from the live desktop and Aarambh.<br/>Website: <link href="https://jatayuos.in">https://jatayuos.in</link>')]),
 ('1. Prepare Windows and the USB',[
 h('Verify the ISO'),p('On Linux, keep the ISO and SHA256SUMS together and run <b>sha256sum -c SHA256SUMS</b>. On Windows, run <b>Get-FileHash -Algorithm SHA256 "C:\\path\\JatayuOS-1.0-Udaan-amd64.iso"</b> in PowerShell and compare the entire hash with SHA256SUMS.'),
 h('Prepare space in Windows'),p('Use Windows Disk Management to shrink the Windows volume. Leave the result <b>unallocated</b>; do not create an NTFS volume there. Plan at least 40-60 GB for comfortable desktop use and more for apps and personal files. The installer minimum is 25 GB.'),
 p('Disable Windows Fast Startup and fully shut Windows down. Do not resize a hibernated or locked encrypted Windows volume from Linux. Manage BitLocker/device encryption from Windows and retain its recovery key; firmware or boot changes can trigger a recovery prompt.'),
 h('Write and boot the USB'),p('Use a trusted ISO-writing tool and verify the selected USB device: writing replaces its contents. Boot the USB in the same firmware mode as Windows. For a typical UEFI Windows installation, select the UEFI USB entry. In the live terminal, <b>test -d /sys/firmware/efi &amp;&amp; echo UEFI || echo BIOS</b> shows the current mode.'),
 p('Secure Boot is not certified for this candidate. Changing firmware security settings can affect BitLocker. Do not change storage-controller modes just to make a disk appear; investigate the hardware first.'),
 h('Check the live desktop first'),p('Test the mouse/touchpad, first-click menus, keyboard, display, network and audio. Open this guide and Install JatayuOS. Confirm the disk model and capacity. If the correct disk is missing, stop before partition changes.')]),
 ('2. Manual Windows dual boot',[
 p('Choose <b>Manual partitioning</b>. Device names vary: /dev/sda and /dev/nvme0n1 are examples, not instructions to select those disks. Identify partitions by disk model, size, filesystem and existing purpose.'),
 table([['Partition','Action'],['Windows / data NTFS','Keep unchanged. Do not format, delete or assign as Linux root.'],['Microsoft reserved / recovery','Keep unchanged.'],['Existing EFI system partition','Select the FAT32 EFI System Partition used for boot. Set mount point /boot/efi. Keep formatting OFF and retain its boot/esp flag.'],['Unallocated space','Create an ext4 partition; mount point /; format this NEW Linux partition.'],['Optional separate home','Create ext4 in remaining unallocated space and mount at /home. This is optional.']]),
 h('EFI details'),p('An existing EFI partition holds boot files, often including EFI/Microsoft. Reuse it without formatting for dual boot. It needs sufficient free space for GRUB; size alone does not prove this. If you cannot identify it, or Windows boot files are already missing, stop and investigate rather than create or format partitions blindly.'),
 h('Review before installing'),p('The summary must format only the new Linux partition(s). It must not show a new partition table, whole-disk erase, Windows/recovery deletion, or EFI formatting. Go Back to correct any mismatch before confirming.'),
 p('For legacy BIOS Windows, boot the USB in BIOS mode. UEFI instructions do not apply. BIOS installation on GPT also needs a BIOS boot partition; use an experienced reviewer for that layout. Never mix boot modes unintentionally.')]),
 ('3. Other installation choices',[
 h('Install alongside, when offered'),p('Calamares offers alongside only when it finds a suitable layout and filesystem. Review the selected partition and resulting sizes carefully. Do not force this option when Windows is encrypted or hibernated. Preparing unallocated space in Windows and using manual partitioning gives clearer control over what changes.'),
 h('Erase disk'),p('Choose this only for a disposable disk or when you intend to remove <b>all operating systems and files on the selected disk</b>. Confirm the disk model and capacity. Calamares creates the needed layout for the boot mode. Erase disk is not a Windows dual-boot option.'),
 h('Reinstall JatayuOS manually'),p('Select the existing Linux root partition, mount it at / and format it. This removes its contents. If you have a separate /home and intend to retain it, mount it at /home with formatting OFF, after making a backup. If /home is inside root, formatting root also removes home data. Reuse EFI with formatting OFF.'),
 h('Finish the setup'),p('Set your keyboard, location, account and password. Review every partition action on the summary page and confirm only when correct. Keep the computer on reliable power. The six Jatayu slides run while files are installed. Do not start a second installer or partition tool during installation.'),
 h('If installation reports an error'),p('Do not immediately repeat disk operations. Save the exact message and Calamares session log to another device before rebooting; the live session is temporary. Record the ISO checksum, boot mode and selected layout. Avoid posting passwords, encryption keys or unrelated personal files.')]),
 ('4. First boot and verification',[
 h('Reboot both operating systems'),p('After a successful install, restart and remove the USB when requested. The Jatayu GRUB menu should appear. Start JatayuOS, then restart and test Windows. Also check that Windows Boot Manager remains available in the firmware boot menu.'),
 h('If Windows is absent from GRUB'),p('First try the firmware boot menu. If Windows Boot Manager works, start installed JatayuOS and run <b>sudo os-prober</b>, then <b>sudo update-grub</b>. Read the output and reboot. Detection needs an accessible Windows bootloader; it cannot restore missing Microsoft EFI files.'),
 p('If Windows Boot Manager is also missing, do not format EFI, delete more partitions or reinstall Windows as a first step. Use Windows recovery media or obtain a diagnosis of the existing EFI files and Windows partition. Preserve data and recovery keys.'),
 h('Check everyday operation'),p('Test menus and apps with a single click, Firefox minimize/maximize, Dolphin Places, Fastfetch, audio, Wi-Fi and the installer-created account. Compare a USB mouse with the touchpad if clicks are missed. Save fresh logs with <b>journalctl -b --user</b> and <b>journalctl -b -p warning</b> for review.'),
 h('Updates and support'),p('Use Discover for Debian updates and reboot when required. Jatayu-specific automatic updates need a separately published signed repository; a new ISO does not upgrade an installed system.'),
 p('Project: <link href="https://jatayuos.in">https://jatayuos.in</link><br/>Source and issues: <link href="https://github.com/jatayuos4u/jatayuos">github.com/jatayuos4u/jatayuos</link><br/>Contact: jatayuos4u@gmail.com'),
 p('References: <link href="https://www.debian.org/CD/live/">Debian Live</link>; <link href="https://www.debian.org/releases/trixie/amd64/">Debian installation guide</link>; <link href="https://github.com/calamares/calamares">Calamares</link>. JatayuOS is an independent project; upstream credits and licences remain in the User Manual and /usr/share/doc.')])]
def footer(c,d):
    w,hh=A4;c.saveState()
    for i,color in enumerate(('#ff9933','#e7ecef','#138808')):
        c.setFillColor(colors.HexColor(color));c.rect(i*w/3,hh-7,w/3,7,fill=1,stroke=0)
    c.setFont('Guide',8);c.setFillColor(colors.HexColor('#506575'))
    c.drawString(50,30,'JatayuOS 1.0 (Udaan) | jatayuos.in | Installation Guide')
    c.drawRightString(w-50,30,str(d.page));c.restoreState()
story=[]
for i,(title,items) in enumerate(pages):
    if i:story.append(PageBreak())
    story.append(Paragraph(title,styles['TitleJ']));story.extend(items)
out=ROOT/'assets/INSTALLATION-GUIDE.pdf'
SimpleDocTemplate(str(out),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=45,bottomMargin=60,title='JatayuOS 1.0 (Udaan) Installation Guide',author='JatayuOS Project').build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
