from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize, QTimer

import random
import time
import copy

from src.common.shared_queues import SharedQueues

class NotesWidget(QWidget):
    def __init__(self, refreshRate=30, parent=None):
        super().__init__(parent=parent)

        self.timer = QTimer(self, timeout=self.update, interval=(1000 / 10))
        self.timer.start()

        self.shared_queues = SharedQueues()

        self.key_width = 32
        self.black_key_positions = [0.5, 1.5, 3.5, 4.5, 5.5]

        self.notes_width = self.key_width * 0.6667
        self.notes_height = 10
        self.widget_height = 500

        self.octaves = 7

        self.time = 0
        self.max_time = 3

        self.test_offsets = []
        self.note_offsets = [0, 0.5, 1, 1.5, 2, 3, 3.5, 4, 4.5, 5, 5.5, 6]

        for i in range(self.octaves * 7 + 1):
            self.test_offsets.append(i * self.notes_height + random.randint(0, int(self.widget_height)))

        self.setBaseSize(self.sizeHint())

    def paintEvent(self, _event):
        qp = QPainter(self)

        if SharedQueues.mixed_output_queue is None:
            return

        n = 0
        current_queue = sorted(SharedQueues.mixed_output_queue.copy_of_queue(), key=lambda x: x.timestamp)
        current_time = time.time()

        while True:
            if n >= len(current_queue):
                break

            event = current_queue[n]
            n += 1

            if event.timestamp > current_time + self.max_time:
                break
            elif event.event.type != "note_on":
                continue

            key = event.event.note - 24
            x = ((key // 12) * 7 + self.note_offsets[key % 12]) * self.key_width
            y = self.widget_height * (1 - ((event.timestamp - time.time()) / self.max_time))

            qp.fillRect(
                x + (self.key_width - self.notes_width) / 2,
                y - self.notes_height,
                self.notes_width,
                self.notes_height,
                QColor(255, 215, 0, 255),
            )

        # # Draw the white key notes
        # for i in range(self.octaves * 7 + 1):
        #     if i % 2 == 1:
        #         continue

        #     delta = self.key_width - self.notes_width
        #     x = i * self.key_width
        #     y = (self.time * testing_speed + self.test_offsets[i]) % self.widget_height

        #     qp.fillRect(
        #         x + delta / 2,
        #         y,
        #         self.notes_width,
        #         self.notes_height,
        #         QColor(255, 215, 0, 255),
        #     )

        self.time += self.timer.interval() / 1000

    def sizeHint(self):
        return QSize(self.octaves * 7 * self.key_width, self.widget_height)