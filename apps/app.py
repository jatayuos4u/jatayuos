#!/usr/bin/env python3
"""Small shared Qt front end for the Jatayu development suite."""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path
from PySide6.QtCore import Qt, QThread, Signal, QProcess, QUrl
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QComboBox,QLineEdit,QFileDialog,QMessageBox,QPlainTextEdit,QCheckBox,QSpinBox,QFormLayout,QListWidget,QListWidgetItem)
import engine

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT if (ROOT/'logo.svg').exists() else ROOT.parent/'assets'
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
        self.setWindowTitle(titles.get(mode,'JatayuOS')); self.resize(850,650)
        self.setWindowIcon(QIcon(str(ASSETS/'logo.svg')))
        central=QWidget();self.setCentralWidget(central);self.layout=QVBoxLayout(central);self.layout.setContentsMargins(24,24,24,24)
        title=QLabel(titles.get(mode,'JatayuOS'));title.setObjectName('title');self.layout.addWidget(title)
        self.text('Udaan Aapki. Shakti Bharat Ki.')
        getattr(self,'page_'+mode)()
        self.log=QPlainTextEdit();self.log.setReadOnly(True);self.log.setMaximumHeight(140);self.layout.addWidget(self.log)
        self.text('Development preview • Independent project by Anup Yadav • No government affiliation')

    def text(self,s):
        w=QLabel(s);w.setWordWrap(True);self.layout.addWidget(w);return w
    def button(self,label,fn):
        w=QPushButton(label);w.clicked.connect(fn);self.layout.addWidget(w);self.buttons.append(w);return w
    def error(self,s): self.log.appendPlainText('Error: '+s)
    def busy(self,value):
        for b in self.buttons:b.setEnabled(not value)
    def work(self,fn,*args):
        if self.worker and self.worker.isRunning():return
        self.busy(True);self.log.appendPlainText('Working… Originals will be preserved.')
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
        self.busy(True);self.proc.start('pkexec',['/usr/libexec/jatayu-admin',*args])
    def closeEvent(self,e):
        if (self.worker and self.worker.isRunning()) or (self.proc and self.proc.state()!=QProcess.NotRunning):
            QMessageBox.information(self,'Operation in progress','Wait for the active operation to finish before closing.');e.ignore()
        else:e.accept()

    def page_live(self):
        self.setStyleSheet(STYLE+' QMainWindow{border-top:8px solid #f6a34a;border-bottom:8px solid #23834b}')
        self.text('Choose your language and keyboard. Try the desktop or open the installer. You can continue without internet.')
        self.lang=QComboBox();self.lang.addItem('English (India)','en_IN.UTF-8');self.lang.addItem('हिन्दी — Hindi','hi_IN.UTF-8');self.layout.addWidget(self.lang)
        self.keys=QComboBox();self.keys.addItem('English (US)','us');self.keys.addItem('Indian layout','in');self.layout.addWidget(self.keys)
        field=QLineEdit();field.setPlaceholderText('Type here to test your keyboard');self.layout.addWidget(field)
        self.button('Apply live-session keyboard and locale',lambda:self.admin(['live-layout',self.lang.currentData(),self.keys.currentData()]))
        self.text('Confirm language and keyboard again in Calamares. The preview interface is currently English; full Hindi translation is pending.')
        self.button('Network settings (optional)',lambda:self.launch(['systemsettings','kcm_networkmanagement']))
        self.button('Try JatayuOS — continue to desktop',self.close)
        self.button('Install JatayuOS…',self.install_os)
        if not live():self.text('Live-session screen preview. Installation is disabled outside a live boot.')
    def install_os(self):
        if not live():return self.error('Installation is only available from the live ISO.')
        if QMessageBox.question(self,'Open installer','Open Calamares? Review its partition summary carefully before approving installation.')==QMessageBox.Yes:
            self.launch(['calamares-install-debian'])

    def page_welcome(self):
        self.text('Choose optional software. Downloads need internet and administrator approval. Nothing is preselected.')
        self.choices=[]
        for key,label in CATALOG:
            c=QCheckBox(label);self.layout.addWidget(c);self.choices.append((key,c))
        self.button('Install selected software',self.install_selected)
        self.button('Software Center',lambda:self.launch(['plasma-discover']))
        self.button('Language and keyboard',lambda:self.launch(['jatayu','language']))
        self.button('Android setup',lambda:self.launch(['jatayu','android']))
        self.button('Finish — do not open automatically again',self.finish_welcome)
    def install_selected(self):
        selected=[k for k,c in self.choices if c.isChecked()]
        if not selected:return self.error('Select at least one software group.')
        if QMessageBox.question(self,'Install software','Install the selected groups and dependencies? This uses internet, disk space and administrator approval.')==QMessageBox.Yes:self.admin(['install',*selected])
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
        self.text('Offline image and PDF tools. New outputs only; originals are never overwritten. Use Up/Down to set PDF page or merge order.')
        self.operation=QComboBox();self.operation.addItems(['Convert / resize / compress image','Images to PDF','Merge PDFs','Compress PDF','PDF to PNG images']);self.layout.addWidget(self.operation)
        self.files=QListWidget();self.layout.addWidget(self.files)
        self.button('Add input files',self.add_files)
        row=QHBoxLayout()
        for label,delta in [('Move up',-1),('Move down',1)]:
            b=QPushButton(label);b.clicked.connect(lambda checked=False,d=delta:self.move_file(d));row.addWidget(b)
        b=QPushButton('Clear');b.clicked.connect(self.files.clear);row.addWidget(b);self.layout.addLayout(row)
        form=QFormLayout();self.fmt=QComboBox();self.fmt.addItems(['PNG','JPG','WEBP','BMP']);form.addRow('Image output format',self.fmt)
        self.width=QSpinBox();self.width.setRange(0,8192);self.width.setSpecialValueText('Original width');form.addRow('Maximum width (pixels)',self.width)
        self.quality=QSpinBox();self.quality.setRange(10,100);self.quality.setValue(85);form.addRow('JPEG/WebP quality',self.quality)
        self.pdfquality=QComboBox();self.pdfquality.addItems(['ebook','screen','printer']);form.addRow('PDF quality preset',self.pdfquality);self.layout.addLayout(form)
        self.button('Choose output and run',self.run_tools)
        self.text('PDF compression may reduce quality. SVG supports self-contained shapes only. This preview processes one image per conversion; multi-image PDF creation is supported.')
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
        self.text('Automatic scheduling and bootable recovery are not implemented in this development preview.')
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
        self.text('Experimental Waydroid integration. Android is optional and not part of the 2 GB RAM promise. The Android image needs a separate download. No Play Store, Google apps or ARM translation libraries are bundled.')
        self.button('Check Android readiness',lambda:self.work(self.android_check))
        self.button('Start installed Waydroid UI',lambda:self.launch(['waydroid','show-full-ui']))
        self.button('Stop Waydroid session',lambda:self.launch(['waydroid','session','stop']))
        self.button('Open official setup documentation',lambda:QDesktopServices.openUrl(QUrl('https://docs.waydro.id/usage/install-on-desktops')))
        self.text('Waydroid host installation is not automated until a maintained Trixie package/repository and signing key have been verified. This screen alone does not provide Android compatibility.')
    def android_check(self):
        mem=next((int(x.split()[1])//1024 for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemTotal:')),0)
        return f'RAM: {mem} MiB\nWayland session: {os.environ.get("XDG_SESSION_TYPE")=="wayland"}\nWaydroid installed: {bool(shutil.which("waydroid"))}\nBinder device present: {any(Path(x).exists() for x in ["/dev/binder","/dev/binderfs/binder-control"])}\nThis is a basic check; GPU and app compatibility still require testing.'

    def page_about(self):
        self.text('JatayuOS 0.1 development preview\nCreated by Anup Yadav, India\nBased on Debian 13 with KDE Plasma and Mozilla Firefox ESR.\nContact: jatayuos4u@gmail.com')
        self.text('JatayuOS is independent and is not affiliated with or endorsed by the Government of India or the Debian Project. Debian is a registered trademark owned by Software in the Public Interest, Inc. Other marks belong to their owners.')
        self.button('Open third-party licence files',lambda:QDesktopServices.openUrl(QUrl.fromLocalFile('/usr/share/doc')))
        self.button('Open development notes',lambda:QDesktopServices.openUrl(QUrl.fromLocalFile(str(ROOT/'README.txt'))))

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',nargs='?',default='welcome',choices=['live','welcome','tools','update','backup','check','language','portals','android','about','autostart']);p.add_argument('--smoke',action='store_true');a=p.parse_args()
    mode=a.mode
    if mode=='autostart':
        if live():mode='live'
        elif (STATE/'welcome-complete').exists():return 0
        else:mode='welcome'
    app=QApplication(sys.argv);app.setStyle('Fusion');app.setStyleSheet(STYLE)
    w=Window(mode);w.show()
    if a.smoke:
        app.processEvents();w.grab().save(os.environ.get('JATAYU_SMOKE_IMAGE','/tmp/jatayu-smoke.png'));w.close();return 0
    return app.exec()
if __name__=='__main__':sys.exit(main())
