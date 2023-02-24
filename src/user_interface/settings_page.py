import os
import sys

from PyQt5.QtGui import QIcon, QDrag
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QToolButton, QStackedLayout, QGridLayout
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
        vbox.addSpacerItem(spacer)

        push = """
            QPushButton{
                color: #fff;
                background-color: #5b2185;
                border-style: outset;
                border-width: 2px;
                border-color: #792cb0;
                max-width: 10em;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: 15px;
                border-radius: 10px;
            }
            QPushButton:hover{
                background: #792cb0;
            }
            QPushButton:pressed{
                border-style: inset;
            }
            """

        tool = """
         QToolButton{
                color: #fff;
                background-color: #5b2185;
                border-style: outset;
                border-width: 2px;
                border-color: #792cb0;
                max-width: 10em;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: 15px;
                border-radius: 10px;
            }
            QToolButton:hover{
                background: #792cb0;
            }
            QToolButton:pressed{
                border-style: inset;
            }
        """

        iconsList = QHBoxLayout()

        self.arrow_down = DragButton("button-arrow-down.svg")
        self.arrow_down.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "button-arrow-down.svg")))
        self.arrow_down.setStyleSheet(tool)
        iconsList.addWidget(self.arrow_down)

        self.arrow_up = DragButton("button-arrow-up.svg")
        self.arrow_up.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "button-arrow-up.svg")))
        self.arrow_up.setStyleSheet(tool)
        iconsList.addWidget(self.arrow_up)

        self.arrow_right = DragButton("button-arrow-right.svg")
        self.arrow_right.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "button-arrow-right.svg")))
        self.arrow_right.setStyleSheet(tool)
        iconsList.addWidget(self.arrow_right)

        self.arrow_left = DragButton("button-arrow-left.svg")
        self.arrow_left.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "button-arrow-left.svg")))
        self.arrow_left.setStyleSheet(tool)
        iconsList.addWidget(self.arrow_left)

        vbox.addLayout(iconsList)
        # CREATE PIANO
        aaa = QGridLayout()
        aaa.setAlignment(Qt.AlignTop)
        aaa.setSpacing(0)
        for i in range(0, 14):
            # Solid white boxes that are part of the piano keys inbetween the black keys
            # This is here to align the icons on the white keys to the bottom of the key
            s = QToolButton()
            s.setFixedSize(25, 400)
            aaa.addWidget(s, 0, i*2+1)
            aaa.setAlignment(s, Qt.AlignTop)
            s.setStyleSheet("""
                color: #00FF00;
                background-color: #00FF00;
                border-style: outset;
                border-width: 2px;
                border-color: #00FF99;
                max-width: 50em;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: 20px;
                border-radius: 20px;
            """)

            # white keys
            aac = pianoKey()
            aac.setAutoFillBackground(True)
            aac.setFixedSize(50, 200)
            aac.setAcceptDrops(True)
            aaa.addWidget(aac, 0, i*2+1)
            aaa.setAlignment(aac, Qt.AlignBottom)
            aac.setIconSize(QSize(60, 60))
            aac.setStyleSheet("""
                color: #0000ff;
                background-color: #0000ff;
                border-style: outset;
                border-width: 2px;
                border-color: #0099ff;
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
                aaa.addWidget(aab, 0, i*2)
                aaa.setAlignment(aab, Qt.AlignTop)
                aab.setIconSize(QSize(60, 60))
                aab.setStyleSheet("""
                    color: #444444;
                    background-color: #441144;
                    border-style: outset;
                    border-width: 2px;
                    border-color: #444411;
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
                aaa.addWidget(s, 0, i*2)
                aaa.setAlignment(s, Qt.AlignTop)
                s.setStyleSheet("""
                    color: transparent;
                    background-color: transparent;
                    border-color: #aaaaaa;
                    border-width: 2px;
                    max-width: 50em;
                    min-width: 5em;
                    padding: 5px;
                    font-family: "Times New Roman", Times, serif;
                    font: 12px;
                    border-radius: 10px;
                """)

        for i in range(29, 36):
            s = QToolButton()
            s.setText("T" + str(i))
            s.setAutoFillBackground(True)
            s.setFixedSize(25, 400)
            aaa.addWidget(s, 0, i)
            aaa.setAlignment(s, Qt.AlignTop)
            s.setStyleSheet("""
                    color: transparent;
                    background-color: transparent;
                    border-color: #FF0000;
                    border-width: 2px;
                    max-width: 50em;
                    min-width: 5em;
                    padding: 5px;
                    font-family: "Times New Roman", Times, serif;
                    font: 7px;
                    border-radius: 10px;
                """)

        piano_spacer = QHBoxLayout()
        piano_spacer.addLayout(aaa)

        vbox.addLayout(piano_spacer)

        #### gpthbox = QHBoxLayout()
        #### gptgrid = QGridLayout()
        #### for i in range(12):
        ####     button = QPushButton()
        ####     row = 0
        ####     if i % 2 == 1:
        ####         row = 0
        ####         if i in [5, 13, 19]:
        ####             button.setStyleSheet("background-color: transparent; color: transparent; border-radius: 0px;")
        ####         else:
        ####             button.setStyleSheet("background-color: black; color: white; border-radius: 0px;")
        ####         button.setFixedSize(5, 200)
        ####     else:
        ####         row = 1
        ####         button.setStyleSheet("background-color: white; color: black; border-radius: 0px;")
        ####         button.setFixedSize(5, 400)
        ####     ## gpthbox.addWidget(button)
        ####     gptgrid.addWidget(button, row, i)
        ####     ##gpthbox.setAlignment(button, Qt.AlignTop)

        #### ##gpthbox.setSpacing(10)
        #### gptgrid.setVerticalSpacing(0)
        #### vbox.addLayout(gptgrid)

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
