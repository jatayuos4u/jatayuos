#!/usr/bin/env python3
"""Generate the offline RC manual and FAQ from reviewed content."""
from pathlib import Path
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
FONT='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('Jatayu',FONT+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('Jatayu-Bold',FONT+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('Jatayu',normal='Jatayu',bold='Jatayu-Bold',italic='Jatayu',boldItalic='Jatayu-Bold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body',fontName='Jatayu',fontSize=10,leading=15,spaceAfter=9,textColor=colors.HexColor('#253746')))
styles.add(ParagraphStyle(name='Section',fontName='Jatayu-Bold',fontSize=19,leading=25,spaceAfter=16,textColor=colors.HexColor('#10212d')))
styles.add(ParagraphStyle(name='Sub',fontName='Jatayu-Bold',fontSize=11.5,leading=17,spaceBefore=8,spaceAfter=6,textColor=colors.HexColor('#10212d')))
styles.add(ParagraphStyle(name='Small',fontName='Jatayu',fontSize=8.5,leading=12,spaceAfter=7,textColor=colors.HexColor('#253746')))
styles.add(ParagraphStyle(name='Cover',fontName='Jatayu-Bold',fontSize=32,leading=39,spaceAfter=18,textColor=colors.HexColor('#10212d')))

REFERENCES=[
 ('JatayuOS - official website','https://jatayuos.in'),
 ('Debian - source and distribution obligations','https://www.debian.org/CD/vendors/legal'),
 ('Debian - trademark policy','https://www.debian.org/trademark'),
 ('KDE - project and contributors','https://kde.org/community/'),
 ('KDE - licensing','https://develop.kde.org/docs/getting-started/licenses/'),
 ('Mozilla - software distribution policy','https://www.mozilla.org/en-US/foundation/trademarks/distribution-policy/'),
 ('Mozilla - trademark guidelines','https://www.mozilla.org/en-US/foundation/trademarks/policy/'),
 ('LibreOffice - licences','https://www.libreoffice.org/licenses/'),
 ('Qt - licensing','https://www.qt.io/licensing/'),
 ('Calamares - project and contributors','https://github.com/calamares/calamares'),
 ('Waydroid - official setup guide','https://docs.waydro.id/usage/install-on-desktops'),
 ('GNU GPL version 3','https://www.gnu.org/licenses/gpl-3.0.html')]

def p(text,style='Body'):return Paragraph(text,styles[style])
def h(text):return p(text,'Sub')
def rows(items):
 data=[[p(a,'Small'),p(b,'Small')] for a,b in items]
 t=Table(data,colWidths=[140,355],hAlign='LEFT')
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#f3f6f7')),('LINEBELOW',(0,0),(-1,-1),.5,colors.HexColor('#d9e1e6')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
 return t
def footer(canvas,doc):
 w,hh=A4;canvas.saveState()
 canvas.setFillColor(colors.HexColor('#ff9933'));canvas.rect(0,hh-7,w/3,7,fill=1,stroke=0)
 canvas.setFillColor(colors.HexColor('#e5e9ed'));canvas.rect(w/3,hh-7,w/3,7,fill=1,stroke=0)
 canvas.setFillColor(colors.HexColor('#138808'));canvas.rect(2*w/3,hh-7,w/3,7,fill=1,stroke=0)
 canvas.setStrokeColor(colors.HexColor('#d9e1e6'));canvas.line(50,48,w-50,48)
 canvas.setFont('Jatayu',8);canvas.setFillColor(colors.HexColor('#526572'))
 canvas.drawString(50,33,'JatayuOS 1.0 (Udaan)  |  Made in India')
 canvas.drawString(50,20,'https://jatayuos.in')
 canvas.linkURL('https://jatayuos.in',(50,18,160,29),relative=0)
 canvas.drawRightString(w-50,33,str(doc.page));canvas.restoreState()
def build(name,title,pages):
 story=[]
 for i,(heading,items) in enumerate(pages):
  if i:story.append(PageBreak())
  story.append(p(heading,'Section'))
  story.extend(items)
 SimpleDocTemplate(str(ASSETS/name),pagesize=A4,rightMargin=50,leftMargin=50,topMargin=45,bottomMargin=65,title=title,author='JatayuOS Project - Anup Yadav',subject='Offline guide for the JatayuOS Release Candidate').build(story,onFirstPage=footer,onLaterPages=footer)

