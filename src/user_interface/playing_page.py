import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QLabel, QToolButton, QProgressBar
from PyQt5.QtGui import QIcon, QShowEvent
from PyQt5.QtCore import pyqtSlot, QSize, Qt
import time
from src.communication.messages import Message, MessageType, PlayingState, Song
from src.user_interface.song_progress import SongWidget
from src.user_interface.ui_comm import UICommSystem
from src.user_interface.visualization.visualization import VisualizationWidget
from src.user_interface.configPopup import ConfigPopup


class PlayingPage(QWidget):
    def __init__(self, song_name="DEFAULT"):
        button = """
        max-width: 10em;
        min-width: 3em;
        """

        super().__init__()
        self.playingFlag = False # flag for play pause toggle true means the song is playing
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
        self.configure.clicked.connect(self.on_click_configure_pop_up)

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

        self.songWidget = SongWidget()

        self.button_ack = QLabel()
        self.button_ack.setObjectName('buttonAck')
        self.button_ack.setFixedSize(300,50)
        self.button_ack.setText('PRESS PLAY')

        self.playPauseButton = QToolButton()
        self.playPauseButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.playPauseButton.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "play-solid.svg")))
        self.playPauseButton.setIconSize(QSize(65, 65))
        self.playPauseButton.setText("play")
        self.playPauseButton.setToolTip("play song")
        self.playPauseButton.setStyleSheet(button)
        self.playPauseButton.clicked.connect(self.on_click_play_pause)

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
        rewindTenSec.setText('back 10 seconds')
        rewindTenSec.setToolTip('back 10 seconds')
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
        hbox.addWidget(self.playPauseButton)
        hbox.addWidget(forwardTenSec)

        ############################################################
        # add song display here
        ############################################################
        song_hbox = QHBoxLayout()
        song_hbox.setAlignment(Qt.AlignCenter)
        song_hbox.setContentsMargins(500,0,500,0) # setContentsMargin(left, top, right, bottom)
        song_hbox.addWidget(self.nav_home)
        song_hbox.addWidget(self.songWidget)

        top = QHBoxLayout()
        top.addWidget(self.nav_home)
        top.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Expanding))
        top.addWidget(self.configure)
        btn_ack_hbox = QHBoxLayout()
        btn_ack_hbox.setAlignment(Qt.AlignCenter)
        btn_ack_hbox.addWidget(self.button_ack)

        vbox = QVBoxLayout(self)
        vbox.addLayout(top)
        # vbox.addWidget(self.nav_home)
        vbox.addLayout(song_hbox)
        vbox.addLayout(btn_ack_hbox)

        vbox.addWidget(VisualizationWidget(parent=self))
        vbox.addLayout(hbox)

        # pop-up for configuration
        ##self.config = ConfigPopup()
        ##vbox.addLayout(self.config)

        self.initUI()

    def initUI(self):
        # self.showFullScreen()
        self.showMaximized()

    def on_click_quit(self):
        print('quit pushed')

    @pyqtSlot()
    def on_click_stop(self):
        self.comm_system.send(Message(MessageType.STATE_UPDATE,PlayingState.STOP))
        self.button_ack.setText('STOPPED')

    def on_click_play_pause(self):
        if self.playingFlag: # pause state
            self.comm_system.send(Message(MessageType.STATE_UPDATE,PlayingState.PAUSE))
            self.songWidget.stopTimer()
            self.set_to_play()
        else: # play state
            self.comm_system.send(Message(MessageType.STATE_UPDATE,PlayingState.PLAY))
            self.songWidget.setDuration(self.song_duration)
            self.songWidget.startTimer()
            self.button_ack.setText('')
            self.playingFlag = True
            self.playPauseButton.setIcon(
                QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "pause-solid.svg")))
            self.playPauseButton.setText('pause')
            self.playPauseButton.setToolTip('pause song')

    # set the play pause button to play, this is for navigating to this page to make sure it is correct
    def set_to_play(self):
        self.button_ack.setText('PAUSED')
        self.playingFlag = False
        self.playPauseButton.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "play-solid.svg")))
        self.playPauseButton.setText('play')
        self.playPauseButton.setToolTip('play song')

    def on_click_restart(self):
        self.songWidget.resetTimer()
        self.comm_system.send(Message(MessageType.STATE_UPDATE,PlayingState.STOP))
        self.comm_system.send(Message(MessageType.SONG_UPDATE, Song.RESTART))

    def on_click_rewind(self):
        pass

    def on_click_forward(self):
        pass

    def on_click_configure_pop_up(self):
        self.config = ConfigPopup()
        self.config.setWindowTitle("Configure popup")
        self.config.setWindowModality(Qt.ApplicationModal)
        self.config.setFixedWidth(1700)
        self.config.move(100, 300)
        ##self.config.exec_()

    def set_song(self, song):
        print("setting song: " + song)
        self.title = song
        ##self.nav_home.setText("SONG: " + song)
        self.setWindowTitle("Player Piano: " + song)
        #self.songWidget.setDuration(self.song_duration)
        self.button_ack.setText('PRESS PLAY')

    def set_song_duration(self, message : Message):
        """ Set the song duration once the page has been loaded
        """
        self.song_duration = round(message.data) + 1
