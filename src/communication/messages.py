from enum import Enum

from src.common.midi_event import MidiEvent

class MessageType(Enum):
    ERROR = 1
    OUTPUT_QUEUE_UPDATE = 2
    STATE_UPDATE = 3
    MODE_UPDATE = 4
    BUTTON_CONFIG_UPDATE = 5
    SONG_UPDATE = 6
    SYSTEM_STOP = 7
    NOTE_OUTPUT = 8

class PlayingState(Enum):
    PLAY = 1
    PAUSE = 2
    STOP = 3

class NoteOutputMessage():
    def __init__(self, event: MidiEvent, relative_timestamp: float, absolute_timestamp: float):
        self.event = event
        self.relative_timestamp = relative_timestamp
        self.absolute_timestamp = absolute_timestamp

class Message():
    def __init__(self, type, data = None):
        self.type = type
        self.data = data