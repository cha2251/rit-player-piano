from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize, QTimer

import random

class NotesWidget(QWidget):
    def __init__(self, refreshRate=30, parent=None):
        super().__init__(parent=parent)

        self.timer = QTimer(self, timeout=self.update, interval=(1000 / refreshRate))
        self.timer.start()

        self.key_width = 64
        self.black_key_positions = [0.5, 1.5, 3.5, 4.5, 5.5]

        self.notes_width = self.key_width * 0.6667
        self.notes_height = self.notes_width * 3
        self.widget_height = 500

        self.octaves = 3

        self.time = 0

        self.test_offsets = []

        for i in range(self.octaves * 7 + 1):
            self.test_offsets.append(i * self.notes_height + random.randint(0, int(self.widget_height)))

        self.setBaseSize(self.sizeHint())

    def paintEvent(self, _event):
        qp = QPainter(self)

        testing_speed = 200

        # Draw the white key notes
        for i in range(self.octaves * 7 + 1):
            if i % 2 == 1:
                continue

            delta = self.key_width - self.notes_width
            x = i * self.key_width
            y = (self.time * testing_speed + self.test_offsets[i]) % self.widget_height

            qp.fillRect(
                x + delta / 2,
                y,
                self.notes_width,
                self.notes_height,
                QColor(255, 215, 0, 255),
            )

        self.time += self.timer.interval() / 1000

    def sizeHint(self):
        return QSize(self.octaves * 7 * self.key_width, self.widget_height)