from queue import PriorityQueue, Empty
import mido
import time
from threading import Thread
from multiprocessing import Process, Manager, Queue

from src.common.midi_event import MidiEvent

MAXIMUM_QUEUE_TRANSFER_TIME = 0.003

def _runOutputQueue(inputQueue, selectDeviceQueue, running):
    output = OutputQueueProcess(inputQueue, selectDeviceQueue, running)
    output.run()

class OutputQueue():
    def __init__(self, inputQueue):
        self._processShouldRun = Manager().Value('i', False)
        self._selectDeviceQueue = Queue()
        self._outputSystem = Process(target=_runOutputQueue, args=(inputQueue, self._selectDeviceQueue, self._processShouldRun,))

    def start(self):
        self._processShouldRun.value = True
        self._outputSystem.start()

    def deactivate(self):
        self._processShouldRun.value = False
        self._outputSystem.join()

    # Selects the output device to send MIDI to. If `name` is None then the system default is used
    def select_device(self, name=None):
        self._selectDeviceQueue.put(name)

class OutputQueueProcess():
    def __init__(self, inputQueue, selectDeviceQueue, running):
        self.inputQueue = inputQueue
        self.queue = PriorityQueue()
        self._selectDeviceQueue = selectDeviceQueue
        self._open_port = None
        self._running = running

    def __del__(self):
        if self._open_port != None:
            self._open_port.close()

    # Selects the output device to send MIDI to. If `name` is None then the system default is used
    def select_device(self, name=None):
        if name is not None and name not in mido.get_output_names():
            print('"{}" does not match any of the available devices'.format(name))

        if self._open_port is not None:
            self._open_port.close()

        self._open_port = mido.open_output(name)

        print('Switched output device to "{}"'.format(self._open_port.name))
        
    # Processes any incoming commands
    def _process_command_queue(self):
        while not self._selectDeviceQueue.empty():
            self.select_device(self._selectDeviceQueue.get_nowait())

    # Transfers messages from the process input queue to our internal priority queue
    def _transfer_queues(self):
        now = time.time()

        while not self.inputQueue.empty() and time.time() - now < MAXIMUM_QUEUE_TRANSFER_TIME:
            self.queue.put(self.inputQueue.get())

    # Checks the queue for messages and sends them to the output as needed and returns the number of message sent (mainly for testing)
    def _check_priority_queue(self):
        if self._open_port == None:
            return
        
        now = time.time()

        while not self.queue.empty() and now >= self.queue.queue[0].timestamp:
            midiEvent = self.queue.get()

            self._open_port.send(midiEvent.event)

    def run(self):
        while self._running.value:
            self._process_command_queue()
            self._transfer_queues()
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