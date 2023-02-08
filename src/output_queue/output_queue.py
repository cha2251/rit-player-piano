from queue import PriorityQueue, Empty
import mido
import time
import platform
from threading import Thread
from multiprocessing import Process, Manager, Queue

from src.common.midi_event import MidiEvent
from src.output_queue.synth import MIDISynthesizer, SYNTHESIZER_NAME

def _runOutputQueue(inputQueue, selectDeviceString, running):
    output = OutputQueueProcess(inputQueue, selectDeviceString, running)
    output.run()

class OutputQueue():
    def __init__(self, inputQueue):
        # Created a variable that can be shared between processes to notify the output system to stop
        self._processShouldRun = Manager().Value('c_bool', False)

        # Created a variable that can be shared between processes to notify the output to
        # switch to a different output device. A value other than None indicates a device change
        self._selectDeviceString = Manager().Value('c_char_p', None)

        self._outputSystem = Process(target=_runOutputQueue, args=(inputQueue, self._selectDeviceString, self._processShouldRun,))

    def start(self):
        self._processShouldRun.value = True
        self._outputSystem.start()

    def deactivate(self):
        self._processShouldRun.value = False
        self._outputSystem.join()

    # Selects the output device to send MIDI to. If `name` is None then the system default is used
    def select_device(self, name=None):
        if name is not None and name not in self.get_device_list():
            raise Exception("Device \"{}\" does not exist".format(name))

        if name is None:
            if platform.system() != "Windows" or len(mido.get_output_names()) == 0:
                name = SYNTHESIZER_NAME
            else:
                name = mido.get_output_names()[0]

        self._selectDeviceString.value = name

    def get_device_list(self):
        return [SYNTHESIZER_NAME] + mido.get_output_names()

class OutputQueueProcess():
    def __init__(self, inputQueue, selectDeviceString, running):
        self.queue = inputQueue
        self._selectDeviceString = selectDeviceString
        self._open_port = None
        self._running = running

    def __del__(self):
        if self._open_port != None:
            self._open_port.close()

    # Selects the output device to send MIDI to. If `name` is None then the system default is used
    def select_device(self, name):
        if name != SYNTHESIZER_NAME and name not in mido.get_output_names():
            print('"{}" does not match any of the available devices'.format(name))
            return

        if self._open_port is not None:
            self._open_port.close()

        if name == SYNTHESIZER_NAME:
            self._open_port = MIDISynthesizer()
        else:
            try:
                self._open_port = mido.open_output(name)
            except:
                print("Failed to open output device \"{}\". Using synthesizer instead".format(name))
                self._open_port = MIDISynthesizer()

        print('Switched output device to "{}"'.format(self._open_port.name))

    # Checks the queue for messages and sends them to the output as needed and returns the number of message sent (mainly for testing)
    def _check_priority_queue(self):
        if self._open_port == None:
            return

        now = time.time()

        try:
            while not self.queue.empty() and now >= self.queue.peek().timestamp:
                midiEvent = self.queue.get()

                self._open_port.send(midiEvent.event)
        except IndexError:
            pass # Expected when pausing/stopping and the queue is cleared

    def run(self):
        while self._running.value:
            if self._selectDeviceString.value is not None:
                 self.select_device(self._selectDeviceString.value)
                 self._selectDeviceString.value = None

            self._check_priority_queue()

def play_test_tones(queue, delay=0.0):
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