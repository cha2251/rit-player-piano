from PyQt5.QtWidgets import QToolButton, QGridLayout
from PyQt5.QtCore import Qt, QSize

from src.user_interface.pianoKey import pianoKey


class Piano(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignTop)
        self.setSpacing(0)

        self.piano_dict = {
            "c3": [],
            "c#3": [],
            "d3": [],
            "d#3": [],
            "e3": [],
            "f3": [],
            "f#3": [],
            "g3": [],
            "g#3": [],
            "a3": [],
            "a#3": [],
            "b3": [],
            "c4": [],
            "c#4": [],
            "d4": [],
            "d#4": [],
            "e4": [],
            "f4": [],
            "f#4": [],
            "g4": [],
            "g#4": [],
            "a4": [],
            "a#4": [],
            "b4": []
        }
        white_notes = ["c3", "d3", "e3", "f3", "g3", "a3", "b3", "c4", "d4", "e4", "f4", "g4", "a4", "b4"]
        wi = 0
        black_notes = ["c#3", "d#3", "f#3", "g#3", "a#3", "c#4", "d#4", "f#4", "g#4", "a#4"]
        bi = 0
        for i in range(0, 14):
            # Solid white boxes that are part of the piano keys inbetween the black keys
            # This is here to align the icons on the white keys to the bottom of the key
            white_sup = QToolButton()
            white_sup.setFixedSize(25, 400)
            self.addWidget(white_sup, 0, i * 2 + 1)
            self.setAlignment(white_sup, Qt.AlignTop)
            white_sup.setStyleSheet("""
                color: #DDDDDD;
                background-color: #FFFFFF;
                border-style: outset;
                border-width: 1px;
                border-color: #000000;
                max-width: 50em;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: 20px;
                border-radius: 0px;
            """)

            # white keys
            white_key = pianoKey(white_notes[wi], self.piano_dict)
            wi += 1
            white_key.setAutoFillBackground(True)
            white_key.setFixedSize(50, 200)
            white_key.setAcceptDrops(True)
            self.addWidget(white_key, 0, i * 2 + 1)
            self.setAlignment(white_key, Qt.AlignBottom)
            white_key.setIconSize(QSize(60, 60))
            white_key.setStyleSheet("""
                color: #FFFFFF;
                background-color: #FFFFFF;
                border-style: outset;
                border-width: 2px;
                border-color: transparent;
                max-width: 50em;
                min-width: 5em;
                padding: 5px;
                font-family: "Times New Roman", Times, serif;
                font: 17px;
                border-radius: 10px;
            """)

            # black keys these skip in the appropriate pattern sorry its hard coded
            if i != 0 and i != 3 and i != 7 and i != 10:
                black_key = pianoKey(black_notes[bi], self.piano_dict)
                bi += 1
                black_key.setAutoFillBackground(True)
                black_key.setFixedSize(25, 200)
                black_key.acceptDrops()
                self.addWidget(black_key, 0, i * 2)
                self.setAlignment(black_key, Qt.AlignTop)
                black_key.setIconSize(QSize(60, 60))
                black_key.setStyleSheet("""
                    color: #666666;
                    background-color: #666666;
                    border-style: outset;
                    border-width: 2px;
                    border-color: #666666;
                    max-width: 50em;
                    min-width: 5em;
                    padding: 5px;
                    font-family: "Times New Roman", Times, serif;
                    font: 12px;
                    border-radius: 8px;
                """)
                # insert an invisible spacer so that the black keys are spaced right
            elif i != 0:
                space = QToolButton()
                space.setAutoFillBackground(True)
                space.setFixedSize(25, 200)
                self.addWidget(space, 0, i * 2)
                self.setAlignment(space, Qt.AlignTop)
                space.setStyleSheet("""
                    color: transparent;
                    background-color: transparent;
                    border-color: transparent;
                    border-width: 2px;
                    max-width: 50em;
                    min-width: 5em;
                    padding: 5px;
                    font-family: "Times New Roman", Times, serif;
                    font: 12px;
                    border-radius: 10px;
                """)

        # invisible spacer that pushes the keys closer together to eliminate the space between keys
        for i in range(29, 36):
            spacer = QToolButton()
            spacer.setText("T" + str(i))
            spacer.setAutoFillBackground(True)
            spacer.setFixedSize(25, 400)
            self.addWidget(spacer, 0, i)
            self.setAlignment(spacer, Qt.AlignTop)
            spacer.setStyleSheet("""
                    color: transparent;
                    background-color: transparent;
                    border-color: transparent;
                    border-width: 2px;
                    max-width: 50em;
                    min-width: 5em;
                    padding: 5px;
                    font-family: "Times New Roman", Times, serif;
                    font: 7px;
                    border-radius: 10px;
                """)

    def get_dict(self):
        return self.piano_dict
