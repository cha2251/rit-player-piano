import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, \
    QStackedLayout

from src.user_interface.home_page import HomePage
from src.user_interface.playing_page import PlayingPage


class MainPage(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Player Piano'
        self.left = 100
        self.top = 50
        self.width = 320
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.first = HomePage()
        self.first.linkbtn.clicked.connect(self.go_to_second)

        self.second = PlayingPage()
        self.second.linkbtn.clicked.connect(self.go_to_first)

        #self.stackedWidget = QStackedWidget(self)
        self.stackLayout = QStackedLayout(self)
        self.stackLayout.addWidget(self.first)
        self.stackLayout.addWidget(self.second)

        self.showMaximized()

    def go_to_first(self):
        self.stackLayout.setCurrentIndex(0)

    def go_to_second(self):
        self.stackLayout.setCurrentIndex(1)


if __name__ == '__main__':
    app = QApplication([])
    window = MainPage()
    window.show()
    app.exec_()
