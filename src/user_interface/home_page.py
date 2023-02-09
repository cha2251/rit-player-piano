import sys
import os
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy, QFileDialog


class HomePage(QWidget):

    MIDI_FILE_PATH = "MIDI_Files" # Path to check for midi files to display. For now just checks folder in same directory

    def __init__(self):
        super().__init__()
        self.nav_play = QPushButton("Play")
        self.nav_settings = QPushButton("Settings")
        self.pick_song_lambda = None
        self.title = 'Player Piano'
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

        title = QLabel("RIT Player Piano")
        title.setAlignment(Qt.AlignCenter)
        title_spacer = QSpacerItem(400, 5, QSizePolicy.Fixed)
        outer_spacer = QSpacerItem(200, 5, QSizePolicy.Fixed)

        add_song = QPushButton("upload song")
        add_song.clicked.connect(self.import_midi)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignTop)
        hbox.addSpacerItem(outer_spacer)
        hbox.addWidget(add_song)
        hbox.addSpacerItem(title_spacer)
        hbox.addWidget(title)
        hbox.addSpacerItem(title_spacer)
        hbox.addWidget(self.nav_settings)
        hbox.addSpacerItem(outer_spacer)
        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignTop)
        vbox.addLayout(hbox)
        spacer = QSpacerItem(100, 200, QSizePolicy.Expanding)
        ## vbox.addSpacerItem(spacer)
        v = self.get_current_songs()
        vbox.addLayout(v)
        ## spacer_bot = QSpacerItem(100, 200, QSizePolicy.Expanding)
        ## vbox.addSpacerItem(spacer_bot)
        ## vbox.addLayout(h)
        # vbox.addLayout(hbox)
        # vbox.addWidget(button)
        # vbox.setAlignment(Qt.AlignCenter)
        self.initUI()

    def initUI(self):
        self.showFullScreen()
        # self.showMaximized()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def get_current_songs(self):
        bigHbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        ##vbox.setAlignment(Qt.AlignRight)
        vbox.addSpacerItem(QSpacerItem(100, 100, QSizePolicy.Expanding))
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addStretch()

        button = QPushButton("1", self)
        button.clicked.connect(lambda: self.show_song_page(1))

        hbox.addWidget(button)
        stuffs = [hbox]


        # get list of songs
        songs = self.get_songs_from_directory()
        count = 0
        for song in songs:
            if count > 20:
                count = 0
            label = QPushButton(song)
            label.clicked.connect(lambda state, x=song: self.song_on_click(x))
            vbox.addWidget(label)
        vbox.addSpacerItem(QSpacerItem(100, 100, QSizePolicy.Expanding))
        hbox.addStretch()
        vbox.addLayout(hbox)
        bigHbox.addStretch()
        bigHbox.addLayout(vbox)
        bigHbox.addStretch()
        return bigHbox

    def get_songs_from_directory(self):
        try:
            songs = os.listdir(self.MIDI_FILE_PATH)
            filteredSongs = []
            for song in songs: # Remove .mid extension
                filteredSongs.append(song.replace(".mid", ""))
            return filteredSongs
        except FileNotFoundError:
            print("ERROR: Could not find directory at path: "+self.MIDI_FILE_PATH)
            return []

    def song_on_click(self, song_name):
        print("Song name: " + song_name)
        # self.nav_play.set_song(song_name)
        self.pick_song_lambda(song_name)
        self.nav_play.click()

    def show_song_page(self, page_num):
        pass

    def import_midi(self):
        add_song = QFileDialog()
        add_song.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomePage()
    sys.exit(app.exec_())
