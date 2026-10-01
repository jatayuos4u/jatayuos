#!/usr/bin/python3
"""Jatayu Wallpaper Changer GUI. SPDX-License-Identifier: GPL-3.0-or-later."""
import json
import os
import re
import sys
import time
from pathlib import Path
from PyQt6.QtCore import Qt, QSize, QRect, QTimer, QLockFile, QProcess, QCoreApplication
from PyQt6.QtGui import QColor, QIcon, QPixmap, QPainter, QImageReader, QFont, QPen, QPalette
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QAbstractItemView,
    QStyledItemDelegate, QStyle, QComboBox, QCheckBox, QFrame, QFileDialog,
    QMessageBox, QDialog, QTextBrowser, QSplitter, QScrollArea, QSizeGrip, QSizePolicy)
from core import *
from plasma import Plasma

BASE = Path(__file__).resolve().parent.parent
ICON = BASE/'assets/jatayu-wallpaper.svg'
if not ICON.exists():
    ICON = Path('/usr/share/icons/hicolor/scalable/apps/org.jatayuos.WallpaperChanger.svg')

STYLE = '''
QWidget { color: #26313b; font-family: "Noto Sans", "DejaVu Sans"; font-size: 13px; }
QMainWindow, #body, QDialog { background: #faf9f6; }
QFileDialog QWidget { color: #26313b; }
QFileDialog QTreeView, QFileDialog QListView, QDialog QListWidget { background: #fff; color: #26313b; alternate-background-color: #f4f5f6; selection-background-color: #ffe0bf; selection-color: #26313b; }
QHeaderView::section { background: #edece7; color: #26313b; border: 1px solid #dadbd7; padding: 5px; }
QMenu { background: #fff; color: #26313b; border: 1px solid #d6d8d6; }
QMenu::item:selected { background: #ffe0bf; color: #26313b; }
QHeaderView { background: #eeece7; color: #26313b; }
QToolButton { color: #26313b; background: #f4f3ef; }
#titlebar { background: #fff; border-bottom: 1px solid #e5e3df; }
#sidebar { background: #f3f1ed; border-right: 1px solid #e5e3df; }
#inspector { background: #fff; border-left: 1px solid #e5e3df; }
QLabel#heading { font-size: 27px; font-weight: 700; }
QLabel#selectedtitle { font-size: 21px; font-weight: 700; }
QLabel#muted { color: #596675; }
#inspectorContent, #inspectorScroll, #inspectorScroll > QWidget, #inspectorScroll > QWidget > QWidget { background: #fff; color: #26313b; }
QComboBox QAbstractItemView { background: #fff; color: #26313b; selection-background-color: #ffe7d2; selection-color: #26313b; }
QScrollBar:vertical { background: #eeece7; width: 16px; margin: 0; }
QScrollBar::handle:vertical { background: #89949e; min-height: 35px; border: 3px solid #eeece7; border-radius: 7px; }
QScrollBar::handle:vertical:hover { background: #df731a; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: #eeece7; }
QPushButton { background: #fff; border: 1px solid #dbdcd9; border-radius: 7px; padding: 9px 12px; }
QPushButton:hover { border-color: #e98229; background: #fff4e8; }
QPushButton:pressed { background: #ffe2c6; }
QPushButton:disabled { color: #a2a6a9; background: #f0efec; }
QPushButton#primary { color: white; background: #ed7a18; border-color: #ed7a18; font-weight: 700; }
QPushButton#primary:hover { background: #d96709; }
QPushButton#nav { background: transparent; border: 0; text-align: left; padding: 13px 14px; }
QPushButton#nav:checked { color: #bf570a; background: #ffe7d2; font-weight: 700; }
QLineEdit, QComboBox { background: #fff; border: 1px solid #d6d8d6; border-radius: 7px; padding: 8px; }
QComboBox::drop-down { border: 0; width: 22px; }
QListWidget { background: transparent; border: 0; outline: 0; }
QCheckBox { color: #26313b; background: transparent; spacing: 8px; padding: 5px 0; }
QCheckBox::indicator { width: 17px; height: 17px; border: 1px solid #b8bdbf; border-radius: 4px; background: #fff; }
QCheckBox::indicator:checked { background: #ec7b1d; border-color: #ec7b1d; image: none; }
QScrollArea { border: 0; background: transparent; }
QSplitter::handle { background: #e6e4df; width: 2px; }
QTextBrowser { background: #fff; border: 0; padding: 12px; }
'''

