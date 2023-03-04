from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QColor

from src.user_interface.visualization.piano_widget import PianoWidget
from src.user_interface.visualization.notes_widget import NotesWidget

KEY_ASPECT_RATIO = 4
BLACK_KEY_WIDTH_MULT = 0.67
BLACK_KEY_HEIGHT_MULT = 0.61

class VisualizationConfig:
    def __init__(self):
        self.key_width = 36 # In pixels
        self.key_border_size = 3 # In pixels
        self.note_width_mult = 0.67 # How much of the key width a note should take up vs a piano key
        self.visualization_height = 500 # In pixels

        self.octaves = 7 # How many octaves to render. Don't touch this for now, it doesn't like being touched
        self.display_lead_time = 3 # How long a note takes to travel down the screen in seconds

        self.left_hand_color = QColor(0, 179, 255, 255)
        self.right_hand_color = QColor(0, 255, 119, 255)
        self.key_border_color = QColor(0, 0, 0, 255)

        self.note_offsets = [0, 0.5, 1, 1.5, 2, 3, 3.5, 4, 4.5, 5, 5.5, 6]
        self.white_key_indices = [0, 2, 4, 5, 7, 9, 11]
        self.black_key_indices = [1, 3, 6, 8, 10]

    def get_key_height(self):
        return self.key_width * KEY_ASPECT_RATIO

    def get_black_key_width(self):
        return self.key_width * BLACK_KEY_WIDTH_MULT

    def get_black_key_height(self):
        return self.get_key_height() * BLACK_KEY_HEIGHT_MULT

    def get_note_width(self):
        return self.key_width * self.note_width_mult


class VisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.config = VisualizationConfig()

        self.notes_widget = NotesWidget(self.config, parent=self)
        self.piano_widget = PianoWidget(self.config, parent=self)

        hbox = QHBoxLayout(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.notes_widget)
        vbox.addWidget(self.piano_widget)

        hbox.addLayout(vbox)