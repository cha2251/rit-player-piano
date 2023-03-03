import queue
import time
from threading import Thread
from pynput import keyboard
import mido
from src.button_input.controller import ControllerButton, XboxController

from src.common.midi_event import MidiEvent


class ButtonInput:
    button_input_queue: queue.Queue
    keyMap = dict
    default = {'q': [53,54,55], 'w': [56], 'e': [57], 'r': [58], 't': [59],
               'y': [60], 'u': [61], 'i': [62], 'o': [63], 'p': [64],
               ControllerButton.A: [65], ControllerButton.B: [66, 68, 70]}

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
        
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.keyboard_listener.start()
        self.controller = XboxController(self.add_controller_note)

    # Updates the keymap with a new set of mappings
    def change_map(self, keyMap):
        self.keyMap = keyMap

    # Updates a single key's mapping or adds a new key mapping if the key lacks a map
    def change_key(self, key, notes):
        # Check if chord or single note
        if isinstance(notes, list):
            self.keyMap[key] = notes
        else:
            self.keyMap[key] = [notes] # Make single note a chord

    def delete_key(self, key):
        self.keyMap.pop(key)

    def run(self):
        self.keyboard_listener.start()

    # Reacts to key presses and sends a midi event if the key is mapped
    def on_press(self, key):
        try:
            k = key.char
        except:
            k = key.name
        if k in self.keyMap.keys():
            for note in self.get_notes(k):
                self.button_input_queue.put(
                    MidiEvent(mido.Message('note_on', note=note, velocity=120), 0))

    # Reacts to key releases and sends a midi event if the key is mapped
    def on_release(self, key):
        try:
            k = key.char
        except:
            k = key.name
        if k in self.keyMap.keys():
            for note in self.get_notes(k):
                self.button_input_queue.put(
                    MidiEvent(mido.Message('note_off', note=note, velocity=120), 0))
            
    # Adds a note when a button on the controller is pressed
    def add_controller_note(self, button : ControllerButton, state):
        if state == 1:
            for note in self.get_notes(button):
                self.button_input_queue.put(
                    MidiEvent(mido.Message('note_on', note=note, velocity=120), 0))
        else:
            for note in self.get_notes(button):
                self.button_input_queue.put(
                    MidiEvent(mido.Message('note_off', note=note, velocity=0), 0))
            
    def get_notes(self, button : ControllerButton):
        try:
            return self.keyMap[button]
        except KeyError:
            return []

    # Stops listener thread
    def deactivate(self):
        self.controller.deactivate()
        self.keyboard_listener.stop()
