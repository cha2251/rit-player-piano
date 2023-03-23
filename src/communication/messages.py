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
    TEMPO_MODE_UPDATE = 9
    SET_HAND_TO_PLAY = 10
    SET_DURATION = 11

class PianoAssistPlaying(Enum):
    LEFT = 1
    RIGHT = 2
    NEITHER = 3
    BOTH = 4

class Song(Enum):
    FREEPLAY = 1

class PlayingState(Enum):
    PLAY = 1
    PAUSE = 2
    STOP = 3

class TempoModeMessageType(Enum):
    HIT_NOTE = 1
    MISSED_NOTE = 2

class Message():
    def __init__(self, type, data = None):
        self.type = type
        self.data = data

class NoteOutputMessage(Message):
    def __init__(self, event: MidiEvent, relative_timestamp: float, absolute_timestamp: float):
        self.event = event
        self.relative_timestamp = relative_timestamp
        self.absolute_timestamp = absolute_timestamp

class TempoModeMessage(Message):
    def __init__(self, type: TempoModeMessageType, time_delta: float):
        self.type = type
        self.time_delta = time_delta
