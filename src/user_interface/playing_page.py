import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QLabel, QToolButton, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize, Qt
import time
from src.communication.messages import Message, MessageType, PlayingState
from src.user_interface.song_progress import SongWidget

from src.user_interface.ui_comm import UICommSystem

from src.user_interface.visualization.visualization import VisualizationWidget


class PlayingPage(QWidget):
    def __init__(self, song_name="DEFAULT"):
        button = """
        max-width: 7em;
        min-width: 3em;
        """

        super().__init__()
        self.nav_home = QToolButton()
        self.nav_home.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.nav_home.setIconSize(QSize(55, 55))
        self.nav_home.setText("back")
        self.nav_home.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "navigation", "back-arrow.svg")))
        self.nav_home.setStyleSheet(button)  # it seems like the min-width is the important one

        self.configure = QToolButton()
        self.configure.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.configure.setIconSize(QSize(55, 55))
        self.configure.setText("Configure input")
        self.configure.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "gear.svg")))
        self.configure.setStyleSheet(button)

        self.song_name = song_name
        self.left = 100
        self.top = 50
        self.width = 320
        self.height = 200
        self.title = "RIT Player Piano"
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.song_duration = 0
        self.comm_system = UICommSystem()
        self.comm_system.registerListener(MessageType.SET_DURATION, self.set_song_duration)

        #################
        # Song Timer/Progress Bar
        #################
        self.songWidget = SongWidget()
        #################

        playButton = QToolButton()
        playButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        playButton.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "play-solid.svg")))
        playButton.setIconSize(QSize(65, 65))
        playButton.setText("play")
        playButton.setToolTip("play song")
        playButton.setStyleSheet(button)
        playButton.clicked.connect(self.on_click_play)

        pauseButton = QToolButton()
        pauseButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        pauseButton.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "pause-solid.svg")))
        pauseButton.setIconSize(QSize(65, 65))
        pauseButton.setText('pause')
        pauseButton.setToolTip('pause song')
        pauseButton.setStyleSheet(button)
        pauseButton.clicked.connect(self.on_click_pause)

        restartButton = QToolButton()
        restartButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        restartButton.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "rotate-left-solid.svg")))
        restartButton.setIconSize(QSize(65, 65))
        restartButton.setText('restart')
        restartButton.setToolTip('restart song')
        restartButton.setStyleSheet(button)
        restartButton.clicked.connect(self.on_click_restart)

        rewindTenSec = QToolButton()
        rewindTenSec.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        rewindTenSec.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "backward-solid.svg")))
        rewindTenSec.setIconSize(QSize(65, 65))
        rewindTenSec.setText('rewind 10 seconds')
        rewindTenSec.setToolTip('rewind 10 seconds')
        rewindTenSec.setStyleSheet(button)
        rewindTenSec.clicked.connect(self.on_click_rewind)

        forwardTenSec = QToolButton()
        forwardTenSec.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        forwardTenSec.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "forward-solid.svg")))
        forwardTenSec.setIconSize(QSize(65, 65))
        forwardTenSec.setText('skip 10 seconds')
        forwardTenSec.setToolTip('skip 10 seconds')
        forwardTenSec.setStyleSheet(button)
        forwardTenSec.clicked.connect(self.on_click_forward)

        spacer = QSpacerItem(1000, 5, QSizePolicy.Expanding)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(rewindTenSec)
        hbox.addWidget(restartButton)
        hbox.addWidget(pauseButton)
        hbox.addWidget(playButton)
        hbox.addWidget(forwardTenSec)

        ############################################################
        # add song display here
        ############################################################
        song_hbox = QHBoxLayout()
        song_hbox.setAlignment(Qt.AlignCenter)
        song_hbox.addWidget(self.songWidget)

        top = QHBoxLayout()
        top.addWidget(self.nav_home)
        top.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Expanding))
        top.addWidget(self.configure)

        vbox = QVBoxLayout(self)
        vbox.addLayout(top)
        vbox.addLayout(song_hbox)

        vbox.addWidget(VisualizationWidget(parent=self))
        vbox.addLayout(hbox)

        self.initUI()

    def initUI(self):
        # self.showFullScreen()
        self.showMaximized()

    def on_click_quit(self):
        print('quit pushed')

    def on_click_pause(self):
        self.comm_system.send(Message(MessageType.STATE_UPDATE,PlayingState.PAUSE))
        self.songWidget.stopTimer()

    def on_click_play(self):
        self.comm_system.send(Message(MessageType.STATE_UPDATE,PlayingState.PLAY))
        self.songWidget.setDuration(self.song_duration)
        self.songWidget.startTimer()

    def on_click_restart(self):
        print('restart pushed')
        self.songWidget.resetTimer()

    def on_click_rewind(self):
        pass

    def on_click_forward(self):
        pass

    def set_song(self, song):
        print("setting song: " + song)
        self.title = song
        ##self.nav_home.setText("SONG: " + song)
        self.setWindowTitle("Player Piano: " + song)
        #self.songWidget.setDuration(self.song_duration)

    def set_song_duration(self, message : Message):
        """ Set the song duration once the page has been loaded
        """
        self.song_duration = round(message.data) + 1
