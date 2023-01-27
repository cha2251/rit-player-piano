import math
from threading import Thread
import pyaudio
import itertools
import numpy as np

BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMPLITUDE = 0.1

class MIDISynthesizer(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.active = False
        self.notes_dict = {}
        self.name = "CodeToJoy Synthesizer"

    def close(self):
        self.active = False

    def send(self, message):
        if (message.type == 'note_off' or message.velocity == 0) and message.note in self.notes_dict:
            del self.notes_dict[message.note]
        elif message.type == 'note_on':
            if message.note in self.notes_dict:
                self.notes_dict[message.note] = (self.notes_dict[message.note][0], message.velocity / 127)
            else:
                self.notes_dict[message.note] = (self.sound_generator(message.note), message.velocity / 127)

    def sound_generator(self, note):
        freq = note_to_freq(note)
        increment = (2 * math.pi * freq) / SAMPLE_RATE

        return (
            sound_function(t) * self.notes_dict[note][1] for t in itertools.count(start=0, step=increment)
        )

    def run(self):
        self.active = True
        self.stream = pyaudio.PyAudio().open(
            rate=SAMPLE_RATE,
            channels=1,
            format=pyaudio.paInt16,
            output=True,
            frames_per_buffer=BUFFER_SIZE,
        )

        try:
            while self.active:
                # We copy notes_dict because send(..) could be called from another thread
                samples = get_samples(dict(self.notes_dict))
                samples = np.int16(samples).tobytes()
                self.stream.write(samples)

        except Exception as err:
            print("Synthesizer error: ", err)
        finally:
            self.stream.close()

def sound_function(t):
    # Makes it sound vaguely more like a piano
    component1 = math.pow(math.sin(t), 3)
    component2 = math.sin(t + math.pi * 0.66667)

    return (component1 + component2) * NOTE_AMPLITUDE

def get_samples(notes_dict, num_samples=BUFFER_SIZE):
    return [
        sum([int(next(osc) * 32767) for _, (osc, _) in notes_dict.items()])
        for _ in range(num_samples)
    ]

def note_to_freq(note):
    return int(round(440 * math.pow(2, (note - 69) / 12), 1))