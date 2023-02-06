import queue
from threading import Lock, Thread
from src.file_input.MIDI_file_class import MIDIFileObject
import time

class FileInput(Thread):
    whitelisted_types = ['note_on','note_off']
    file_input_queue: queue.Queue = None
    filename = None
    fileObject = None
    active = False
    accessLock = Lock()

    def __init__(self, file_input_queue):
        Thread.__init__(self)
        self.file_input_queue = file_input_queue
    
    def run(self):
        self.active = True
        self.copy_file_to_queue()
    
    def copy_file_to_queue(self):
        while self.active:
            while self.filename is not None:
                with self.accessLock:
                    if self.fileObject is None:
                        self.fileObject = MIDIFileObject(self.filename)
                    if self.fileObject.has_next():
                        message = self.fileObject.get_next_message()
                        if message.event.type in self.whitelisted_types:
                            self.file_input_queue.put(message)
                            time.sleep(0)
            time.sleep(0)

    def openFile(self,filename):
        with self.accessLock:
            self.file_input_queue.queue.clear()

            if not filename.endswith(".mid"):
                filename += ".mid"

            self.fileObject = None
            self.filename = filename

    def deactivate(self):
        self.active = False
