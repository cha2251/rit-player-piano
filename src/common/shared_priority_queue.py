from copy import deepcopy
import queue
from heapq import heappush, heappop
from multiprocessing.managers import SyncManager
from threading import Lock

class PeekingPriorityQueue(queue.Queue):
    '''Variant of a PriorityQueue that actually has a peek() function.'''

    accessLock = Lock() #Needed for non built-ins

    def _init(self, maxsize):
        self.queue = []

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        with self.accessLock:
            heappush(self.queue, item)

    def _get(self):
        with self.accessLock:
            return heappop(self.queue)

    def peek(self):
        return self.queue[0]

    def get_and_clear_queue(self):
        with self.accessLock:
            val = deepcopy(self.queue)
            self.queue.clear()
            return val
    
    def set_queue(self, queue):
        with self.accessLock:
            self.queue = deepcopy(queue)

class SharedQueueSyncManager(SyncManager):
    '''Manages the synchronization of Python objects in between processes'''
    def __init__(self):
        SyncManager.__init__(self)
        self.start()

SharedQueueSyncManager.register("PeekingPriorityQueue", PeekingPriorityQueue)  # Register a shared PriorityQueue