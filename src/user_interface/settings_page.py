import os
import sys

from PyQt5.QtGui import QIcon, QDrag
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QToolButton, QStackedLayout, QGridLayout, QComboBox
from PyQt5.QtCore import pyqtSlot, Qt, QSize, QRect, QMimeData

from src.user_interface.DragButton import DragButton
from src.user_interface.pianoKey import pianoKey
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
        self.nav_home.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "navigation", "back-arrow.svg")))
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
        #vbox.addSpacerItem(spacer)

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
        iconsList = QHBoxLayout()

        self.arrow_up = DragButton("button-arrow-up")
        self.arrow_up.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-up.svg")))
        self.arrow_up.setStyleSheet(tool)
        self.arrow_up.setIconSize(QSize(60, 60))
        iconsList.addWidget(self.arrow_up)

        # The down arrow and left arrow have been commented out because
        # up and down cannot be pressed at the same time and left and
        # right cannot be played at the same time either so we decided
        # to remove them so the user cannot account this problem
        ## self.arrow_down = DragButton("button-arrow-down")
        ## self.arrow_down.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-down.svg")))
        ## self.arrow_down.setStyleSheet(tool)
        ## self.arrow_down.setIconSize(QSize(60, 60))
        ## iconsList.addWidget(self.arrow_down)

        ## self.arrow_left = DragButton("button-arrow-left")
        ## self.arrow_left.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-left.svg")))
        ## self.arrow_left.setStyleSheet(tool)
        ## self.arrow_left.setIconSize(QSize(60, 50))
        ## iconsList.addWidget(self.arrow_left)

        self.arrow_right = DragButton("button-arrow-right")
        self.arrow_right.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-right.svg")))
        self.arrow_right.setStyleSheet(tool)
        self.arrow_right.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.arrow_right)

        self.a = DragButton("button-A")
        self.a.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-A.svg")))
        self.a.setStyleSheet(tool)
        self.a.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.a)

        self.B = DragButton("button-B")
        self.B.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-B.svg")))
        self.B.setStyleSheet(tool)
        self.B.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.B)

        self.X = DragButton("button-X")
        self.X.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-X.svg")))
        self.X.setStyleSheet(tool)
        self.X.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.X)

        self.Y = DragButton("button-Y")
        self.Y.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-Y.svg")))
        self.Y.setStyleSheet(tool)
        self.Y.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.Y)

        self.RB = DragButton("button-RB")
        self.RB.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-RB.svg")))
        self.RB.setStyleSheet(tool)
        self.RB.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.RB)

        self.LB = DragButton("button-LB")
        self.LB.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-LB.svg")))
        self.LB.setStyleSheet(tool)
        self.LB.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.LB)

        self.RT = DragButton("button-RT")
        self.RT.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-RT.svg")))
        self.RT.setStyleSheet(tool)
        self.RT.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.RT)

        self.LT = DragButton("button-LT")
        self.LT.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-LT.svg")))
        self.LT.setStyleSheet(tool)
        self.LT.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.LT)

        self.LS = DragButton("button-LS")
        self.LS.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-LS.svg")))
        self.LS.setStyleSheet(tool)
        self.LS.setIconSize(QSize(60, 50))
        iconsList.addWidget(self.LS)

        vbox.addLayout(iconsList)

        # CREATE PIANO
        piano = QGridLayout()
        piano.setAlignment(Qt.AlignTop)
        piano.setSpacing(0)

        self.piano_dict = {
            "c3": [],
            "c#3": [],
            "d3": [],
            "d#3": [],
            "e3": [],
            "f3": [],
            "f#3": [],
            "g3": [],
            "g#3": [],
            "a3": [],
            "a#3": [],
            "b3": [],
            "c4": [],
            "c#4": [],
            "d4": [],
            "d#4": [],
            "e4": [],
            "f4": [],
            "f#4": [],
            "g4": [],
            "g#4": [],
            "a4": [],
            "a#4": [],
            "b4": []
        }
        white_notes = ["c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4"]
        wi = 0
        black_notes = ["c#3", "d#3", "f#3", "g#3", "a#3", "c#4", "d#4", "f#4", "g#4", "a#4"]
        bi = 0
        for i in range(0, 14):
            # Solid white boxes that are part of the piano keys inbetween the black keys
            # This is here to align the icons on the white keys to the bottom of the key
            white_sup = QToolButton()
            white_sup.setFixedSize(25, 400)
            piano.addWidget(white_sup, 0, i*2+1)
            piano.setAlignment(white_sup, Qt.AlignTop)
            white_sup.setStyleSheet("""
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
            white_key = pianoKey(white_notes[wi], self.piano_dict)
            wi += 1
            white_key.setAutoFillBackground(True)
            white_key.setFixedSize(50, 200)
            white_key.setAcceptDrops(True)
            piano.addWidget(white_key, 0, i*2+1)
            piano.setAlignment(white_key, Qt.AlignBottom)
            white_key.setIconSize(QSize(60, 60))
            white_key.setStyleSheet("""
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
                black_key = pianoKey(black_notes[bi], self.piano_dict)
                bi += 1
                black_key.setAutoFillBackground(True)
                black_key.setFixedSize(25, 200)
                black_key.acceptDrops()
                piano.addWidget(black_key, 0, i*2)
                piano.setAlignment(black_key, Qt.AlignTop)
                black_key.setIconSize(QSize(60, 60))
                black_key.setStyleSheet("""
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
                space = QToolButton()
                space.setAutoFillBackground(True)
                space.setFixedSize(25, 200)
                piano.addWidget(space, 0, i*2)
                piano.setAlignment(space, Qt.AlignTop)
                space.setStyleSheet("""
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

    def on_drop_down_selected(self, index):
        """ if you want to play the right hand the piano has to play the left.
        0:'Right', 1:'Left', 2:'Both', 3:'Neither'
        """
        self.hand_to_play = index + 1
        self.comm_system.send(Message(MessageType.SET_HAND_TO_PLAY, self.hand_to_play))
        
    def get_piano_dict(self):
        return self.piano_dict

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsPage()
    sys.exit(app.exec_())
