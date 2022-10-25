import mido
import time

from src.common.midi_event import MidiEvent

class OutputQueue:
    def __init__(self):
        self._open_port = None

    # Selects the output device to send MIDI to. If `name` is None then the system default is used
    def select_device(self, name=None):
        if not name == None and not name in mido.get_output_names():
            raise Exception('"{}" does not match any of the available devices'.format(name))

        self._open_port = mido.open_output(name)

        print('Switched output device to "{}"'.format(self._open_port.name))

    def check_queue(self, queue):
        now = time.time()
        
        while not queue.empty() and now >= queue.queue[0].timestamp:
            midiEvent = queue.get()

            self._open_port.send(midiEvent.event)

    def play_test_tones(self, queue, delay=0.0):
        if self._open_port == None:
            raise Exception('There is no currently selected device')

        now = time.time() + delay

        for i in [0, 2, 4, 5, 7]:
            queue.put(MidiEvent(mido.Message('note_on',note=60+i), now))
            now += 0.2
            queue.put(MidiEvent(mido.Message('note_off',note=60+i), now))
            now += 0.05

        for i in [5, 4, 2, 0]:
            queue.put(MidiEvent(mido.Message('note_on',note=60+i), now))
            now += 0.2
            queue.put(MidiEvent(mido.Message('note_off',note=60+i), now))
            now += 0.05

        for i in [0, 4, 7]:
           queue.put(MidiEvent(mido.Message('note_on',note=60+i), now))
        now += 0.4

        for i in [0, 4, 7]:
            queue.put(MidiEvent(mido.Message('note_off',note=60+i), now))
        now += 0.05

        for i in [0, 5, 9]:
            queue.put(MidiEvent(mido.Message('note_on',note=60+i), now))
        now += 0.4

        for i in [0, 5, 9]:
            queue.put(MidiEvent(mido.Message('note_off',note=60+i), now))
        now += 0.05

        for i in [0, 4, 7]:
            queue.put(MidiEvent(mido.Message('note_on',note=60+i), now))
        now += 0.4

        for i in [0, 4, 7]:
            queue.put(MidiEvent(mido.Message('note_off',note=60+i), now))
        now += 0.05

    # Test fucntions for setting up unit test infra. TODO: Remove in sprint 2.
    def is_even(self, number):
        if number % 2 == 0:
            return True
        return False

    # Test fucntions for setting up unit test infra. TODO: Remove in sprint 2.
    def in_range(self, number):
        lower = 3
        upper = 8
        if number > lower and number < upper:
            return True
        return False