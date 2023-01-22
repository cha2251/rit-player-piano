import queue
import multiprocessing
from src.common.shared_priority_queue import PeekingPriorityQueue, SharedQueueSyncManager

class SharedQueues:
    file_input_queue: queue.Queue = None # Default is FIFO
    button_input_queue: queue.Queue = None
    mixed_output_queue: PeekingPriorityQueue = None
    sync_manager: SharedQueueSyncManager = None

    def create_queues(self):
        self.sync_manager = SharedQueueSyncManager()
        self.file_input_queue = queue.Queue() 
        self.button_input_queue = queue.Queue()
        self.mixed_output_queue = self.sync_manager.PeekingPriorityQueue()

    def deactivate(self):
        self.sync_manager.shutdown()
        self.sync_manager.join()
