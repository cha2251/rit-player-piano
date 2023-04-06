from threading import Lock, Timer
import time
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QSize, QTimer
from src.communication.messages import MessageType

from src.user_interface.ui_comm import UICommSystem

WIDGET_REFRESH_RATE = 1.0 / 60

class PianoWidget(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent=parent)

        self.config = config
        self.comm_system = UICommSystem()
        self.playing_notes = {}
        self.accessLock = Lock()

        self.update()
        self.comm_system.registerListener(MessageType.NOTE_OUTPUT, self.on_note_output)

        self.setBaseSize(self.sizeHint())

    def on_note_output(self, message):
        with self.accessLock:
            midiEvent = message.data.event
            if midiEvent.event.type == "note_off" or midiEvent.event.velocity == 0:
                if midiEvent.event.note in self.playing_notes:
                    del self.playing_notes[midiEvent.event.note]
            else:
                self.playing_notes[midiEvent.event.note] = True

    def paintEvent(self, _event):
        start_time = time.time()
        qp = QPainter(self)

        # Draw the white keys
        for i in range(self.config.octaves * 7 + 1):
            x = i * self.config.key_width
            y = 0

            octave_note = self.config.white_key_indices[i % 7]
            note = 24 + octave_note + (i // 7) * 12

            # Draw the key border
            qp.setPen(QPen(self.config.key_border_color, self.config.key_border_size))
            qp.drawRect(
                x + self.config.key_border_size,
                y,
                self.config.key_width - self.config.key_border_size * 2,
                self.config.get_key_height() - self.config.key_border_size / 2,
            )

            # Draw the key
            qp.fillRect(
                x + self.config.key_border_size,
                y,
                self.config.key_width - self.config.key_border_size * 2,
                self.config.get_key_height(),
                (self.config.left_hand_color if note < 60 else self.config.right_hand_color) if note in self.playing_notes.keys() else Qt.white,
            )

        # Draw the black keys
        for i in range(self.config.octaves * 5):
            octave_note = self.config.black_key_indices[i % 5]
            note = 24 + octave_note + (i // 5) * 12

            octave_offset = (i // 5) * 7 * self.config.key_width
            note_offset = self.config.note_offsets[octave_note] * self.config.key_width
            x = octave_offset + note_offset + self.config.get_black_key_width() / 4
            y = 0

            # Draw the key border
            qp.setPen(QPen(QColor(50, 50, 50, 255), self.config.key_border_size))
            qp.drawRect(
                x + self.config.key_border_size,
                y,
                self.config.get_black_key_width() - self.config.key_border_size * 2,
                self.config.get_black_key_height() - self.config.key_border_size / 2,
            )

            # Draw the key
            qp.fillRect(
                x + self.config.key_border_size,
                y,
                self.config.get_black_key_width() - self.config.key_border_size * 2,
                self.config.get_black_key_height() - self.config.key_border_size / 2,
                (self.config.left_hand_color if note < 60 else self.config.right_hand_color) if note in self.playing_notes.keys() else Qt.black,
            )

        qp.end()

        elapsed = time.time() - start_time
        if elapsed >= WIDGET_REFRESH_RATE:
            self.update()
        else:
            Timer(WIDGET_REFRESH_RATE - elapsed, self.update).start()

    def sizeHint(self):
        return QSize(self.config.octaves * 7 * self.config.key_width, self.config.get_key_height())