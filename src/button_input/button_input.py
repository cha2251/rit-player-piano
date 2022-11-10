import mido
import queue
from threading import Thread


class ButtonInput(Thread):
    button_input_queue: queue.Queue

    def __init__(self, button_input_queue):
        Thread.__init__(self)
        self.button_input_queue = button_input_queue
        self.active = False

    def run(self):
        self.active = True
        while self.active:
            if True:  # replace with key check
                pass  # replace with queue addition

    def deactivate(self):
        self.active = False
