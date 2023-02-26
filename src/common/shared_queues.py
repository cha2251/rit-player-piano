import queue
import multiprocessing


# Queues used internally in the Mixing process to communciate with File and Button systems
class SharedQueues:
    def __init__(self):
        self.file_input_queue = queue.Queue() 
        self.button_input_queue = queue.Queue()
