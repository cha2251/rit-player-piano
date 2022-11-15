from heapq import heappush, heappop
import queue
import multiprocessing

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
    pass

SharedQueueSyncManager.register("PeekingPriorityQueue", PeekingPriorityQueue)  # Register a shared PriorityQueue

def CreateSharedQueueSyncManager():
    m = SharedQueueSyncManager()
    m.start()
    return m


class SharedQueues:
    file_input_queue: queue.Queue = None # Default is FIFO
    button_input_queue: queue.Queue = None
    mixed_output_queue: PeekingPriorityQueue = None
    sync_manager: SharedQueueSyncManager = None

    def create_queues(self):
        self.sync_manager = CreateSharedQueueSyncManager()
        self.file_input_queue = queue.Queue() 
        self.button_input_queue = queue.Queue()
        self.mixed_output_queue = self.sync_manager.PeekingPriorityQueue()

    def deactivate(self):
        self.sync_manager.shutdown()
        self.sync_manager.join()
