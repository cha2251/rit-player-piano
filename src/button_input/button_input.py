import mido
import queue
from threading import Thread
from src.common.midi_event import MidiEvent
from src.common.shared_queues import SharedQueues
import keyboard
import time


class ButtonInput(Thread):
    button_input_queue: queue.Queue
    active = False

    def __init__(self, button_input_queue):
        Thread.__init__(self)
        self.button_input_queue = button_input_queue

    def run(self):
        self.active = True
        keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
        while self.active:
            for i in range(10):
                if keyboard.is_pressed(keys[i]):
                    self.button_input_queue.put(
                        MidiEvent(mido.Message('note_on', note=55 + i, velocity=120), time.time()))
                    self.button_input_queue.put(
                        MidiEvent(mido.Message('note_off', note=55 + i, velocity=120), time.time()+.5))

    def deactivate(self):
        self.active = False
