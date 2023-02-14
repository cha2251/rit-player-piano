from threading import Thread
import time
from src.communication.process_queues import ProcessQueues


class CommSystem(Thread):

    def __init__(self, process_queues:ProcessQueues):
        Thread.__init__(self)
        self.active = False
        self.all_queues = process_queues.all_queues

    def run(self):
        self.active = True
        self.startup()
        
    def startup(self):
        self.main_loop()

    def main_loop(self):
        while(self.active):
            for queue in self.all_queues:
                try:
                    message = queue.get_nowait()
                    self.send_message(message)
                except queue.Empty:
                    pass # Expected if we dont have anything in the queue
            time.sleep(0)
    
    def send_message(self, message):
        for queue in self.all_queues:
            queue.put(message)
    
    def deactivate(self):
        self.active = False