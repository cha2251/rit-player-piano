import queue
from threading import Thread
import time
from src.button_input.button_input import ButtonInput
from src.file_input.file_input import FileInput
from src.mixing.mixing_comm import MixingCommSystem
from src.communication.messages import Message, MessageType, PlayingState
import mido

class Mixing(Thread):
    file_input_queue = queue.Queue()
    button_input_queue = queue.Queue()
    holding_queue: queue.PriorityQueue = None
    active = False
    state = PlayingState.STOP

    current_notes = {}

    def __init__(self, input_queue, output_queue):
        Thread.__init__(self)
        self.comm_system = MixingCommSystem()
        self.comm_system.set_queues(input_queue, output_queue)
        self.comm_system.start()
        
    
    def run(self):
        self.active = True
        self.file_input = FileInput(self.file_input_queue)
        self.file_input.start()
        self.button_input = ButtonInput(self.button_input_queue)
        self.startup()
        
    def startup(self):
        self.registerCallbacks()
        self.main_loop()

    def registerCallbacks(self):
        self.comm_system.registerListener(MessageType.STATE_UPDATE, self.stateChanged)
        self.comm_system.registerListener(MessageType.MODE_UPDATE, self.modeChanged)
        self.comm_system.registerListener(MessageType.SONG_UPDATE, self.songChanged)
        self.comm_system.registerListener(MessageType.SYSTEM_STOP, self.deactivate)

    def stateChanged(self, message : Message):
        if message.data == PlayingState.PLAY:
            self.play_pushed()
        if message.data == PlayingState.PAUSE:
            self.pause_pushed()
        if message.data == PlayingState.STOP:
            self.stop_pushed()

    def songChanged(self, message : Message):
        self.stop_pushed() # Mixing does not care about song name, but should stop current song

    def modeChanged(self, message : Message):
        pass #TODO Implement when mutiple play modes are enabled

    def play(self):
        self.state = PlayingState.PLAY

    def play_pushed(self):
        if self.state is PlayingState.STOP:
            self.play()
        if self.state is PlayingState.PAUSE:
            self.unpause()

    def pause_pushed(self):
        if self.state is PlayingState.PLAY:
            self.pause()
        elif self.state is PlayingState.PAUSE:
            self.unpause()
    
    def stop_pushed(self):
        if self.state is PlayingState.PLAY:
            self.stop()
        elif self.state is PlayingState.PAUSE:
            self.stop()

    def pause(self):
        self.state = PlayingState.PAUSE

        for note in self.current_notes.keys():
            if(self.current_notes[note]=='note_on'):
                event = mido.Message('note_off', note=note)
                self.comm_system.send(Message(MessageType.OUTPUT_QUEUE_UPDATE,event))
    
    def unpause(self):
        self.state = PlayingState.PLAY
    
    def stop(self):
        self.state = PlayingState.STOP

        for note in self.current_notes.keys():
            if(self.current_notes[note]=='note_on'):
                event = mido.Message('note_off', note=note)
                self.comm_system.send(Message(MessageType.OUTPUT_QUEUE_UPDATE,event))
    
    def main_loop(self):
        while(self.active):
            try:
                event = self.button_input_queue.get_nowait()
                self.comm_system.send(Message(MessageType.OUTPUT_QUEUE_UPDATE,event))
            except queue.Empty:
                pass # Expected if we dont have anything in the queue
            if(self.state == PlayingState.PLAY):
                try:
                    event = self.file_input_queue.get_nowait()
                    self.current_notes.update({event.event.note:event.event.type})
                    self.comm_system.send(Message(MessageType.OUTPUT_QUEUE_UPDATE,event))
                except queue.Empty:
                    pass # Expected if we dont have anything in the queue
            time.sleep(0)
        

    def deactivate(self, message=None):
        print("Mixing System Deactivated")
        self.active = False
        self.file_input.deactivate()
        self.button_input.deactivate()
