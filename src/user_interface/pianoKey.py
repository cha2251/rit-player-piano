import os

from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap, QIcon
from PyQt5.QtWidgets import QToolButton


class pianoKey(QToolButton):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        print("pianoKey DROP EVENT")
        print(e.source())
        print(e.mimeData().text())
        print("pianoKey DROP END")
        file = e.mimeData().text()
        self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", file),))
        e.accept()
        # if e.mimeData().hasurls():
        #     e.accept()
        #     for url in e.mimeData().urls():
        #         self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", url)))