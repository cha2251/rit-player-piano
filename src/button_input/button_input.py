import queue
import time
from threading import Thread
from pynput import keyboard

import mido
import queue
from threading import Thread
from src.common.midi_event import MidiEvent
from src.common.shared_queues import SharedQueues
import keyboard
import time

from src.common.midi_event import MidiEvent


class ButtonInput:
    button_input_queue: queue.Queue
    keyMap = dict
    default = {'q': 55, 'w': 56, 'e': 57, 'r': 58, 't': 59,
               'y': 60, 'u': 61, 'i': 62, 'o': 63, 'p': 64}

    """ Sets initial values of Thread
    button_input_queue: global queue responsible for carrying midi events to mixing subsystem
    keyMap: dictionary of key mappings for input interpretation, set to default if not given
    
    a keyboard listener from pynput is also created to detect key presses.
    """
    def __init__(self, button_input_queue, keyMap=None):
        self.button_input_queue = button_input_queue
        if keyMap is None:
            self.keyMap = self.default
        else:
            self.keyMap = keyMap
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    # Updates the keymap with a new set of mappings
    def change_map(self, keyMap):
        self.keyMap = keyMap

    # Updates a single key's mapping or adds a new key mapping if the key lacks a map
    def change_key(self, key, note):
        self.keyMap[key] = note

    # Removes an unneeded key from the key map
    def delete_key(self, key):
        self.keyMap.pop(key)

    # Enables keyboard listener while thread is active
    def run(self):
        self.listener.start()

    # Reacts to key presses and sends a midi event if the key is mapped
    def on_press(self, key):
        try:
            k = key.char
        except:
            k = key.name
        if k in self.keyMap.keys():
            note = self.keyMap[k]
            self.button_input_queue.put(
                MidiEvent(mido.Message('note_on', note=note, velocity=120), time.time()))

    # Reacts to key releases and sends a midi event if the key is mapped
    def on_release(self, key):
        try:
            k = key.char
        except:
            k = key.name
        if k in self.keyMap.keys():
            note = self.keyMap[k]
            self.button_input_queue.put(
                MidiEvent(mido.Message('note_off', note=note, velocity=120), time.time()))

    # Stops listener thread
    def deactivate(self):
        self.listener.stop()
