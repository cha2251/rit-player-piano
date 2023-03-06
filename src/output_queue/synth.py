import math
from threading import Lock, Thread
import pyaudio
import itertools
import numpy as np

BUFFER_SIZE = 256
SAMPLE_RATE = 32000
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
        self.notes_dict_lock = Lock()
        self.name = SYNTHESIZER_NAME

        self.start()

    def close(self):
        """Stops the synthesizer, closes the audio stream, and joins the thread."""
        self.active = False
        self.join()

    def send(self, message):
        """Send a MIDI event to the synthesizer."""

        with self.notes_dict_lock:
        # Some MIDI streams don't use `note_off` and instead send a `note_on` with velocity 0
            if (message.type == 'note_off' or message.velocity == 0) and message.note in self.notes_dict:
                del self.notes_dict[message.note]
            elif message.type == 'note_on':
                # Get an amplitude/loudness between [0-1] for a note with velocity [0-127]
                amplitude = message.velocity / 127
                self.notes_dict[message.note] = self.sound_generator(message.note, amplitude)

    def sound_generator(self, note, amplitude):
        """Returns a generator that produces samples for a given note and amplitude."""
        freq = note_to_freq(note)
        increment = (2 * math.pi * freq) / SAMPLE_RATE

        amplitude *= NOTE_AMPLITUDE

        return (
            math.sin(t) * amplitude for t in itertools.count(start=0, step=increment)
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
                with self.notes_dict_lock:
                    samples = get_samples(self.notes_dict)
                samples = np.int16(samples).tobytes()
                self.stream.write(samples)
            except Exception as err:
                print("Synthesizer error: ", err)

        self.stream.close()

def get_samples(notes_dict, num_samples=BUFFER_SIZE):
    """Returns a list of audio samples (amplitude values) for a given slice of time determined by `num_samples`"""
    return [
        sum([int(next(osc) * 32767) for _, osc in notes_dict.items()])
        for _ in range(num_samples)
    ]

def note_to_freq(note):
    """Converts a MIDI note number to a frequency in Hz."""
    return int(440 * math.pow(2, (note - 69) / 12))