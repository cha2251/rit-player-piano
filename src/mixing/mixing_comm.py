from multiprocessing import Queue
import queue
from threading import Lock
from src.communication.local_comm_system import LocalCommSystem
from src.communication.messages import MessageType



class MixingCommSystem(LocalCommSystem):
    handler_map = {MessageType : []} # Map of message types with list of function calls
    input_queue : Queue
    output_queue : Queue
    active = False
    accessLock = Lock()
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LocalCommSystem, cls).__new__(cls)
        return cls.instance
    
    def set_queues(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue