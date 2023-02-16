from threading import Timer
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer, QRect, QPropertyAnimation, QPoint, QAbstractAnimation, QSequentialAnimationGroup

import random
import time
import copy

RENDER_BUFFER_TIME = 2 # In seconds
QUEUE_UPDATE_RATE = 2.2 # In seconds
QUEUE_BUFFER_SIZE = 1024
ANIMATION_RATE = 1 # In seconds
RENDER_RATE = 0.25 # In seconds

class NotesWidget(QWidget):
    def __init__(self, config, parent=None, output=None):
        super().__init__(parent=parent)

        self.config = config

        self.widget_height = 750

        self.last_rendered_time = 0
        self.max_render_time = self.config.display_lead_time + RENDER_BUFFER_TIME
        self.output = output

        self.update_note_queue()
        self.rendered_image = QImage(self.sizeHint().width(), self.sizeHint().height() * (self.max_render_time / self.config.display_lead_time), QImage.Format_ARGB32)
        self.paintScene()

        self.paintScene()
        QTimer(self, timeout=self.thingy, interval=int(ANIMATION_RATE * 1000)).start()

        self.setBaseSize(self.sizeHint())

        # This label is used to animate the notes. It "becomes" this entire widget and displays the image
        # that gets rendered to and animates it downwards. Yes it's complicated, but also yes the built-in
        # animation is faster than having to render on the fly at >= 30 FPS.
        self.label = QLabel(self)
        self.label.hide()

    def thingy(self):
        yoffset = self.rendered_image.height() / self.max_render_time
        doffset = (self.last_rendered_time - time.time()) / self.max_render_time * self.rendered_image.height()
        hoffset = self.rendered_image.height() - self.height()
        start_offset = -doffset - hoffset

        # Move the animation back to the start instantly
        self.anim = QPropertyAnimation(self.label, b"pos")
        self.anim.setEndValue(QPoint(0, start_offset))
        self.anim.setDuration(0)
        self.anim.start(QAbstractAnimation.DeleteWhenStopped)

        # Update the label's image
        self.label.hide()
        self.label.setPixmap(QPixmap.fromImage(self.rendered_image))
        self.label.show()

        # Move the animation downwards until the next animation cycle
        self.anim = QPropertyAnimation(self.label, b"pos")
        self.anim.setEndValue(QPoint(0, start_offset + yoffset))
        self.anim.setDuration(int(ANIMATION_RATE * 1000))
        self.anim.start(QAbstractAnimation.DeleteWhenStopped)

    def paintScene(self):
        Timer(RENDER_RATE, self.paintScene).start()

        self.rendered_image.fill(Qt.transparent)
        current_time = time.time()
        qp = QPainter()
        qp.begin(self.rendered_image)

        for i in range(len(self.notes_queue)):
            event = self.notes_queue[i]

            start_timestamp = event.timestamp
            end_timestamp = event.timestamp + 0.5

            if event.timestamp > current_time + self.max_render_time:
                break
            elif event.event.type != "note_on" or event.event.velocity == 0:
                # Fill in notes who's on_event already happened but are still playing (so we need to render)

                # Make sure that the note isn't already playing
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
                # Find the note_off event so we know what the render
                for j in range(i + 1, len(self.notes_queue)):
                    if (self.notes_queue[j].event.type == "note_off" or self.notes_queue[j].event.velocity == 0) and self.notes_queue[j].event.note == event.event.note:
                        end_timestamp = self.notes_queue[j].timestamp
                        break

            # Figure out the positions of the rectangle to render for this note
            key = event.event.note - 24
            x = ((key // 12) * 7 + self.config.note_offsets[key % 12]) * self.config.key_width
            y = self.rendered_image.height() * (1 - ((start_timestamp - current_time) / self.max_render_time))
            y2 = self.rendered_image.height() * (1 - ((end_timestamp - current_time) / self.max_render_time))

            qp.fillRect(
                x + (self.config.key_width - self.config.get_note_width()) / 2,
                y2,
                self.config.get_note_width(),
                y - y2,
                self.config.left_hand_color if event.event.note < 60 else self.config.right_hand_color
            )

        qp.end()

        elapsed = time.time() - current_time
        if elapsed > RENDER_RATE:
            print("Warning: NotesWidget took too long to render ({:.1} ms).".format(elapsed * 1e3))

        self.last_rendered_time = time.time()

    def update_note_queue(self):
        self.notes_queue = self.output.get_queue().peekn(QUEUE_BUFFER_SIZE)

        Timer(QUEUE_UPDATE_RATE, self.update_note_queue).start()

    def sizeHint(self):
        return QSize(self.config.octaves * 7 * self.config.key_width, self.widget_height)