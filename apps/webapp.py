#!/usr/bin/python3
"""Standalone windows for the owner's unchanged local HTML tools."""
import sys
from pathlib import Path
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

APPS = {
    'kavach': 'Kavach',
    'sarkar-setu': 'Sarkar Setu',
    'utsav': 'Utsav',
}
ROOT = Path('/usr/share/jatayu').resolve()

class AppPage(QWebEnginePage):
    def __init__(self, owner, external_only=False):
        super().__init__(owner)
        self.external_only = external_only
        self.popup_pages = []

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        if url.scheme() in ('http', 'https', 'mailto', 'tel'):
            QDesktopServices.openUrl(url)
            return False
        if self.external_only:
            return False
        if url.isLocalFile():
            path = Path(url.toLocalFile()).resolve()
            return path == ROOT / (sys.argv[1] + '.html')
        return url.scheme() in ('about', 'data', 'blob')

    def createWindow(self, kind):
        popup = AppPage(self, external_only=True)
        self.popup_pages.append(popup)
        return popup

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in APPS:
        print('Usage: jatayu-webapp kavach|sarkar-setu|utsav', file=sys.stderr)
        return 2
    app = QApplication(sys.argv)
    app.setApplicationName(APPS[sys.argv[1]])
    window = QMainWindow()
    window.setWindowTitle(APPS[sys.argv[1]] + ' · JatayuOS')
    window.setWindowIcon(QIcon(str(ROOT / 'logo.png')))
    view = QWebEngineView(window)
    page = AppPage(view)
    view.setPage(page)
    view.settings().setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
    window.setCentralWidget(view)
    window.resize(1180, 780)
    window.setMinimumSize(760, 520)
    view.load(QUrl.fromLocalFile(str(ROOT / (sys.argv[1] + '.html'))))
    window.show()
    return app.exec()

if __name__ == '__main__':
    raise SystemExit(main())
