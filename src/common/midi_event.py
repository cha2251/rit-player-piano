from dataclasses import dataclass, field
import mido


@dataclass(order=True)
class MidiEvent:
    event: mido.Message=field(compare=False) # Don't use this when sorting in a priority queue
    timestamp: float                         # Time.time() returns seconds as float
    from_user_input: bool = False
    split_note: bool = False
    was_hit: bool = False
    play_note: bool = False                  # If false, don't send the note

    # Add time in seconds to this event's timestamp
    def addTime(self, time):
        self.timestamp += time
