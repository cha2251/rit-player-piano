import time

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer
from src.communication.messages import Message, MessageType, TempoModeMessageType

from src.user_interface.ui_comm import UICommSystem

REFRESH_RATE = 0.1

class TimingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.comm_system = UICommSystem()
        self.comm_system.registerListener(MessageType.TEMPO_MODE_UPDATE, self.on_tempo_mode_update)

        self.vbox = QVBoxLayout(self)

        self.label = QLabel()
        self.label.setText("")

        self.score_label = QLabel()
        self.score_label.setText("Score: 0")

        self.vbox.addWidget(self.score_label)
        self.vbox.addWidget(self.label)

        self.last_event_timestamp = 0
        self.score = 0

        self.refresh_timer = QTimer(self, timeout=self.refresh_label, interval=int(1000 * REFRESH_RATE))
        self.refresh_timer.start()

    def refresh_label(self):
        if time.time() - self.last_event_timestamp > 0.667:
            self.label.setText("")

    def on_tempo_mode_update(self, event: Message):
        self.last_event_timestamp = time.time()

        if event.data.type == TempoModeMessageType.HIT_NOTE:
            if abs(event.data.time_delta) < 0.15:
                self.label.setText("! PERFECT !")
                self.score += 10
            elif abs(event.data.time_delta) < 0.25:
                self.label.setText("GOOD")
                self.score += 5
            else:
                self.label.setText("Ok...")
                self.score += 1

            self.score_label.setText(f"Score: {self.score}")