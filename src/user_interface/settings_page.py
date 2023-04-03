import os
import sys

from PyQt5.QtGui import QIcon, QDrag
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QToolButton, QStackedLayout, QGridLayout, QComboBox
from PyQt5.QtCore import pyqtSlot, Qt, QSize, QRect, QMimeData

from src.user_interface.DragButton import DragButton
from src.user_interface.pianoKey import pianoKey
from src.user_interface.iconsList import IconsList
from src.user_interface.piano import Piano
from src.user_interface.ui_comm import UICommSystem
from src.communication.messages import Message, MessageType


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.comm_system = UICommSystem()
        self.acceptDrops()

        self.nav_home = QToolButton()
        self.nav_home.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.nav_home.setIconSize(QSize(55, 55))
        self.nav_home.setText("back")
        self.nav_home.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "navigation", "back-arrow.svg")))
        self.nav_home.setStyleSheet("""
        max-width: 3em;
        min-width: 3em;
        """)  # it seems like the min-width is the important one

        self.title = 'PLayer Piano'
        self.setWindowTitle(self.title)
        self.hand_to_play = ""

        ########################################################
        # This appears to fix the resizing issue by preventing
        # the window from getting bigger. This does not seem
        # like the optimal fix but it works ¯\_(ツ)_/¯ ~dsp9049
        self.setMaximumWidth(1920)
        ########################################################
        self.keys = []

        # button = QPushButton('PyQt5 button', self)
        # button.setIcon(QIcon(r"images\play-solid.svg"))
        # button.setIconSize(QSize(65, 65))
        # button.setToolTip('This is an example button')
        # button.clicked.connect(self.on_click)

        title = QLabel("SETTINGS")
        title.setAlignment(Qt.AlignCenter)
        # title.setAlignment(Qt.AlignTop)
        title_spacer = QSpacerItem(1000, 5, QSizePolicy.Expanding)

        hbox = QHBoxLayout()
        hbox.addWidget(self.nav_home)
        hbox.addSpacerItem(title_spacer)
        hbox.addWidget(title)
        hbox.addSpacerItem(title_spacer)
        hbox.addSpacerItem(title_spacer)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignTop)
        vbox.addLayout(hbox)
        spacer = QSpacerItem(300, 200, QSizePolicy.Expanding)
        # vbox.addSpacerItem(spacer)

        prompt = QLabel("Select which hand(s) you would like to play")
        prompt.setStyleSheet("""
            font: 35px;
        """)
        vbox.addWidget(prompt)
        self.hand_select = QComboBox()
        self.hand_select.addItems(['Right', 'Left', 'Both', 'Neither'])
        self.hand_select.setCurrentIndex(3)
        self.hand_select.activated.connect(self.on_drop_down_selected)

        vbox.addWidget(self.hand_select)

        vbox.addSpacerItem(spacer)

        configure = QLabel("Drag and drop the icons below onto the piano keys to create a custom configuration")
        configure2 = QLabel("Click a key to remove assigned mapping")
        configure.setStyleSheet("""
            font:35px;
        """)
        configure2.setStyleSheet("""
            font:35px;
        """)
        vbox.addWidget(configure)
        vbox.addWidget(configure2)
        # create draggable buttons
        tool = """
        QToolButton {
            color: transparent;
            background-color: transparent;
            border-color: transparent;
            max-width: 3em;
            min-width: 3em;
            font: 25px;
            padding: 5px;
            font-family: "Times New Roman", Times, serif;
        }
        """
        iconsList = IconsList()
        vbox.addLayout(iconsList)

        self.piano = Piano()
        vbox.addLayout(self.piano)

        # self.showFullScreen()
        self.showMaximized()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def show_song_page(self, page_num):
        pass

    def on_drop_down_selected(self, index):
        """ if you want to play the right hand the piano has to play the left.
        0:'Right', 1:'Left', 2:'Both', 3:'Neither'
        """
        self.hand_to_play = index + 1
        self.comm_system.send(Message(MessageType.SET_HAND_TO_PLAY, self.hand_to_play))

    def get_piano_dict(self):
        return self.piano.get_dict()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsPage()
    sys.exit(app.exec_())
