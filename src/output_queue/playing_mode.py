from abc import abstractmethod
from src.common.midi_event import MidiEvent
from src.communication.messages import PlayingState

class PlayingMode():
    @abstractmethod
    def update(self, immediate_events: list, button_events: list, relative_time: float):
        pass
