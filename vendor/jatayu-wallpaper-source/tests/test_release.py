import os,sys,tempfile,subprocess,time,json,zipfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
os.environ['QT_QPA_PLATFORM']='offscreen'
os.environ['XDG_CONFIG_HOME']=tempfile.mkdtemp(prefix='jatayu-test-')
os.environ['JATAYU_WALLPAPER_DATA']=str(ROOT/'build/app/usr/share/wallpapers/Jatayu-Collection')
from core import *
from plasma import Plasma
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtTest import QTest

# Unit/asset checks
entries=collection(settings());assert len(entries)==len(read_json(DATA/'collection.json',[]))
manifest=read_json(DATA/'collection.json',[])
from PIL import Image
for e in manifest:
    with Image.open(DATA/e['file']) as im: im.load();assert im.size==(1920,1080)
    assert hashlib.sha256((DATA/e['file']).read_bytes()).digest()==hashlib.sha256((ROOT/'wallpapers'/e['file']).read_bytes()).digest()
c=settings();c['shuffle']=True
for _ in range(50):assert next_image(entries,c,entries[0]['path'])!=entries[0]['path']
c['favourites_only']=True;assert next_image(entries,c,'') is None
c['favourites']=[entries[0]['path']];assert next_image(entries,c,'')==entries[0]['path']
save(c);assert settings()['favourites']==c['favourites']
weird=CONFIG/'quote " \' unicode भारत.jpg';weird.write_bytes((DATA/manifest[0]['file']).read_bytes())
script=wallpaper_script(weird,2,6);assert weird.as_uri() in json.loads(script.split('d.writeConfig("Image",')[1].split(');')[0])

# Real session D-Bus transport against a mock Plasma engine, with JS execution.
log=CONFIG/'writes.jsonl';log.parent.mkdir(parents=True,exist_ok=True)
mock=subprocess.Popen([sys.executable,str(ROOT/'tests/mock_plasma.py'),str(log)],stdout=subprocess.PIPE,text=True)
assert mock.stdout.readline().strip()=='READY'
app=QApplication([]);backend=Plasma()
ok,result=backend.sync(wallpaper_script(weird,2,6));assert ok and 'JATAYU_OK:1' in result,(ok,result)
writes=json.loads(log.read_text().splitlines()[-1]);assert writes==[[2,'Image',weird.as_uri()],[2,'FillMode',6]],writes
ok,result=backend.sync(wallpaper_script(weird,-1,2));assert ok and 'JATAYU_OK:2' in result
ok,result=backend.sync(wallpaper_script(weird,1,2));assert ok and 'JATAYU_OK:0' in result
results=[];backend.call(SCREENS_SCRIPT,lambda *a:results.append(a))
for _ in range(100):
    QTest.qWait(20)
    if results:break
assert results and results[0][0] and 'JATAYU_SCREENS:[0,2]' in results[0][1],results

# Actual GUI actions, gallery loading and responsive layout.
from app import Window, STYLE
from PyQt6.QtGui import QPalette, QColor
palette=QPalette()
for role in (QPalette.ColorRole.Window,QPalette.ColorRole.Base,QPalette.ColorRole.Button): palette.setColor(role,QColor('#202326'))
for role in (QPalette.ColorRole.WindowText,QPalette.ColorRole.Text,QPalette.ColorRole.ButtonText): palette.setColor(role,QColor('#fafafa'))
app.setPalette(palette);app.setStyle('Fusion');app.setStyleSheet(STYLE)
c=settings();c['favourites_only']=False;c['favourites']=[];save(c)
w=Window();w.show()
for _ in range(100):
    QTest.qWait(100)
    if w.gallery.count()==len(manifest):break
assert w.gallery.count()==len(manifest),w.gallery.count()
assert w.screen.count()==3,w.screen.count()
# Every original card must be reachable via the explicit page buttons.
seen=set()
for page in range(w.page_total):
    seen.update(w.gallery.item(i).data(Qt.ItemDataRole.UserRole)['path'] for i in range(w.gallery.count()) if not w.gallery.item(i).isHidden())
    if page+1<w.page_total:w.next_page.click();QTest.qWait(30)
