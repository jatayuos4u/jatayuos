"""KDE session integration. SPDX-License-Identifier: GPL-3.0-or-later."""
from PyQt6.QtCore import QObject
from PyQt6.QtDBus import QDBusConnection, QDBusMessage, QDBusPendingCallWatcher, QDBusPendingReply, QDBus

class Plasma(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pending = set()

    def message(self, script):
        msg = QDBusMessage.createMethodCall('org.kde.plasmashell', '/PlasmaShell',
                                          'org.kde.PlasmaShell', 'evaluateScript')
        msg.setArguments([script])
        return msg

    @staticmethod
    def unpack(reply):
        if reply.type() == QDBusMessage.MessageType.ErrorMessage:
            return False, 'KDE Plasma did not accept the request. Log into a Plasma session and retry.\n'+reply.errorMessage()
        return True, '\n'.join(str(x) for x in reply.arguments())

    def call(self, script, callback):
        watcher = QDBusPendingCallWatcher(QDBusConnection.sessionBus().asyncCall(self.message(script), 8000), self)
        self.pending.add(watcher)
        def done(w):
            self.pending.discard(w)
            callback(*self.unpack(QDBusPendingReply(w).reply()))
            w.deleteLater()
        watcher.finished.connect(done)

    def sync(self, script):
        return self.unpack(QDBusConnection.sessionBus().call(self.message(script),
                        QDBus.CallMode.Block, 8000))
