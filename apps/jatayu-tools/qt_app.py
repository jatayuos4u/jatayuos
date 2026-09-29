"""Jatayu Tools Creative Studio — offline Qt desktop interface."""
from __future__ import annotations

from dataclasses import dataclass, field
from io import BytesIO
import json
from pathlib import Path
import sys

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QPixmap, QDesktopServices
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog, QFileDialog, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QProgressBar,
    QPushButton, QScrollArea, QSlider, QSpinBox, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QHeaderView, QAbstractItemView
)

from PIL import Image, ImageOps
from pypdf import PdfReader
import core

APP = Path('/usr/share/jatayu-tools')
DOC = Path('/usr/share/doc/jatayu-tools')
STATE = Path.home() / '.local/state/jatayu-tools/history.json'
CONFIG = Path.home() / '.config/jatayu-tools/presets.json'
INK = '#192640'
GREEN = '#359165'
ORANGE = '#e96e29'

QSS = """
QMainWindow, QWidget#root { background: #f9f8f5; color: #192640; }
QFileDialog, QFileDialog QWidget, QFileDialog QTreeView, QFileDialog QListView { background: #f9f8f5; color: #192640; }
QFileDialog QLineEdit, QFileDialog QComboBox { background: white; color: #192640; }
QFileDialog QPushButton { background: white; color: #192640; border: 1px solid #aab7c3; padding: 5px; }
QWidget { font-family: 'Noto Sans', 'DejaVu Sans', sans-serif; font-size: 10pt; color: #192640; }
QFrame#header, QFrame#sidebar { background: #192640; }
QFrame#sidebar { border-right: 1px solid #33435e; }
QLabel#brand, QLabel#headerTitle { color: #fff; font-size: 17pt; font-weight: 750; }
QLabel#tagline { font-size: 12pt; color: #647084; }
QLabel#hero { font-size: 25pt; font-weight: 750; }
QLabel#section { font-size: 13pt; font-weight: 700; }
QLabel#muted { color: #657187; }
QLabel#small { color: #8894a2; font-size: 9pt; }
QLabel#sideNote { color: #aab8c9; font-size: 9pt; }
QPushButton#nav { color: #e8eff7; background: transparent; border: none; text-align: left; padding: 12px 17px; border-radius: 10px; font-weight: 550; }
QPushButton#nav:hover, QPushButton#nav:checked { background: #3b465a; color: #fff; }
QPushButton#primary { background: #e96e29; color: white; border: none; border-radius: 9px; padding: 11px 17px; font-weight: 700; }
QPushButton#primary:hover { background: #d85d18; }
QPushButton#primary:disabled { background: #bdc4ca; }
QPushButton#quiet { background: white; color: #192640; border: 1px solid #d5dce3; border-radius: 8px; padding: 8px 11px; }
QPushButton#quiet:hover { background: #eff4f6; }
QFrame#card { background: #ffffff; border: 1px solid #e5e7e9; border-radius: 14px; }
QFrame#imageCard { background: #f1f7f0; border: 1px solid #dbe9da; border-radius: 14px; }
QFrame#pdfCard { background: #fff5ed; border: 1px solid #f6e5d6; border-radius: 14px; }
QFrame#drop { background: white; border: 2px dashed #c9d3dd; border-radius: 13px; }
QFrame#drop[dragging="true"] { background: #f1faf5; border-color: #359165; }
QFrame#inspector { background: white; border-left: 1px solid #e2e6ea; }
QFrame#divider { background: #e8edf0; max-height: 1px; min-height: 1px; }
QTableWidget { background: white; alternate-background-color: #fafbfa; border: none; gridline-color: #e9ecef; selection-background-color: #e4f2e8; }
QHeaderView::section { background: #f3f5f6; color: #627083; border: none; padding: 7px; font-weight: 600; }
QLineEdit, QComboBox, QSpinBox { background: white; border: 1px solid #d7dfe5; border-radius: 7px; padding: 6px; min-height: 20px; }
QComboBox QAbstractItemView { background: white; }
QProgressBar { border: 0; background: #e5ebef; border-radius: 5px; max-height: 9px; }
QProgressBar::chunk { background: #359165; border-radius: 5px; }
QSlider::groove:horizontal { height: 5px; background: #dbe1e4; border-radius: 2px; }
QSlider::handle:horizontal { background: #e96e29; width: 15px; margin: -5px 0; border-radius: 7px; }
QSlider::sub-page:horizontal { background: #e96e29; }
"""


