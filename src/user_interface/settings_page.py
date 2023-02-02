import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QToolButton
from PyQt5.QtCore import pyqtSlot, Qt, QSize


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()
        self.nav_home = QToolButton()
        self.nav_home.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.nav_home.setIconSize(QSize(55, 55))
        self.nav_home.setText("back")
        self.nav_home.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "back-arrow.svg")))



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

        ##### drop1 = Draggable("first", "second") # don't do this it wont work??
        drop1 = ""
        drop1 = QLabel("STUFF")
        drop1.setAcceptDrops(True)

        title = QLabel("SETTINGS")
        title.setAlignment(Qt.AlignLeft)
        # title.setAlignment(Qt.AlignTop)
        title_spacer = QSpacerItem(1000, 5, QSizePolicy.Expanding)

        hbox = QHBoxLayout()
        hbox.addWidget(self.nav_home)
        hbox.addSpacerItem(title_spacer)
        hbox.addWidget(title)
        hbox.addSpacerItem(title_spacer)
        hbox.addWidget(drop1)
        hbox.addSpacerItem(title_spacer)


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
