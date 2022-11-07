import sys
import mido
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize, Qt




class HomePage(QWidget):
    # Test fucntions for setting up unit test infra. TODO: Remove in sprint 2.
    def is_even(self, number):
        if number % 2 == 0:
            return True
        return False

    # Test fucntions for setting up unit test infra. TODO: Remove in sprint 2.
    def in_range(self, number):
        lower = 3
        upper = 8
        if lower < number < upper:
            return True
        return False

    def get_current_songs(self):
        vbox = QVBoxLayout()
        # get list of songs
        songs = ["Ode to joy", "song 2", "song 3", "song 4"]
        for song in songs:
            label = QPushButton(song)
            label.clicked.connect(lambda: self.song_on_click(song))
            vbox.addWidget(label)

        return vbox

    def song_on_click(self, song_name):
        print("Song name: " + song_name)

    def __init__(self):
        super().__init__()
        self.linkbtn = QPushButton("LINK")
        self.title = 'PLayer Piano'
        self.left = 100
        self.top = 50
        self.width = 320
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('PyQt5 button', self)
        button.setIcon(QIcon(r"images\play-solid.svg"))
        button.setIconSize(QSize(65, 65))
        button.setToolTip('This is an example button')
        button.clicked.connect(self.on_click)

        quit_button = QPushButton("Exit", self)

        title = QLabel("Hello")
        title.setAlignment(Qt.AlignCenter)
        # title.setAlignment(Qt.AlignTop)

        hbox = QHBoxLayout()
        hbox.addWidget(self.linkbtn)
        hbox.addWidget(quit_button)
        vbox = QVBoxLayout(self)
        vbox.addWidget(title)
        vbox.addLayout(self.get_current_songs())
        vbox.addLayout(hbox)
        vbox.addWidget(button)
        # vbox.setAlignment(Qt.AlignCenter)
        self.initUI()

    def initUI(self):
        # self.showFullScreen()
        self.showMaximized()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomePage()
    sys.exit(app.exec_())
