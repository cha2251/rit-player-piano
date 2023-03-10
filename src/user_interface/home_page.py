import shutil
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
        self.table_buttons = QHBoxLayout()
        self.songs_dict = []
        self.songs_dict_index = 0

        # button = QPushButton('PyQt5 button', self)
        # button.setIcon(QIcon(r"images\play-solid.svg"))
        # button.setIconSize(QSize(65, 65))
        # button.setToolTip('This is an example button')
        # button.clicked.connect(self.on_click)

        # quit_button = QPushButton("Exit", self)

        title = QLabel("RIT Player Piano")
        title.setAlignment(Qt.AlignCenter)
        title_spacer = QSpacerItem(40, 5, QSizePolicy.Fixed)
        outer_spacer = QSpacerItem(20, 5, QSizePolicy.Fixed)

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
        self.song_list_vbox = QVBoxLayout(self)
        self.song_list_vbox.setAlignment(Qt.AlignTop)
        self.song_list_vbox.addLayout(hbox)
        spacer = QSpacerItem(100, 200, QSizePolicy.Expanding)
        ## vbox.addSpacerItem(spacer)
        v = self.get_current_songs()
        self.song_list_vbox.addLayout(v)
        ## spacer_bot = QSpacerItem(100, 200, QSizePolicy.Expanding)
        ## vbox.addSpacerItem(spacer_bot)
        ## vbox.addLayout(h)
        # vbox.addLayout(hbox)
        # vbox.addWidget(button)
        # vbox.setAlignment(Qt.AlignCenter)
        #self.showFullScreen()
        self.setLayout(self.song_list_vbox)
        self.showMaximized()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def get_current_songs(self):
        bigHbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.songs_dict = []
        
        vbox.addSpacerItem(QSpacerItem(100, 100, QSizePolicy.Expanding))
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addStretch()

        stuffs = [hbox]


        # get list of songs
        songs = self.get_songs_from_directory()
        num_btns = (len(songs) // 4) + 1
        print(f'# Songs: {len(songs)}, # num btns: {num_btns}')
        self.create_table_buttons(num_btns)
        hbox = self.table_buttons


        count = 0
        index = 0
        current_dict_idx = 0
        arr = []
        for song in songs:
            if count > 20:
                count = 0

            if index%4 == 0 and index > 0:
                #current_dict_idx+=1     # if there are 5 in the current row, move to the next
                self.songs_dict.append(arr)
                arr = []

            label = QPushButton(song)
            label.clicked.connect(lambda state, x=song: self.song_on_click(x))
            arr.append(label)
            

            if index > 4:
                label.hide()            # if there are more than 5, we want to hide the others until we move to that table set

            vbox.addWidget(label)
            index += 1
        self.songs_dict.append(arr)

        print(f'======Songs dict: {self.songs_dict[0]}')



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
        self.pick_song_lambda(song_name)
        self.nav_play.click()

    def show_song_page(self, page_num):
        """
        
        """
        print(f'Change table page: {page_num}, total tables: {len(self.songs_dict[page_num])}')
        self.hide_all_songs()

        self.show_songs_at(page_num)

        # if page_num == -1:
        #     # we want to display the previous 5 songs
            
        #     if self.songs_dict_index <= 0:
        #         return
        #     else:                
        #         self.songs_dict_index -= 1
        #         print(f'New index: {self.songs_dict_index}')
        #         self.show_songs_at(self.songs_dict_index)
        # elif page_num == 0:
        #     # we want to do nothing
        #     pass
        # elif page_num == 1:

        #     if self.songs_dict_index < (len(self.songs_dict)+1):
        #         self.songs_dict_index += 1
        #         self.show_songs_at(self.songs_dict_index)




    def hide_all_songs(self):
        for arr in self.songs_dict:
            for song in arr:
                song.hide()

    def show_songs_at(self, index):
        # if index >= len(self.songs_dict):
        #     return
        for song in self.songs_dict[index]:
            song.show()

    def import_midi(self):
        #add_song = QFileDialog()

        file_path, _ = QFileDialog.getOpenFileName(None, "Select File", "", "All Files (*.*)")
        if not file_path:
            return

        # Copy the selected file to the project folder
        project_folder = self.MIDI_FILE_PATH
        filename = os.path.basename(file_path)
        new_path = os.path.join(project_folder, filename)
        print(f'File path is: {new_path}')
        shutil.copy(file_path, new_path)
        self.reload_hbox()
        
        #add_song.exec()

    def reload_hbox(self):
        layout_rm = self.song_list_vbox.takeAt(1)

        while self.table_buttons.count():
            widget = self.table_buttons.takeAt(0).widget()
            self.table_buttons.removeWidget(widget)
            # widget.setParent(None)
            # widget.deleteLater()

        layout_rm.setParent(None)
        layout_rm.deleteLater()
        self.song_list_vbox.addLayout(self.get_current_songs())

    def create_table_buttons(self, num_btns):
        self.table_buttons = QHBoxLayout()
        for i in range(num_btns):
            print(f'==============Creating button {i}==============')
            btn = QPushButton(f'{i}', self)
            btn.clicked.connect(lambda _, x=i: self.show_song_page(x))
            self.table_buttons.addWidget(btn)

        # btn1 = QPushButton('<', self)
        # btn1.clicked.connect(lambda: self.show_song_page(-1))

        # self.current_table = QPushButton('1', self)
        # self.current_table.clicked.connect(lambda: self.show_song_page(0))

        # btn2 = QPushButton('>', self)
        # btn2.clicked.connect(lambda: self.show_song_page(1))

        # self.table_buttons.addWidget(btn1)
        # self.table_buttons.addWidget(self.current_table)
        # self.table_buttons.addWidget(btn2)

        





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomePage()
    sys.exit(app.exec_())