manual=[
 ('User Manual',[
  Image(str(ASSETS/'logo.png'),width=86,height=86,hAlign='LEFT'),Spacer(1,16),p('Welcome to<br/>JatayuOS','Cover'),
  p('Udaan Aapki. Shakti Bharat Ki.','Sub'),p('<b>Made in India</b> - an independent desktop project created by Anup Yadav, built with Debian 13 and KDE Plasma.'),
  p('Version 1.0 (Udaan) | AMD64 | Guide edition: 2 October 2026'),
  p('This candidate is prepared for testing before the final release. A successful ISO build does not replace live-session, installation and hardware tests.'),
  h('Start here'),p('Boot the ISO and open Aarambh. Choose <b>Try JatayuOS</b> to explore the desktop or <b>Install JatayuOS</b> to open the installer. The manual and FAQ are available offline from Aarambh, the application menu and the live desktop.'),
  rows([('Before installing','Back up your data and verify the ISO checksum. First test the candidate in a disposable virtual machine.'),('Guide map','2 Installation | 3 Desktop and applications | 4 Jatayu apps | 5 Language and Android | 6 Help | 7 Credits and legal notices')])]),
 ('Install and first start',[
  h('1. Verify the download'),p('Keep the ISO and SHA256SUMS together. On Linux, run <b>sha256sum -c SHA256SUMS</b>. On Windows PowerShell, use <b>Get-FileHash -Algorithm SHA256 path-to-iso</b> and compare the complete hash. A matching checksum confirms the downloaded bytes match the supplied file.'),
  h('2. Prepare a test environment'),p('Use an AMD64 virtual machine or a supported 64-bit PC. The installer checks for at least 25 GB storage and 1.5 GiB RAM. Those are installer thresholds, not a performance guarantee. Allocate additional space and memory for office work, updates and Android.'),
  h('3. Boot the live session'),p('Attach the ISO to the VM, or write it to a USB device using a trusted image-writing tool. Writing an image replaces the USB contents. Start from the selected device, then wait for the boot menu, Plymouth and KDE desktop. Secure Boot compatibility has not been certified for this candidate.'),
  h('4. Review the installer'),p('Open Install JatayuOS. Confirm your keyboard, time zone, account and target disk. India / Asia-Kolkata is the initial time-zone choice. Read the partition summary carefully: erase-disk installation deletes data on the chosen disk. The desktop welcome screen has no language selector.'),
  h('5. Restart into the installed system'),p('After the installer completes, restart and remove the installation medium when requested. Aarambh opens on the installed desktop. Connect to your network, open Discover and review updates.'),
  h('Offline installation'),p('The build includes desktop packages and both BIOS and UEFI GRUB platform binaries for an offline installation path. Online services, new software, updates and Android image setup require internet. Offline installation still needs testing on this exact candidate.')]),
 ('Your desktop and daily applications',[
  p('The Jatayu menu opens installed applications. The bottom panel provides pinned apps, running windows, network and sound controls, the clock and a desktop switch. Firefox ESR remains Mozilla-branded.'),
  rows([('Dolphin','Browse Home, Desktop, Documents, Downloads, Pictures, Music and Videos. Open Places from the side-panel controls if hidden. Your own bookmarks remain editable.'),('Firefox ESR','Web browsing using the Debian Firefox ESR package. External links from Jatayu web apps open in your default browser.'),('LibreOffice','Writer for documents, Calc for spreadsheets, Impress for presentations, plus Draw and the other packaged suite components.'),('Discover / Settings','Discover manages software and updates. System Settings controls displays, audio, network, appearance, shortcuts and regional options.'),('Files and media','Kate edits text; Konsole provides a terminal; Ark handles archives; Gwenview views images; Okular reads documents; Spectacle captures screenshots.'),('Storage and diagnostics','Partition Manager and GParted manage storage; htop and fastfetch show system information. Partition changes can destroy data.'),('Desktop services','NetworkManager, PipeWire, Bluetooth, Fcitx5 and firmware packages support common hardware; actual compatibility depends on the device.')]),
  h('Useful keyboard shortcuts'),p('Meta: application menu. Meta+E: Dolphin. Alt+Space: KRunner. Alt+Tab: switch windows. Ctrl+Alt+T: terminal when the KDE default binding is enabled. Custom bindings can be changed in System Settings.'),
  h('Dock and files'),p('Right-click an application to manage its panel pin. New accounts receive standard user folders before Aarambh opens; Dolphin supplies its native Places model. Mounted drives appear when detected. Existing bookmarks and user preferences are not reset.')]),
 ('Jatayu applications',[
  p('Open the Jatayu Tools menu for the bundled utility suite. Each application has a specific purpose; online services retain their own terms and privacy policies.'),
  rows([('Aarambh','Welcome and first-start hub: offline help, Files, Firefox, Discover, Settings, Editing Tools, Wallpaper Changer and About. Clear the startup checkbox to stop automatic opening.'),('Jatayu Editing Tools','The supplied 2.0.2 desktop utility for image/PDF processing. Choose input files, operation and a new output path. Keep originals and check exported results.'),('Jatayu Wallpaper Changer','Version 1.2.1: 24 offline India, nature and space scenes, search, favourites and automatic rotation. Choose a screen or all screens; the app applies wallpapers through Plasma.'),('Kavach','Local dashboard with links to firewall settings, system updates and personal-file backup. Its dashboard does not certify system security.'),('Sarkar Setu','A local directory of public-service links. External sites open in Firefox; their operators handle accounts and transactions.'),('Utsav','The owner-supplied local HTML application, opened in its own desktop window. Its content is bundled unchanged.'),('Sanjeevani / Jaanch','The shared Jatayu app contains personal-folder backup and basic local diagnostics. These are not full-system snapshots or boot recovery.'),('Bhasa Setu / Android Setup','Shared-app entry points for language/input settings and Waydroid readiness. Standard KDE settings and official Android setup remain authoritative.')]),
  h('Wallpaper collection'),p('The bundled PNG exports are 1920 x 1080, resized from generated masters. The scenes are generated illustrations, not verified photographs of the depicted locations. Application licensing and artwork notices are separate. Your wallpaper settings are stored in your own account.'),
  h('Personal-file backup'),p('Use Kavach\'s backup action or <b>jatayu backup</b>. Choose a source folder and a separate destination, preferably on an external disk. Restore to a new directory; verify important files before deleting any originals.')]),
 ('Language, input and Android',[
  h('Indian languages and keyboard input'),p('Open System Settings for display language, regional formats and keyboard layouts. These are separate choices. Open Fcitx5 Configuration to add an input method such as a Hindi method supplied by m17n. Sign out and back in when required.'),
  p('The Wayland configuration lets KWin start Fcitx5 through its input-method socket. The independent XDG autostart is limited to an X11 fallback. If typing fails, review Virtual Keyboard settings in KDE and confirm the selected input method rather than starting several Fcitx processes.'),
  h('Waydroid is included; Android setup is separate'),p('Waydroid needs a compatible Wayland session, Linux binder support and working graphics. Download and initialise the Android system/vendor images using the official guide. Android images, Google apps, Play Store and ARM translation libraries are not bundled.'),
  p('Typical initial setup, after reviewing the official guide: open a terminal and run <b>sudo waydroid init</b>; then start a user session with <b>waydroid session start</b> and open <b>waydroid show-full-ui</b>. Use administrator authentication for setup. Network access and additional disk space are required.'),
  p('<link href="https://docs.waydro.id/usage/install-on-desktops" color="#176879">Official Waydroid installation guide</link><br/><link href="https://docs.waydro.id/usage/waydroid-command-line-options" color="#176879">Official command-line reference</link>'),
  h('Android troubleshooting'),p('If the UI does not start, check <b>echo $XDG_SESSION_TYPE</b> and <b>waydroid status</b>. An X11 session, missing binder devices or unsupported VM graphics can prevent operation. Android support varies by hardware and app; a VM may not provide suitable graphics.'),
  h('Updates'),p('Review Debian package updates in Discover. A separate signed Jatayu update repository has not been published. New ISO builds do not automatically update installed machines.')]),
 ('Help and candidate testing',[
  rows([('Only Home in Dolphin','Open the Places panel. Confirm standard folders exist. Open the desired folder and add it to Places if needed. This build creates standard directories before Aarambh; user bookmarks stay under your control.'),('Installer does not open','Installation is available from the live ISO. Use the branded Install JatayuOS entry. If it fails, capture the error and the Calamares log; do not start another partition operation.'),('Wallpaper does not apply','Confirm that KDE Plasma is running. Check the selected screen and show the app error details. Automatic rotation needs the account\'s background service and a live Plasma D-Bus session.'),('Fcitx startup warning','Allow the desktop to settle, then inspect your input-method configuration. This build preserves diagnostics and extends the startup grace period; that is not proof of correct input on every machine.'),('Boot or display failure','Record BIOS/UEFI mode, VM configuration or hardware model and the exact stage reached. Test a graphics-safe boot option if provided by the boot menu.'),('Network or audio failure','Check the panel and System Settings. Record the adapter and driver information; do not assume a firmware package covers every device.')]),
  h('Report a problem'),p('Contact <b>jatayuos4u@gmail.com</b> or use the project repository. Include the candidate ISO checksum, hardware/VM details, boot mode, exact steps, expected result and relevant logs. Review logs and screenshots for personal information before sharing.'),
  h('Before the final release'),p('Test live BIOS and UEFI boot; offline installation; first installed boot; network/audio; Dolphin Places; every dock pin; the wallpaper gallery and rotation; LibreOffice; input methods; and Waydroid on compatible hardware. A successful build precheck verifies source/package inputs, not all these behaviours.'),
  p('<link href="https://github.com/jatayuos4u/jatayuos" color="#176879">Project source repository</link> - access may be restricted while the candidate is under review.')]),
 ('Identity, credits and legal notices',[
  h('Why JatayuOS?'),p('Jatayu is the courageous bird associated with the Ramayana. The project uses the name to express courage, service and protection, and to connect its desktop identity with Indian culture. This is the project\'s naming story; it does not imply religious, governmental or institutional endorsement.'),
  p('<b>Made in India</b> describes the project\'s origin and distribution work. JatayuOS is built on contributions from global open-source communities; it does not claim that every bundled component was developed in India.'),
  p('<b>Creator and maintainer:</b> Anup Yadav. Thanks to Debian contributors, the Linux kernel community, KDE, Mozilla, Qt/PySide/PyQt, The Document Foundation, Calamares, Fcitx, Waydroid and the maintainers of all installed utilities, fonts, drivers and firmware. Exact package names and versions are recorded in the image\'s package manifest.'),
  p('Installed copyright and licence files are retained under <b>/usr/share/doc</b>. Collected notices and the build package/source-version manifest are available under <b>/usr/share/jatayu</b>. Wallpaper application source is bundled under <b>/usr/share/doc/jatayu-wallpaper</b>.'),
  p('JatayuOS is independent and is not affiliated with or endorsed by the Government of India, Debian, KDE, Mozilla or other upstream projects. Third-party names and marks remain those of their respective owners. Bundled components retain their individual licences. The project\'s original integration/artwork publication licence remains a maintainer decision; this guide grants no new licence.'),
  p('Public redistribution requires review of applicable licences, trademarks, firmware/artwork rights and corresponding-source delivery. This candidate\'s notice collection and generic upstream links alone do not supply all required corresponding source.'),
  *[p(f'<link href="{url}" color="#176879">{escape(label)}</link>','Small') for label,url in REFERENCES]])]

