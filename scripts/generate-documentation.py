#!/usr/bin/env python3
"""Generate the illustrated offline guides and About page for JatayuOS 1.0."""
from pathlib import Path
from html import escape
import runpy
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
runpy.run_path(str(ROOT/'scripts/generate-illustrated-guides.py'),run_name='__main__')
REFERENCES=[["JatayuOS - official website","https://jatayuos.in"],["JatayuOS - source and release records","https://github.com/jatayuos4u/jatayuos"],["Debian - source and distribution obligations","https://www.debian.org/CD/vendors/legal"],["KDE - community and contributors","https://kde.org/community/"],["Mozilla - software distribution policy","https://www.mozilla.org/en-US/foundation/trademarks/distribution-policy/"],["LibreOffice - licenses","https://www.libreoffice.org/licenses/"],["GNU GPL version 3","https://www.gnu.org/licenses/gpl-3.0.html"]]
about='''<h1>JatayuOS 1.0 (Udaan)</h1><h3>Made in India</h3>
<p><b>Udaan Aapki. Shakti Bharat Ki.</b></p>
<p>Created and maintained by <b>Anup Yadav</b>. An independent desktop project built on Debian 13, the Linux kernel and KDE Plasma, with Mozilla Firefox ESR and LibreOffice.</p>
<h2>Why JatayuOS?</h2><p>The name draws on the courage, service and protection associated with Jatayu in the Ramayana. It connects the project's identity with Indian culture. Made in India describes the project's origin; the operating system also depends on global open-source contributions.</p>
<h2>Applications made for your desktop</h2><p><b>Aarambh:</b> welcome, help and everyday shortcuts. <b>Jatayu Editing Tools:</b> image and PDF utilities. <b>Jatayu Wallpaper Changer 1.2.1:</b> an offline gallery, favourites and rotation. <b>Kavach:</b> system dashboard. <b>Sarkar Setu:</b> public-service links. <b>Utsav:</b> the supplied local web app. The shared suite also includes personal-folder backup, diagnostics, language settings and Android readiness entry points.</p>
<p><b>Everyday software:</b> Dolphin, Konsole, Kate, Ark, Gwenview, Okular, Spectacle, Discover, System Settings, LibreOffice, Firefox ESR, Partition Manager, GParted, Fcitx5, Info Center and Waydroid. Discover supports Debian APT packages and Flatpak apps from Flathub. Android starts on demand and needs separate image setup and compatible hardware. Minimum RAM: 4 GB; 8 GB recommended.</p>
<h2>Credits and open-source foundations</h2><p>Thanks to Debian, Linux, KDE, Mozilla, Qt/PySide/PyQt, The Document Foundation, Calamares, Fcitx, Waydroid and every package, font, driver and firmware maintainer. Exact package/source versions are recorded in the installed build manifest. Installed licences remain under /usr/share/doc. The Wallpaper Changer application retains GPL-3.0-or-later; generated-artwork notices are separate.</p>
<h2>Legal and project identity</h2><p>JatayuOS is independent and is not affiliated with or endorsed by the Government of India or upstream projects. Third-party marks belong to their respective owners. Every component retains its individual licence. Original JatayuOS software is GPL-3.0-or-later under the maintainer-approved scope in COPYRIGHT.md. Artwork and documentation publication terms remain separate. Public redistribution requires corresponding-source delivery and the applicable licence, trademark and artwork review; this page does not grant legal clearance.</p>
<h3>Credits, licences and policies</h3>'''
about+=''.join(f'<p><a href="{url}">{escape(label)}</a></p>' for label,url in REFERENCES)
about+='''<p><a href="https://github.com/jatayuos4u/jatayuos">Project repository</a> · <a href="mailto:jatayuos4u@gmail.com">Contact the maintainer</a></p><p>JatayuOS 1.0 Udaan. See the project website for downloads, release notes and tested scenarios.</p>'''
(ASSETS/'ABOUT.html').write_text('<!doctype html><html><head><meta charset="utf-8"><title>About JatayuOS</title></head><body>'+about+'</body></html>')
(ASSETS/'README.txt').write_text('JatayuOS 1.0 (Udaan)\nMade in India - Created by Anup Yadav\nOffline help: USER-MANUAL.pdf and FAQ.pdf.\nOfficial website: https://jatayuos.in\nOpen About JatayuOS for credits, policies and project information.\nSee the release page for tested installation and hardware scenarios.\n')
print('Generated offline manual, FAQ and About page.')

