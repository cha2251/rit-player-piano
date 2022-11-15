from copy import deepcopy
import queue
from threading import Thread
import time
from src.common.midi_event import MidiEvent
from src.common.shared_queues import SharedQueues

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
        self.mixed_output_queue.queue.clear()
    
    def unpause(self):
        self.state = self.State.PLAY
        offset_time = time.time() - self.pause_time
        for event in self.holding_queue:
            self.mixed_output_queue.put(MidiEvent(event.event,event.timestamp+offset_time))
        self.holding_queue.clear()
    
    def main_loop(self):
        while(self.active):
            if(self.state == self.State.PLAY):
                try:
                    event = self.button_input_queue.get(timeout=0) # We need a timeout or else we hang here on shutdown
                    self.mixed_output_queue.put(event)
                    time.sleep(0)
                except queue.Empty:
                    pass # Expected if we dont have anything in the queue
                try:
                    event = self.file_input_queue.get(timeout=0)
                    self.mixed_output_queue.put(event)
                except queue.Empty:
                    pass # Expected if we dont have anything in the queue
        

    def deactivate(self):
        self.active = False