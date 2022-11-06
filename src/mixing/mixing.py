import queue
from threading import Thread
from time import sleep
import time
import mido

from src.common.shared_queues import SharedQueues

class Mixing(Thread):
    file_input_queue: queue.Queue = None
    button_input_queue: queue.Queue = None
    mixed_output_queue: queue.PriorityQueue = None
    active = False

    def __init__(self, shared_queues:SharedQueues):
        Thread.__init__(self)
        self.file_input_queue = shared_queues.file_input_queue
        self.button_input_queue = shared_queues.button_input_queue
        self.mixed_output_queue = shared_queues.mixed_output_queue
    
    def run(self):
        self.active = True
        self.startup()
        
    def startup(self):
        self.main_loop()
    
    def main_loop(self):
        while(self.active):
            try:
                event = self.button_input_queue.get(timeout=.005) # We need a timeout or else we hang here on shutdown
                self.mixed_output_queue.put(event)
            except queue.Empty:
                pass # Expected if we dont have anything in the queue
            try:
                event = self.file_input_queue.get(timeout=.005)
                self.mixed_output_queue.put(event)
            except queue.Empty:
                pass # Expected if we dont have anything in the queue
        

    def deactivate(self):
        self.active = False