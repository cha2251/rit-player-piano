from queue import Empty
from threading import Thread
import time
from src.mixing.mixing_comm import MixingCommSystem
from src.output_queue.output_comm import OutputCommSystem
from src.user_interface.ui_comm import UICommSystem

class CommSystem(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.active = False
        self.get_all_queues()

    def get_all_queues(self):
        mixing_comm = MixingCommSystem()
        ui_comm = UICommSystem()
        output_comm = OutputCommSystem()
        self.out_queues = [ # Queues are named relative to local system
            mixing_comm.input_queue,
            ui_comm.input_queue,
            output_comm.input_queue
        ]
        self.in_queues = [
            mixing_comm.output_queue,
            ui_comm.output_queue,
            output_comm.output_queue,
        ]

    def run(self):
        self.active = True
        self.startup()
        
    def startup(self):
        self.main_loop()

    def main_loop(self):
        while(self.active):
            for queue in self.in_queues:
                try:
                    message = queue.get_nowait()
                    self.send_message(message)
                except Empty:
                    pass # Expected if we dont have anything in the queue
            time.sleep(0)
    
    def send_message(self, message):
        for queue in self.out_queues:
            queue.put(message)
    
    def deactivate(self):
        self.active = False