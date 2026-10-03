#!/usr/bin/env python3
"""Small shared Qt front end for the Jatayu development suite."""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path
from PySide6.QtCore import Qt, QThread, Signal, QProcess, QUrl, QTimer
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
from PySide6.QtWidgets import (QScrollArea,QTextBrowser,QGridLayout,QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QComboBox,QLineEdit,QFileDialog,QMessageBox,QPlainTextEdit,QCheckBox,QSpinBox,QFormLayout,QListWidget,QListWidgetItem)
import engine

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT if (ROOT/'logo.png').exists() else ROOT.parent/'assets'
STATE=Path.home()/'.local/state/jatayu'
CATALOG=[('office','LibreOffice'),('media','VLC media player'),('graphics','GIMP image editor'),('drawing','Inkscape'),('audio','Audacity'),('video','Kdenlive (more RAM recommended)'),('developer','Developer tools: Git, compiler, debugger'),('printing','Printer support'),('hindi','Hindi language packages')]
STYLE='''QWidget{background:#10212d;color:#eef2f5;font-size:14px} QMainWindow{background:#10212d} QPushButton{background:#203847;border:1px solid #b98e42;border-radius:7px;padding:10px} QPushButton:hover{background:#365268} QPushButton:disabled{color:#71818a;border-color:#465461} QLineEdit,QComboBox,QSpinBox,QPlainTextEdit,QListWidget{background:#192f3e;border:1px solid #526572;border-radius:5px;padding:6px} QLabel#title{font-size:27px;font-weight:bold;color:#ffd17b} QCheckBox{padding:5px}'''

def live():
    try:return 'boot=live' in Path('/proc/cmdline').read_text().split()
    except OSError:return False

class Worker(QThread):
    result=Signal(str); failed=Signal(str)
    def __init__(self,fn,*args):super().__init__();self.fn,self.args=fn,args
    def run(self):
        try:self.result.emit(str(self.fn(*self.args)))
        except Exception as e:self.failed.emit(str(e))

