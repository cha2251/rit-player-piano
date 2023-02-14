from enum import Enum

class MessageType(Enum):
    ERROR = 1
    OUTPUT_QUEUE_UPDATE = 2
    STATE_UPDATE = 3
    MODE_UPDATE = 4
    BUTTON_CONFIG = 5
    SONG_CHANGE = 6

class Message():
    def __init__(self, type, data):
        self.type = type
        self.data = data