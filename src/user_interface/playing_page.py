import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QLabel, QToolButton, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize, Qt
import time
from src.communication.messages import Message, MessageType, PlayingState

from src.user_interface.ui_comm import UICommSystem

from src.user_interface.visualization.visualization import VisualizationWidget


class PlayingPage(QWidget):
    def __init__(self, song_name="DEFAULT"):
        button = """
        max-width: 3em;
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
        self.configure.setIcon(QSize(55, 55))
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
        self.pbar_location = 0
        self.comm_system = UICommSystem()

        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 100, 200, 30)
        # self.progress.setAlignment(Qt.AlignRight)
        # self.progress.setFormat("")
        self.progress_label = QLabel(self)
        self.progress_label.setText("0:00")

        playButton = QToolButton()
        playButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        playButton.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "play-solid.svg")))
        playButton.setIconSize(QSize(65, 65))
        playButton.setText("play")
        playButton.setToolTip("play song")
        playButton.setStyleSheet(button)
        ###playButton.clicked.connect(self.on_click_play)

        pauseButton = QToolButton()
        pauseButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        pauseButton.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "pause-solid.svg")))
        pauseButton.setIconSize(QSize(65, 65))
        pauseButton.setText('pause')
        pauseButton.setToolTip('pause song')
        pauseButton.setStyleSheet(button)
        ###pauseButton.clicked.connect(self.on_click_pause)

        restartButton = QToolButton()
        restartButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        restartButton.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "playing", "rotate-left-solid.svg")))
        restartButton.setIconSize(QSize(65, 65))
        restartButton.setText('restart')
        restartButton.setToolTip('restart song')
        restartButton.setStyleSheet(button)
        ###restartButton.clicked.connect(self.on_click_restart)

        spacer = QSpacerItem(1000, 5, QSizePolicy.Expanding)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addWidget(restartButton)
        ##hbox.addWidget(stopButton)
        hbox.addWidget(pauseButton)
        hbox.addWidget(playButton)

        ############################################################
        # add song display here
        ############################################################
        song_hbox = QHBoxLayout()
        song_hbox.setAlignment(Qt.AlignCenter)
        song_hbox.setContentsMargins(500, 0, 500, 0)  # setContentsMargin(left, top, right, bottom)
        song_hbox.addWidget(self.progress)
        song_hbox.addWidget(self.progress_label)

        ##top = QHBoxLayout()
        ##top.addWidget(self.nav_home)
        ##top.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Expanding))
        ##top.addWidget(self.configure)

        vbox = QVBoxLayout(self)
        ##vbox.addLayout(top)
        vbox.addLayout(song_hbox)

        ############################################################
        ## vbox.addWidget()  ## ADD PROGRESS BAR WIDGET HERE to vbox
        ############################################################

        # vbox.addWidget(VisualizationWidget(parent=self, output=output)) # TODO CHA-PROC Readd
        vbox.addLayout(hbox)

        self.initUI()

    def initUI(self):
        # self.showFullScreen()
        self.showMaximized()

    @pyqtSlot()
    def on_click_quit(self):
        print('quit pushed')

    @pyqtSlot()
    def on_click_pause(self):
        self.comm_system.send(Message(MessageType.STATE_UPDATE, PlayingState.PAUSE))

    @pyqtSlot()
    def on_click_play(self):
        self.comm_system.send(Message(MessageType.STATE_UPDATE, PlayingState.PLAY))
        self.progress_action()

    @pyqtSlot()
    def on_click_restart(self):
        print('restart pushed')

    def set_song(self, song):
        print("setting song: " + song)
        self.title = song
        ##self.nav_home.setText("SONG: " + song)
        self.setWindowTitle("Player Piano: " + song)

    def progress_action(self):
        # for i in range(101):
        #     time.sleep(0.05)
        #     self.progress.setValue(i)
              # self.progress.setFormat(f'0:{i}')
        message_delta_time = 1
        self.progress_label.setText(f'0:{message_delta_time}')

    def update_song_progress(self):
        """
        This function will be called whenever the next message
        comes in and will update the song progress bar.
        """
        self.progress.setValue(self.pbar_location)