def light_palette():
    p=QPalette()
    colors={'Window':'#faf9f6','WindowText':'#26313b','Base':'#ffffff','AlternateBase':'#f4f5f6',
            'Text':'#26313b','Button':'#f4f3ef','ButtonText':'#26313b','Highlight':'#ffe0bf',
            'HighlightedText':'#26313b','ToolTipBase':'#fff8ed','ToolTipText':'#26313b',
            'PlaceholderText':'#697684'}
    for role,color in colors.items():p.setColor(getattr(QPalette.ColorRole,role),QColor(color))
    p.setColor(QPalette.ColorGroup.Disabled,QPalette.ColorRole.Text,QColor('#78838c'))
    p.setColor(QPalette.ColorGroup.Disabled,QPalette.ColorRole.ButtonText,QColor('#78838c'))
    return p

def label(text, name=None):
    w = QLabel(text)
    if name:
        w.setObjectName(name)
    w.setWordWrap(True)
    return w

def button(text, callback, name=None):
    w = QPushButton(text)
    if name:
        w.setObjectName(name)
    w.clicked.connect(callback)
    return w

class TitleBar(QFrame):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setObjectName('titlebar')
        box = QHBoxLayout(self)
        box.setContentsMargins(18, 10, 14, 10)
        icon = QLabel()
        icon.setPixmap(QIcon(str(ICON)).pixmap(32, 32))
        box.addWidget(icon)
        title = label('Jatayu Wallpaper Changer')
        title.setStyleSheet('font-size: 17px; font-weight: 700;')
        title.setWordWrap(False)
        box.addWidget(title, 1)
        for text, color, tip, fn in [('\u2212', '#e6b40a', 'Minimise', window.showMinimized),
            ('+', '#2e9c47', 'Maximise / Restore', self.toggle), ('×', '#df4944', 'Close', window.close)]:
            b = button(text, fn)
            b.setFixedSize(30, 30)
            b.setToolTip(tip)
            b.setAccessibleName(tip)
            b.setStyleSheet('QPushButton {color:white;background:'+color+';border:0;border-radius:4px;padding:0;font-size:19px;}')
            box.addWidget(b)
    def toggle(self):
        self.window.showNormal() if self.window.isMaximized() else self.window.showMaximized()
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.window.windowHandle():
            self.window.windowHandle().startSystemMove()
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle()

class CardDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        return self.parent().gridSize()
    def paint(self, painter, option, index):
        entry = index.data(Qt.ItemDataRole.UserRole)
        if not entry:
            return
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = option.rect.adjusted(5, 5, -5, -5)
        selected = bool(option.state & QStyle.StateFlag.State_Selected)
        painter.setBrush(QColor('#fff'))
        painter.setPen(QPen(QColor('#ec7b1d' if selected else '#e2e3e0'), 2 if selected else 1))
        painter.drawRoundedRect(rect, 9, 9)
        image_rect = QRect(rect.x()+4, rect.y()+4, rect.width()-8, 126)
        pix = index.data(Qt.ItemDataRole.DecorationRole)
        if isinstance(pix, QPixmap) and not pix.isNull():
            scaled = pix.scaled(image_rect.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            painter.save()
            painter.setClipRect(image_rect)
            painter.drawPixmap(image_rect.x()+(image_rect.width()-scaled.width())//2,
                               image_rect.y()+(image_rect.height()-scaled.height())//2, scaled)
            painter.restore()
        else:
            painter.fillRect(image_rect, QColor('#e9e7e1'))
        title_rect = QRect(rect.x()+12, image_rect.bottom()+10, rect.width()-43, 25)
        painter.setPen(QColor('#24313a'))
        f = QFont(option.font); f.setBold(True); painter.setFont(f)
        title = painter.fontMetrics().elidedText(entry['title'], Qt.TextElideMode.ElideRight, title_rect.width())
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignVCenter, title)
        painter.setFont(option.font); painter.setPen(QColor('#727c87'))
        sub = entry['place'] or entry.get('dimensions', 'Local image')
        painter.drawText(QRect(rect.x()+12, title_rect.bottom()+1, rect.width()-24, 21),
                         Qt.AlignmentFlag.AlignVCenter, painter.fontMetrics().elidedText(sub, Qt.TextElideMode.ElideRight, rect.width()-24))
        painter.setPen(QColor('#dc731b' if entry.get('fav') else '#77818b'))
        painter.drawText(QRect(rect.right()-29, title_rect.y(), 24, 25), Qt.AlignmentFlag.AlignCenter, '♥' if entry.get('fav') else '♡')
        painter.restore()

class Preview(QLabel):
    """Paint a cached image without feeding image dimensions back into the layout."""
    def __init__(self):
        super().__init__('Select a wallpaper')
        self.image = QPixmap()
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(195)

    def setPixmap(self, pix):
        self.image = pix
        self.setText('')
        self.update()

    def clear(self):
        self.image = QPixmap()
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.image.isNull(): return
        pix = self.image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation)
        painter = QPainter(self)
        painter.drawPixmap((self.width()-pix.width())//2, (self.height()-pix.height())//2, pix)

class Gallery(QListWidget):
    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = max(225, self.viewport().width())
        cols = max(1, width // 225)
        self.setGridSize(QSize((width-8)//cols, 204))

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.c = settings()
        self.backend = Plasma(self)
        self.entries = []
        self.view = 'Library'
        self.selected = None
        self.loading_generation = 0
        self.page = 0
        self.page_size = 9
        self.page_total = 0
        self.setWindowTitle('Jatayu Wallpaper Changer')
        self.setWindowIcon(QIcon(str(ICON)))
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(940, 620)
        self.resize(1280, 800)
        root = QWidget(); root.setObjectName('body'); self.setCentralWidget(root)
        main = QVBoxLayout(root); main.setSpacing(0); main.setContentsMargins(0,0,0,0)
        main.addWidget(TitleBar(self))
        split = QSplitter(Qt.Orientation.Horizontal)
        main.addWidget(split, 1)
        sidebar = QFrame(); sidebar.setObjectName('sidebar'); sidebar.setMinimumWidth(155); sidebar.setMaximumWidth(210)
        sb = QVBoxLayout(sidebar); sb.setContentsMargins(12, 22, 12, 16)
        self.nav = {}
        for text in ('Library', 'Favourites', 'My folders', 'Slideshow', 'Settings'):
            b = button(text, lambda checked=False, t=text:self.navigate(t), 'nav')
            b.setCheckable(True); sb.addWidget(b); self.nav[text] = b
        self.nav['Library'].setChecked(True)
        sb.addStretch()
        sb.addWidget(label('JatayuOS\nUdaan Aapki.\nShakti Bharat Ki.', 'muted'))
        sb.addWidget(button('About & Help', self.about))
        split.addWidget(sidebar)
        center = QWidget(); cv = QVBoxLayout(center); cv.setContentsMargins(20,20,20,10)
        self.heading = label('Explore India & Beyond', 'heading'); cv.addWidget(self.heading)
        self.count = label('', 'muted'); cv.addWidget(self.count)
        toolbar = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText('Search wallpapers or places…'); self.search.textChanged.connect(self.search_changed)
        toolbar.addWidget(self.search, 1); toolbar.addWidget(button('Add folder', self.add_folder))
        cv.addLayout(toolbar)
        self.gallery = Gallery(); self.gallery.setViewMode(QListWidget.ViewMode.IconMode)
        self.gallery.setResizeMode(QListWidget.ResizeMode.Adjust); self.gallery.setMovement(QListWidget.Movement.Static)
        self.gallery.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.gallery.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.gallery.setWrapping(True); self.gallery.setSpacing(0); self.gallery.setUniformItemSizes(True)
        self.gallery.setGridSize(QSize(240, 204)); self.gallery.setItemDelegate(CardDelegate(self.gallery))
        self.gallery.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.gallery.currentItemChanged.connect(self.select)
        self.gallery.itemDoubleClicked.connect(lambda *_:self.apply())
        cv.addWidget(self.gallery, 1)
        pager = QHBoxLayout()
        self.previous_page = button('‹ Previous', lambda: self.move_page(-1))
        self.next_page = button('Next ›', lambda: self.move_page(1))
        self.page_label = label('', 'muted')
        pager.addWidget(self.previous_page); pager.addWidget(self.page_label, 1); pager.addWidget(self.next_page)
        cv.addLayout(pager)
        self.empty = label('No matching images. Add a folder or adjust your search.', 'muted'); cv.addWidget(self.empty)
        split.addWidget(center)
        inspector = QFrame(); inspector.setObjectName('inspector'); inspector.setMinimumWidth(275); inspector.setMaximumWidth(390)
        iv = QVBoxLayout(inspector); iv.setContentsMargins(18,20,18,16)
        scroll = QScrollArea(); scroll.setObjectName('inspectorScroll'); scroll.setWidgetResizable(True); iv.addWidget(scroll)
        content = QWidget(); content.setObjectName('inspectorContent'); content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True); rv = QVBoxLayout(content); rv.setContentsMargins(0,0,0,0); scroll.setWidget(content)
        self.preview = Preview(); self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setMinimumHeight(175); self.preview.setMaximumHeight(210)
        self.preview.setStyleSheet('background:#f0ede6;border-radius:8px;'); rv.addWidget(self.preview)
        self.title = label('Choose your view', 'selectedtitle'); rv.addWidget(self.title)
        self.place = label('', 'muted'); rv.addWidget(self.place)
        self.dimension = label('', 'muted'); rv.addWidget(self.dimension)
        self.quality = label('', 'muted'); rv.addWidget(self.quality)
        self.favourite = button('♡  Add to favourites', self.toggle_favourite); self.favourite.setEnabled(False); rv.addWidget(self.favourite)
        rv.addSpacing(8); rv.addWidget(label('Display · current KDE Activity'))
        self.screen = QComboBox(); self.screen.addItem('All screens', -1); rv.addWidget(self.screen)
        rv.addWidget(button('Refresh screens', self.refresh_screens))
        rv.addWidget(label('Layout'))
        self.layout = QComboBox()
        for text, value in LAYOUTS.items(): self.layout.addItem(text, value)
        self.layout.setCurrentIndex(max(0,self.layout.findData(self.c['layout']))); rv.addWidget(self.layout)
        self.apply_button = button('Apply Wallpaper', self.apply, 'primary'); self.apply_button.setEnabled(False); rv.addWidget(self.apply_button)
        rv.addSpacing(12)
        self.auto = QCheckBox('Auto change'); self.auto.setChecked(self.c['enabled']); rv.addWidget(self.auto)
        self.interval = QComboBox()
        for text, value in [('Every minute',60),('Every 15 minutes',900),('Every 30 minutes',1800),('Every hour',3600),('Every 6 hours',21600),('Every day',86400)]: self.interval.addItem(text,value)
        self.interval.setCurrentIndex(max(0,self.interval.findData(self.c['interval']))); rv.addWidget(self.interval)
        self.shuffle = QCheckBox('Shuffle — avoid repeats'); self.shuffle.setChecked(self.c['shuffle']); rv.addWidget(self.shuffle)
        self.fav_only = QCheckBox('Rotate favourites only'); self.fav_only.setChecked(self.c['favourites_only']); rv.addWidget(self.fav_only)
        self.login = QCheckBox('Change when agent starts / at login'); self.login.setChecked(self.c['at_login']); rv.addWidget(self.login)
        rv.addWidget(button('Change now', self.change_now))
        self.rotation_status=label('Automatic rotation is off.', 'muted');rv.addWidget(self.rotation_status)
        rv.addWidget(button('Restart auto changer', self.restart_service));rv.addStretch()
        split.addWidget(inspector); split.setSizes([175,770,335]); split.setCollapsible(0,False); split.setCollapsible(1,False); split.setCollapsible(2,False)
        self.status = label('Works offline · Checking KDE Plasma…', 'muted'); self.status.setContentsMargins(16,9,16,9)
        footer=QHBoxLayout();footer.addWidget(self.status,1);footer.addWidget(QSizeGrip(self));main.addLayout(footer)
        for w in (self.auto,self.shuffle,self.fav_only,self.login): w.toggled.connect(self.update_settings)
        for w in (self.interval,self.layout,self.screen): w.currentIndexChanged.connect(self.update_settings)
        self.reload()
        QTimer.singleShot(100,self.refresh_screens)
        QTimer.singleShot(300,self.ensure_service)
        self.health_timer=QTimer(self);self.health_timer.timeout.connect(self.show_rotation_status);self.health_timer.start(2000)

    def navigate(self, text):
        if text in ('Library','Favourites','My folders'):
            self.view = text
            for t,b in self.nav.items(): b.setChecked(t == text)
            self.heading.setText({'Library':'Explore India & Beyond','Favourites':'Your favourites','My folders':'Your local collection'}[text]); self.page = 0; self.filter()
        elif text == 'Slideshow':
            self.auto.setFocus()
            self.dialog('Slideshow', '<h2>Your wallpaper rotation</h2><p>The controls on the right save automatically. Enable <b>Auto change</b> to continue rotation after closing the app and at login. Choose the interval, shuffle, favourites-only pool, display and layout.</p><p>Press <b>Change now</b> to try the next image. No available favourites means favourites-only rotation pauses.</p>')
        else:
            self.manage_folders()
        for t,b in self.nav.items(): b.setChecked(t == self.view)

    def update_settings(self, *_):
        self.c.update(enabled=self.auto.isChecked(), interval=self.interval.currentData(),
            shuffle=self.shuffle.isChecked(), favourites_only=self.fav_only.isChecked(),
            at_login=self.login.isChecked(), screen=self.screen.currentData(), layout=self.layout.currentData())
        try:
            save(self.c)
            self.ensure_service()
        except OSError as e:
            QMessageBox.warning(self,'Settings could not be saved',str(e))

    def ensure_service(self):
        startup = Path(os.environ.get('XDG_CONFIG_HOME',str(Path.home()/'.config')))/'autostart/jatayu-wallpaper.desktop'
        if self.c['enabled']:
            startup.parent.mkdir(parents=True,exist_ok=True)
            startup.write_text('[Desktop Entry]\nType=Application\nName=Jatayu Wallpaper Rotation\nExec=jatayu-wallpaper --start-service\nOnlyShowIn=KDE;\nX-KDE-autostart-after=panel\nNoDisplay=true\n')
        elif startup.exists():startup.unlink()
        CONFIG.mkdir(parents=True,exist_ok=True)
        proc=QProcess()
        proc.setProgram(sys.executable)
        proc.setArguments([str(Path(__file__).resolve()),'--start-service'])
        proc.setStandardErrorFile(str(CONFIG/'service-launch.log'))
        started,pid=proc.startDetached()
        if not started:self.rotation_status.setText('Could not start the background agent. Please reopen the app.')
        self.show_rotation_status()

    def restart_service(self):
        if not self.auto.isChecked():self.auto.setChecked(True);return
        self.auto.setChecked(False)
        QTimer.singleShot(3000,lambda:self.auto.setChecked(True))

    def show_rotation_status(self):
        if not self.c['enabled']:
            self.rotation_status.setText('Automatic rotation is off.');return
        state=read_json(CONFIG/'service-status.json',{})
        if time.time()-state.get('time',0)>15 or state.get('state')=='disabled':
            self.rotation_status.setText('Starting rotation… If this stays here, use Restart auto changer.')
        elif not state.get('ok'):
            self.rotation_status.setText('Auto change: '+state.get('message','Could not change wallpaper.'))
        else:
            remaining=max(0,int(state.get('next_due',time.time())-time.time()))
            self.rotation_status.setText(f'Auto change running · next in {remaining//60:02d}:{remaining%60:02d}')

    def reload(self):
        self.loading_generation += 1
        generation = self.loading_generation
        self.page = 0
        self.entries = collection(self.c)
        self.gallery.clear(); self.selected = None
        self.apply_button.setEnabled(False); self.favourite.setEnabled(False)
        self.preview.clear(); self.title.setText('Choose your view'); self.place.clear(); self.dimension.clear(); self.quality.clear()
        queue = list(self.entries)
        def batch():
            if generation != self.loading_generation: return
            for _ in range(min(6,len(queue))):
                entry = queue.pop(0)
                reader = QImageReader(entry['path']); reader.setAutoTransform(True)
                size = reader.size()
                if not size.isValid(): continue
                entry['dimensions'] = f'{size.width()} × {size.height()}'
                reader.setScaledSize(size.scaled(QSize(480,270),Qt.AspectRatioMode.KeepAspectRatio))
                image = reader.read()
                if image.isNull(): continue
                entry['fav'] = entry['path'] in self.c['favourites']
                item = QListWidgetItem(); item.setData(Qt.ItemDataRole.UserRole,entry)
                item.setData(Qt.ItemDataRole.DecorationRole,QPixmap.fromImage(image)); item.setSizeHint(QSize(220,204))
                item.setText(entry['title']); item.setToolTip(entry['title']+'\n'+entry['path'])
                self.gallery.addItem(item)
            self.filter()
            self.gallery.setGridSize(QSize(max(220,(self.gallery.viewport().width()-8)//max(1,self.gallery.viewport().width()//225)),204))
            if queue: QTimer.singleShot(0,batch)
            elif self.gallery.count() and not self.gallery.currentItem(): self.gallery.setCurrentRow(0)
        QTimer.singleShot(0,batch)

    def search_changed(self, *_):
        self.page = 0
        self.filter()

    def move_page(self, delta):
        self.page = max(0, min(max(0, self.page_total-1), self.page + delta))
        self.filter()
        self.gallery.scrollToTop()
        visible = [self.gallery.item(i) for i in range(self.gallery.count()) if not self.gallery.item(i).isHidden()]
        if visible:
            self.gallery.setCurrentItem(visible[0])

    def filter(self, *_):
        query = self.search.text().casefold()
        matches = []
        for i in range(self.gallery.count()):
            item = self.gallery.item(i); e = item.data(Qt.ItemDataRole.UserRole)
            show = query in (e['title']+' '+e['place']+' '+e['path']).casefold()
            show = show and (self.view!='Favourites' or e['path'] in self.c['favourites']) and (self.view!='My folders' or not e['bundled'])
            if show: matches.append(i)
        total = len(matches)
        self.page_total = max(1, (total+self.page_size-1)//self.page_size)
        self.page = min(self.page, self.page_total-1)
        start = self.page*self.page_size
        visible = set(matches[start:start+self.page_size])
        self.gallery.blockSignals(True)
        for i in range(self.gallery.count()): self.gallery.item(i).setHidden(i not in visible)
        self.count.setText(f'{total} wallpapers · '+('Jatayu Collection' if self.view=='Library' else self.view))
        self.page_label.setText(f'{start+1 if total else 0}–{min(start+self.page_size,total)} of {total} · Page {self.page+1}/{self.page_total}')
        self.previous_page.setEnabled(self.page>0)
        self.next_page.setEnabled(self.page+1<self.page_total)
        self.empty.setVisible(total==0)
        current = self.gallery.currentItem()
        if current is None or current.isHidden():
            self.gallery.setCurrentItem(self.gallery.item(matches[start]) if visible else None)
        self.gallery.blockSignals(False)
        if self.gallery.currentItem() is not current:
            self.select(self.gallery.currentItem())

    def select(self, item, *_):
        self.selected = item.data(Qt.ItemDataRole.UserRole) if item else None
        self.apply_button.setEnabled(bool(item)); self.favourite.setEnabled(bool(item))
        if not item:
            self.preview.clear();self.title.setText('Choose your view');self.place.clear();self.dimension.clear();self.quality.clear();return
        e=self.selected
        self.title.setText(e['title']); self.place.setText(e['place'])
        self.dimension.setText(e.get('dimensions','')+' · '+Path(e['path']).suffix[1:].upper())
        size = QImageReader(e['path']).size()
        self.quality.setText('Below Full HD: enlarging on a larger screen can soften detail.' if size.width()<1920 or size.height()<1080 else ('AI artwork · Full HD export' if e.get('generated') else 'Original full-resolution image is applied.'))
        reader=QImageReader(e['path']);reader.setAutoTransform(True)
        reader.setScaledSize(reader.size().scaled(QSize(680,420),Qt.AspectRatioMode.KeepAspectRatio))
        pix=QPixmap.fromImage(reader.read())
        self.preview.setPixmap(pix)
        self.favourite.setText('♥  Remove from favourites' if e['path'] in self.c['favourites'] else '♡  Add to favourites')

    def toggle_favourite(self):
        if not self.selected:return
        path=self.selected['path']; fav=self.c['favourites']
        fav.remove(path) if path in fav else fav.append(path)
        save(self.c)
        item=self.gallery.currentItem(); e=item.data(Qt.ItemDataRole.UserRole); e['fav']=path in fav;item.setData(Qt.ItemDataRole.UserRole,e)
        self.select(item);self.filter()

    def refresh_screens(self):
        def done(ok,result):
            match=re.search(r'JATAYU_SCREENS:(\[[^\n]*\])',result)
            self.screen.blockSignals(True);self.screen.clear();self.screen.addItem('All screens',-1)
            if ok and match:
                for n in json.loads(match.group(1)):self.screen.addItem(f'Screen {n+1} (Plasma ID {n})',n)
                if self.c['screen']>=0 and self.screen.findData(self.c['screen'])<0:
                    self.screen.addItem(f'Screen {self.c["screen"]+1} (disconnected)',self.c['screen'])
                self.screen.setCurrentIndex(max(0,self.screen.findData(self.c['screen'])))
                self.status.setText('Works offline · KDE Plasma ready' if self.screen.count()>1 else 'KDE Plasma has no active desktop screens yet. Retry after login.')
            else:
                self.status.setText('Gallery ready · KDE Plasma unavailable in this session')
            self.screen.blockSignals(False)
        self.backend.call(SCREENS_SCRIPT,done)

    def apply(self, path=None):
        if isinstance(path,bool):path=None
        if not path and not self.selected:return
        path=path or self.selected['path']
        try:script=wallpaper_script(path,self.c['screen'],self.c['layout'])
        except ValueError as e:QMessageBox.warning(self,'Cannot apply wallpaper',str(e));return
        self.apply_button.setEnabled(False);self.status.setText('Applying wallpaper…')
        def done(ok,result):
            match=re.search(r'JATAYU_OK:(\d+)',result)
            success=ok and bool(match) and int(match.group(1))>0
            self.apply_button.setEnabled(bool(self.selected))
            if success:
                self.c['last']=path;save(self.c);write_json(CONFIG/'rotation.json',{'last':path})
                self.status.setText('Wallpaper applied · '+Path(path).stem)
            else:
                message=result if not ok else 'No matching active desktop was found. Refresh screens and choose an available screen.'
                self.status.setText('Wallpaper was not applied')
                QMessageBox.warning(self,'Cannot apply wallpaper',message)
        self.backend.call(script,done)

    def change_now(self):
        state=read_json(CONFIG/'rotation.json',{})
        chosen=next_image(collection(self.c),self.c,state.get('last',self.c['last']))
        if chosen:self.apply(chosen)
        else:QMessageBox.information(self,'No wallpapers','Add images or mark favourites for your selected rotation pool.')

    def folder_dialog(self):
        d=QFileDialog(self,'Add wallpaper folder',str(Path.home()))
        d.setOption(QFileDialog.Option.DontUseNativeDialog,True)
        d.setOption(QFileDialog.Option.ShowDirsOnly,True)
        d.setFileMode(QFileDialog.FileMode.Directory)
        d.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        d.setPalette(light_palette());d.setStyleSheet(STYLE)
        d.resize(760,500)
        return d

    def add_folder(self):
        d=self.folder_dialog()
        if d.exec()!=QDialog.DialogCode.Accepted:return
        selected=d.selectedFiles()
        if not selected:return
        folder=str(Path(selected[0]).resolve())
        if Path(folder).is_dir() and folder not in self.c['folders']:
            self.c['folders'].append(folder);save(self.c);self.reload()

    def manage_folders(self):
        d=QDialog(self);d.setWindowTitle('Settings · Wallpaper folders');d.resize(560,380)
        v=QVBoxLayout(d);v.addWidget(label('External folders are referenced; removing one here leaves all its images intact.','muted'))
        listing=QListWidget();listing.addItems(self.c['folders']);v.addWidget(listing)
        def remove():
            item=listing.currentItem()
            if item:self.c['folders'].remove(item.text());save(self.c);listing.takeItem(listing.row(item));self.reload()
        def add():
            self.add_folder();listing.clear();listing.addItems(self.c['folders'])
        v.addWidget(button('Remove selected folder',remove));v.addWidget(button('Add folder',add))
        v.addWidget(label('Settings save automatically. Image formats: JPG, JPEG, JFIF, PNG, WebP, BMP. The preview uses original images.','muted'))
        v.addWidget(button('Close',d.accept));d.exec()

    def dialog(self,title,html):
        d=QDialog(self);d.setWindowTitle(title);d.resize(680,560)
        v=QVBoxLayout(d);browser=QTextBrowser();browser.setHtml(html);browser.setOpenExternalLinks(False);v.addWidget(browser)
        v.addWidget(button('Close',d.accept));d.exec()

    def about(self):
        self.dialog('About & Help',f'<h1>Jatayu Wallpaper Changer {VERSION}</h1><p>Created for JatayuOS by the JatayuOS Project.</p><p>Udaan Aapki. Shakti Bharat Ki.</p><p>Application source: GPL-3.0-or-later. Built with Python, Qt 6 and PyQt6. Debian and KDE Plasma are independent upstream projects; their names acknowledge compatibility and do not imply endorsement.</p><p>The bundled collection contains 24 AI-generated scenes created for this JatayuOS release using the built-in image generator. Full HD exports are resized from generated masters; no exclusive copyright is asserted in purely AI-generated imagery. No third-party source photos were used.</p>'+HELP)

def main():
    if '--start-service' in sys.argv:
        from service import start_background
        app=QCoreApplication(sys.argv);return start_background()
    if '--service' in sys.argv:
        from service import run_service
        app=QCoreApplication(sys.argv);app.setApplicationName(APP_ID)
        return run_service(app)
    app=QApplication(sys.argv);app.setApplicationName(APP_ID);app.setStyle('Fusion');app.setPalette(light_palette());app.setStyleSheet(STYLE)
    CONFIG.mkdir(parents=True,exist_ok=True)
    lock=QLockFile(str(CONFIG/'gui.lock'))
    if '--screenshot' not in sys.argv and not lock.tryLock(0):
        QMessageBox.information(None,'Jatayu Wallpaper Changer','The app is already running. Switch to its existing window.');return 0
    window=Window();window.show()
    if '--screenshot' in sys.argv:
        target=sys.argv[sys.argv.index('--screenshot')+1]
        def shot():
            window.grab().save(target);app.quit()
        QTimer.singleShot(1800,shot)
    result=app.exec();lock.unlock();return result

if __name__=='__main__':
    sys.exit(main())
