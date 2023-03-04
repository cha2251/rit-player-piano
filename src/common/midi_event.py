from dataclasses import dataclass, field
import mido


@dataclass(order=True)
class MidiEvent:

    # def __init__(self, event, timestamp, play_note=False):    
    #     self.event = event # : mido.Message=field(compare=False) # Don't use this when sorting in a priority queue
    #     self.timestamp = timestamp # : float                         # Time.time() returns seconds as float
    #     self.play_note =play_note #  : False                          # If false, don't send the note

    event: mido.Message=field(compare=False) # Don't use this when sorting in a priority queue
    timestamp: float                         # Time.time() returns seconds as float
    play_note: bool = False                          # If false, don't send the note

    # Add time in seconds to this event's timestamp
    def addTime(self, time):
        self.timestamp += time
