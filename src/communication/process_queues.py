from src.mixing.mixing_comm import MixingCommSystem
from src.output_queue.output_comm import OutputCommSystem
from src.user_interface.ui_comm import UICommSystem


class ProcessQueues:
    def __init__(self):
        self.mixing_to_comm = MixingCommSystem().output_queue
        self.comm_to_mixing = MixingCommSystem().input_queue
        self.ui_to_comm = UICommSystem().output_queue
        self.comm_to_ui = UICommSystem().input_queue
        self.output_to_comm = OutputCommSystem().output_queue
        self.comm_to_output = OutputCommSystem().input_queue
        self.all_queues = [
            self.mixing_to_comm, 
            self.comm_to_mixing, 
            self.ui_to_comm, 
            self.comm_to_ui,
            self.output_to_comm,
            self.comm_to_output]