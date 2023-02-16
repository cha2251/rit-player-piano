import queue
import multiprocessing
from src.common.shared_priority_queue import PeekingPriorityQueue, SharedQueueSyncManager

class SharedQueues:
    def create_queues(self):
        self.sync_manager = SharedQueueSyncManager()
        self.file_input_queue = queue.Queue() 
        self.button_input_queue = queue.Queue()
        self.mixed_output_queue = self.sync_manager.PeekingPriorityQueue()

        SharedQueues.mixed_output_queue = self.mixed_output_queue

    def deactivate(self):
        self.sync_manager.shutdown()
        self.sync_manager.join()
