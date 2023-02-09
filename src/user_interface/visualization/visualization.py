from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QSize, QTimer

from src.user_interface.visualization.piano_widget import PianoWidget
from src.user_interface.visualization.notes_widget import NotesWidget

class VisualizationWidget(QWidget):
    def __init__(self, refreshRate=30, parent=None, output=None):
        super().__init__(parent=parent)

        self.notes_widget = NotesWidget(refreshRate=refreshRate, parent=self, output=output)
        self.piano_widget = PianoWidget(refreshRate=refreshRate, parent=self, output=output)

        hbox = QHBoxLayout(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.notes_widget)
        vbox.addWidget(self.piano_widget)

        hbox.addLayout(vbox)