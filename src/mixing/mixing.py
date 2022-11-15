from copy import deepcopy
import queue
from threading import Thread
import time
from src.common.midi_event import MidiEvent
from src.common.shared_queues import SharedQueues
import mido

class Mixing(Thread):
    class State():
        PLAY = 1
        PAUSE = 2
        STOP = 3
    
    file_input_queue: queue.Queue = None
    button_input_queue: queue.Queue = None
    mixed_output_queue: queue.PriorityQueue = None
    holding_queue: queue.PriorityQueue = None
    active = False
    state = State.STOP
    pause_time = 0

    paused_notes = {}

    def __init__(self, shared_queues:SharedQueues):
        Thread.__init__(self)
        self.file_input_queue = shared_queues.file_input_queue
        self.button_input_queue = shared_queues.button_input_queue
        self.mixed_output_queue = shared_queues.mixed_output_queue
    
    def run(self):
        self.active = True
        self.startup()
        
    def startup(self):
        self.state = self.State.PLAY
        self.main_loop()

    def pause(self):
        self.state = self.State.PAUSE
        self.pause_time= time.time()
        with self.mixed_output_queue.mutex: #Thread safe
            self.holding_queue = deepcopy(self.mixed_output_queue.queue)

        for note in self.paused_notes.keys():
            if(self.paused_notes[note]=='note_on'):
                self.mixed_output_queue.put(
                        MidiEvent(mido.Message('note_off', note, velocity=0), time.time()))

        self.mixed_output_queue.queue.clear()
    
    def unpause(self):
        self.state = self.State.PLAY
        offset_time = time.time() - self.pause_time
        for event in self.holding_queue:
            self.mixed_output_queue.put(MidiEvent(event.event,event.timestamp+offset_time))
        
        for note in self.paused_notes.keys():
            if(self.paused_notes[note]=='note_off'):
                self.mixed_output_queue.put(
                        MidiEvent(mido.Message('note_on', note, velocity=120), time.time()))

        self.holding_queue.clear()
    
    def main_loop(self):
        while(self.active):
            try:
                event = self.button_input_queue.get(timeout=.005) # We need a timeout or else we hang here on shutdown
                self.mixed_output_queue.put(event)
                time.sleep(0)
            except queue.Empty:
                pass # Expected if we dont have anything in the queue
            if(self.state == self.State.PLAY):
                try:
                    event = self.file_input_queue.get(timeout=.005)
                    self.paused_notes.update({event.event.note:event.event.type})
                    self.mixed_output_queue.put(event)
                except queue.Empty:
                    pass # Expected if we dont have anything in the queue
        

    def deactivate(self):
        self.active = False