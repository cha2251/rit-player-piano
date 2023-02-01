from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize, QTimer

class PianoWidget(QWidget):
    def __init__(self, refreshRate=24, parent=None, output=None):
        super().__init__(parent=parent)

        self.timer = QTimer(self, timeout=self.update, interval=(1000 / refreshRate))
        self.timer.start()

        self.border_size = 3
        self.key_width = 48
        self.key_height = self.key_width * 4

        self.black_key_width = self.key_width * 0.66667
        self.black_key_height = self.key_height * 0.6
        self.black_key_positions = [0.5, 1.5, 3.5, 4.5, 5.5]

        self.octaves = 7

        self.output = output

        self.setBaseSize(self.sizeHint())

    def paintEvent(self, _event):
        qp = QPainter(self)

        white_key_note_offset = [0, 2, 4, 5, 7, 9, 11]
        black_key_note_offset = [1, 3, 6, 8, 10]

        playing_notes = self.output.get_playing_notes()

        # Draw the white keys
        for i in range(self.octaves * 7 + 1):
            x = i * self.key_width
            y = 0

            note = 24 + white_key_note_offset[i % 7] + (i // 7) * 12

            # Draw the key border
            qp.setPen(QPen(QColor(0, 0, 0, 255), self.border_size))
            qp.drawRect(
                x + self.border_size,
                y,
                self.key_width - self.border_size * 2,
                self.key_height - self.border_size / 2,
            )

            # Draw the key
            qp.fillRect(
                x + self.border_size,
                y,
                self.key_width - self.border_size * 2,
                self.key_height,
                Qt.yellow if note in playing_notes else Qt.white,
            )

        # Draw the black keys
        for i in range(self.octaves * 5):
            black_key_offset = self.key_width * self.black_key_positions[i % 5]
            octave_offset = self.key_width * (i // 5) * 7
            x = black_key_offset + octave_offset + self.black_key_width / 4
            y = 0

            note = 24 + black_key_note_offset[i % 5] + (i // 5) * 12

            # Draw the key border
            qp.setPen(QPen(QColor(50, 50, 50, 255), self.border_size))
            qp.drawRect(
                x + self.border_size,
                y,
                self.black_key_width - self.border_size * 2,
                self.black_key_height - self.border_size / 2,
            )

            # Draw the key
            qp.fillRect(
                x + self.border_size,
                y,
                self.black_key_width - self.border_size * 2,
                self.black_key_height - self.border_size / 2,
                Qt.yellow if note in playing_notes else Qt.black,
            )

    def sizeHint(self):
        return QSize(self.octaves * 7 * self.key_width, self.key_height)