import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget, \
    QStackedLayout

from src.user_interface.home_page import HomePage
from src.user_interface.playing_page import PlayingPage
from src.user_interface.settings import SettingsPage



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

        self.home_page = HomePage()
        self.home_page.nav_play.clicked.connect(self.go_to_play_page)
        self.home_page.nav_settings.clicked.connect(self.go_to_settings_page)
        self.home_page.lambda_thing = lambda song: self.update_playing_page_song(song)

        self.play_page = PlayingPage()
        self.play_page.nav_home.clicked.connect(self.go_to_home_page)

        self.settings_page = SettingsPage()
        self.settings_page.nav_home.clicked.connect(self.go_to_home_page)

        # self.stackedWidget = QStackedWidget(self)
        self.stackLayout = QStackedLayout(self)
        self.stackLayout.addWidget(self.home_page)
        self.stackLayout.addWidget(self.play_page)
        self.stackLayout.addWidget(self.settings_page)

        self.showMaximized()

    def go_to_home_page(self):
        self.stackLayout.setCurrentIndex(0)

    def go_to_play_page(self):
        self.stackLayout.setCurrentIndex(1)

    def go_to_settings_page(self):
        self.stackLayout.setCurrentIndex(2)

    def update_playing_page_song(self, song_name):
        self.play_page.set_song(song_name)
        print("MAIN UPDATE SONG NAME")


if __name__ == '__main__':
    app = QApplication([])
    style = """
        QWidget {
            background: #262d37;
        }
        QLabel{
            color: #fff;
        }
        QPushButton{
            color: #fff;
        }
        QPushButton:hover{
            background: #fff;
        }
    """
    app.setStyleSheet(style)
    window = MainPage()
    window.show()
    app.exec_()
