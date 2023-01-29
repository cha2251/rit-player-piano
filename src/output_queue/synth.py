import math
from threading import Thread
import pyaudio
import itertools
import numpy as np

BUFFER_SIZE = 128
SAMPLE_RATE = 44100
NOTE_AMPLITUDE = 0.05

SYNTHESIZER_NAME = "CodeToJoy Synthesizer"

class MIDISynthesizer(Thread):
    """
    A simple synthesizer that accepts MIDI input from our system and plays it through
    the system's default audio output device. This mocks a mido output port for interopability.

    This was heavily inspired by this post here:
    https://python.plainenglish.io/build-your-own-python-synthesizer-part-3-162796b7d351
    """
    def __init__(self):
        Thread.__init__(self)

        self.active = False
        self.notes_dict = {}
        self.name = SYNTHESIZER_NAME

    def close(self):
        """Stops the synthesizer, closes the audio stream, and joins the thread."""
        self.active = False
        self.join()

    def send(self, message):
        """Send a MIDI event to the synthesizer."""

        # Some MIDI streams don't use `note_off` and instead send a `note_on` with velocity 0
        if (message.type == 'note_off' or message.velocity == 0) and message.note in self.notes_dict:
            del self.notes_dict[message.note]
        elif message.type == 'note_on':
            self.notes_dict[message.note] = self.sound_generator(message.note, message.velocity / 127)

    def sound_generator(self, note, amplitude):
        """Returns a generator that produces samples for a given note and amplitude."""
        freq = note_to_freq(note)
        increment = (2 * math.pi * freq) / SAMPLE_RATE

        return (
            sound_function(t) * amplitude for t in itertools.count(start=0, step=increment)
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

        while self.active:
            try:
                # We copy notes_dict because it could be concurrently modified by another thread
                samples = get_samples(dict(self.notes_dict))
                samples = np.int16(samples).tobytes()
                self.stream.write(samples)
            except Exception as err:
                print("Synthesizer error: ", err)

        self.stream.close()

def sound_function(t):
    """Returns an audio amplitude for a given time t. This is the function that determines the sound."""
    # Makes it sound vaguely more like a piano
    component1 = math.pow(math.sin(t), 3)
    component2 = math.sin(t + math.pi * 0.66667)

    return (component1 + component2) * NOTE_AMPLITUDE

def get_samples(notes_dict, num_samples=BUFFER_SIZE):
    """Returns a list of audio samples (amplitude values) for a given slice of time determined by `num_samples`"""
    return [
        sum([int(next(osc) * 32767) for _, osc in notes_dict.items()])
        for _ in range(num_samples)
    ]

def note_to_freq(note):
    return int(round(440 * math.pow(2, (note - 69) / 12), 1))