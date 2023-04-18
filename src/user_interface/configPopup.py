from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedLayout
from src.user_interface.iconsList import IconsList
from src.user_interface.piano import Piano
from PyQt5.QtCore import Qt, QRect


class ConfigPopup(QDialog):

    def __init__(self):
        super().__init__()
        stacked = QStackedLayout()
        gray = QRect()
        layout = QVBoxLayout()
        # Uncomment this later when you can gray out the background
        ##self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 500, 200)
        layout.addLayout(IconsList())
        layout.addLayout(Piano())

        # confirm / cancel buttons

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignRight)
        cancel = QPushButton("cancel")
        cancel.setStyleSheet("""
            max-width: 5em;
        """)
        cancel.clicked.connect(self.close)
        confirm = QPushButton("Confirm")
        confirm.setStyleSheet("""
            max-width: 5em:
        """)
        hbox.addWidget(cancel)
        hbox.addWidget(confirm)
        layout.addLayout(hbox)
        self.setLayout(layout)
        # self.addLayout(Piano())

        self.show()

    def showEvent(self, event):
        # geom = self.frameGeometry()
        # geom.moveCenter(QtGui.QCursor.pos())
        # self.setGeometry(geom)
        ##self.paintEvent(event)
        super(ConfigPopup, self).showEvent(event)
        # self.showEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            event.accept()
        else:
            super(ConfigPopup, self).keyPressEvent(event)

    def save(self):
        pass

    def paintEvent(self, event):
        # Override the paint event to draw a semi-transparent gray box behind the dialog
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 127))
        painter.fillRect(self.rect().adjusted(50, 50, -50, -50), QColor(255, 255, 255, 255))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white)
        painter.drawRoundedRect(self.rect().adjusted(50, 50, -50, -50), 10, 10)
        super().paintEvent(event)
