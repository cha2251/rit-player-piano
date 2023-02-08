import sys
from src.mixing.mixing import Mixing
# from PyQt5.QtWidgets import QApplication, QWidget,  QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
#     QSizePolicy
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QLabel, QToolButton, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize, Qt
import time


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
        self.pbar_location = 0;

        playButton = QPushButton('', self)
        playButton.setIcon(QIcon(r"UI_Images/play-solid.svg"))
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 100, 200, 30)
        #self.progress.setAlignment(Qt.AlignRight)
        #self.progress.setFormat("")
        self.progress_label = QLabel(self)
        self.progress_label.setText("0:00")
        

        playButton = QToolButton()
        playButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        playButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "play-solid.svg")))
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

        ############################################################
        # add song display here
        ############################################################
        song_hbox = QHBoxLayout()
        song_hbox.setAlignment(Qt.AlignCenter)
        song_hbox.setContentsMargins(500,0,500,0) # setContentsMargin(left, top, right, bottom)
        song_hbox.addWidget(self.progress)
        song_hbox.addWidget(self.progress_label)


        vbox = QVBoxLayout(self)
        vbox.addWidget(self.nav_home)
        vbox.addLayout(song_hbox)
        
        ############################################################
        ## vbox.addWidget()  ## ADD VISUALIZER WIDGET HERE to vbox
        ## vbox.addWidget()  ## ADD PROGRESS BAR WIDGET HERE to vbox
        ############################################################
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
        self.mixing_system.stop_pushed()

    @pyqtSlot()
    def on_click_pause(self):
        self.mixing_system.pause_pushed()

    @pyqtSlot()
    def on_click_play(self):
        self.mixing_system.play_pushed()
        print('play')
        self.progress_action()

    @pyqtSlot()
    def on_click_restart(self):
        print('restart pushed')

    def set_song(self, song):
        print("setting song: " + song)
        self.title = song
        self.nav_home.setText("SONG: " + song)
        self.setWindowTitle("Player Piano: " + song)

    def progress_action(self):
        # for i in range(101):
        #     time.sleep(0.05)
        #     self.progress.setValue(i)
            #self.progress.setFormat(f'0:{i}')
        message_delta_time = 1
        self.progress_label.setText(f'0:{message_delta_time}')
            
    def update_song_progress(self):
        """
        This function will be called whenever the next message
        comes in and will update the song progress bar.
        """
        self.progress.setValue(self.pbar_location)

        

            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlayingPage()
    sys.exit(app.exec_())
