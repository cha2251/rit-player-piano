import sys
import mido
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize, Qt


class SettingsPage(QWidget):


    def __init__(self):
        super().__init__()
        self.nav_home = QPushButton("Home")
        self.title = 'PLayer Piano'
        self.left = 100
        self.top = 50
        self.width = 320
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # button = QPushButton('PyQt5 button', self)
        # button.setIcon(QIcon(r"images\play-solid.svg"))
        # button.setIconSize(QSize(65, 65))
        # button.setToolTip('This is an example button')
        # button.clicked.connect(self.on_click)

        # quit_button = QPushButton("Exit", self)

        title = QLabel("SETTINGS")
        title.setAlignment(Qt.AlignLeft)
        # title.setAlignment(Qt.AlignTop)
        title_spacer = QSpacerItem(1000, 5, QSizePolicy.Expanding)

        hbox = QHBoxLayout()
        hbox.addWidget(title)
        hbox.addSpacerItem(title_spacer)
        hbox.addWidget(self.nav_home)
        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox)
        spacer = QSpacerItem(100, 200, QSizePolicy.Expanding)
        vbox.addSpacerItem(spacer)
        # v, h = self.get_current_songs()
        # vbox.addLayout(v)
        spacer_bot = QSpacerItem(100, 1000, QSizePolicy.Expanding)
        vbox.addSpacerItem(spacer_bot)
        # vbox.addLayout(h)
        # vbox.addLayout(hbox)
        # vbox.addWidget(button)
        # vbox.setAlignment(Qt.AlignCenter)
        self.initUI()

    def initUI(self):
        # self.showFullScreen()
        self.showMaximized()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def show_song_page(self, page_num):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsPage()
    sys.exit(app.exec_())