faq=[('Frequently Asked Questions',[
 p('JatayuOS 1.0 (Udaan) | Offline help | 2 October 2026'),
 h('What is JatayuOS?'),p('An independent Debian 13 desktop with KDE Plasma, Firefox ESR, LibreOffice and Jatayu applications. Created by Anup Yadav, with an India-first project identity and global open-source foundations.'),
 h('Is this the final version?'),p('No. This is a Release Candidate for testing. Development Preview wording has been retired from the desktop, but final-release validation is still required.'),
 h('Why the name JatayuOS?'),p('The name draws on Jatayu\'s courage, service and protection in the Ramayana. It expresses the project\'s intended identity without claiming institutional endorsement.'),
 h('What does Made in India mean?'),p('It refers to the origin of the JatayuOS project and its distribution work. Debian, Linux, KDE and other upstream components come from international communities.'),
 h('Do I need internet to install?'),p('The candidate includes an offline installation path. Internet is needed for updates, online services, extra software and Android image setup. Test offline installation in a disposable VM first.'),
 h('Does installation erase files?'),p('Erase-disk installation deletes the selected disk\'s data. Other partition changes can also cause data loss. Back up your files and read Calamares\' final summary before confirming.'),
 h('Does the live session save my changes?'),p('Do not rely on persistence. An ordinary live session loses settings when restarted. Save important files to a separate device or complete installation.')]),
 ('Desktop and Jatayu apps',[
 h('Where are Firefox and LibreOffice?'),p('Firefox ESR is pinned to the panel and listed in the menu. LibreOffice applications are in the Office category. Aarambh links to everyday apps and settings.'),
 h('Why does Dolphin show only Home?'),p('Check that Places is visible and standard folders exist. This candidate creates the standard directories before Aarambh opens and leaves the KDE Places model native. You may add folders to Places yourself; existing bookmarks are not reset.'),
 h('How do I stop Aarambh opening at sign-in?'),p('Clear Show Aarambh when I sign in, then close the app. Reopen Aarambh from the menu to enable it again.'),
 h('Where is Wallpaper Changer?'),p('Open Jatayu Tools or Aarambh. Version 1.2.1 includes 24 offline scenes, favourites and rotation. Choose a screen and apply a wallpaper. Rotation still needs testing through logout/login on the target Plasma desktop.'),
 h('Are the wallpapers real photographs?'),p('No. They are generated artistic illustrations. Full HD describes their exported 1920 x 1080 dimensions. Location labels do not guarantee geographic accuracy.'),
 h('Do Sarkar Setu and Kavach store my passwords?'),p('Their wrappers open external links in Firefox and do not implement government account login. The linked sites and browser have their own handling of credentials and personal data. Review each service\'s address and privacy policy.'),
 h('Is Kavach a security certificate?'),p('No. It is a local dashboard with system actions. Effective firewall, update and backup behaviour must be checked on the installed system.'),
 h('How do I get Hindi typing?'),p('Use KDE regional/keyboard settings and Fcitx5 Configuration. Add the desired input method. On Wayland, review KDE\'s Virtual Keyboard selection. Sign out and back in if needed.')]),
 ('Android, updates and support',[
 h('Can Android apps run immediately?'),p('Waydroid is included, but Android system/vendor images require a separate initial download. A compatible Wayland session, binder support and graphics are required. App compatibility is not universal.'),
 h('Are Play Store and Google apps included?'),p('No. Google apps, Play Store and ARM translation libraries are not bundled. Follow official Waydroid guidance and the terms of any additional software you choose.'),
 h('How do I update JatayuOS?'),p('Use Discover for Debian package updates. The candidate has no published signed Jatayu repository. Downloading a new ISO does not update an installed system.'),
 h('Is Secure Boot supported?'),p('This candidate does not claim certified Secure Boot compatibility. Record firmware settings when testing BIOS and UEFI boot.'),
 h('Does a precheck PASS mean everything works?'),p('It confirms required source files, package integrity, declared package availability and dependency checks for the build. It does not replace boot, installer, desktop or hardware testing.'),
 h('Where are credits and licences?'),p('Open About JatayuOS or the credits chapter of the User Manual. Installed notices are under /usr/share/doc; the build manifest identifies exact shipped packages and source versions.'),
 h('Can I redistribute this ISO publicly?'),p('The candidate is for project testing. Public distribution needs a completed licence, trademark/artwork and corresponding-source review. Including credits alone does not satisfy every redistribution requirement.'),
 h('How do I report a problem?'),p('Contact jatayuos4u@gmail.com with the ISO checksum, device/VM details, exact steps and reviewed logs. Do not include passwords or private account data.')])]
