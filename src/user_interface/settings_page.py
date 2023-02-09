import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QToolButton, QStackedLayout, QGridLayout
from PyQt5.QtCore import pyqtSlot, Qt, QSize, QRect


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

        title = QLabel("SETTINGS")
        title.setAlignment(Qt.AlignCenter)
        # title.setAlignment(Qt.AlignTop)
        title_spacer = QSpacerItem(1000, 5, QSizePolicy.Expanding)

        hbox = QHBoxLayout()
        hbox.addWidget(self.nav_home)
        hbox.addSpacerItem(title_spacer)
        hbox.addWidget(title)
        hbox.addSpacerItem(title_spacer)
        #hbox.addSpacerItem(title_spacer)


        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignTop)
        vbox.addLayout(hbox)
        spacer = QSpacerItem(300, 200, QSizePolicy.Expanding)
        vbox.addSpacerItem(spacer)
        # v, h = self.get_current_songs()
        # vbox.addLayout(v)
        ##spacer_bot = QSpacerItem(100, 1000, QSizePolicy.Expanding)
        ##vbox.addSpacerItem(spacer_bot)
        # vbox.addLayout(h)
        # vbox.addLayout(hbox)
        # vbox.addWidget(button)
        # vbox.setAlignment(Qt.AlignCenter)


        ##piano = QHBoxLayout()
        ##group = QStackedLayout()
        ##bKeys = QHBoxLayout()
        ##wKeys = QHBoxLayout()
        ##for i in range(0, 3):
        ##    wKey = QToolButton()
        ##    wKey.setAutoFillBackground(True)
        ##    wKey.setFixedWidth(100)
        ##    wKey.setFixedHeight(500)
        ##    wKey.setStyleSheet("""
        ##        background: #ffffff;
        ##    """)
        ##    wKeys.addWidget(wKey)

        ##for i in range(0, 3):
        ##    bKey = QToolButton()
        ##    bKey.setAutoFillBackground(True)
        ##    bKey.setFixedWidth(100)
        ##    bKey.setFixedHeight(500)
        ##    bKey.setStyleSheet("""
        ##        background: #ffffff;
        ##    """)
        ##    bKeys.addWidget(bKey)

        ##group.addWidget(wKeys)
        ##group.addWidget(bKeys)

        ##piano.addWidget(group)

        ####  piano = QHBoxLayout()
        ####  piano.setAlignment(Qt.AlignTop)
        ####  piano.setSpacing(-50)
        ####  for i in range(0, 8):
        ####      wKey = QToolButton()
        ####      wKey.setAutoFillBackground(True)
        ####      wKey.setFixedWidth(100)
        ####      wKey.setFixedHeight(500)
        ####      wKey.move(50, 100)
        ####      wKey.setStyleSheet("""
        ####          background: #ffffff;
        ####      """)
        ####      #piano.addWidget(wKey)
        ####      if i != 2 and i != 5:
        ####          bKey = QToolButton()
        ####          bKey.setAutoFillBackground(True)
        ####          bKey.setFixedWidth(100)
        ####          bKey.setFixedHeight(250)
        ####          bKey.setStyleSheet("""
        ####              background: #000000;
        ####          """)
        ####          piano.addWidget(bKey)

        ####  wKey = QToolButton()
        ####  wKey.setAutoFillBackground(True)
        ####  wKey.setFixedWidth(100)
        ####  wKey.setFixedHeight(500)
        ####  wKey.move(50, 100)
        ####  wKey.setStyleSheet("""
        ####      background: #ffffff;
        ####  """)
        #vbox.addLayout(piano)
        aaa = QGridLayout()
        aaa.setAlignment(Qt.AlignTop)

        ######aab = QToolButton()
        ######aab.setAutoFillBackground(True)
        ######aab.setFixedWidth(100)
        ######aab.setFixedHeight(250)
        ######aab.setStyleSheet("""
        ######            background: #000000;
        ######            """)
        ######aaa.addWidget(aab,0,1)

        for i in range(0, 14):
            aac = QToolButton()
            aac.setAutoFillBackground(True)
            aac.setFixedWidth(100)
            aac.setFixedHeight(400)
            aac.setStyleSheet("""
                    background: #cccccc;
                    """)
            aaa.addWidget(aac,1,i*2+1)

            if i != 0 and i != 3 and i != 7 and i != 10:
                aab = QToolButton()
                aab.setAutoFillBackground(True)
                aab.setFixedSize(25, 200)
                aab.setStyleSheet("""
                            background: #000000;
                            selection-color: #999999;
                            hover {background-color: #00ff00;}
                            """)
                aaa.addWidget(aab, 1, i*2)
                aaa.setAlignment(aab, Qt.AlignTop)
            elif i != 0:
                s = QToolButton()
                s.setFixedSize(25, 200)
                s.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
                aaa.addWidget(s, 1, i*2)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SettingsPage()
    sys.exit(app.exec_())
