import queue
from threading import Thread
import time
from src.common.midi_event import MidiEvent
from src.common.shared_queues import SharedQueues
import mido

class Mixing(Thread):
    class State():
        PLAY = 1
        PAUSE = 2
        STOP = 3
    
    file_input_queue: queue.Queue = None
    button_input_queue: queue.Queue = None
    mixed_output_queue: queue.PriorityQueue = None
    holding_queue: queue.PriorityQueue = None
    active = False
    state = State.STOP
    current_pause_time = 0
    total_pause_time = 0

    paused_notes = {}

    def __init__(self, shared_queues:SharedQueues):
        Thread.__init__(self)
        self.file_input_queue = shared_queues.file_input_queue
        self.button_input_queue = shared_queues.button_input_queue
        self.mixed_output_queue = shared_queues.mixed_output_queue
    
    def run(self):
        self.active = True
        self.startup()
        
    def startup(self):
        self.state = self.State.PLAY
        self.main_loop()

    def play(self):
        pass

    def pause(self):
        self.state = self.State.PAUSE
        self.current_pause_time= time.time()
        
        self.holding_queue = self.mixed_output_queue.get_and_clear_queue()

        for note in self.paused_notes.keys():
            if(self.paused_notes[note]=='note_on'):
                event = mido.Message('note_off', note=note)
                self.mixed_output_queue.put(MidiEvent(event, time.time()))
    
    def unpause(self):
        offset_time = time.time() - self.current_pause_time

        for note in self.paused_notes.keys():
            if(self.paused_notes[note]=='note_off'):
                event = mido.Message('note_on', note=note, velocity=120)
                self.mixed_output_queue.put(MidiEvent(mido.Message(event, time.time())))


        for event in self.holding_queue:
            event.addTime(offset_time)
        self.mixed_output_queue.set_queue(self.holding_queue)

        self.holding_queue.clear()

        self.total_pause_time += self.current_pause_time
        self.state = self.State.PLAY
    
    def stop(self):
        pass
    
    def play_pushed(self):
        if self.state is self.State.STOP:
            self.play()
        if self.state is self.State.PAUSE:
            self.unpause()

    def pause_pushed(self):
        if self.state is self.State.PLAY:
            self.pause()
        elif self.state is self.State.PAUSE:
            self.unpause()
    
    def stop_pushed(self):
        if self.state is self.State.PLAY:
            self.stop()
        elif self.state is self.State.PAUSE:
            self.stop()
    
    def main_loop(self):
        while(self.active):
            try:
                event = self.button_input_queue.get_nowait()
                self.mixed_output_queue.put(event)
                time.sleep(0)
            except queue.Empty:
                pass # Expected if we dont have anything in the queue
            if(self.state == self.State.PLAY):
                try:
                    event = self.file_input_queue.get_nowait()
                    event.addTime(self.total_pause_time)
                    self.paused_notes.update({event.event.note:event.event.type})
                    self.mixed_output_queue.put(event)
                except queue.Empty:
                    pass # Expected if we dont have anything in the queue
        

    def deactivate(self):
        self.active = False
