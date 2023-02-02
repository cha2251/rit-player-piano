import sys
from src.mixing.mixing import Mixing
from PyQt5.QtWidgets import QApplication, QWidget,  QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize, Qt


class PlayingPage(QWidget):
    def __init__(self, mixing_system, song_name="DEFAULT"):
        super().__init__()
        self.mixing_system = mixing_system
        self.song_name = song_name
        self.nav_home = QPushButton("LINK: " + song_name)
        self.title = "TITLE: "
        self.left = 100
        self.top = 50
        self.width = 320
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        playButton = QPushButton('', self)
        playButton.setIcon(QIcon(r"UI_Images/play-solid.svg"))
        playButton.setIconSize(QSize(65, 65))
        playButton.setToolTip('play song')
        playButton.clicked.connect(self.on_click_play)

        stopButton = QPushButton('', self)
        stopButton.setIcon(QIcon(r"UI_Images/stop-solid.svg"))
        stopButton.setIconSize(QSize(65, 65))
        stopButton.setToolTip('stop song')
        stopButton.clicked.connect(self.on_click_stop)

        pauseButton = QPushButton('', self)
        pauseButton.setIcon(QIcon(r"UI_Images/pause-solid.svg"))
        pauseButton.setIconSize(QSize(65, 65))
        pauseButton.setToolTip('pause song')
        pauseButton.clicked.connect(self.on_click_pause)

        restartButton = QPushButton('', self)
        restartButton.setIcon(QIcon(r"UI_Images/rotate-left-solid.svg"))
        restartButton.setIconSize(QSize(65, 65))
        restartButton.setToolTip('restart song')
        restartButton.clicked.connect(self.on_click_restart)

        spacer = QSpacerItem(1000, 5, QSizePolicy.Expanding)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(restartButton)
        hbox.addWidget(stopButton)
        hbox.addWidget(pauseButton)
        hbox.addWidget(playButton)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.nav_home)
        vbox.addLayout(hbox)
        # vbox.addWidget(playButton)
        self.initUI()

    def initUI(self):
        # self.showFullScreen()
        self.showMaximized()

    @pyqtSlot()
    def on_click_quit(self):
        print('quit pushed')

    @pyqtSlot()
    def on_click_stop(self):
        print('stop pushed')
        self.mixing_system.stop_pushed()

    @pyqtSlot()
    def on_click_pause(self):
        print('pause pushed')
        self.mixing_system.pause_pushed()

    @pyqtSlot()
    def on_click_play(self):
        print('play pushed')
        self.mixing_system.play_pushed()

    @pyqtSlot()
    def on_click_restart(self):
        print('restart pushed')

    def set_song(self, song):
        print("setting song: " + song)
        self.title = song
        self.nav_home.setText("SONG: " + song)
        self.setWindowTitle("Player Piano: " + song)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlayingPage()
    sys.exit(app.exec_())
