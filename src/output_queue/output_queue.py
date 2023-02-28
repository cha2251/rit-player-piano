from queue import PriorityQueue, Empty
import mido
import time
import platform
from threading import Thread
from multiprocessing import Process, Manager

from src.common.midi_event import MidiEvent
from src.common.shared_priority_queue import PeekingPriorityQueue
from src.output_queue.output_comm import OutputCommSystem
from src.output_queue.synth import MIDISynthesizer, SYNTHESIZER_NAME

def _runOutputQueue(selectDeviceString, _notePlayingSet, running):
    output = OutputQueueProcess(selectDeviceString, _notePlayingSet, running)
    output.run()

LINUX_SYNTH_KEYWORDS = "midi through port"
WINDOWS_SYNTH_KEYWORDS = "microsoft gs wavetable synth"
class OutputQueue():
    def __init__(self, input_queue, output_queue):
        # Created a variable that can be shared between processes to notify the output system to stop
        self._processShouldRun = Manager().Value('c_bool', False)

        # Created a variable that can be shared between processes to notify the output to
        # switch to a different output device. A value other than None indicates a device change
        self._selectDeviceString = Manager().Value('c_char_p', None)

        self._notePlayingSet = Manager().dict() # Create a new dictionary that can be shared between processes

        self._outputSystem = Process(target=_runOutputQueue, args=(self._selectDeviceString, self._notePlayingSet, self._processShouldRun, input_queue, output_queue,))

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
            name = self._get_devices_by_priority()[-1]

        self._selectDeviceString.value = name

    def get_device_list(self):
        return [SYNTHESIZER_NAME] + mido.get_output_names()

    def _get_devices_by_priority(self):
        devices_by_priority = []

        # Create a priority-based list of devices to use and select the best one
        for device in self.get_device_list():
            if device == SYNTHESIZER_NAME:                  # The built-in synthesizer
                devices_by_priority += [(1, device)]
            elif LINUX_SYNTH_KEYWORDS in device.lower():    # Non-functional virtual ports on Linux, never use these
                devices_by_priority += [(0, device)]
            elif WINDOWS_SYNTH_KEYWORDS in device.lower():  # Windows synth, better than our synthesizer
                devices_by_priority += [(2, device)]
            else:                                           # Any other devices are likely physical devices so prioritize these
                devices_by_priority += [(3, device)]

        devices_by_priority.sort(key=lambda x: x[0])
        return [x[1] for x in devices_by_priority] # Only return the names, not the priorities

    def get_playing_notes(self):
        return list(self._notePlayingSet.keys())

    def get_queue(self):
        return self._queue

class OutputQueueProcess():
    def __init__(self, selectDeviceString, _notePlayingSet, running, input_queue, output_queue):
        self.queue : PeekingPriorityQueue
        self._selectDeviceString = selectDeviceString
        self._notePlayingSet = _notePlayingSet
        self._open_port = None
        self._running = running
        self.last_note_timestamp = 0
        self.last_note_time_played = 0
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.comm_system = OutputCommSystem()
        self.comm_system.set_queues(input_queue, output_queue)
        self.comm_system.start()

        # TODO CHA-PROC Listen for Stop and Song Changes and reset timing variables to 0

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
            if self.last_note_time_played - self.last_note_timestamp <= now - self.queue.peek().timestamp:
                midiEvent = self.queue.get()
                self.last_note_time_played = now
                self.last_note_timestamp = midiEvent.timestamp

                if midiEvent.event.type == 'note_off' or midiEvent.event.velocity == 0:
                    if midiEvent.event.note in self._notePlayingSet.keys():
                        del self._notePlayingSet[midiEvent.event.note]
                elif midiEvent.event.type == 'note_on':
                    self._notePlayingSet[midiEvent.event.note] = True

                self._open_port.send(midiEvent.event)
        except IndexError:
            pass # Expected when the queue is empty
        except AttributeError:
            pass # Expected when the queue wasn't empty, but got preempted and becomes empty mid-way through the loop

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