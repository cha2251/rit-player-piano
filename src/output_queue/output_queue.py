import queue
import mido
import time
import platform
from threading import Thread
from multiprocessing import Lock, Process, Manager

from src.common.midi_event import MidiEvent
from src.common.shared_priority_queue import PeekingPriorityQueue
from src.communication.messages import Message, MessageType, NoteOutputMessage, PlayingState, TimeSkipMessageType, Song
from src.output_queue.output_comm import OutputCommSystem
from src.output_queue.synth import MIDISynthesizer, SYNTHESIZER_NAME
from src.output_queue.tempo_mode import TempoMode

LINUX_SYNTH_KEYWORDS = "midi through port"
WINDOWS_SYNTH_KEYWORDS = "microsoft gs wavetable synth"

class OutputQueue():
    def __init__(self, input_queue, output_queue):
        self.queue = PeekingPriorityQueue()
        self.played_notes = []
        self._open_port = None
        self.active = False
        self.last_note_timestamp = 0
        self.last_note_time_played = 0
        self.paused_delta_time = 0
        self.last_time_sync_time = 0
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.current_song = None
        self.state = PlayingState.STOP
        self.previous_state = self.state
        self.playing_notes = {}
        self.accessLock = Lock()

        self.comm_system = OutputCommSystem()
        self.comm_system.set_queues(input_queue, output_queue)
        self.comm_system.registerListener(MessageType.SYSTEM_STOP, self.deactivate)
        self.comm_system.registerListener(MessageType.OUTPUT_QUEUE_UPDATE, self.process_note_event)
        self.comm_system.registerListener(MessageType.STATE_UPDATE, self.stateChanged)
        self.comm_system.registerListener(MessageType.SONG_UPDATE, self.songChanged)
        self.comm_system.registerListener(MessageType.TIME_SKIP, self.timeSkip)
        self.comm_system.start()

        # TODO DJA-PROC Add a mode system to allow for different play modes
        self.playing_mode = None # TempoMode(self)

        # TODO CHA-PROC Listen for Stop and Song Changes and reset timing variables to 0

    def process_note_event(self, message : Message):
        if message.data.song_name != self.current_song and not message.data.from_user_input:
            return

        self.queue.put(message.data)

    def stateChanged(self, message : Message):
        self.state = message.data

    def songChanged(self, message : Message):
        if message.data != Song.RESTART:
            self.current_song = message.data

    def timeSkip(self, message : Message):
        if message.data == TimeSkipMessageType.FORWARD:
            time_change = self.skip_forward(10)
        elif message.data == TimeSkipMessageType.BACKWARD:
            time_change = self.skip_backward(10)
        self.comm_system.send(Message(MessageType.TIME_CHANGE, time_change))

    def skip_forward(self, seconds : int):
        time_change = 0
        try:
            with self.accessLock:
                current_time = self.queue.peek().timestamp
                while self.queue.peek().timestamp < current_time + seconds:
                    event = self.queue.get_nowait()
                    self.last_note_timestamp = event.timestamp
                    time_change = event.timestamp - current_time
                    self.played_notes.append(event)

                self.stop_playing_notes()
        except queue.Empty as e:
            pass # Expected if we dont have anything in the queue
        except AttributeError as e:
            pass # Expected if we dont have anything in the queue
        return time_change
    
    def skip_backward(self, seconds : int):
        time_change = 0
        try:
            with self.accessLock:
                current_time = self.queue.peek().timestamp
                while self.played_notes[len(self.played_notes)-1].timestamp > current_time - seconds:
                    event = self.played_notes.pop(len(self.played_notes)-1)
                    self.last_note_timestamp = event.timestamp
                    time_change = event.timestamp - current_time
                    self.queue.put(event)

                self.stop_playing_notes()
        except IndexError as e:
            pass # Expected if we dont have anything in the queue
        except AttributeError as e:
            pass # Expected if we dont have anything in the queue
        return time_change

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

        if self.previous_state != self.state:
            if self.state == PlayingState.PLAY:
                self.play()
                self.previous_state = self.state
            elif self.state == PlayingState.PAUSE:
                if self.previous_state == PlayingState.PLAY:
                    self.pause()
                    self.previous_state = self.state
                else:
                    # Only pause if coming from a PLAY state
                    self.state = self.previous_state
            elif self.state == PlayingState.STOP:
                self.stop()
                self.previous_state = self.state

        now = time.time()

        # How many seconds into the song we are
        if self.last_note_timestamp is not None:
            relative_time = now - self.last_note_time_played + self.last_note_timestamp
        else: # Last song was stopped
            relative_time = now

        if self.state == PlayingState.PLAY and time.time() - self.last_time_sync_time > 0.25:
            self.last_time_sync_time = time.time()
            self.comm_system.send(Message(MessageType.SONG_TIME_SYNC, relative_time))

        immediate_events = []
        button_events = []

        # Separate events from buttons vs events from the song
        while self.queue.qsize() > 0:
            event = self.queue.peek()

            if event.from_user_input:
                button_events += [self.queue.get()]
            elif self.state == PlayingState.PLAY and event.timestamp <= relative_time:
                event = self.queue.get()
                immediate_events += [event]
                self.played_notes.append(event)
            else:
                break

        if self.playing_mode is not None:
            self.playing_mode.update(immediate_events, button_events, relative_time)

        for button_event in button_events:
            self._send_midi_event(button_event)
            time.sleep(0.001)

        # Handle regular queue events
        for midiEvent in immediate_events:
            # A timestamp of 0 means the note should be played immediately and is
            # valid, but would otherwise mess up the timings
            if midiEvent.timestamp > 1e-4:
                self.last_note_time_played = now
                self.last_note_timestamp = midiEvent.timestamp

            if midiEvent.event.type == "note_off":
                if midiEvent.event.note in self.playing_notes.keys():
                    del self.playing_notes[midiEvent.event.note]
            elif midiEvent.event.type == "note_on" and midiEvent.play_note:
                self.playing_notes[midiEvent.event.note] = midiEvent.event

            if not midiEvent.play_note:
                self.comm_system.send(Message(MessageType.NOTE_OUTPUT, NoteOutputMessage(midiEvent, relative_time, now)))
                time.sleep(0.001)
            else:
                self._send_midi_event(midiEvent)
                time.sleep(0.001)

    def _send_midi_event(self, midiEvent: MidiEvent):
        if type(midiEvent) != MidiEvent:
            return

        now = time.time()
        relative_now = now - self.last_note_time_played + self.last_note_timestamp

        self._open_port.send(midiEvent.event)
        self.comm_system.send(Message(MessageType.NOTE_OUTPUT, NoteOutputMessage(midiEvent, relative_now, now)))

    def play(self):
        if self.previous_state != PlayingState.STOP:
            # Restore the difference so that the timing remains correct
            self.last_note_time_played = time.time() - self.paused_delta_time
            self.resume_playing_notes()
        else:
            # If we are starting from the beginning, clear the queue and reset the timestamp
            self.last_note_timestamp = 0
            self.last_note_time_played = time.time()
            self.queue.clear()

    def pause(self):
        self.paused_delta_time = time.time() - self.last_note_time_played
        self.stop_playing_notes()

    def stop(self):
        self.stop_playing_notes()
        self.playing_notes.clear()
        self.queue.clear()

        self.last_note_timestamp = 0
        self.last_note_time_played = 0
        self.paused_delta_time = 0

    def stop_playing_notes(self):
        for event in self.playing_notes.values():
            self._send_midi_event(MidiEvent(mido.Message('note_off', note=event.note), 0))

    def resume_playing_notes(self):
        for event in self.playing_notes.values():
            self._send_midi_event(event)

    def stop_playing_notes(self):
        for event in self.playing_notes.values():
            self._send_midi_event(MidiEvent(mido.Message('note_off', note=event.note), 0))

    def resume_playing_notes(self):
        for event in self.playing_notes.values():
            self._send_midi_event(event)

    def run(self):
        self.active = True
        self.select_device(None)
        while self.active:
            with self.accessLock:
                self._check_priority_queue()
            time.sleep(0)

        self._open_port.close()
    
    def deactivate(self, message=None):
        print("Output System Deactivated")
        self.active = False