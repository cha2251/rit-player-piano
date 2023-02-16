import os

from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap, QIcon
from PyQt5.QtWidgets import QToolButton


class pianoKey(QToolButton):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        try:
            e.accept()
        except:
            print("exception in dragEnterEvent")

    def dropEvent(self, e):
        try:
            print("pianoKey DROP EVENT")
            print(e.source())
            print(e.mimeData().text())
            file = e.mimeData().text()
            self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", file),))
            #####e.accept()
            # if e.mimeData().hasurls():
            #     e.accept()
            #     for url in e.mimeData().urls():
            #         self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", url)))
            print("pianoKey DROP END")
        except:
            print("exception occured in drop event")