@dataclass
class Job:
    path: str
    operation: str
    status: str = 'Queued'
    outputs: list[str] = field(default_factory=list)
    error: str = ''
    progress: int = 0
    options: dict = field(default_factory=dict)


def fmt_bytes(amount):
    for suffix in ('B', 'KB', 'MB', 'GB'):
        if amount < 1024 or suffix == 'GB':
            return f'{amount:.1f} {suffix}' if suffix != 'B' else f'{amount} B'
        amount /= 1024


def read_history():
    try:
        value = json.loads(STATE.read_text(encoding='utf-8'))
        return value if isinstance(value, list) else []
    except (OSError, ValueError):
        return []


def save_history(value):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(value[-200:], ensure_ascii=False, indent=2), encoding='utf-8')


def image_thumbnail(path, size=QSize(112, 82)):
    try:
        with Image.open(path) as source:
            source.seek(0)
            im = ImageOps.exif_transpose(source)
            im.thumbnail((size.width(), size.height()))
            stream = BytesIO()
            im.convert('RGB').save(stream, 'PNG')
        pixmap = QPixmap()
        pixmap.loadFromData(stream.getvalue(), 'PNG')
        return pixmap
    except Exception:
        return QPixmap()


class DropZone(QFrame):
    pathsDropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setObjectName('drop')
        self.setProperty('dragging', False)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and any(u.isLocalFile() for u in event.mimeData().urls()):
            event.acceptProposedAction()
            self.setProperty('dragging', True)
            self.style().unpolish(self)
            self.style().polish(self)

    def dragLeaveEvent(self, event):
        self.setProperty('dragging', False)
        self.style().unpolish(self)
        self.style().polish(self)
        event.accept()

    def dropEvent(self, event):
        self.setProperty('dragging', False)
        self.style().unpolish(self)
        self.style().polish(self)
        paths = [u.toLocalFile() for u in event.mimeData().urls() if u.isLocalFile()]
        self.pathsDropped.emit(paths)
        event.acceptProposedAction()


