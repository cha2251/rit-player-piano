import queue
from threading import Lock, Thread
import time
from src.communication.messages import Message, MessageType


class LocalCommSystem(Thread):
    def __init__(self):
        self.handler_map = {MessageType : []} # Map of message types with list of function calls
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.active = False
        self.accessLock = Lock()

    # Overwrite new to only create an instance of this class
    # if there is not one already. If there is an instance
    # return a refernece to that instead. Implemented only
    # in children of this class
    ''''
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LocalCommSystem, cls).__new__(cls)
        return cls.instance
    '''
    
    def send(self, message : Message):
        self.output_queue.put(message)
    
    def registerListner(self, type : MessageType, function):
        with self.accessLock:
            if type in self.handler_map.keys():
                self.handler_map[type].append(function)
            else:
                self.handler_map[type] = [function]

    def callHandlers(self, message : Message):
        with self.accessLock:
            if type in self.handler_map.keys():
                for function in self.handler_map[message.type]:
                    function(message)
    
    def checkMessages(self):
        while self.active:
            try:
                message = self.input_queue.get_nowait()
                self.callHandlers(message)
                time.sleep(0)
            except queue.Empty:
                pass # Expected if we dont have anything in the queue
    
    def deactivate(self):
        self.active = False

    def run(self):
        self.active = True
        self.checkMessages()
