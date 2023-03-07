import os
import sys

from PyQt5.QtGui import QIcon, QDrag
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QToolButton, QStackedLayout, QGridLayout, QComboBox
from PyQt5.QtCore import pyqtSlot, Qt, QSize, QRect, QMimeData

from src.user_interface.DragButton import DragButton
from src.user_interface.pianoKey import pianoKey


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.acceptDrops()

        self.nav_home = QToolButton()
        self.nav_home.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.nav_home.setIconSize(QSize(55, 55))
        self.nav_home.setText("back")
        self.nav_home.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "navigation", "back-arrow.svg")))
        self.nav_home.setStyleSheet("""
        max-width: 3em;
        min-width: 3em;
        """)  # it seems like the min-width is the important one

        self.title = 'PLayer Piano'
        self.setWindowTitle(self.title)

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
        #vbox.addSpacerItem(spacer)

        prompt = QLabel("Select which hand(s) you would like to play")
        prompt.setStyleSheet("""
            font: 35px;
        """)
        vbox.addWidget(prompt)
        hand_select = QComboBox()
        hand_select.addItems(['Right', 'Left', 'Both', 'Neither'])
        hand_select.setCurrentIndex(2)
        vbox.addWidget(hand_select)

        vbox.addSpacerItem(spacer)

        configure = QLabel("Drag and drop the icons below onto the piano keys to create a custom configuration")
        configure.setStyleSheet("""
            font:35px;
        """)
        vbox.addWidget(configure)
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
        iconsList = QHBoxLayout()

        self.arrow_up = DragButton("settings/button-arrow-up.svg")
        self.arrow_up.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-up.svg")))
        self.arrow_up.setStyleSheet(tool)
        self.arrow_up.setIconSize(QSize(60, 60))
        iconsList.addWidget(self.arrow_up)

        self.arrow_down = DragButton("settings/button-arrow-down.svg")
        self.arrow_down.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-down.svg")))
        self.arrow_down.setStyleSheet(tool)
        self.arrow_down.setIconSize(QSize(60, 60))
        iconsList.addWidget(self.arrow_down)

        self.arrow_left = DragButton("settings/button-arrow-left.svg")
        self.arrow_left.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-left.svg")))
        self.arrow_left.setStyleSheet(tool)
        self.arrow_left.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.arrow_left)

        self.arrow_right = DragButton("settings/button-arrow-right.svg")
        self.arrow_right.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-right.svg")))
        self.arrow_right.setStyleSheet(tool)
        self.arrow_right.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.arrow_right)

        self.a = DragButton("settings/button-A.svg")
        self.a.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-A.svg")))
        self.a.setStyleSheet(tool)
        self.a.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.a)

        self.B = DragButton("settings/button-B.svg")
        self.B.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-B.svg")))
        self.B.setStyleSheet(tool)
        self.B.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.B)

        self.X = DragButton("settings/button-X.svg")
        self.X.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-X.svg")))
        self.X.setStyleSheet(tool)
        self.X.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.X)

        self.Y = DragButton("settings/button-Y.svg")
        self.Y.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-Y.svg")))
        self.Y.setStyleSheet(tool)
        self.Y.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.Y)

        self.RT = DragButton("settings/button-RT.svg")
        self.RT.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-RT.svg")))
        self.RT.setStyleSheet(tool)
        self.RT.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.RT)

        self.LT = DragButton("settings/button-LT.svg")
        self.LT.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-LT.svg")))
        self.LT.setStyleSheet(tool)
        self.LT.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.LT)

        vbox.addLayout(iconsList)

        # CREATE PIANO
        piano = QGridLayout()
        piano.setAlignment(Qt.AlignTop)
        piano.setSpacing(0)
        for i in range(0, 14):
            # Solid white boxes that are part of the piano keys inbetween the black keys
            # This is here to align the icons on the white keys to the bottom of the key
            s = QToolButton()
            s.setFixedSize(25, 400)
            piano.addWidget(s, 0, i*2+1)
            piano.setAlignment(s, Qt.AlignTop)
            s.setStyleSheet("""
                color: #DDDDDD;
                background-color: #FFFFFF;
                border-style: outset;
                border-width: 1px;
                border-color: #000000;
                max-width: 50em;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: 20px;
                border-radius: 0px;
            """)

            # white keys
            aac = pianoKey()
            aac.setAutoFillBackground(True)
            aac.setFixedSize(50, 200)
            aac.setAcceptDrops(True)
            piano.addWidget(aac, 0, i*2+1)
            piano.setAlignment(aac, Qt.AlignBottom)
            aac.setIconSize(QSize(60, 60))
            aac.setStyleSheet("""
                color: #FFFFFF;
                background-color: #FFFFFF;
                border-style: outset;
                border-width: 2px;
                border-color: transparent;
                max-width: 50em;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: 17px;
                border-radius: 10px;
            """)

            # black keys these skip in the appropriate pattern sorry its hard coded
            if i != 0 and i != 3 and i != 7 and i != 10:
                aab = pianoKey()
                aab.setAutoFillBackground(True)
                aab.setFixedSize(25, 200)
                aab.acceptDrops()
                piano.addWidget(aab, 0, i*2)
                piano.setAlignment(aab, Qt.AlignTop)
                aab.setIconSize(QSize(60, 60))
                aab.setStyleSheet("""
                    color: #666666;
                    background-color: #666666;
                    border-style: outset;
                    border-width: 2px;
                    border-color: #666666;
                    max-width: 50em;
                    min-width: 5em;
                    padding: 5px;
                    font-family: "Times New Roman", Times, serif;
                    font: 12px;
                    border-radius: 8px;
                """)
                # insert an invisible spacer so that the black keys are spaced right
            elif i != 0:
                s = QToolButton()
                s.setAutoFillBackground(True)
                s.setFixedSize(25, 200)
                piano.addWidget(s, 0, i*2)
                piano.setAlignment(s, Qt.AlignTop)
                s.setStyleSheet("""
                    color: transparent;
                    background-color: transparent;
                    border-color: transparent;
                    border-width: 2px;
                    max-width: 50em;
                    min-width: 5em;
                    padding: 5px;
                    font-family: "Times New Roman", Times, serif;
                    font: 12px;
                    border-radius: 10px;
                """)

        # invisible spacer that pushes the keys closer together to eliminate the space between keys
        for i in range(29, 36):
            spacer = QToolButton()
            spacer.setText("T" + str(i))
            spacer.setAutoFillBackground(True)
            spacer.setFixedSize(25, 400)
            piano.addWidget(spacer, 0, i)
            piano.setAlignment(spacer, Qt.AlignTop)
            spacer.setStyleSheet("""
                    color: transparent;
                    background-color: transparent;
                    border-color: transparent;
                    border-width: 2px;
                    max-width: 50em;
                    min-width: 5em;
                    padding: 5px;
                    font-family: "Times New Roman", Times, serif;
                    font: 7px;
                    border-radius: 10px;
                """)

        #piano_spacer = QHBoxLayout()
        #piano_spacer.addLayout(piano)

        vbox.addLayout(piano)
        ##vbox.addSpacerItem(spacer)  # THIS DOESN'T WORK??????

        #self.showFullScreen()
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
