from copy import deepcopy
import queue
import copy
from heapq import heappush, heappop, nsmallest
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
        try:
            return self.queue[0]
        except:
            return None

    def get_and_clear_queue(self):
        with self.accessLock:
            val = deepcopy(self.queue)
            self.queue.clear()
            return val

    def set_queue(self, queue):
        with self.accessLock:
            self.queue = deepcopy(queue)
    def copy_of_queue(self):
        return copy.copy(self.queue)

    def peekn(self, n):
        try:
            return nsmallest(n, self.queue)
        except:
            return None

    def copy(self):
        # new_queue = PeekingPriorityQueue()
        # new_queue.queue = self.queue.copy()

        return self.queue.copy()

class SharedQueueSyncManager(SyncManager):
    '''Manages the synchronization of Python objects in between processes'''
    def __init__(self):
        SyncManager.__init__(self)
        self.start()

SharedQueueSyncManager.register("PeekingPriorityQueue", PeekingPriorityQueue)  # Register a shared PriorityQueue