assert len(seen)==len(manifest),len(seen)
assert str(len(manifest)) in w.page_label.text(),w.page_label.text()
w.page=0;w.filter();w.gallery.setCurrentRow(0);QTest.qWait(30)
content=w.findChild(__import__('PyQt6.QtWidgets',fromlist=['QWidget']).QWidget,'inspectorContent')
# Check actual rendered background with a dark upstream palette.
pixel=content.grab().toImage().pixelColor(content.width()-8,380)
assert pixel.lightness()>230, pixel.name()
assert w.quality.text().startswith('AI artwork'),w.quality.text()

w.search.setText('Crystal Alpine Lake');QTest.qWait(40)
visible=[w.gallery.item(i) for i in range(w.gallery.count()) if not w.gallery.item(i).isHidden()]
assert len(visible)==1;w.gallery.setCurrentItem(visible[0]);w.toggle_favourite();assert w.selected['path'] in settings()['favourites']
w.search.clear();w.navigate('Favourites');w.gallery.setCurrentItem(visible[0]);assert sum(not w.gallery.item(i).isHidden() for i in range(len(manifest)))==1
w.apply();QTest.qWait(150);assert w.status.text().startswith('Wallpaper applied'),w.status.text()
w.navigate('Library');w.resize(960,640);QTest.qWait(150);assert w.width()==960
w.resize(1280,800);QTest.qWait(150);w.search.setText('Crystal Alpine Lake');QTest.qWait(50);w.gallery.setCurrentItem(visible[0]);w.search.clear();QTest.qWait(300);w.gallery.setCurrentRow(0);QTest.qWait(100)
from PyQt6.QtCore import QBuffer, QIODevice
buffer=QBuffer();buffer.open(QIODevice.OpenModeFlag.WriteOnly);assert w.grab().save(buffer,'PNG')
(ROOT.parent/'dist/Jatayu-Wallpaper-Changer-1.2.0-preview.png').write_bytes(bytes(buffer.data()))
# Non-native folder dialog must stay readable under a dark upstream palette.
d=w.folder_dialog();d.setDirectory(str(ROOT));d.show();QTest.qWait(300)
from PyQt6.QtWidgets import QFileDialog,QTreeView
assert d.testOption(QFileDialog.Option.DontUseNativeDialog)
assert d.palette().color(QPalette.ColorRole.Base).lightness()>230
assert d.palette().color(QPalette.ColorRole.Text).lightness()<80
buffer=QBuffer();buffer.open(QIODevice.OpenModeFlag.WriteOnly);assert d.grab().save(buffer,'PNG')
(ROOT.parent/'dist/Jatayu-Folder-Dialog-1.2.0.png').write_bytes(bytes(buffer.data()))
d.reject()
# A real 60-second interval while the window is closed; verifies second rotation.
w.interval.setCurrentIndex(w.interval.findData(60))
w.auto.setChecked(True)
for _ in range(100):
    QTest.qWait(50)
    state=read_json(CONFIG/'service-status.json',{})
    if state.get('cycles',0)>=1:break
assert state.get('cycles',0)>=1,state
first_path=state['last']
assert (CONFIG.parent/'autostart/jatayu-wallpaper.desktop').exists()
app.setQuitOnLastWindowClosed(False);w.close()
print('First background rotation passed; waiting for the real one-minute interval.',flush=True)
for _ in range(700):
    QTest.qWait(100)
    state=read_json(CONFIG/'service-status.json',{})
    if state.get('cycles',0)>=2:break
assert state.get('cycles',0)>=2,state
assert state['last']!=first_path,'Shuffle repeated the previous wallpaper'
c=settings();c['enabled']=False;save(c)
w.c=c;w.auto.blockSignals(True);w.auto.setChecked(False);w.auto.blockSignals(False);w.ensure_service()
assert not (CONFIG.parent/'autostart/jatayu-wallpaper.desktop').exists()
for _ in range(60):
    QTest.qWait(100)
    if not (CONFIG/'service.lock').exists():break
assert not (CONFIG/'service.lock').exists(),'Background agent did not stop'
# Error handling when the real service disappears.
mock.terminate();mock.wait(timeout=3);errors=[]
backend.call(SCREENS_SCRIPT,lambda *a:errors.append(a))
for _ in range(100):
    QTest.qWait(20)
    if errors:break
assert errors and errors[0][0] is False,errors
w.close();print('PASS: all Full HD PNG exports, settings, shuffle, favourites, JS safety, sync/async D-Bus, screen targeting, missing service, GUI actions, dark palette contrast, all gallery pages, resize, folder dialog contrast, timed rotation after closing GUI and enable/disable lifecycle.')
