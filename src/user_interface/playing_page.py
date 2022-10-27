import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize


class PlayingPage(QWidget):
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

        playButton = QPushButton('', self)
        playButton.setIcon(QIcon(r"images\play-solid.svg"))
        playButton.setIconSize(QSize(65, 65))
        playButton.setToolTip('play song')
        playButton.clicked.connect(self.on_click_play)

        stopButton = QPushButton('', self)
        stopButton.setIcon(QIcon(r"images\stop-solid.svg"))
        stopButton.setIconSize(QSize(65, 65))
        stopButton.setToolTip('stop song')
        stopButton.clicked.connect(self.on_click_stop)

        pauseButton = QPushButton('', self)
        pauseButton.setIcon(QIcon(r"images\pause-solid.svg"))
        pauseButton.setIconSize(QSize(65, 65))
        pauseButton.setToolTip('pause song')
        pauseButton.clicked.connect(self.on_click_pause)

        restartButton = QPushButton('', self)
        restartButton.setIcon(QIcon(r"images\rotate-left-solid.svg"))
        restartButton.setIconSize(QSize(65, 65))
        restartButton.setToolTip('restart song')
        restartButton.clicked.connect(self.on_click_restart)

        quit_button = QPushButton("Exit", self)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Hello"))
        hbox.addWidget(quit_button)
        hbox.addWidget(restartButton)
        hbox.addWidget(stopButton)
        hbox.addWidget(pauseButton)
        hbox.addWidget(playButton)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.linkbtn)
        vbox.addLayout(hbox)
        # vbox.addWidget(playButton)
        self.initUI()

    def initUI(self):
        # self.showFullScreen()
        self.showMaximized()

    @pyqtSlot()
    def on_click_quit(self):
        print('quit')

    @pyqtSlot()
    def on_click_stop(self):
        print('stop')

    @pyqtSlot()
    def on_click_pause(self):
        print('pause')

    @pyqtSlot()
    def on_click_play(self):
        print('play')

    @pyqtSlot()
    def on_click_restart(self):
        print('restart')


#    def setupUiOld(self, MainWindow):
#        MainWindow.setObjectName("MainWindow")
#        MainWindow.resize(1117, 899)
#        self.centralwidget = QtWidgets.QWidget(MainWindow)
#        self.centralwidget.setObjectName("centralwidget")
#        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
#        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 1121, 861))
#        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
#        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
#        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
#        self.verticalLayout.setObjectName("verticalLayout")
#        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
#        self.label_2.setObjectName("label_2")
#        self.verticalLayout.addWidget(self.label_2)
#        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
#        self.label.setObjectName("label")
#        self.verticalLayout.addWidget(self.label)
#        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
#        self.verticalLayout.addItem(spacerItem)
#        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
#        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#        self.stop = QtWidgets.QGraphicsView(self.verticalLayoutWidget)
#        self.stop.setMaximumSize(QtCore.QSize(200, 200))
#        self.stop.setObjectName("stop")
#        self.horizontalLayout_2.addWidget(self.stop)
#        self.PlayPauseButton = QtWidgets.QGraphicsView(self.verticalLayoutWidget)
#        self.PlayPauseButton.setMaximumSize(QtCore.QSize(200, 200))
#        self.PlayPauseButton.setObjectName("PlayPauseButton")
#        self.horizontalLayout_2.addWidget(self.PlayPauseButton)
#        self.restart = QtWidgets.QGraphicsView(self.verticalLayoutWidget)
#        self.restart.setMaximumSize(QtCore.QSize(200, 200))
#        self.restart.setObjectName("restart")
#        self.horizontalLayout_2.addWidget(self.restart)
#        self.verticalLayout.addLayout(self.horizontalLayout_2)
#        MainWindow.setCentralWidget(self.centralwidget)
#        self.menubar = QtWidgets.QMenuBar(MainWindow)
#        self.menubar.setGeometry(QtCore.QRect(0, 0, 1117, 26))
#        self.menubar.setObjectName("menubar")
#        MainWindow.setMenuBar(self.menubar)
#        self.statusbar = QtWidgets.QStatusBar(MainWindow)
#        self.statusbar.setObjectName("statusbar")
#        MainWindow.setStatusBar(self.statusbar)
#
#        self.retranslateUi(MainWindow)
#        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#    def retranslateUiold(self, MainWindow):
#        _translate = QtCore.QCoreApplication.translate
#        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#        self.label_2.setText(_translate("MainWindow", "TITLE of SONG"))
#        self.label.setText(_translate("MainWindow", "TextLabel"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlayingPage()
    sys.exit(app.exec_())
