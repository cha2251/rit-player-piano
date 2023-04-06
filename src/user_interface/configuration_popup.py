from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QDialog


class configuration_popup(QDialog):
    def __init__(self):
        super().__init__()
        self.label = QLabel('Enter your name:')
        self.textbox = QLineEdit()
        self.button_ok = QPushButton('OK')
        self.button_cancel = QPushButton('Cancel')

        # Add the widgets to a layout
        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.textbox, 0, 1)
        layout.addWidget(self.button_ok, 1, 0)
        layout.addWidget(self.button_cancel, 1, 1)
        self.setLayout(layout)

        # Set the size and title of the window
        self.setWindowTitle('Popup Window')
        self.resize(250, 100)

        # Connect the signals to the slots
        self.button_ok.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)
