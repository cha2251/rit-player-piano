from threading import Timer
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer, QRect, QPropertyAnimation, QPoint, QAbstractAnimation, QSequentialAnimationGroup

import random
import time
import copy

from src.common.shared_queues import SharedQueues

class NotesWidget(QWidget):
    def __init__(self, refreshRate=30, parent=None, output=None):
        super().__init__(parent=parent)

        self.refreshRate = 30.0

        self.key_width = 36
        self.black_key_positions = [0.5, 1.5, 3.5, 4.5, 5.5]

        self.notes_width = self.key_width * 0.5
        self.notes_height = 10
        self.widget_height = 750

        self.octaves = 7

        self.time = 0
        self.max_time = 3
        self.max_render_time = self.max_time + 2

        self.note_offsets = [0, 0.5, 1, 1.5, 2, 3, 3.5, 4, 4.5, 5, 5.5, 6]
        self.update_note_queue()
        self.rendered_image = QImage(self.sizeHint().width(), self.sizeHint().height() * (self.max_render_time / self.max_time), QImage.Format_ARGB32)
        self.paintScene()

        self.render_timer = QTimer(self, timeout=self.thingy, interval=(1000 / 1.0))
        self.render_timer.start()

        # QTimer(self, timeout=self.paintScene, interval=1000).start()
        Timer(0.1, self.paintScene).start()

        self.output = output
        self.shared_queues = SharedQueues()

        self.setBaseSize(self.sizeHint())

        self.label = QLabel(self)
        self.label.hide()

    def thingy(self):
        yoffset = self.rendered_image.height() / self.max_render_time
        doffset = (self.time - time.time()) / self.max_render_time * self.rendered_image.height()
        hoffset = self.rendered_image.height() - self.height()

        self.anim = QPropertyAnimation(self.label, b"pos")
        self.anim.setEndValue(QPoint(0, -doffset - hoffset))
        self.anim.setDuration(0)
        self.anim.start(QAbstractAnimation.DeleteWhenStopped)

        self.label.hide()
        self.label.setPixmap(QPixmap.fromImage(self.rendered_image))
        self.label.show()

        self.anim = QPropertyAnimation(self.label, b"pos")
        self.anim.setEndValue(QPoint(0, yoffset - doffset - hoffset))
        self.anim.setDuration(1000)
        self.anim.start(QAbstractAnimation.DeleteWhenStopped)

    def paintScene(self):
        Timer(1, self.paintScene).start()

        self.time = time.time()
        self.rendered_image.fill(Qt.transparent)
        current_time = time.time()
        qp = QPainter()
        qp.begin(self.rendered_image)

        if SharedQueues.mixed_output_queue is None:
            return

        i = -1
        for event in self.notes_queue:
            i += 1
            start_timestamp = event.timestamp
            end_timestamp = event.timestamp + 0.5

            if event.timestamp > current_time + self.max_render_time:
                break
            elif event.event.type != "note_on" or event.event.velocity == 0:
                found = False

                for j in range(i - 1, -1, -1):
                    if self.notes_queue[j].event.note == event.event.note:
                        found = True
                        break

                if found:
                    continue

                end_timestamp = event.timestamp
                start_timestamp = event.timestamp - self.max_render_time
            else:
                for j in range(i + 1, len(self.notes_queue)):
                    if (self.notes_queue[j].event.type == "note_off" or self.notes_queue[j].event.velocity == 0) and self.notes_queue[j].event.note == event.event.note:
                        end_timestamp = self.notes_queue[j].timestamp
                        break

            key = event.event.note - 24
            x = ((key // 12) * 7 + self.note_offsets[key % 12]) * self.key_width
            y = self.rendered_image.height() * (1 - ((start_timestamp - current_time) / self.max_render_time))
            y2 = self.rendered_image.height() * (1 - ((end_timestamp - current_time) / self.max_render_time))

            qp.fillRect(
                x + (self.key_width - self.notes_width) / 2,
                y2,
                self.notes_width,
                y - y2,
                QColor(0, 179, 255) if event.event.note < 60 else QColor(0, 255, 119)
            )

        elapsed = time.time() - current_time
        # print("{}, {}".format(elapsed, 1 / self.refreshRate - elapsed))

        if elapsed > 1 / self.refreshRate:
            print("Warning: NotesWidget took too long to render ({:.1} ms).".format(elapsed * 1e3))

        qp.end()

    def update_note_queue(self):
        self.notes_queue = SharedQueues.mixed_output_queue.peekn(512)

        Timer(1.1, self.update_note_queue).start()

    def sizeHint(self):
        return QSize(self.octaves * 7 * self.key_width, self.widget_height)