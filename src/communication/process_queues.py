import queue

class ProcessQueues:
    def __init__(self):
        self.mixing_to_comm = queue.Queue()
        self.comm_to_mixing = queue.Queue()
        self.ui_to_comm = queue.Queue()
        self.comm_to_ui = queue.Queue()
        self.output_to_comm = queue.Queue()
        self.comm_to_output = queue.Queue()
        self.all_queues = [
            self.mixing_to_comm, 
            self.comm_to_mixing, 
            self.ui_to_comm, 
            self.comm_to_ui,
            self.output_to_comm,
            self.comm_to_output]