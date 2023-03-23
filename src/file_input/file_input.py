import json
import os
import queue
from threading import Lock, Thread
from src.communication.messages import Message, MessageType, PianoAssistPlaying, Song
from src.button_input import controller
from src.file_input.MIDI_file_class import MIDIFileObject
import time

from src.mixing.mixing_comm import MixingCommSystem

class FileInput(Thread):
    whitelisted_types = ['note_on','note_off']
    file_input_queue: queue.Queue = None
    file_output_queue: queue.Queue = None
    filename = None
    fileObject = None
    active = False
    accessLock = Lock()
    hand_to_play = PianoAssistPlaying.BOTH.value

    def __init__(self, file_input_queue, file_output_queue):
        Thread.__init__(self)
        self.file_input_queue = file_input_queue
        self.file_output_queue = file_output_queue
        self.comm_system = MixingCommSystem()
    
    def run(self):
        self.registerCallbacks()
        self.active = True
        self.copy_file_to_queue()
    
    def registerCallbacks(self):        
        self.comm_system.registerListener(MessageType.SET_HAND_TO_PLAY, self.set_hand_to_play)
        self.comm_system.registerListener(MessageType.SONG_UPDATE, self.openFile)
        self.comm_system.registerListener(MessageType.STORE_BUTTON_MAPPING, self.store_button_mappings)
    
    def copy_file_to_queue(self):
        while self.active:
            while self.filename is not None:
                with self.accessLock:
                    if self.fileObject is None:
                        MIDIFileObject.hand_to_play = self.hand_to_play
                        self.fileObject = MIDIFileObject(self.filename)         
                        self.comm_system.send(Message(MessageType.SET_DURATION, self.fileObject.get_end_time()))
                    if self.fileObject.has_next():
                        message = self.fileObject.get_next_message()
                        if message.event.type in self.whitelisted_types:
                            self.file_input_queue.put(message)
                            time.sleep(0)
            time.sleep(0)

    def openFile(self,message : Message):
        filename = message.data
        with self.accessLock:
            self.file_input_queue.queue.clear()

            if filename == Song.FREEPLAY:
                self.filename = None
                self.fileObject = None
                return

            if not filename.endswith(".mid"):
                filename += ".mid"

            self.fileObject = None
            self.filename = filename

    def deactivate(self):
        self.active = False
        self.filename = None
        self.fileObject = None

    def set_hand_to_play(self, message : Message):
        print(f'Update hand (in file_input.py): {message.data}')
        self.hand_to_play = message.data

    def store_button_mappings(self, message : Message):
        """ Depending on the format of the data, we will store them in a file.
        """
        file_name = os.path.join(os.path.dirname(__file__), "..", "..", "config_files", "button_mappings.json")

        with open(file_name, "r+") as f:
            file_data = json.load(f)
            file_data["mappings"].append(message.data)
            f.seek(0)
            json.dump(file_data, f, indent=4, default=controller.serialize_enum)


    