class Window(QMainWindow):
    def __init__(self,mode):
        super().__init__(); self.mode=mode;self.worker=None;self.proc=None; self.buttons=[]
        titles={'live':'Welcome to JatayuOS','welcome':'Aarambh','tools':'Jatayu Tools','update':'Jatayu Update','backup':'Jatayu Sanjeevani','check':'Jaanch','language':'Bhasa Setu','portals':'Sarkar Setu','android':'Android Setup','about':'About JatayuOS'}
        self.setWindowTitle(titles.get(mode,'JatayuOS')); self.resize(820,650 if mode in ('live','welcome','about') else 540)
        self.setWindowIcon(QIcon(str(ASSETS/'logo.png')))
        central=QWidget();scroll=QScrollArea();scroll.setWidgetResizable(True);scroll.setWidget(central);scroll.setFrameShape(QScrollArea.NoFrame);self.setCentralWidget(scroll);self.layout=QVBoxLayout(central);self.layout.setContentsMargins(28,26,28,24);self.layout.setSpacing(12)
        if mode in ('live','welcome'):
            header=QHBoxLayout()
            mark=QLabel();mark.setFixedSize(72,72);mark.setPixmap(QPixmap(str(ASSETS/'logo.png')).scaled(72,72,Qt.KeepAspectRatio,Qt.SmoothTransformation));header.addWidget(mark)
            heading=QVBoxLayout()
            title=QLabel('Welcome to JatayuOS' if mode=='live' else 'Aarambh');title.setWordWrap(True);title.setObjectName('title');heading.addWidget(title)
            heading.addWidget(QLabel('Udaan Aapki. Shakti Bharat Ki.'))
            header.addLayout(heading);header.addStretch();self.layout.addLayout(header)
        else:
            title=QLabel(titles.get(mode,'JatayuOS'));title.setObjectName('title');self.layout.addWidget(title)
            self.text('Udaan Aapki. Shakti Bharat Ki.')
        getattr(self,'page_'+mode)()
        self.button('Official website: jatayuos.in',lambda:QDesktopServices.openUrl(QUrl('https://jatayuos.in')))
        self.log=QPlainTextEdit();self.log.setReadOnly(True);self.log.setMaximumHeight(90);self.log.setVisible(False);self.layout.addWidget(self.log)
        self.text('JatayuOS 1.0 (Udaan) • Made in India • Independent project by Anup Yadav')

    def text(self,s):
        w=QLabel(s);w.setWordWrap(True);self.layout.addWidget(w);return w
    def button(self,label,fn):
        w=QPushButton(label);w.clicked.connect(fn);self.layout.addWidget(w);self.buttons.append(w);return w
    def error(self,s): self.log.setVisible(True); self.log.appendPlainText('Error: '+s)
    def busy(self,value):
        for b in self.buttons:b.setEnabled(not value)
    def work(self,fn,*args):
        if self.worker and self.worker.isRunning():return
        self.busy(True);self.log.setVisible(True);self.log.appendPlainText('Working… Originals will be preserved.')
        self.worker=Worker(fn,*args);self.worker.result.connect(self.log.appendPlainText);self.worker.failed.connect(self.error);self.worker.finished.connect(lambda:self.busy(False));self.worker.start()
    def launch(self,args):
        if not shutil.which(args[0]):return self.error('Not installed: '+args[0])
        if not QProcess.startDetached(args[0],args[1:]):self.error('Could not launch '+args[0])
    def admin(self,args):
        if self.proc and self.proc.state()!=QProcess.NotRunning:return
        self.proc=QProcess(self);self.proc.setProcessChannelMode(QProcess.MergedChannels)
        self.proc.readyReadStandardOutput.connect(lambda:self.log.appendPlainText(bytes(self.proc.readAllStandardOutput()).decode(errors='replace')))
        self.proc.finished.connect(lambda code,status:(self.busy(False),self.log.appendPlainText('Completed.' if code==0 else 'Operation failed or authentication was cancelled.')))
        self.proc.errorOccurred.connect(lambda err:(self.busy(False),self.error('Unable to start authenticated operation.')))
        self.busy(True);self.log.setVisible(True);self.proc.start('pkexec',['/usr/libexec/jatayu-admin',*args])
    def closeEvent(self,e):
        if (self.worker and self.worker.isRunning()) or (self.proc and self.proc.state()!=QProcess.NotRunning):
            QMessageBox.information(self,'Operation in progress','Wait for the active operation to finish before closing.');e.ignore()
        else:e.accept()

    def document(self,name):
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(ASSETS/name)))

    def quick_links(self):
        grid=QGridLayout()
        actions=[('Files',['dolphin']),('Firefox',['firefox-esr']),('Software Center',['plasma-discover']),('System Settings',['systemsettings']),('Jatayu Tools',['jatayu-tools']),('Wallpaper Changer',['jatayu-wallpaper'])]
        for i,(label,args) in enumerate(actions):
            button=QPushButton(label);button.clicked.connect(lambda checked=False,a=args:self.launch(a));grid.addWidget(button,i//3,i%3);self.buttons.append(button)
        self.layout.addLayout(grid)

    def page_live(self):
        self.text('Aarambh is your starting point for JatayuOS. Explore the live desktop, review essential help, or begin installation. Internet is optional.')
        self.text('Made in India • Independent project • Debian 13 + KDE Plasma')
        self.button('User Manual',lambda:self.document('USER-MANUAL.pdf'))
        self.button('Frequently Asked Questions',lambda:self.document('FAQ.pdf'))
        self.button('About JatayuOS',lambda:self.launch(['jatayu','about']))
        self.quick_links()
        self.button('Try JatayuOS',self.close)
        self.button('Install JatayuOS',self.install_os)
        if not live():self.text('Live-session preview. Installation is available only from the ISO.')
    def install_os(self):
        if not live():return self.error('Installation is only available from the live ISO.')
        if QMessageBox.question(self,'Open installer','Open Calamares? For Windows dual boot, use free space and reuse the EFI partition without formatting. Back up your files and BitLocker recovery key. Review the final partition summary before installation.')==QMessageBox.Yes:
            self.log.setVisible(True);self.log.clear()
            self.proc=QProcess(self);self.proc.setProcessChannelMode(QProcess.MergedChannels)
            self.proc.readyReadStandardOutput.connect(lambda:self.log.appendPlainText(bytes(self.proc.readAllStandardOutput()).decode(errors='replace')))
            self.proc.errorOccurred.connect(lambda err:self.error('Could not start the installer. Check the live-session privileges.'))
            self.proc.finished.connect(lambda code,status:self.error('Installer exited with code '+str(code)) if code else None)
            self.proc.start('pkexec',['/usr/libexec/jatayu-live-installer'])

    def page_welcome(self):
        self.text('Made in India • Debian 13 + KDE Plasma')
        self.text('Aarambh helps you get productive quickly. Open essential help, software and settings from one clean starting point.')
        self.text('Shortcuts: Meta opens the app menu; Meta+E opens Files; Ctrl+Alt+T opens Terminal; Print captures the screen. Customize these in System Settings.')
        self.button('User Manual',lambda:self.document('USER-MANUAL.pdf'))
        self.button('Frequently Asked Questions',lambda:self.document('FAQ.pdf'))
        self.quick_links()
        self.text('Useful shortcuts: Meta opens the menu; Meta+E opens Files; Alt+Space opens KRunner; Ctrl+Alt+T opens Terminal.')
        self.button('About JatayuOS',lambda:self.launch(['jatayu','about']))
        startup=QCheckBox('Show Aarambh when I sign in');startup.setChecked(not (STATE/'welcome-complete').exists());startup.toggled.connect(self.set_startup);self.layout.addWidget(startup)
        self.button('Start using JatayuOS',self.close)
    def install_selected(self):
        selected=[k for k,c in self.choices if c.isChecked()]
        if not selected:return self.error('Select at least one software group.')
        if QMessageBox.question(self,'Install software','Install the selected groups and dependencies? This uses internet, disk space and administrator approval.')==QMessageBox.Yes:self.admin(['install',*selected])
    def set_startup(self,enabled):
        STATE.mkdir(parents=True,exist_ok=True)
        marker=STATE/'welcome-complete'
        if enabled:marker.unlink(missing_ok=True)
        else:marker.touch()

    def finish_welcome(self):
        STATE.mkdir(parents=True,exist_ok=True);(STATE/'welcome-complete').touch();self.close()

    def page_update(self):
        self.text('Debian packages are updated through the established Software Center. Review updates there. This preview does not create a separate update engine.')
        self.button('Refresh package information',lambda:self.admin(['refresh']))
        self.button('Open Software Center updates',lambda:self.launch(['plasma-discover','--mode','Update']))
        self.button('Show available package updates',lambda:self.work(engine.command,['apt','list','--upgradable']))
        self.button('Show recent APT history',lambda:self.work(self.apt_history))
        self.text('Jatayu cosmetic updates will require a signed project repository. No unverified repository is configured in this build.')
    def apt_history(self):
        p=Path('/var/log/apt/history.log');return p.read_text(errors='replace')[-12000:] if p.exists() else 'No APT history yet.'

    def page_tools(self):
        self.text('Jatayu Tools Creative Studio is installed for offline image and PDF work.')
        self.button('Open Jatayu Tools',lambda:self.launch(['jatayu-tools']))
    def add_files(self):
        files,_=QFileDialog.getOpenFileNames(self,'Choose input files',str(Path.home()),'Supported documents (*.jpg *.jpeg *.png *.webp *.bmp *.svg *.pdf);;All files (*)')
        for f in files:self.files.addItem(f)
    def move_file(self,delta):
        n=self.files.currentRow();dest=n+delta
        if n>=0 and 0<=dest<self.files.count():item=self.files.takeItem(n);self.files.insertItem(dest,item);self.files.setCurrentRow(dest)
    def run_tools(self):
        files=[self.files.item(i).text() for i in range(self.files.count())]
        if not files:return self.error('Add input files first.')
        op=self.operation.currentIndex()
        if op in (0,3,4) and len(files)!=1:return self.error('This operation accepts one input file.')
        suffix='.'+self.fmt.currentText().lower() if op==0 else '.pdf'
        if op==4:
            parent=QFileDialog.getExistingDirectory(self,'Choose parent folder for a NEW page-images folder')
            if not parent:return
            output=str(Path(parent)/(Path(files[0]).stem+'-pages'))
        else:
            output,_=QFileDialog.getSaveFileName(self,'New output filename',str(Path(files[0]).with_name(Path(files[0]).stem+'-jatayu'+suffix)))
            if not output:return
        if op==0:self.work(engine.convert_image,files,output,self.fmt.currentText(),self.width.value(),self.quality.value())
        elif op==1:self.work(engine.images_to_pdf,files,output)
        elif op==2:self.work(engine.merge_pdf,files,output)
        elif op==3:self.work(engine.compress_pdf,files,output,self.pdfquality.currentText())
        else:self.work(engine.pdf_to_images,files,output)

    def page_backup(self):
        self.text('Create a dated personal-file backup, preferably on an external drive. Restore into a NEW folder. This is not full-system recovery or an encrypted backup.')
        self.button('Back up a folder',self.backup_folder)
        self.button('Restore a Jatayu backup',self.restore_folder)
        self.text('Automatic scheduling and bootable recovery are not implemented in this release candidate.')
    def backup_folder(self):
        src=QFileDialog.getExistingDirectory(self,'Folder to back up',str(Path.home()))
        if not src:return
        dest=QFileDialog.getExistingDirectory(self,'Backup destination — external drive recommended')
        if dest:self.work(engine.backup,src,dest)
    def restore_folder(self):
        src=QFileDialog.getExistingDirectory(self,'Choose a JatayuBackup folder')
        if not src:return
        parent=QFileDialog.getExistingDirectory(self,'Parent directory for a new restored folder')
        if parent:self.work(engine.restore,src,str(Path(parent)/'Jatayu-Restored'))

    def page_check(self):
        self.text('Local system checks. No report is uploaded automatically.')
        self.button('Run basic diagnostics',lambda:self.work(engine.diagnostics))
        self.button('Save visible report',self.save_report)
        self.button('Open system monitor',lambda:self.launch(['konsole','-e','htop']))
    def save_report(self):
        p,_=QFileDialog.getSaveFileName(self,'Save report','jatayu-diagnostics.txt')
        if p:
            try:
                with open(p,'x') as f:f.write(self.log.toPlainText())
            except Exception as e:self.error(str(e))

    def page_language(self):
        self.text('Manage desktop language, Indian input methods and keyboard layouts with KDE and Fcitx. Changes may require signing out.')
        self.button('Language and regional settings',lambda:self.launch(['systemsettings','kcm_regionandlang']))
        self.button('Keyboard layouts',lambda:self.launch(['systemsettings','kcm_keyboard']))
        self.button('Indian input methods',lambda:self.launch(['fcitx5-config-qt']))
        self.button('Input method setup',lambda:self.launch(['im-config']))
        self.button('Install Hindi language packages',lambda:self.admin(['install','hindi']))

    def page_portals(self):
        self.text('Links open in Firefox. These services are run by their respective organizations. JatayuOS does not collect credentials or represent the Government of India. Verify the address before signing in.')
        for title,url in [('National Portal of India','https://www.india.gov.in/'),('DigiLocker','https://www.digilocker.gov.in/'),('UIDAI','https://uidai.gov.in/'),('UMANG','https://web.umang.gov.in/'),('National Scholarship Portal','https://scholarships.gov.in/')]:
            self.button(title+' — '+url,lambda checked=False,u=url:QDesktopServices.openUrl(QUrl(u)))

    def page_android(self):
        self.text('Waydroid is included from Debian Trixie backports. A Wayland session, compatible kernel binder support, and a separate Android image download are required. No Google apps or ARM translation libraries are bundled.')
        self.button('Check Android readiness',lambda:self.work(self.android_check))
        self.button('Start installed Waydroid UI',lambda:self.launch(['waydroid','show-full-ui']))
        self.button('Stop Waydroid session',lambda:self.launch(['waydroid','session','stop']))
        self.button('Open official setup documentation',lambda:QDesktopServices.openUrl(QUrl('https://docs.waydro.id/usage/install-on-desktops')))
        self.text('Initialize Waydroid after installation using its official setup documentation. Hardware and app compatibility still require testing.')
    def android_check(self):
        mem=next((int(x.split()[1])//1024 for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemTotal:')),0)
        return f'RAM: {mem} MiB\nWayland session: {os.environ.get("XDG_SESSION_TYPE")=="wayland"}\nWaydroid installed: {bool(shutil.which("waydroid"))}\nBinder device present: {any(Path(x).exists() for x in ["/dev/binder","/dev/binderfs/binder-control"])}\nThis is a basic check; GPU and app compatibility still require testing.'

    def page_about(self):
        page=QTextBrowser();page.setOpenExternalLinks(True);page.setMinimumHeight(350)
        page.setHtml((ASSETS/'ABOUT.html').read_text())
        self.layout.addWidget(page)
        grid=QGridLayout()
        actions=[('Offline User Manual',lambda:self.document('USER-MANUAL.pdf')),('Offline FAQ',lambda:self.document('FAQ.pdf')),('Installed licences and credits',lambda:QDesktopServices.openUrl(QUrl.fromLocalFile('/usr/share/doc'))),('Installed package manifest',lambda:self.document('build-package-manifest.tsv'))]
        for i,(label,action) in enumerate(actions):
            button=QPushButton(label);button.clicked.connect(action);grid.addWidget(button,i//2,i%2);self.buttons.append(button)
        self.layout.addLayout(grid)

def initialise_user_folders():
    if shutil.which('xdg-user-dirs-update'):
        subprocess.run(['xdg-user-dirs-update'],check=False)
    for name in ('Desktop','Documents','Downloads','Music','Pictures','Videos','Templates','Public'):
        (Path.home()/name).mkdir(exist_ok=True)
    # Leave user bookmarks and Dolphin's native Places model untouched.


def main():
    direct_install=len(sys.argv)>1 and sys.argv[1]=='live-install'
    if direct_install:
        if not live():
            print('Installation is available only from the live ISO.',file=sys.stderr);return 2
        sys.argv[1]='live'
    p=argparse.ArgumentParser();p.add_argument('mode',nargs='?',default='welcome',choices=['live','welcome','tools','update','backup','check','language','portals','android','about','autostart']);p.add_argument('--smoke',action='store_true');a=p.parse_args()
    mode=a.mode
    if mode=='autostart':
        if live():
            desktop=Path.home()/'Desktop';desktop.mkdir(exist_ok=True)
            for name in ('org.jatayu.installer.desktop',):
                source=Path('/usr/share/applications')/name
                if source.is_file():
                    target=desktop/name
                    if not target.exists():shutil.copyfile(source,target);target.chmod(0o755)
            mode='live'
        elif (STATE/'welcome-complete').exists():return 0
        else:mode='welcome'
    initialise_user_folders()
    app=QApplication(sys.argv);app.setDesktopFileName('org.jatayu.welcome' if mode in ('live','welcome') else 'org.jatayu.'+mode);app.setStyle('Fusion');app.setStyleSheet(STYLE)
    w=Window(mode);w.show()
    if direct_install:QTimer.singleShot(0,w.install_os)
    if a.smoke:
        app.processEvents();w.grab().save(os.environ.get('JATAYU_SMOKE_IMAGE','/tmp/jatayu-smoke.png'));w.close();return 0
    return app.exec()
if __name__=='__main__':sys.exit(main())
