from queue import PriorityQueue, Empty
import mido
import time
import platform
from threading import Thread
from multiprocessing import Process, Manager

from src.common.midi_event import MidiEvent
from src.common.shared_priority_queue import PeekingPriorityQueue
from src.communication.messages import MessageType
from src.output_queue.output_comm import OutputCommSystem
from src.output_queue.synth import MIDISynthesizer, SYNTHESIZER_NAME

LINUX_SYNTH_KEYWORDS = "midi through port"
WINDOWS_SYNTH_KEYWORDS = "microsoft gs wavetable synth"

class OutputQueue():
    def __init__(self, input_queue, output_queue):
        self.queue : PeekingPriorityQueue
        self._open_port = None
        self.active = False
        self.last_note_timestamp = 0
        self.last_note_time_played = 0
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.comm_system = OutputCommSystem()
        self.comm_system.set_queues(input_queue, output_queue)
        self.comm_system.registerListener(MessageType.SYSTEM_STOP, self.deactivate)
        self.comm_system.start()

        # TODO CHA-PROC Listen for Stop and Song Changes and reset timing variables to 0

    def __del__(self):
        if self._open_port != None:
            self._open_port.close()

    # Selects the output device to send MIDI to. If `name` is None then the system default is used
    def select_device(self, name):
        if name is not None and name != SYNTHESIZER_NAME and name not in mido.get_output_names():
            print('"{}" does not match any of the available devices'.format(name))
            return

        if self._open_port is not None:
            self._open_port.close()

        if name is None:
            name = self._get_devices_by_priority()[-1]

        if name == SYNTHESIZER_NAME:
            self._open_port = MIDISynthesizer()
        else:
            try:
                self._open_port = mido.open_output(name)
            except:
                print("Failed to open output device \"{}\". Using synthesizer instead".format(name))
                self._open_port = MIDISynthesizer()

        print('Switched output device to "{}"'.format(self._open_port.name))

    def _get_devices_by_priority(self):
        devices_by_priority = []

        # Create a priority-based list of devices to use and select the best one
        for device in mido.get_output_names() + [SYNTHESIZER_NAME]:
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
        self.active = True
        self.select_device(None) #TODO Fix during merge w/ device prioritizaion
        while self.active:
            self._check_priority_queue()
    
    def deactivate(self, message=None):
        print("Output System Deactivated")
        self.active = False