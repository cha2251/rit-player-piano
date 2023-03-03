from threading import Timer
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer, QRect, QPropertyAnimation, QPoint, QAbstractAnimation, QSequentialAnimationGroup

import random
import time
import copy
from src.common.shared_priority_queue import PeekingPriorityQueue
from src.communication.messages import Message, MessageType, PlayingState

from src.user_interface.ui_comm import UICommSystem

RENDER_BUFFER_TIME = 2 # In seconds
QUEUE_UPDATE_RATE = 2.2 # In seconds
QUEUE_BUFFER_SIZE = 1024
ANIMATION_RATE = 1 # In seconds
RENDER_RATE = 0.25 # In seconds

class NotesWidget(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent=parent)

        self.config = config
        self.comm_system = UICommSystem()
        self.comm_system.registerListener(MessageType.STATE_UPDATE, self.on_state_change)
        self.comm_system.registerListener(MessageType.OUTPUT_QUEUE_UPDATE, self.queue_update)

        self.notes_queue = PeekingPriorityQueue()
        self.widget_height = 750

        self.state = PlayingState.STOP
        self.last_note_timestamp = None
        self.last_note_time_played = 0
        self.last_rendered_time = 0
        self.max_render_time = self.config.display_lead_time + RENDER_BUFFER_TIME

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

        if self.last_note_timestamp is None:
            self.last_rendered_time = time.time()
            return

        current_time = time.time()

        # Remove all notes that have been played from the queue and update the timing variables
        try:
            last_note_timestamp = None
            while self.notes_queue.peek() is not None and self.state == PlayingState.PLAY:
                if self.last_note_time_played - self.last_note_timestamp <= current_time - self.notes_queue.peek().timestamp:
                    last_note_timestamp = self.notes_queue.get().timestamp
                else:
                    break

            if last_note_timestamp is not None:
                self.last_note_time_played = current_time
                self.last_note_timestamp = last_note_timestamp
        except:
            pass

        self.rendered_image.fill(Qt.transparent)
        qp = QPainter()
        qp.begin(self.rendered_image)

        relative_time = current_time - self.last_note_time_played + self.last_note_timestamp
        print("nw: {}".format(relative_time))

        sorted_notes = self.notes_queue.peekn(self.notes_queue.qsize())

        for i in range(len(sorted_notes)):
            event = sorted_notes[i]

            start_timestamp = event.timestamp
            end_timestamp = event.timestamp + 0.5

            if event.timestamp > relative_time + self.max_render_time:
                break
            elif event.event.type != "note_on" or event.event.velocity == 0:
                # Fill in notes who's on_event already happened but are still playing (so we need to render)

                # Make sure that the note isn't already playing
                found = False
                for j in range(i - 1, -1, -1):
                    if sorted_notes[j].event.note == event.event.note:
                        found = True
                        break

                if found:
                    continue

                end_timestamp = event.timestamp
                start_timestamp = event.timestamp - self.max_render_time
            else:
                # Find the note_off event so we know what the render
                for j in range(i + 1, len(sorted_notes)):
                    if (sorted_notes[j].event.type == "note_off" or sorted_notes[j].event.velocity == 0) and sorted_notes[j].event.note == event.event.note:
                        end_timestamp = sorted_notes[j].timestamp
                        break

            # Figure out the positions of the rectangle to render for this note
            key = event.event.note - 24
            x = ((key // 12) * 7 + self.config.note_offsets[key % 12]) * self.config.key_width
            y = self.rendered_image.height() * (1 - ((start_timestamp - relative_time) / self.max_render_time))
            y2 = self.rendered_image.height() * (1 - ((end_timestamp - relative_time) / self.max_render_time))

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

    def play(self):
        if self.last_note_timestamp is not None:
            # Restore the difference so that the timing remains correct
            self.last_note_timestamp += time.time()
        else:
            # If we are starting from the beginning, clear the queue and reset the timestamp
            self.last_note_timestamp = 0
            self.notes_queue.clear()

    def pause(self):
        if self.last_note_timestamp is not None:
            self.last_note_timestamp -= time.time() # Store the difference between this and now for later

    def stop(self):
        self.last_note_timestamp = None # Signals that we removed all notes from the queue and want to start over
        self.last_note_time_played = 0
        self.notes_queue.clear()

    def on_state_change(self, message: Message):
        self.state = message.data

        if self.state == PlayingState.PLAY:
            self.play()
        elif self.state == PlayingState.PAUSE:
            self.pause()
        elif self.state == PlayingState.STOP:
            self.stop()

    def queue_update(self, message: Message):
        self.notes_queue.put(message.data)

    def sizeHint(self):
        return QSize(self.config.octaves * 7 * self.config.key_width, self.widget_height)