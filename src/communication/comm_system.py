from queue import Empty
from threading import Thread
import time
from src.communication.messages import MessageType
from src.mixing.mixing_comm import MixingCommSystem
from src.output_queue.output_comm import OutputCommSystem
from src.user_interface.ui_comm import UICommSystem

class CommSystem():
    def __init__(self, input_queues, output_queues):
        Thread.__init__(self)
        self.active = False
        self.input_queues = input_queues
        self.output_queues = output_queues


    def run(self):
        self.active = True
        self.startup()
        
    def startup(self):
        self.main_loop()

    def main_loop(self):
        while(self.active):
            for queue in self.input_queues:
                try:
                    message = queue.get_nowait()
                    print("ECHOING MESSAGE"+str(message))
                    self.send_message(message)

                    if message.type == MessageType.SYSTEM_STOP:
                        self.deactivate()
                except Empty:
                    pass # Expected if we dont have anything in the queue
            time.sleep(0)
    
    def send_message(self, message):
        for queue in self.output_queues:
            queue.put(message)
    
    def deactivate(self):
        print("Comm System Deactivated")
        self.active = False