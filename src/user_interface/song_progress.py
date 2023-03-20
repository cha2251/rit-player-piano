from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QProgressBar, QLabel, QHBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QFont

class SongWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        self.value = 0

        self.timeLabel = QLabel("00:00")
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        layout = QHBoxLayout()
        layout.addWidget(self.timeLabel)
        layout.addWidget(self.progressBar)
        self.setLayout(layout)

        styleSheet = """
            QProgressBar {
                border: 2px solid gray;
                border-radius: 8px;
                background-color: #FFFFFF;
            }
            QProgressBar::chunk {
                border-radius: 8px;
                background-color: #FFA07A;
            }
        """
        self.progressBar.setStyleSheet(styleSheet)

    def startTimer(self):
        self.timer.start(1000)  # update every second

    def stopTimer(self):
        self.timer.stop()

    def resetTimer(self):
        self.timer.stop()
        self.progressBar.setValue(0)
        self.timeLabel.setText("00:00")

    def setDuration(self, duration):
        self.duration = duration
        self.progressBar.setMaximum(self.duration)

    def updateTimer(self):
        self.value = self.progressBar.value() + 1
        self.progressBar.setValue(self.value)

        minutes = int(self.value / 60)
        seconds = int(self.value % 60)
        timeStr = "{:02d}:{:02d}".format(minutes, seconds)
        self.timeLabel.setText(timeStr)

