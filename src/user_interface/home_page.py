import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt
from distributed.utils import import_file


class HomePage(QWidget):

    def get_current_songs(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        
        button = QPushButton("1", self)
        button.clicked.connect(lambda: self.show_song_page(1))

        hbox.addWidget(button)
        hbox.setAlignment(Qt.AlignCenter)
        stuffs = [hbox]
        # get list of songs
        songs = ["Ode to joy", "song 2", "song 3", "song 4"]
        count = 0
        for song in songs:
            if count > 20:
                count = 0

            label = QPushButton(song)
            label.clicked.connect(lambda: self.song_on_click(song))
            vbox.addWidget(label)
            vbox.setAlignment(Qt.AlignTop)
        return vbox, hbox

    def song_on_click(self, song_name):
        print("Song name: " + song_name)

    def __init__(self):
        super().__init__()
        self.nav_play = QPushButton("Play")
        self.nav_settings = QPushButton("Settings")
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

        # quit_button = QPushButton("Exit", self)

        title = QLabel("Select a song to start playing:")
        title.setAlignment(Qt.AlignLeft)
        # title.setAlignment(Qt.AlignTop)
        title_spacer = QSpacerItem(1000, 5, QSizePolicy.Expanding)

        add_song = QPushButton("Import")
        add_song.clicked.connect(self.import_midi)

        hbox = QHBoxLayout()
        hbox.addWidget(title)
        hbox.addSpacerItem(title_spacer)
        hbox.addWidget(add_song)
        hbox.addWidget(self.nav_settings)
        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox)
        spacer = QSpacerItem(100, 200, QSizePolicy.Expanding)
        vbox.addSpacerItem(spacer)
        v, h = self.get_current_songs()
        vbox.addLayout(v)
        spacer_bot = QSpacerItem(100, 1000, QSizePolicy.Expanding)
        vbox.addSpacerItem(spacer_bot)
        vbox.addLayout(h)
        # vbox.addLayout(hbox)
        # vbox.addWidget(button)
        # vbox.setAlignment(Qt.AlignCenter)
        self.initUI()

    def initUI(self):
        # self.showFullScreen()
        self.showMaximized()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def show_song_page(self, page_num):
        pass

    def import_midi(self):
        add_song = QFileDialog()
        add_song.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomePage()
    sys.exit(app.exec_())
