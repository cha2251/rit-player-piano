from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QToolButton


class DragButton(QToolButton):
    def __init__(self, mimeText):
        super().__init__()
        self.mimeText = mimeText

    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeData.setText(self.mimeText)
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            drag.setMimeData(mimeData)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.CopyAction)
