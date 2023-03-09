import queue
import mido
import time
import platform
from threading import Thread
from multiprocessing import Process, Manager

from src.common.midi_event import MidiEvent
from src.common.shared_priority_queue import PeekingPriorityQueue
from src.communication.messages import Message, MessageType, NoteOutputMessage, PlayingState, TempoModeMessage, TempoModeMessageType
from src.output_queue.output_comm import OutputCommSystem
from src.output_queue.synth import MIDISynthesizer, SYNTHESIZER_NAME

LINUX_SYNTH_KEYWORDS = "midi through port"
WINDOWS_SYNTH_KEYWORDS = "microsoft gs wavetable synth"

class OutputQueue():
    def __init__(self, input_queue, output_queue):
        self.queue = PeekingPriorityQueue()
        self.button_queue = queue.Queue()
        self._open_port = None
        self.active = False
        self.last_note_timestamp = 0
        self.last_note_time_played = 0
        self.paused_delta_time = 0
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.state = PlayingState.STOP
        self.state_changed = False
        self.playing_notes = {}
        self.comm_system = OutputCommSystem()
        self.comm_system.set_queues(input_queue, output_queue)
        self.comm_system.registerListener(MessageType.SYSTEM_STOP, self.deactivate)
        self.comm_system.registerListener(MessageType.OUTPUT_QUEUE_UPDATE, self.process_note_event)
        self.comm_system.registerListener(MessageType.BUTTON_NOTE, self.process_button_note)
        self.comm_system.registerListener(MessageType.STATE_UPDATE, self.stateChanged)
        self.comm_system.start()

        self.playing_missed_notes = []
        self.playing_hit_notes = []

        # TODO CHA-PROC Listen for Stop and Song Changes and reset timing variables to 0

    def process_note_event(self, message : Message):
        self.queue.put(message.data)

    def process_button_note(self, message : Message):
        self.button_queue.put(message.data)

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
        relative_time = now - self.last_note_time_played + (self.last_note_timestamp if self.state == PlayingState.PLAY else 0)

        try:
            if self.state_changed:
                self.state_changed = False

                if self.state == PlayingState.PLAY:
                    self.play()
                elif self.state == PlayingState.PAUSE:
                    self.pause()
                elif self.state == PlayingState.STOP:
                    self.stop()

            if self.state == PlayingState.PLAY:
                if not self.button_queue.empty():
                    button_pressed = False
                    button_released = False

                    while not self.button_queue.empty():
                        if self.button_queue.get().event.type == 'note_on':
                            button_pressed = True
                        else:
                            button_released = True

                    if button_pressed:
                        sorted_notes = self.queue.peekn(8)

                        found_time = None

                        for note in sorted_notes:
                            if note.timestamp - relative_time > 0.333:
                                break
                            elif not note.was_hit and note.split_note and (found_time is None or abs(note.timestamp - found_time) < 0.1):
                                if found_time is None:
                                    found_time = note.timestamp

                                    self.comm_system.send(Message(MessageType.TEMPO_MODE_UPDATE, TempoModeMessage(TempoModeMessageType.HIT_NOTE, note.timestamp - relative_time)))

                                if abs(note.timestamp - relative_time) < 0.15:
                                    # If they're close enough, make it *sound* perfect
                                    note.should_play = True
                                    note.was_hit = True
                                else:
                                    # Otherwise make them hear the pain of their bad timing
                                    note.was_hit = True
                                    self._send_midi_event(note)
                            elif (found_time is not None and abs(note.timestamp - found_time) >= 0.1):
                                break

                        if found_time is None and len(self.playing_missed_notes) > 0:
                            played_missed_note = False

                            for event in self.playing_missed_notes:
                                if relative_time - event.timestamp < 0.333:
                                    played_missed_note = True
                                    event.timestamp = relative_time
                                    self._send_midi_event(event)
                                else:
                                    self.comm_system.send(Message(MessageType.TEMPO_MODE_UPDATE, TempoModeMessage(TempoModeMessageType.MISSED_NOTE, note.timestamp - relative_time)))

                            if played_missed_note:
                                self.comm_system.send(Message(MessageType.TEMPO_MODE_UPDATE, TempoModeMessage(TempoModeMessageType.HIT_NOTE, note.timestamp - relative_time)))

                            self.last_note_time_played = now
                            self.last_note_timestamp = relative_time
                            self.playing_missed_notes = []
                    elif button_released:
                        pass # TODO Release timing
            else:
                while not self.button_queue.empty():
                    self._send_midi_event(self.button_queue.get())

            if self.queue.peek() is not None:
                if self.state == PlayingState.PLAY and self.queue.peek().timestamp < relative_time:
                    midiEvent = self.queue.get()

                    self.last_note_time_played = now
                    self.last_note_timestamp = midiEvent.timestamp

                    if midiEvent.event.type == "note_off":
                        if midiEvent.event.note in self.playing_notes.keys():
                            del self.playing_notes[midiEvent.event.note]

                        self.playing_missed_notes = list(filter(lambda x: x.event.note != midiEvent.event.note, self.playing_missed_notes))
                    elif midiEvent.event.type == "note_on" and midiEvent.should_play:
                        self.playing_notes[midiEvent.event.note] = midiEvent.event

                    if midiEvent.split_note and midiEvent.should_play:
                        pass # print("HIT THIS")
                    elif midiEvent.split_note and not midiEvent.should_play:
                        self.playing_missed_notes += [midiEvent]

                    if midiEvent.should_play:
                        self._send_midi_event(midiEvent)
                    else:
                        self.comm_system.send(Message(MessageType.NOTE_OUTPUT, NoteOutputMessage(midiEvent, relative_time, now)))
        except IndexError:
            pass # Expected when the queue is empty

    def _send_midi_event(self, midiEvent: MidiEvent):
        if type(midiEvent) != MidiEvent:
            return

        now = time.time()
        relative_now = now - self.last_note_time_played + self.last_note_timestamp

        self._open_port.send(midiEvent.event)
        self.comm_system.send(Message(MessageType.NOTE_OUTPUT, NoteOutputMessage(midiEvent, relative_now, now)))

    def play(self):
        if self.last_note_timestamp is not None:
            # Restore the difference so that the timing remains correct
            self.last_note_time_played = time.time() - self.paused_delta_time

            for event in self.playing_notes.values():
                self._send_midi_event(event)
        else:
            # If we are starting from the beginning, clear the queue and reset the timestamp
            self.last_note_timestamp = 0
            self.queue.clear()

    def pause(self):
        self.paused_delta_time = time.time() - self.last_note_time_played

        # Turn off all notes currently playing
        for event in self.playing_notes.values():
            self._send_midi_event(MidiEvent(mido.Message('note_off', note=event.note), 0))

    def stop(self):
        # Turn off all notes currently playing and clear everything
        for event in self.playing_notes.values():
            self._send_midi_event(MidiEvent(mido.Message('note_off', note=event.note), 0))
        self.playing_notes.clear()
        self.queue.clear()

        self.last_note_timestamp = None # Signals that we removed all notes from the queue and want to start over
        self.last_note_time_played = 0

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