# Genuine owner-provided captures; keep their testing-build provenance visible.
manual.insert(3,('Desktop screenshot',[
 p('This real-PC capture was supplied during release testing on 2 October 2026. It shows the existing desktop design; the window footer belongs to the earlier candidate.'),
 Image(str(ROOT/'docs/screenshots/desktop-dolphin-testing.png'),width=495,height=290,hAlign='LEFT'),
 h('Dolphin Places'),p('The left sidebar provides Home, Desktop, Documents, Downloads, Music, Pictures, Videos, Trash and Network. Devices depend on the hardware and mounted disks.'),
 p('JatayuOS 1.0 (Udaan) keeps this desktop style. Updated version labels and the approved Fastfetch design must be captured from the final tested ISO before publication.')]))
manual[0][1][-1]=rows([('Before installing','Back up your data and verify the ISO checksum. First test the candidate in a disposable virtual machine.'),('Guide map','2 Installation | 3 Desktop | 4 Screenshot | 5 Jatayu apps | 6 Language and Android | 7 Help | 8 Credits')])
faq.append(('Dolphin troubleshooting screenshot',[
 p('Earlier VM testing capture, supplied 2 October 2026. Standard folders existed, but their Places shortcuts were missing. This is a troubleshooting example, not the intended 1.0 sidebar.'),
 Image(str(ROOT/'docs/screenshots/dolphin-vm-before-fix.png'),width=495,height=309,hAlign='LEFT'),
 h('What to check'),p('Confirm the Places panel is visible. The 1.0 image initializes missing standard shortcuts for new accounts. For an existing account, add the desired folders to Places; do not reset customized bookmarks.'),
 h('Firefox window buttons'),p('Open about:config and set the Number preference browser.tabs.inTitlebar to 0, then close and reopen Firefox. The owner confirmed this restores native window controls in the test ISO. New profiles receive this default.')]))