class Worker(QThread):
    changed = pyqtSignal(int, str, int)
    completed = pyqtSignal(int, object, str)

    def __init__(self, jobs, options, folder):
        super().__init__()
        self.jobs = jobs
        self.options = options
        self.folder = folder
        self.cancelled = False

    def run(self):
        for index, job in self.jobs:
            if self.cancelled:
                self.completed.emit(index, [], 'Cancelled before processing')
                continue
            self.changed.emit(index, 'Processing', 0)
            try:
                if job.operation == 'Merge PDFs':
                    outputs = [core.merge(job.path, self.folder, layout='PDF')]
                elif job.operation == 'Images to PDF':
                    # A single image becomes a PDF; a merged batch uses Merge images to PDF.
                    outputs = core.process_one(job.path, 'Convert', self.folder, fmt='PDF')
                else:
                    outputs = core.process_one(job.path, job.operation, self.folder, **self.options[index])
                self.completed.emit(index, outputs, '')
            except Exception as exc:
                self.completed.emit(index, [], str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.jobs = []
        self.history = read_history()
        self.worker = None
        self.active_index = None
        self.output_folder = str(Path.home() / 'Documents' / 'Jatayu Tools')
        self.setWindowTitle('Jatayu Tools · Creative Studio')
        self.setWindowIcon(QIcon(str(APP / 'jatayu-tools.png')))
        self.resize(1280, 760)
        self.setMinimumSize(960, 600)
        self._build()

    def label(self, text, kind='', wrap=False):
        label = QLabel(text)
        if kind:
            label.setObjectName(kind)
        label.setWordWrap(wrap)
        return label

    def button(self, text, callback, kind='quiet'):
        b = QPushButton(text)
        b.setObjectName(kind)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.clicked.connect(callback)
        return b

    def _build(self):
        root = QWidget()
        root.setObjectName('root')
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        header = QFrame()
        header.setObjectName('header')
        header.setFixedHeight(72)
        h = QHBoxLayout(header)
        h.setContentsMargins(22, 8, 24, 8)
        mark = QLabel()
        mark.setPixmap(QPixmap(str(APP / 'jatayu-tools.png')).scaled(46,46,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
        h.addWidget(mark)
        h.addWidget(self.label('Jatayu Tools', 'headerTitle'))
        badge = QLabel('  ●  Local & private  ')
        badge.setStyleSheet('color:#bce9cc;background:#2b4b49;border-radius:9px;padding:8px;')
        h.addWidget(badge)
        h.addStretch(1)
        help_button = self.button('Help', self.show_help)
        help_button.setStyleSheet('color:#fff;background:transparent;border:none;padding:8px;')
        h.addWidget(help_button)
        settings_button = self.button('⚙', self.show_settings)
        settings_button.setStyleSheet('color:#fff;background:transparent;border:none;font-size:17pt;')
        h.addWidget(settings_button)
        outer.addWidget(header)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        outer.addLayout(body, 1)
        sidebar = QFrame()
        sidebar.setObjectName('sidebar')
        sidebar.setFixedWidth(200)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(14, 18, 14, 18)
        side.setSpacing(5)
        nav = [
            ('⌂   Workspace', self.show_workspace),
            ('▧   Image Studio', lambda: self.add_files('image')),
            ('▤   PDF Studio', lambda: self.add_files('pdf')),
            ('☷   Batch Queue', self.focus_queue),
            ('⚙   Presets', self.show_presets),
            ('◷   History', self.show_history),
            ('ⓘ   About', self.show_about),
        ]
        for i, (name, action) in enumerate(nav):
            b = self.button(name, action, 'nav')
            b.setCheckable(True)
            b.setChecked(i == 0)
            b.clicked.connect(lambda _, current=b: self._nav_select(current))
            side.addWidget(b)
        side.addStretch(1)
        side.addWidget(self.label('Every tool. Every file.\nOn your device.', 'sideNote'))
        body.addWidget(sidebar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        canvas = QWidget()
        scroll.setWidget(canvas)
        self.center = QVBoxLayout(canvas)
        self.center.setContentsMargins(27, 25, 23, 24)
        self.center.setSpacing(15)
        self.center.addWidget(self.label('What would you like to do?', 'hero'))
        self.center.addWidget(self.label('Your files. Your device. Your way.', 'tagline'))
        modules = QHBoxLayout()
        modules.setSpacing(13)
        modules.addWidget(self._module('imageCard','▧','Image Studio','Convert · Compress · Resize · Merge','Work with your images, offline and on your terms.',lambda: self.add_files('image')),1)
        modules.addWidget(self._module('pdfCard','▤','PDF Studio','Merge · Compress · PDF to JPG · Extract pages','Transform and organize PDFs locally.',lambda: self.add_files('pdf')),1)
        self.center.addLayout(modules)
        drop = DropZone()
        drop.setMinimumHeight(170)
        drop.pathsDropped.connect(self.import_paths)
        d = QVBoxLayout(drop)
        d.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d.setSpacing(7)
        icon = self.label('⇧', 'section')
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet('font-size:28pt;color:#70808c;')
        d.addWidget(icon)
        title = self.label('Add files or drag and drop here', 'section')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d.addWidget(title)
        detail = self.label('PNG · JPG/JPEG · WebP · BMP · TIFF · GIF · PDF    •    Processed on this device','muted')
        detail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d.addWidget(detail)
        add = self.button('Add files', lambda: self.add_files('all'), 'primary')
        add.setFixedWidth(160)
        d.addWidget(add, alignment=Qt.AlignmentFlag.AlignCenter)
        self.center.addWidget(drop)
        queue_bar = QHBoxLayout()
        self.queue_heading = self.label('Work Queue (0)', 'section')
        queue_bar.addWidget(self.queue_heading)
        queue_bar.addStretch(1)
        queue_bar.addWidget(self.button('Merge selected PDFs', self.merge_pdfs))
        queue_bar.addWidget(self.button('Merge images to PDF', self.merge_images))
        queue_bar.addWidget(self.button('Clear completed', self.clear_completed))
        self.center.addLayout(queue_bar)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['File', 'Operation', 'Status', 'Progress', 'Output'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for column, width in ((1, 170), (2, 115), (3, 130), (4, 210)):
            self.table.setColumnWidth(column, width)
        self.table.itemSelectionChanged.connect(self._inspect)
        self.table.setMinimumHeight(250)
        self.center.addWidget(self.table, 1)
        body.addWidget(scroll, 1)
        self._inspector(body)

    def _module(self, object_name, symbol, title, tools, detail, action):
        card = QFrame()
        card.setObjectName(object_name)
        card.setMinimumHeight(170)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 17, 18, 17)
        large = QLabel(symbol)
        large.setAlignment(Qt.AlignmentFlag.AlignCenter)
        large.setFixedSize(96, 95)
        large.setStyleSheet('font-size:54pt;color:#359165;' if object_name=='imageCard' else 'font-size:54pt;color:#e96e29;')
        layout.addWidget(large)
        text = QVBoxLayout()
        text.addWidget(self.label(title, 'section'))
        text.addWidget(self.label(detail, 'muted', True))
        pill = self.label(tools, 'small', True)
        pill.setStyleSheet('background:#e7efe8;border-radius:7px;padding:7px;' if object_name=='imageCard' else 'background:#fde9d8;border-radius:7px;padding:7px;')
        text.addWidget(pill)
        layout.addLayout(text, 1)
        layout.addWidget(self.button('›', action))
        return card

    def _inspector(self, body):
        inspector = QFrame()
        inspector.setObjectName('inspector')
        inspector.setMinimumWidth(270)
        panel = QVBoxLayout(inspector)
        panel.setContentsMargins(19, 21, 19, 18)
        panel.setSpacing(10)
        self.preview = QLabel('▧')
        self.preview.setFixedHeight(82)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.preview.setStyleSheet('font-size:32pt;color:#359165;')
        panel.addWidget(self.preview)
        self.inspect_title = self.label('Select a file in the queue', 'section', True)
        panel.addWidget(self.inspect_title)
        self.inspect_detail = self.label('Settings for that file appear here.', 'muted', True)
        panel.addWidget(self.inspect_detail)
        panel.addWidget(self._line())
        self.operation = QComboBox()
        self.operation.currentTextChanged.connect(self._operation_changed)
        panel.addWidget(self.label('Operation', 'section'))
        panel.addWidget(self.operation)
        self.format_row = self._form_row(panel, 'Output format', QComboBox())
        self.format_box = self.format_row[1]
        self.format_box.addItems(['JPG','PNG','WEBP','TIFF','BMP','PDF'])
        self.quality_row = self._form_row(panel, 'Image quality', QSlider(Qt.Orientation.Horizontal))
        self.quality_slider = self.quality_row[1]
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(85)
        self.quality_value = self.label('85%', 'small')
        self.quality_slider.valueChanged.connect(lambda n: self.quality_value.setText(f'{n}%'))
        panel.addWidget(self.quality_value)
        self.width_row = self._form_row(panel, 'Width (px)', QSpinBox())
        self.width = self.width_row[1]
        self.width.setRange(0, 30000)
        self.width.setValue(1920)
        self.height_row = self._form_row(panel, 'Height (px)', QSpinBox())
        self.height = self.height_row[1]
        self.height.setRange(0, 30000)
        self.height.setValue(1080)
        self.keep_ratio = QCheckBox('Keep aspect ratio')
        self.keep_ratio.setChecked(True)
        panel.addWidget(self.keep_ratio)
        self.pages_row = self._form_row(panel, 'Pages (all or 1-3,5)', QLineEdit('all'))
        self.pages = self.pages_row[1]
        self.dpi_row = self._form_row(panel, 'Render resolution (DPI)', QSpinBox())
        self.dpi = self.dpi_row[1]
        self.dpi.setRange(72, 600)
        self.dpi.setValue(150)
        self.preset_row = self._form_row(panel, 'PDF compression', QComboBox())
        self.preset = self.preset_row[1]
        self.preset.addItems(list(core.PDF_PRESETS))
        self.preset.setCurrentText('Ebook')
        self.rotation_row = self._form_row(panel, 'Rotate clockwise', QComboBox())
        self.rotation = self.rotation_row[1]
        self.rotation.addItems(['90','180','270'])
        panel.addWidget(self._line())
        panel.addWidget(self.label('Output folder', 'section'))
        self.folder_label = self.label(self.output_folder, 'small', True)
        panel.addWidget(self.folder_label)
        panel.addWidget(self.button('Browse…', self.choose_folder))
        panel.addStretch(1)
        self.run_button = self.button('▶  Run selected jobs', self.run_selected, 'primary')
        panel.addWidget(self.run_button)
        self.cancel_button = self.button('Cancel remaining', self.cancel_remaining)
        self.cancel_button.setVisible(False)
        panel.addWidget(self.cancel_button)
        panel.addWidget(self.label('Processed locally. No files are uploaded.', 'small', True))
        inspector_scroll = QScrollArea()
        inspector_scroll.setWidgetResizable(True)
        inspector_scroll.setFrameShape(QFrame.Shape.NoFrame)
        inspector_scroll.setFixedWidth(294)
        inspector_scroll.setWidget(inspector)
        body.addWidget(inspector_scroll)
        self._toggle_options('')

    def _form_row(self, layout, caption, widget):
        label = self.label(caption, 'muted')
        layout.addWidget(label)
        layout.addWidget(widget)
        return label, widget

    def _line(self):
        line = QFrame()
        line.setObjectName('divider')
        return line

    def _nav_select(self, current):
        for button in self.findChildren(QPushButton, 'nav'):
            button.setChecked(button is current)

    def show_workspace(self):
        self.table.setFocus()

    def focus_queue(self):
        self.table.setFocus()
        if self.table.rowCount():
            self.table.selectRow(0)

    def add_files(self, mode='all'):
        filters = {'image':'Images (*.png *.jpg *.jpeg *.webp *.bmp *.tif *.tiff *.gif)',
                   'pdf':'PDFs (*.pdf)',
                   'all':'Images and PDFs (*.png *.jpg *.jpeg *.webp *.bmp *.tif *.tiff *.gif *.pdf)'}
        paths, _ = QFileDialog.getOpenFileNames(self, 'Add local files', str(Path.home()), filters[mode], options=QFileDialog.Option.DontUseNativeDialog)
        self.import_paths(paths)

    def import_paths(self, paths):
        self._save_active()
        rejected = []
        existing = {job.path for job in self.jobs}
        for path in paths:
            try:
                kind = core.kind(path)
                if not Path(path).is_file():
                    raise ValueError('Not a file')
            except Exception:
                rejected.append(Path(path).name)
                continue
            if path in existing:
                continue
            existing.add(path)
            self.jobs.append(Job(path, 'Compress' if kind == 'image' else 'Compress'))
        self.refresh_table()
        if rejected:
            QMessageBox.warning(self, 'Unsupported files', 'Skipped: ' + ', '.join(rejected[:8]))

    def _operations_for(self, job):
        return (['Convert','Compress','Resize','Images to PDF'] if core.kind(job.path) == 'image'
                else ['Compress','PDF to images','Extract pages','Split PDF','Rotate PDF'])

    def _inspect(self):
        self._save_active()
        row = self.table.currentRow()
        if row < 0 or row >= len(self.jobs):
            self.active_index = None
            return
        job = self.jobs[row]
        self.active_index = row
        path = Path(job.path)
        self.inspect_title.setText(path.name)
        info = f'{path.suffix.upper().lstrip(".")} · {fmt_bytes(path.stat().st_size)}'
        if core.kind(path) == 'image':
            try:
                with Image.open(path) as image:
                    info += f' · {image.width} × {image.height} px'
            except Exception:
                pass
            pixmap = image_thumbnail(path)
            self.preview.setPixmap(pixmap if not pixmap.isNull() else QPixmap())
        else:
            try:
                info += f' · {len(PdfReader(str(path)).pages)} pages'
            except Exception:
                info += ' · unreadable PDF'
            self.preview.setText('▤')
        self.inspect_detail.setText(info)
        self.operation.blockSignals(True)
        self.operation.clear()
        self.operation.addItems(self._operations_for(job))
        self.operation.setCurrentText(job.operation)
        self.operation.blockSignals(False)
        if job.options:
            options = job.options
            self.format_box.setCurrentText(options.get('fmt','JPG'))
            self.quality_slider.setValue(options.get('quality',85))
            self.width.setValue(options.get('width',1920))
            self.height.setValue(options.get('height',1080))
            self.keep_ratio.setChecked(options.get('keep_ratio',True))
            self.pages.setText(options.get('pages','all'))
            self.dpi.setValue(options.get('dpi',150))
            self.preset.setCurrentText(options.get('preset','Ebook'))
            self.rotation.setCurrentText(str(options.get('rotation',90)))
        self._toggle_options(job.operation)

    def _save_active(self):
        if self.active_index is not None and 0 <= self.active_index < len(self.jobs):
            self.jobs[self.active_index].options = self._settings_snapshot()

    def _operation_changed(self, value):
        row = self.table.currentRow()
        if 0 <= row < len(self.jobs) and value:
            self.jobs[row].operation = value
            self.table.item(row, 1).setText(value)
        self._toggle_options(value)

    def _toggle_options(self, operation):
        current_row = self.table.currentRow()
        is_pdf = (0 <= current_row < len(self.jobs)
                  and core.kind(self.jobs[current_row].path) == 'pdf')
        formats = ['JPG','PNG','WEBP','TIFF','BMP']
        if operation in ('Convert','Resize'):
            formats.append('PDF')
        previous = self.format_box.currentText()
        if [self.format_box.itemText(i) for i in range(self.format_box.count())] != formats:
            self.format_box.blockSignals(True)
            self.format_box.clear()
            self.format_box.addItems(formats)
            self.format_box.setCurrentText(previous if previous in formats else 'JPG')
            self.format_box.blockSignals(False)
        controls = [(self.format_row, operation in ('Convert','Resize','PDF to images')),
                    (self.quality_row, operation in ('Convert','Resize','PDF to images')
                     or (operation == 'Compress' and not is_pdf)),
                    (self.width_row, operation == 'Resize'), (self.height_row, operation == 'Resize'),
                    (self.pages_row, operation in ('PDF to images','Extract pages','Split PDF','Rotate PDF')),
                    (self.dpi_row, operation == 'PDF to images'),
                    (self.preset_row, operation == 'Compress' and is_pdf),
                    (self.rotation_row, operation == 'Rotate PDF')]
        for (label, widget), visible in controls:
            label.setVisible(visible)
            widget.setVisible(visible)
        self.keep_ratio.setVisible(operation == 'Resize')
        self.quality_value.setVisible(operation in ('Convert','Resize','PDF to images')
                                      or (operation == 'Compress' and not is_pdf))

    def refresh_table(self):
        self._save_active()
        self.active_index = None
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.jobs))
        for row, job in enumerate(self.jobs):
            path = Path(job.path)
            first = QTableWidgetItem(path.name + '\n' + fmt_bytes(path.stat().st_size))
            first.setFlags(first.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            first.setCheckState(Qt.CheckState.Checked if job.status == 'Queued' else Qt.CheckState.Unchecked)
            self.table.setItem(row, 0, first)
            self.table.setItem(row, 1, QTableWidgetItem(job.operation))
            self.table.setItem(row, 2, QTableWidgetItem(job.status))
            bar = QProgressBar()
            bar.setValue(job.progress)
            bar.setTextVisible(False)
            self.table.setCellWidget(row, 3, bar)
            self.table.setItem(row, 4, QTableWidgetItem(', '.join(Path(p).name for p in job.outputs) if job.outputs else '—'))
            self.table.setRowHeight(row, 54)
        self.table.blockSignals(False)
        self.queue_heading.setText(f'Work Queue ({len(self.jobs)})')
        if self.jobs:
            self.table.selectRow(len(self.jobs)-1)

    def _checked(self):
        return [(i, job) for i, job in enumerate(self.jobs)
                if self.table.item(i, 0).checkState() == Qt.CheckState.Checked]

    def _settings_snapshot(self):
        return dict(fmt=self.format_box.currentText(), quality=self.quality_slider.value(),
                    width=self.width.value(), height=self.height.value(),
                    keep_ratio=self.keep_ratio.isChecked(), pages=self.pages.text().strip(),
                    dpi=self.dpi.value(), preset=self.preset.currentText(),
                    rotation=int(self.rotation.currentText()))

    def run_selected(self):
        if self.worker is not None and self.worker.isRunning():
            return
        selected = self._checked()
        if not selected:
            QMessageBox.information(self, 'Select jobs', 'Check one or more queued files first.')
            return
        self._save_active()
        snapshot = self._settings_snapshot()
        settings = {i: dict(job.options or snapshot) for i, job in selected}
        # PDF to images must use an image output even if the previous job used PDF.
        for i, job in selected:
            if job.operation == 'PDF to images' and settings[i]['fmt'] == 'PDF':
                settings[i]['fmt'] = 'JPG'
        self.worker = Worker(selected, settings, self.output_folder)
        self.worker.changed.connect(self._worker_changed)
        self.worker.completed.connect(self._worker_completed)
        self.worker.finished.connect(self._worker_finished)
        self.run_button.setEnabled(False)
        self.cancel_button.setVisible(True)
        self.worker.start()

    def _worker_changed(self, index, status, percent):
        job = self.jobs[index]
        job.status = status
        job.progress = percent
        self.table.item(index, 2).setText(status)
        self.table.cellWidget(index, 3).setRange(0, 0)

    def _worker_completed(self, index, outputs, error):
        job = self.jobs[index]
        job.outputs = list(outputs)
        job.error = error
        job.status = 'Cancelled' if error.startswith('Cancelled') else 'Failed' if error else 'Completed'
        job.progress = 0 if error else 100
        self.table.item(index, 2).setText(job.status)
        self.table.item(index, 4).setText(', '.join(Path(p).name for p in outputs) if outputs else error[:90])
        self.table.cellWidget(index, 3).setRange(0, 100)
        self.table.cellWidget(index, 3).setValue(job.progress)
        self.table.item(index, 0).setCheckState(Qt.CheckState.Unchecked)
        self.history.append(dict(file=Path(job.path).name, operation=job.operation,
                                 status=job.status, outputs=job.outputs, error=job.error))
        try:
            save_history(self.history)
        except OSError:
            pass

    def _worker_finished(self):
        self.run_button.setEnabled(True)
        self.cancel_button.setVisible(False)
        failures = [job for job in self.jobs if job.status == 'Failed']
        if failures:
            QMessageBox.warning(self, 'Jobs finished', f'{len(failures)} job(s) failed. Select a row to review its error in the Output column.')

    def cancel_remaining(self):
        if self.worker:
            self.worker.cancelled = True

    def merge_pdfs(self):
        self._merge('pdf')

    def merge_images(self):
        self._merge('image')

    def _merge(self, kind):
        selected = [job.path for _, job in self._checked() if core.kind(job.path) == kind]
        if len(selected) < 2:
            QMessageBox.information(self, 'Merge files', f'Check at least two {kind} files in the desired table order.')
            return
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, 'Processing', 'Wait for the active queue before merging.')
            return
        try:
            output = core.merge(selected, self.output_folder, layout='PDF', name='merged-' + kind)
            self.history.append(dict(file=f'{len(selected)} {kind} files', operation='Merge', status='Completed', outputs=[output], error=''))
            save_history(self.history)
            QMessageBox.information(self, 'Merge complete', f'Saved locally:\n{output}')
        except Exception as exc:
            QMessageBox.warning(self, 'Merge failed', str(exc))

    def clear_completed(self):
        if self.worker and self.worker.isRunning():
            return
        self._save_active()
        self.active_index = None
        self.jobs = [job for job in self.jobs if job.status not in ('Completed','Cancelled')]
        self.refresh_table()

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Choose output folder', self.output_folder, options=QFileDialog.Option.DontUseNativeDialog)
        if folder:
            self.output_folder = folder
            self.folder_label.setText(folder)

    def _dialog(self, title, text):
        dlg = QDialog(self)
        dlg.setWindowTitle(title)
        dlg.resize(620, 490)
        layout = QVBoxLayout(dlg)
        area = QScrollArea()
        area.setWidgetResizable(True)
        label = self.label(text, wrap=True)
        label.setTextFormat(Qt.TextFormat.PlainText)
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        label.setContentsMargins(15, 15, 15, 15)
        area.setWidget(label)
        layout.addWidget(area)
        layout.addWidget(self.button('Close', dlg.accept), alignment=Qt.AlignmentFlag.AlignRight)
        dlg.exec()

    def show_help(self):
        self._dialog('Help · Jatayu Tools', (DOC / 'USER_GUIDE.txt').read_text(encoding='utf-8'))

    def show_about(self):
        self._dialog('About Jatayu Tools', (DOC / 'ABOUT.txt').read_text(encoding='utf-8'))

    def show_history(self):
        lines = [f"{entry.get('status')}  ·  {entry.get('operation')}  ·  {entry.get('file')}\n  {', '.join(entry.get('outputs', [])) or entry.get('error', '')}"
                 for entry in self.history[-40:][::-1]]
        self._dialog('History (on this device)', '\n\n'.join(lines) or 'No jobs have been processed yet.')

    def show_settings(self):
        self.choose_folder()

    def show_presets(self):
        current = self._settings_snapshot()
        reply = QMessageBox.question(self, 'Presets', 'Save your current format, quality, page range and PDF options as a local preset?')
        if reply == QMessageBox.StandardButton.Yes:
            try:
                CONFIG.parent.mkdir(parents=True, exist_ok=True)
                CONFIG.write_text(json.dumps(current, indent=2), encoding='utf-8')
                QMessageBox.information(self, 'Preset saved', 'Saved to your local configuration folder.')
            except OSError as exc:
                QMessageBox.warning(self, 'Could not save preset', str(exc))
        elif CONFIG.exists():
            if QMessageBox.question(self, 'Presets', 'Load your saved local preset?') == QMessageBox.StandardButton.Yes:
                try:
                    settings = json.loads(CONFIG.read_text(encoding='utf-8'))
                    self.format_box.setCurrentText(settings.get('fmt','JPG'))
                    self.quality_slider.setValue(int(settings.get('quality',85)))
                    self.width.setValue(int(settings.get('width',1920)))
                    self.height.setValue(int(settings.get('height',1080)))
                    self.pages.setText(str(settings.get('pages','all')))
                    self.preset.setCurrentText(settings.get('preset','Ebook'))
                except (OSError,ValueError,TypeError) as exc:
                    QMessageBox.warning(self, 'Could not load preset', str(exc))

    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, 'Processing files',
                                    'Wait for the current file to finish, or choose Cancel remaining.')
            event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Jatayu Tools')
    app.setDesktopFileName('org.jatayuos.JatayuTools')
    app.setStyleSheet(QSS)
    app.setWindowIcon(QIcon(str(APP / 'jatayu-tools.png')))
    window = MainWindow()
    window.show()
    if '--smoke' in sys.argv:
        app.processEvents()
        window.grab().save('/tmp/jatayu-tools-smoke.png')
        window.close()
        return 0
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
