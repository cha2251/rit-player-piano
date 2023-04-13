import json
import os

from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap, QIcon
from PyQt5.QtWidgets import QToolButton
from src.button_input.controller import ControllerButton
from src.communication.messages import Message, MessageType
from src.user_interface.ui_comm import UICommSystem

# mapping of the string names of the buttons to the enum values
CONTROLLER_BUTTON_MAP = {
    '': ControllerButton.LeftJoystickY,
    '': ControllerButton.LeftJoystickX,
    '': ControllerButton.RightJoystickY,
    '': ControllerButton.RightJoystickX,
    'button-LT': ControllerButton.LeftTrigger,
    'button-RT': ControllerButton.RightTrigger,
    'button-LB': ControllerButton.LeftBumper,
    'button-RB': ControllerButton.RightBumper,
    'button-A': ControllerButton.A,
    'button-B': ControllerButton.B,
    'button-Y': ControllerButton.Y,
    'button-X': ControllerButton.X,
    'button-LS': ControllerButton.LeftThumb,
    'button-RS': ControllerButton.RightThumb,
    'button-select': ControllerButton.Back,
    'button-start': ControllerButton.Start,
    'button-arrow-left': ControllerButton.LeftDPad,
    'button-arrow-right': ControllerButton.RightDPad,
    'button-arrow-up': ControllerButton.UpDPad,
    'button-arrow-down': ControllerButton.DownDPad
}

class pianoKey(QToolButton):

    def __init__(self, key, piano_dict):
        super().__init__()
        self.setAcceptDrops(True)
        self.key = key
        self.piano_dict = piano_dict
        self.comm_system = UICommSystem()
        self.clicked.connect(self.onClick)

        if self.piano_dict[self.key]:
            file = None
            for name in CONTROLLER_BUTTON_MAP:
                if CONTROLLER_BUTTON_MAP[name] == self.piano_dict[self.key][0]:
                    file = name
                    break

            self.setIconHelper(file)

    def dragEnterEvent(self, e):
        try:
            e.accept()
        except:
            print("exception in dragEnterEvent")

    def dropEvent(self, e):
        try:
            file = e.mimeData().text()
            self.setIconHelper(file)
            self.piano_dict[self.key].append(CONTROLLER_BUTTON_MAP[file])
            self.comm_system.send(Message(MessageType.BUTTON_CONFIG_UPDATE, self.piano_dict))
            self.save_button_mappings()
        except Exception as e:
            print("exception occurred in drop event: " + str(e))

    def onClick(self):
        self.setIconHelper(None)
        self.piano_dict[self.key] = []
        self.comm_system.send(Message(MessageType.BUTTON_CONFIG_UPDATE, self.piano_dict))
        self.save_button_mappings()

    def setIconHelper(self, file):
        if file is None:
            self.setIcon(QIcon())
            return

        filepath = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "UI_Images",
            "settings",
            file + ".svg"
        )
        self.setIcon(QIcon(filepath))

    def save_button_mappings(self):
        filepath = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "buttons.json"
        )

        with open(filepath, "w") as f:
            json.dump(self.piano_dict, f)