build('USER-MANUAL.pdf','JatayuOS 1.0 (Udaan) User Manual',manual)
build('FAQ.pdf','JatayuOS 1.0 (Udaan) FAQ',faq)

about='''<h1>JatayuOS 1.0 (Udaan)</h1><h3>Made in India</h3>
<p><b>Udaan Aapki. Shakti Bharat Ki.</b></p>
<p>Created and maintained by <b>Anup Yadav</b>. An independent desktop project built on Debian 13, the Linux kernel and KDE Plasma, with Mozilla Firefox ESR and LibreOffice.</p>
<h2>Why JatayuOS?</h2><p>The name draws on the courage, service and protection associated with Jatayu in the Ramayana. It connects the project's identity with Indian culture. Made in India describes the project's origin; the operating system also depends on global open-source contributions.</p>
<h2>Applications made for your desktop</h2><p><b>Aarambh:</b> welcome, help and everyday shortcuts. <b>Jatayu Editing Tools:</b> image and PDF utilities. <b>Jatayu Wallpaper Changer 1.2.1:</b> an offline gallery, favourites and rotation. <b>Kavach:</b> system dashboard. <b>Sarkar Setu:</b> public-service links. <b>Utsav:</b> the supplied local web app. The shared suite also includes personal-folder backup, diagnostics, language settings and Android readiness entry points.</p>
<p><b>Everyday software:</b> Dolphin, Konsole, Kate, Ark, Gwenview, Okular, Spectacle, Discover, System Settings, LibreOffice, Firefox ESR, Partition Manager, GParted, Fcitx5 and Waydroid. Android needs separate image setup and compatible hardware.</p>
<h2>Credits and open-source foundations</h2><p>Thanks to Debian, Linux, KDE, Mozilla, Qt/PySide/PyQt, The Document Foundation, Calamares, Fcitx, Waydroid and every package, font, driver and firmware maintainer. Exact package/source versions are recorded in the installed build manifest. Installed licences remain under /usr/share/doc. The Wallpaper Changer application retains GPL-3.0-or-later; generated-artwork notices are separate.</p>
<h2>Legal and project identity</h2><p>JatayuOS is independent and is not affiliated with or endorsed by the Government of India or upstream projects. Third-party marks belong to their respective owners. Every component retains its individual licence. Original integration/artwork publication licensing remains a maintainer decision. Public redistribution requires corresponding-source delivery and the applicable licence, trademark and artwork review; this page does not grant legal clearance.</p>
<h3>Credits, licences and policies</h3>'''
about+=''.join(f'<p><a href="{url}">{escape(label)}</a></p>' for label,url in REFERENCES)
about+='''<p><a href="https://github.com/jatayuos4u/jatayuos">Project repository</a> · <a href="mailto:jatayuos4u@gmail.com">Contact the maintainer</a></p><p>Release Candidate: prepared for validation before the final release.</p>'''
(ASSETS/'ABOUT.html').write_text('<!doctype html><html><head><meta charset="utf-8"><title>About JatayuOS</title></head><body>'+about+'</body></html>')
(ASSETS/'README.txt').write_text('JatayuOS 1.0 (Udaan)\nMade in India - Created by Anup Yadav\nOffline help: USER-MANUAL.pdf and FAQ.pdf.\nOfficial website: https://jatayuos.in\nOpen About JatayuOS for credits, policies and project information.\nThis candidate requires boot, installation and hardware testing before final release.\n')
print('Generated offline manual, FAQ and About page.')
