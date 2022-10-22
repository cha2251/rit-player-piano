from dataclasses import dataclass, field
import mido


@dataclass(order=True)
class MidiEvent:
    event: mido.Message=field(compare=False) # Don't use this when sorting in a priority queue
    timestamp: int # TODO: Better time class?