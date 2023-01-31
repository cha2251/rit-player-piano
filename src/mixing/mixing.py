import queue
from threading import Thread
import time
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
                event = self.button_input_queue.get_nowait()
                self.mixed_output_queue.put(event)
            except queue.Empty:
                pass # Expected if we dont have anything in the queue
            try:
                event = self.file_input_queue.get_nowait()
                self.mixed_output_queue.put(event)
            except queue.Empty:
                pass # Expected if we dont have anything in the queue

            # This yields this thread temporarily so that other threads don't get starved
            time.sleep(0)

    def deactivate(self):
        self.active = False
