import queue
import time
from threading import Thread
from pynput import keyboard

import mido

from src.button_input.KeyListener import KeyListener
from src.common.midi_event import MidiEvent


class ButtonInput(Thread):
    button_input_queue: queue.Queue
    active = False
    keyMap = dict
    default = {'q': 55, 'w': 56, 'e': 57, 'r': 58, 't': 59,
               'y': 60, 'u': 61, 'i': 62, 'o': 63, 'p': 64}

    def __init__(self, button_input_queue, keyMap=None):
        Thread.__init__(self)
        self.button_input_queue = button_input_queue
        if keyMap is None:
            self.keyMap = self.default
        else:
            self.keyMap = keyMap
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def changeMap(self, keyMap):
        self.keyMap = keyMap

    def changeKey(self, key, note):
        self.keyMap[key] = note

    def run(self):
        self.active = True
        self.listener.start()
        self.listener.join()
        while self.active:
            continue

    def on_press(self, key):
        if key.char in self.keyMap.keys():
            note = self.keyMap[key.char]
            self.button_input_queue.put(
                MidiEvent(mido.Message('note_on', note=note, velocity=120), time.time()))

    def on_release(self, key):
        if key.char in self.keyMap.keys():
            note = self.keyMap[key.char]
            self.button_input_queue.put(
                MidiEvent(mido.Message('note_off', note=note, velocity=120), time.time()))

    def deactivate(self):
        self.active = False
