import queue

class SharedQueues:
    file_input_queue: queue.Queue = None # Default is FIFO
    button_input_queue: queue.Queue = None
    mixed_output_queue: queue.PriorityQueue = None # Sorted based on timestamp

    def create_queues(self):
        self.file_input_queue = queue.Queue() 
        self.button_input_queue = queue.Queue()
        self.mixed_output_queue = queue.PriorityQueue()