import mido
import time
from threading import Thread

from src.common.midi_event import MidiEvent

class OutputQueue(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self._open_port = None
        self._running = False

    def __del__(self):
        if self._open_port != None:
            self._open_port.close()

    # Selects the output device to send MIDI to. If `name` is None then the system default is used
    def select_device(self, name=None):
        if name is not None and name not in self.get_device_list():
            raise Exception('"{}" does not match any of the available devices'.format(name))

        if self._open_port is not None:
            self._open_port.close()

        self._open_port = mido.open_output(name)

        print('Switched output device to "{}"'.format(self._open_port.name))

    # Returns the list of currently available MIDI devices that can be connected to
    def get_device_list(self):
        return mido.get_output_names()
        
    # Checks the queue for messages and sends them to the output as needed and returns the number of message sent (mainly for testing)
    def _check_queue(self):
        if self._open_port == None:
            return

        now = time.time()

        while not self.queue.empty() and now >= self.queue.queue[0].timestamp:
            midiEvent = self.queue.get()
            self._open_port.send(midiEvent.event)

    def run(self):
        self._running = True

        while self._running:
            self._check_queue()

    # Tells the output thread that it should stop
    def deactivate(self):
        self._running = False

    def play_test_tones(self, queue, delay=0.0):
        if self._open_port is None:
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