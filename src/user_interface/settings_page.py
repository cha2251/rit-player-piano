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

        iconsList = QHBoxLayout()

        arrow_down_mime = QMimeData()
        arrow_down_mime.setText("button-arrow-down.svg")
        arrow_down = DragButton(arrow_down_mime)
        arrow_down.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "button-arrow-down.svg")))
        iconsList.addWidget(arrow_down)

        arrow_up_mime = QMimeData()
        arrow_up_mime.setText("button-arrow-up.svg")
        arrow_up = DragButton(arrow_down_mime)
        arrow_up.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "button-arrow-up.svg")))
        iconsList.addWidget(arrow_up)

        arrow_right_mime = QMimeData()
        arrow_right_mime.setText("button-arrow-right.svg")
        arrow_right = DragButton(arrow_down_mime)
        arrow_right.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "button-arrow-right.svg")))
        iconsList.addWidget(arrow_right)

        arrow_left_mime = QMimeData()
        arrow_left_mime.setText("button-arrow-left.svg")
        arrow_left = DragButton(arrow_down_mime)
        arrow_left.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "button-arrow-left.svg")))
        iconsList.addWidget(arrow_left)

        vbox.addLayout(iconsList)
        # CREATE PIANO
        aaa = QGridLayout()
        aaa.setAlignment(Qt.AlignTop)
        aaa.setSpacing(0)
        for i in range(0, 14):
            # Solid white boxes that are part of the piano keys inbetween the black keys
            # This is here to better align the icons on the white keys to the bottom of the key
            s = QToolButton()
            s.setFixedSize(25, 400)
            s.setStyleSheet("""
                background: #cccccc;
                border-color: rgba(255, 255, 255, 0);
                """)
            aaa.addWidget(s, 0, i*2+1)
            aaa.setAlignment(s, Qt.AlignTop)

            # white keys
            aac = pianoKey()
            aac.setAutoFillBackground(True)
            aac.setFixedSize(25, 200)
            aac.setAcceptDrops(True)
            aac.setStyleSheet("""
                background: #cccccc;
                border-color: rgba(255, 255, 255, 0);
                    icon-size: 75px;
                    """)
            aaa.addWidget(aac, 0, i*2+1)
            aaa.setAlignment(aac, Qt.AlignBottom)


            if i != 0 and i != 3 and i != 7 and i != 10:
                aab = pianoKey()
                aab.setAutoFillBackground(True)
                aab.setFixedSize(25, 200)
                aab.acceptDrops()
                aab.setStyleSheet("""
                            background: #000000;
                            selection-color: #999999;
                            border-color: rgba(255, 255, 255, 0);
                            hover {background-color: #00ff00;}
                            """)
                aaa.addWidget(aab, 0, i*2)
                aaa.setAlignment(aab, Qt.AlignTop)
            elif i != 0:
                s = QToolButton()
                s.setFixedSize(25, 200)
                s.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0);
                border-color: rgba(255, 255, 255, 0);
                """)
                aaa.addWidget(s, 0, i*2)
                aaa.setAlignment(s, Qt.AlignTop)

        aaa.setSpacing(10)
        vbox.addLayout(aaa)

        self.initUI()

    def initUI(self):
        # self.showFullScreen()
        self.showMaximized()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def show_song_page(self, page_num):
        pass

####    def dragEnterEvent(self, e):
####        pass
####        # do nothing??
####        ##e.accept()

####    def dropEvent(self, e):
####        print("DROP EVENT1")
####        ##pos = e.pos()
####        ##widget = e.source()
####
####        # for n in range(self.blayout.count()):
####        #     # Get the widget at each index in turn.
####        #     w = self.blayout.itemAt(n).widget()
####        #     if pos.x() < w.x() + w.size().width() // 2:
####        #         # We didn't drag past this widget.
####        #         # insert to the left of it.
####        #         self.blayout.insertWidget(n-1, widget)
####        #         break
####
####        ##e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsPage()
    sys.exit(app.exec_())
