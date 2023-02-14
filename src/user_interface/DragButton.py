from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QToolButton


class DragButton(QToolButton):
    def __init__(self, qMimeData):
        super().__init__()
        self.mimeData = qMimeData

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:

            drag = QDrag(self)
            mime = self.mimeData
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.CopyAction)
