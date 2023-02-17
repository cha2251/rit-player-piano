from queue import Queue
from threading import Thread
from src.communication.messages import MessageType


class LocalCommSystem(Thread):
    handler_map = {MessageType : []} # Map of message types with list of function calls
    input_queue : Queue
    output_queue : Queue

    # Overwrite new to only create an instance of this class
    # if there is not one already. If there is an instance
    # return a refernece to that instead
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LocalCommSystem, cls).__new__(cls)
        return cls.instance