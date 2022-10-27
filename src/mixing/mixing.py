import queue
from time import sleep
import mido

from src.common.shared_queues import SharedQueues

class Mixing:
    file_input_queue: queue.Queue = None
    button_input_queue: queue.Queue = None
    mixed_output_queue: queue.PriorityQueue = None

    def __init__(self, shared_queues:SharedQueues):
        self.file_input_queue = shared_queues.file_input_queue
        self.button_input_queue = shared_queues.button_input_queue
        self.mixed_output_queue = shared_queues.mixed_output_queue

    def startup(self):
        self.copy_file_to_output()
        self.main_loop()
    
    def main_loop(self):
        while(True):
            event = self.button_input_queue.get()
            self.mixed_output_queue.put(event)

    def copy_file_to_output(self):
        while(self.file_input_queue.qsize() != 0):
            self.mixed_output_queue.put(self.file_input_queue.get())