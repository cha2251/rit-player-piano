import math
from threading import Thread
import time
import pyaudio
import itertools
import numpy as np
from pygame import midi

BUFFER_SIZE = 512
SAMPLE_RATE = 44100
NOTE_AMP = 0.1

# -- HELPER FUNCTIONS --
def sound_function(v):
    component1 = math.pow(math.sin(v), 3)
    component2 = math.sin(v + 0.66667)

    return component1 + component2

def get_sin_oscillator(freq=55, amp=1, sample_rate=SAMPLE_RATE):
    increment = (2 * math.pi * freq) / sample_rate
    return (
        sound_function(v) * amp * NOTE_AMP for v in itertools.count(start=0, step=increment)
    )

def get_samples(notes_dict, num_samples=BUFFER_SIZE):
    return [
        sum([int(next(osc) * 32767) for _, osc in notes_dict.items()])
        for _ in range(num_samples)
    ]

class Synthesizer(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.active = False
        self.notes_dict = {}

    def close(self):
        self.active = False

    def send(self, message):
        if (message.type == 'note_off' or message.velocity == 0) and message.note in self.notes_dict:
            del self.notes_dict[message.note]
        elif message.type == 'note_on' and message.note not in self.notes_dict:
            freq = midi.midi_to_frequency(message.note)
            self.notes_dict[message.note] = get_sin_oscillator(freq=freq, amp=message.velocity / 127)

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
                samples = get_samples(self.notes_dict)
                samples = np.int16(samples).tobytes()
                self.stream.write(samples)

        except Exception as err:
            print("Synthesizer error: ", err)
        finally:
            self.stream.close()
