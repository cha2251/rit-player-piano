import queue
from heapq import heappush, heappop
from multiprocessing.managers import SyncManager

class PeekingPriorityQueue(queue.Queue):
    '''Variant of a PriorityQueue that actually has a peek() function.'''

    def _init(self, maxsize):
        self.queue = []

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        heappush(self.queue, item)

    def _get(self):
        return heappop(self.queue)

    def peek(self):
        return self.queue[0]

class SharedQueueSyncManager(SyncManager):
    '''Manages the synchronization of Python objects in between processes'''
    def __init__(self):
        SyncManager.__init__(self)
        self.start()

SharedQueueSyncManager.register("PeekingPriorityQueue", PeekingPriorityQueue)  # Register a shared PriorityQueue