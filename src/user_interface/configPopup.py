from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout
from src.user_interface.iconsList import IconsList
from src.user_interface.piano import Piano


class ConfigPopup(QDialog):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        #uncomment this for production
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 500, 200)
        layout.addLayout(IconsList())
        layout.addLayout(Piano())
        self.setLayout(layout)
        #self.addLayout(Piano())

        self.show()

    def showEvent(self, event):
        #geom = self.frameGeometry()
        #geom.moveCenter(QtGui.QCursor.pos())
        #self.setGeometry(geom)
        super(ConfigPopup, self).showEvent(event)
        #self.showEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            event.accept()
        else:
            super(ConfigPopup, self).keyPressEvent(event)