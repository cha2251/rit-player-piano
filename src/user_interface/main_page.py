from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QStackedLayout, qApp

from src.file_input import file_input
from src.mixing import mixing
from src.communication.messages import Message, MessageType
from src.user_interface.home_page import HomePage
from src.user_interface.playing_page import PlayingPage
from src.user_interface.settings_page import SettingsPage
from src.user_interface.ui_comm import UICommSystem
from src.user_interface.loading_dialog import LoadingDialog, WorkerThread, LoadingGif


class MainPage(QWidget, Thread):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        Thread.__init__(self)
        self.comm_system = UICommSystem()
        self.comm_system.set_queues(input_queue,output_queue)
        self.comm_system.start()

        self.loading_dialog = LoadingDialog()
        self.loading_thread = WorkerThread()
        self.loading_gif = LoadingGif()
        self.loading_thread.progress_signal.connect(self.loading_dialog.update_progress)
        self.loading_thread.finished.connect(self.loading_dialog.hide)
        
        #self.loading_thread.finished.connect(self.loading_gif.hide)
        #self.loading_thread.finished.connect(self.loading_thread.deleteLater)
        #self.loading_thread.finished.connect(self.loading_dialog.deleteLater)

        page_color = 'fbfaf4'
        font_color = '006d7a'
        button_color = 'e99e63'
        button_press_color = 'c37335'
        button_border_color = 'df7b2c'

        style = """
            QWidget {
                background: #"""+page_color+""";
            }
            QLabel{
                color: #"""+font_color+""";
                font: 80px;
            }
            QPushButton{
                color: #"""+font_color+""";
                background-color: #"""+button_color+""";
                border-style: outset;
                border-width: 2px;
                border-color: #"""+button_border_color+""";
                max-width: 50em;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: bold 40px;
                border-radius: 10px;
            }
            QPushButton:hover{
                background: #"""+button_press_color+""";
            }
            QPushButton:pressed{
                border-style: inset;
            }
            QToolButton{
                color: #"""+font_color+""";
                background-color: #"""+button_color+""";
                border-style: outset;
                border-width: 2px;
                border-color: #"""+button_border_color+""";
                max-width: 25;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: bold 40px;
                border-radius: 10px;
            }
            QToolButton:hover{
                background: #"""+button_press_color+""";
            }
            QToolButton:pressed{
                border-style: inset;
            }
            QProgressBar{
                background-color: #"""+button_press_color+""";
                border: 1px;
            }
            QProgressBar::chunk{
                background: #fff;
            }
        """
        qApp.setStyleSheet(style)

        self.comm_system = UICommSystem()
        self.comm_system.start()

        self.shutdown = shutdown

        self.mixing_system = mixing
        self.file_input = file_input
        self.output = output

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
        #self.show()

    def go_to_home_page(self):
        self.loading_dialog.show()
        self.loading_thread.start()
        #self.loading_gif.start_loading(self.loading_thread)
        self.stackLayout.setCurrentIndex(0)

    def go_to_play_page(self):
        self.loading_dialog.show()
        self.loading_thread.start()
        #self.loading_gif.start_loading(self.loading_thread)
        self.stackLayout.setCurrentIndex(1)

    def go_to_settings_page(self):
        self.loading_dialog.show()
        self.loading_thread.start()
        #self.loading_gif.start_loading(self.loading_thread)
        self.stackLayout.setCurrentIndex(2)

    def update_playing_page_song(self, song_name):
        self.play_page.set_song(song_name)
        print("MAIN UPDATE SONG NAME")
        self.comm_system.send(Message(MessageType.SONG_UPDATE,song_name))

    def closeEvent(self, event):
        self.comm_system.send(Message(MessageType.SYSTEM_STOP))
        print("System Shutdown Started")
        event.accept()


##if __name__ == '__main__':
##
##    page_color = 'fbfaf4'
##    font_color = '006d7a'
##    button_color = 'e99e63'
##    button_press_color = 'c37335'
##    app = QApplication([])
##    style = """
##        QWidget {
##            background: #"""+page_color+""";
##        }
##        QLabel{
##            color: #"""+font_color+""";
##            font: 40px;
##        }
##        QPushButton{
##            color: #"""+font_color+""";
##            background-color: #"""+button_color+""";
##            border-style: outset;
##            border-width: 2px;
##            border-color: #792cb0;
##            max-width: 50px;
##            min-width: 15px;
##            padding: 5px;
##            font-family: "Times New Roman", Times, serif;
##            font: bold 15px;
##            border-radius: 10px;
##        }
##        QPushButton:hover{
##            background: #"""+button_press_color+""";
##        }
##        QPushButton:pressed{
##            border-style: inset;
##        }
##        QToolButton{
##            color: #"""+font_color+""";
##            background-color: #"""+button_color+""";
##            border-style: outset;
##            border-width: 2px;
##            border-color: #792cb0;
##            max-width: 25px;
##            min-width: 15px;
##            padding: 5px;
##            font-family: "Times New Roman", Times, serif;
##            font: bold 15px;
##            border-radius: 10px;
##        }
##        QToolButton:hover{
##            background: #"""+button_press_color+""";
##        }
##        QToolButton:pressed{
##            border-style: inset;
##        }
##    """
##    window = MainPage(5)
##    window.show()
##    app.exec_()
