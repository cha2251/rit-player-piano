import queue

class SharedQueues:
    def create_queues(self):
        self.file_input_queue = queue.Queue() 
        self.button_input_queue = queue.Queue()
        self.mixed_output_queue = queue.PriorityQueue() # Sorted based on timestamp