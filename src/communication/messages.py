from enum import Enum

class MessageType(Enum):
    ERROR = 1
    OUTPUT_QUEUE_UPDATE = 2
    STATE_UPDATE = 3
    MODE_UPDATE = 4
    BUTTON_CONFIG_UPDATE = 5
    SONG_UPDATE = 6
    SYSTEM_STOP = 7
    SET_HAND_TO_PLAY = 8
    SET_DURATION = 9

class PianoAssistPlaying(Enum):
    LEFT = 1
    RIGHT = 2
    NEITHER = 3
    BOTH = 4

class PlayingState(Enum):
    PLAY = 1
    PAUSE = 2
    STOP = 3

class Message():
    def __init__(self, type, data = None):
        self.type = type
        self.data = data