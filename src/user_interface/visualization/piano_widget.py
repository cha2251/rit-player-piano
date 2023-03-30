import os
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon, QImage
from PyQt5.QtCore import Qt, QSize, QTimer, QRect
from src.communication.messages import MessageType
from src.user_interface.pianoKey import CONTROLLER_BUTTON_MAP

from src.user_interface.ui_comm import UICommSystem

WIDGET_REFRESH_RATE = 60

STRING_NOTE_MAPPING = {
    "c3": 48, # 3rd C
    "c#3": 49,
    "d3": 50,
    "d#3": 51,
    "e3": 52,
    "f3": 53,
    "f#3": 54,
    "g3": 55,
    "g#3": 56,
    "a3": 57,
    "a#3": 58,
    "b3": 59,
    "c4": 60, # Middle C
    "c#4": 61,
    "d4": 62,
    "d#4": 63,
    "e4": 64,
    "f4": 65,
    "f#4": 66,
    "g4": 67,
    "g#4": 68,
    "a4": 69,
    "a#4": 70,
    "b4": 71,
    "c5": 72, # 5th C
}

class PianoWidget(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent=parent)

        self.config = config
        self.comm_system = UICommSystem()
        self.playing_notes = {}
        self.button_icons = {}

        QTimer(self, timeout=self.update, interval=(1000 / WIDGET_REFRESH_RATE)).start()
        self.comm_system.registerListener(MessageType.NOTE_OUTPUT, self.on_note_output)
        self.comm_system.registerListener(MessageType.BUTTON_CONFIG_UPDATE, self.button_config_update)

        self.setBaseSize(self.sizeHint())

    def on_note_output(self, message):
        midiEvent = message.data.event
        if midiEvent.event.type == "note_off" or midiEvent.event.velocity == 0:
            if midiEvent.event.note in self.playing_notes:
                del self.playing_notes[midiEvent.event.note]
        else:
            self.playing_notes[midiEvent.event.note] = True

    def button_config_update(self, message):
        # self.button_config = message.data
        self.button_icons = {}

        for (file, button) in CONTROLLER_BUTTON_MAP.items():
            for (note, buttons) in message.data.items():
                if button in buttons:
                    midi_note = STRING_NOTE_MAPPING[note]
                    icon = self.loadIcon(file)

                    octave_note = midi_note % 12

                    if octave_note in self.config.black_key_indices:
                        icon.invertPixels(QImage.InvertMode.InvertRgb)

                    self.button_icons[midi_note] = icon

        print(self.button_icons)

    def paintEvent(self, _event):
        qp = QPainter(self)

        # Draw the white keys
        for i in range(self.config.octaves * 7 + 1):
            x = i * self.config.key_width
            y = 0

            octave_note = self.config.white_key_indices[i % 7]
            note = 36 + octave_note + (i // 7) * 12

            # Draw the key border
            qp.setPen(QPen(self.config.key_border_color, self.config.key_border_size))
            qp.drawRect(
                x + self.config.key_border_size / 2,
                y,
                self.config.key_width - self.config.key_border_size,
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

            # Draw the note icon if there is one
            if note in self.button_icons:
                icon = self.button_icons[note]
                icon_size = (self.config.key_width - self.config.key_border_size * 2) * 0.667
                icon_x = x + (self.config.key_width - icon_size) / 2
                icon_y = self.config.get_key_height() - (self.config.get_key_height() - self.config.get_black_key_height() + icon_size) / 2

                qp.drawImage(
                    QRect(
                        icon_x,
                        icon_y,
                        icon_size,
                        icon_size,
                    ),
                    icon,
                )

        # Draw the black keys
        for i in range(self.config.octaves * 5):
            octave_note = self.config.black_key_indices[i % 5]
            note = 36 + octave_note + (i // 5) * 12

            octave_offset = (i // 5) * 7 * self.config.key_width
            note_offset = self.config.note_offsets[octave_note] * self.config.key_width
            x = octave_offset + note_offset + (self.config.key_width - self.config.get_black_key_width()) / 2
            y = 0

            # Draw the key border
            qp.setPen(QPen(QColor(50, 50, 50, 255), self.config.key_border_size))
            qp.drawRect(
                x + self.config.key_border_size / 2,
                y,
                self.config.get_black_key_width() - self.config.key_border_size,
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

            # Draw the note icon if there is one
            if note in self.button_icons:
                icon = self.button_icons[note]
                icon_size = (self.config.key_width - self.config.key_border_size * 2) * 0.667
                icon_x = x + (self.config.get_black_key_width() - icon_size) / 2
                icon_y = self.config.get_black_key_height() / 2 - icon_size / 2

                qp.drawImage(
                    QRect(
                        icon_x,
                        icon_y,
                        icon_size,
                        icon_size,
                    ),
                    icon,
                )

    def sizeHint(self):
        return QSize(self.config.octaves * 7 * self.config.key_width, self.config.get_key_height())

    def loadIcon(self, file):
        return QImage(os.path.join(os.path.dirname(__file__), "..", "..", "..", "UI_Images", "settings", (file + ".svg")),)
        # return QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "..", "UI_Images", "settings", (file + ".svg")),)