from dataclasses import dataclass, field
import mido


@dataclass(order=True)
class MidiEvent:
    event: mido.Message=field(compare=False) # Don't use this when sorting in a priority queue
    timestamp: float # Time.time() returns seconds as float
    split_note: bool = False
    should_play: bool = True

    # Add time in seconds to this event's timestamp
    def addTime(self, time):
        self.timestamp += time
