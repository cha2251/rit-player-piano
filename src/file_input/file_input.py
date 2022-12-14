import queue
from threading import Thread
from src.file_input.MIDI_file_class import MIDIFileObject

class FileInput(Thread):
    whitelisted_types = ['note_on','note_off']
    file_input_queue: queue.Queue = None

    def __init__(self, file_input_queue):
        Thread.__init__(self)
        self.file_input_queue = file_input_queue
    
    def run(self):
        self.copy_file_to_queue()
    
    def copy_file_to_queue(self):
        fileObject = self.openFile()
        while fileObject.has_next():
            message = fileObject.get_next_message()
            if message.event.type in self.whitelisted_types:
                self.file_input_queue.put(message)

    def openFile(self):
        return MIDIFileObject('ChamberOfSecrets-HedwigsTheme.mid') #TODO, remove hardcode