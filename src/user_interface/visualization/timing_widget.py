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
        self.score_label.setText("Accuracy: 100%")

        self.vbox.addWidget(self.score_label)
        self.vbox.addWidget(self.label)

        self.last_event_timestamp = 0
        self.hit_notes = 0
        self.total_notes = 0

        self.refresh_timer = QTimer(self, timeout=self.refresh_label, interval=int(1000 * REFRESH_RATE))
        self.refresh_timer.start()

    def refresh_label(self):
        if time.time() - self.last_event_timestamp > 0.667:
            self.label.setText("")

    def on_tempo_mode_update(self, event: Message):
        self.last_event_timestamp = time.time()

        if event.data.type == TempoModeMessageType.HIT_NOTE:
            if abs(event.data.time_delta) < 0.15:
                self.label.setText("PERFECT!")
                self.hit_notes += 1
            elif abs(event.data.time_delta) < 0.25:
                self.label.setText("GOOD")
                self.hit_notes += 0.9
            else:
                self.label.setText("Ok...")
                self.hit_notes += 0.8

        self.total_notes += 1
        self.score_label.setText(f"Accuracy: {int(100 * self.hit_notes / self.total_notes)}%")