import os

from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap, QIcon
from PyQt5.QtWidgets import QToolButton


class pianoKey(QToolButton):

    def __init__(self, key, piano_dict):
        super().__init__()
        self.setAcceptDrops(True)
        self.key = key
        self.piano_dict = piano_dict

    def dragEnterEvent(self, e):
        try:
            e.accept()
        except:
            print("exception in dragEnterEvent")

    def dropEvent(self, e):
        try:
            file = e.mimeData().text()
            self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", (file + ".svg")),))
            self.piano_dict[self.key] += file
        except:
            print("exception occurred in drop event")
