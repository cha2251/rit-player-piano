import queue
import time
from threading import Thread

import mido

from src.button_input.KeyListener import KeyListener
from src.common.midi_event import MidiEvent


class ButtonInput(Thread):
    button_input_queue: queue.Queue
    active = False
    keyMap = dict
    default = {'q': 55, 'w': 56, 'e': 57, 'r': 58, 't': 59,
               'y': 60, 'u': 61, 'i': 62, 'o': 63, 'p': 64}
    listeners = []

    def __init__(self, button_input_queue, keyMap=None):
        Thread.__init__(self)
        self.button_input_queue = button_input_queue
        if keyMap is None:
            self.keyMap = self.default
        else:
            self.keyMap = keyMap
        for k, v in self.keyMap.items():
            self.listeners.append(KeyListener(k, v, button_input_queue))

    def changeMap(self, keyMap):
        self.keyMap = keyMap

    def changeKey(self, key, note):
        self.keyMap[key] = note

    def run(self):
        self.active = True
        for i in self.listeners:
            i.start()
        while self.active:
            continue

    def deactivate(self):
        self.active = False
