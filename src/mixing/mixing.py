import queue
from threading import Thread
import time
from src.common.midi_event import MidiEvent
from src.common.shared_queues import SharedQueues
from src.mixing.mixing_comm import MixingCommSystem
from src.communication.messages import Message, MessageType, State
import mido

class Mixing(Thread):
    file_input_queue: queue.Queue = None
    button_input_queue: queue.Queue = None
    mixed_output_queue: queue.PriorityQueue = None
    holding_queue: queue.PriorityQueue = None
    active = False
    state = State.STOP

    current_notes = {}

    def __init__(self, shared_queues:SharedQueues):
        Thread.__init__(self)
        self.file_input_queue = shared_queues.file_input_queue
        self.button_input_queue = shared_queues.button_input_queue
        self.mixed_output_queue = shared_queues.mixed_output_queue
        self.comm_system = MixingCommSystem()
        self.comm_system.start()
    
    
    def run(self):
        self.active = True
        self.startup()
        
    def startup(self):
        self.registerCallbacks()
        self.main_loop()

    def registerCallbacks(self):
        self.comm_system.registerListner(MessageType.STATE_UPDATE, self.stateChanged)
        self.comm_system.registerListner(MessageType.MODE_UPDATE, self.modeChanged)
        self.comm_system.registerListner(MessageType.SONG_UPDATE, self.songChanged)

    def stateChanged(self, message : Message):
        if message.data == State.PLAY:
            self.play_pushed()
        if message.data == State.PAUSE:
            self.pause_pushed()
        if message.data == State.STOP:
            self.stop_pushed()

    def songChanged(self, message : Message):
        self.stop_pushed() # Mixing does not care about song name, but should stop current song

    def modeChanged(self, message : Message):
        pass #TODO Implement when mutiple play modes are enabled

    def play(self):
        self.state = State.PLAY

    def play_pushed(self):
        if self.state is State.STOP:
            self.play()
        if self.state is State.PAUSE:
            self.unpause()

    def pause_pushed(self):
        if self.state is State.PLAY:
            self.pause()
        elif self.state is State.PAUSE:
            self.unpause()
    
    def stop_pushed(self):
        if self.state is State.PLAY:
            self.stop()
        elif self.state is State.PAUSE:
            self.stop()

    def pause(self):
        self.state = State.PAUSE
        
        self.holding_queue = self.mixed_output_queue.get_and_clear_queue()

        for note in self.current_notes.keys():
            if(self.current_notes[note]=='note_on'):
                event = mido.Message('note_off', note=note)
                self.mixed_output_queue.put(MidiEvent(event, time.time()))
    
    def unpause(self):
        self.mixed_output_queue.set_queue(self.holding_queue)

        self.holding_queue.clear()

        self.state = State.PLAY
    
    def stop(self):
        self.state = State.STOP

        self.mixed_output_queue.get_and_clear_queue()

        for note in self.current_notes.keys():
            if(self.current_notes[note]=='note_on'):
                event = mido.Message('note_off', note=note)
                self.mixed_output_queue.put(MidiEvent(event, time.time()))
    
    def main_loop(self):
        while(self.active):
            try:
                event = self.button_input_queue.get_nowait()
                self.mixed_output_queue.put(event)
                time.sleep(0)
            except queue.Empty:
                pass # Expected if we dont have anything in the queue
            if(self.state == State.PLAY):
                try:
                    event = self.file_input_queue.get_nowait()
                    self.current_notes.update({event.event.note:event.event.type})
                    self.mixed_output_queue.put(event) # TODO CHA-PROC Switch to use Message and Comm system
                except queue.Empty:
                    pass # Expected if we dont have anything in the queue
        

    def deactivate(self):
        self.comm_system.deactivate()
        self.active = False
