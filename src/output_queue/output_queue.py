from queue import PriorityQueue, Empty
import mido
import time
import platform
from threading import Thread
from multiprocessing import Process, Manager

from src.common.midi_event import MidiEvent
from src.common.shared_priority_queue import PeekingPriorityQueue
from src.communication.messages import Message, MessageType, PlayingState
from src.output_queue.output_comm import OutputCommSystem
from src.output_queue.synth import MIDISynthesizer, SYNTHESIZER_NAME

LINUX_SYNTH_KEYWORDS = "midi through port"
WINDOWS_SYNTH_KEYWORDS = "microsoft gs wavetable synth"

class OutputQueue():
    def __init__(self, input_queue, output_queue):
        self.queue = PeekingPriorityQueue()
        self._open_port = None
        self.active = False
        self.last_note_timestamp = 0
        self.last_note_time_played = 0
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.state = PlayingState.STOP
        self.state_changed = False
        self.playing_notes = {}
        self.comm_system = OutputCommSystem()
        self.comm_system.set_queues(input_queue, output_queue)
        self.comm_system.registerListener(MessageType.SYSTEM_STOP, self.deactivate)
        self.comm_system.registerListener(MessageType.OUTPUT_QUEUE_UPDATE, self.process_note_event)
        self.comm_system.registerListener(MessageType.STATE_UPDATE, self.stateChanged)
        self.comm_system.start()

        # TODO CHA-PROC Listen for Stop and Song Changes and reset timing variables to 0

    def process_note_event(self, message : Message):
        self.queue.put(message.data)

    def stateChanged(self, message : Message):
        if self.state != message.data:
            self.state_changed = True

        self.state = message.data

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
            if self.state_changed:
                self.state_changed = False

                if self.state == PlayingState.PLAY:
                    self.play()
                elif self.state == PlayingState.PAUSE:
                    self.pause()
                elif self.state == PlayingState.STOP:
                    self.stop()

            if self.queue.peek() is not None and self.state == PlayingState.PLAY:
                if self.last_note_time_played - self.last_note_timestamp <= now - self.queue.peek().timestamp:
                    midiEvent = self.queue.get()
                    self.last_note_time_played = now
                    self.last_note_timestamp = midiEvent.timestamp

                    if midiEvent.event.type == "note_off" or midiEvent.event.velocity == 0:
                        if midiEvent.event.note in self.playing_notes.keys():
                            del self.playing_notes[midiEvent.event.note]
                    elif midiEvent.event.type == "note_on":                        
                        self.playing_notes[midiEvent.event.note] = midiEvent.event


                    if midiEvent.event.type == "note_on" and midiEvent.play_note:
                        """ TODO: Here's where we filter for the split hands.
                        If the note is not on the correct hand it will not be sent.
                        If the note should be sent anyway, this should be adjusted.
                        """
                        
                        self._open_port.send(midiEvent.event)
                    elif midiEvent.event.type == "note_on" and not midiEvent.play_note:
                        pass # do nothing
                    else:
                        self._open_port.send(midiEvent.event)

                    #self._open_port.send(midiEvent.event)
        except IndexError:
            pass # Expected when the queue is empty

    def play(self):
        if self.last_note_timestamp is not None:
            # Restore the difference so that the timing remains correct
            self.last_note_timestamp += time.time()

            for event in self.playing_notes.values():
                self._open_port.send(event)

        else:
            # If we are starting from the beginning, clear the queue and reset the timestamp
            self.last_note_timestamp = 0
            self.queue.clear()

    def pause(self):
        if self.last_note_timestamp is not None:
            self.last_note_timestamp -= time.time() # Store the difference between this and now for later

        # Turn off all notes currently playing
        for event in self.playing_notes.values():
            self._open_port.send(mido.Message('note_off', note=event.note))

    def stop(self):
        self.last_note_timestamp = None # Signals that we removed all notes from the queue and want to start over
        self.last_note_time_played = 0

        # Turn off all notes currently playing and clear everything
        for event in self.playing_notes.values():
            self._open_port.send(mido.Message('note_off', note=event.note))
        self.playing_notes.clear()
        self.queue.clear()

    def run(self):
        self.active = True
        self.select_device(None)
        while self.active:
            self._check_priority_queue()
            time.sleep(0)

        self._open_port.close()
    
    def deactivate(self, message=None):
        print("Output System Deactivated")
        self.active = False