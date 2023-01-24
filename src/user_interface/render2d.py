from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QSize, QTimer

class PaintWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.refreshRate = 30
        self.timing = 0

        self.points = []

        for i in range(8):
            x = i / 8.0
            y = i / 8.0

            self.points += [(x, y)]

        timer = QTimer(self, timeout=self.update, interval=(1000 / self.refreshRate))
        timer.start()

    def paintEvent(self, event):
        qp = QPainter(self)

        qp.setPen(Qt.black)
        size = self.size()

        for (x, y) in self.points:
            x = x * size.width()
            y = y * size.height()

            y = (y + self.timing / 10) % size.height()

            qp.fillRect(x, y-5, 20, 50, Qt.blue)

        self.timing += self.refreshRate

    def sizeHint(self):
        return QSize(400, 400)