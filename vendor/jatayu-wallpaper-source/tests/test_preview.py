"""Offscreen regression for final-page preview/layout stability."""
import os,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ['QT_QPA_PLATFORM']='offscreen'
os.environ['XDG_CONFIG_HOME']=tempfile.mkdtemp()
os.environ['JATAYU_WALLPAPER_DATA']=str(ROOT/'wallpapers')
sys.path.insert(0,str(ROOT/'src'))
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject,QEvent
from PyQt6.QtTest import QTest
from app import Window,STYLE,light_palette
Window.ensure_service=lambda self:None
Window.refresh_screens=lambda self:None
app=QApplication([]);app.setStyle('Fusion');app.setPalette(light_palette());app.setStyleSheet(STYLE)
w=Window();w.show()
for _ in range(100):
 QTest.qWait(100)
 if w.gallery.count()==24:break
assert w.gallery.count()==24
class Counter(QObject):
 count=0
 def eventFilter(self,obj,event):
  if event.type() in (QEvent.Type.Resize,QEvent.Type.LayoutRequest):self.count+=1
  return False
counter=Counter();w.preview.installEventFilter(counter)
for width,height in [(1280,800),(960,640),(1600,1000)]:
 w.resize(width,height)
 for _ in range(3):
  for page in (0,1,2,1,2):
   w.move_page(page-w.page);QTest.qWait(150)
   assert w.selected and not w.gallery.currentItem().isHidden()
   for i in range(w.gallery.count()):
    item=w.gallery.item(i)
    if not item.isHidden():w.gallery.setCurrentItem(item);QTest.qWait(15)
   QTest.qWait(200);before=counter.count
   QTest.qWait(300)
   assert counter.count==before,(width,page,'Preview layout did not settle')
   assert not w.preview.image.isNull()
w.resize(1280,800);w.move_page(2-w.page);QTest.qWait(300)
from PyQt6.QtCore import QBuffer,QIODevice
buf=QBuffer();buf.open(QIODevice.OpenModeFlag.WriteOnly);w.grab().save(buf,'PNG')
(ROOT.parent/'dist/Jatayu-Wallpaper-Changer-1.2.1-page3.png').write_bytes(bytes(buf.data()))
w.close()
print('PASS: repeated page 3 navigation, every visible wallpaper selection, and stable preview layout at three window sizes')
