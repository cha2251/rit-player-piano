from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout, qApp
from src.communication.messages import Message, MessageType
from src.user_interface.home_page import HomePage
from src.user_interface.playing_page import PlayingPage
from src.user_interface.settings import SettingsPage
from src.user_interface.ui_comm import UICommSystem


class MainPage(QWidget, Thread):

    def __init__(self, shutdown):
        super().__init__()
        Thread.__init__(self)

        style = """
            QWidget {
                background: #2a0b40;
            }
            QLabel{
                color: #fff;
                font: 40px;
            }
            QPushButton{
                color: #fff;
                background-color: #5b2185;
                border-style: outset;
                border-width: 2px;
                border-color: #792cb0;
                max-width: 50em;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: bold 15px;
                border-radius: 10px;
            }
            QPushButton:hover{
                background: #792cb0;
            }
            QPushButton:pressed{
                border-style: inset;
            }
            QToolButton{
                color: #fff;
                background-color: #5b2185;
                border-style: outset;
                border-width: 2px;
                border-color: #792cb0;
                max-width: 25;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: bold 15px;
                border-radius: 10px;
            }
            QToolButton:hover{
                background: #792cb0;
            }
            QToolButton:pressed{
                border-style: inset;
            }
            QProgressBar{
                background-color : rgb(255,255,255);
                border : 1px;
            }
            QProgressBar::chunk{
                background: rgb(0,0,0);
            }
        """
        qApp.setStyleSheet(style)

        self.comm_system = UICommSystem()

        self.shutdown = shutdown

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
        self.home_page.pick_song_lambda = lambda song: self.update_playing_page_song(song)

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
        # self.showFullScreen()

    def go_to_home_page(self):
        self.stackLayout.setCurrentIndex(0)

    def go_to_play_page(self):
        self.stackLayout.setCurrentIndex(1)

    def go_to_settings_page(self):
        self.stackLayout.setCurrentIndex(2)

    def update_playing_page_song(self, song_name):
        self.play_page.set_song(song_name)
        self.comm_system.send(Message(MessageType.SONG_UPDATE,song_name))

    def closeEvent(self, event):
        self.shutdown()
        event.accept()


if __name__ == '__main__':
    app = QApplication([])
    style = """
        QWidget {
            background: #2a0b40;
        }
        QLabel{
            color: #fff;
            font: 40px;
        }
        QPushButton{
            color: #fff;
            background-color: #5b2185;
            border-style: outset;
            border-width: 2px;
            border-color: #792cb0;
            max-width: 50em;
            min-width: 5em;
            padding: 5px;
            font-family: "Times New Roman", Times, serif;
            font: bold 15px;
            border-radius: 10px;
        }
        QPushButton:hover{
            background: #792cb0;
        }
        QPushButton:pressed{
            border-style: inset;
        }
        QToolButton{
            color: #fff;
            background-color: #5b2185;
            border-style: outset;
            border-width: 2px;
            border-color: #792cb0;
            max-width: 25;
            min-width: 5em;
            padding: 5px;
            font-family: "Times New Roman", Times, serif;
            font: bold 15px;
            border-radius: 10px;
        }
        QToolButton:hover{
            background: #792cb0;
        }
        QToolButton:pressed{
            border-style: inset;
        }
    """
    #app.setStyleSheet(style)
    window = MainPage(5)
    window.show()
    app.exec_()
