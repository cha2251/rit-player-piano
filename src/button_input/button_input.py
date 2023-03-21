import queue
import time
from threading import Thread
from pynput import keyboard
import mido
from src.button_input.controller import ControllerButton, XboxController

from src.common.midi_event import MidiEvent
from src.communication.messages import Message, MessageType
from src.mixing.mixing_comm import MixingCommSystem


class ButtonInput:
    button_input_queue: queue.Queue
    keyMap = dict
    default = {'q': [53,54,55], 'w': [56], 'e': [57], 'r': [58], 't': [59], 'y': [60],
                ControllerButton.RightTrigger: [60],
                ControllerButton.Y: [61], 
                ControllerButton.LeftTrigger: [62],
                ControllerButton.X: [63],
                ControllerButton.LeftBumper: [64],
                ControllerButton.RightDPad: [65],
                ControllerButton.B: [66],
                ControllerButton.UpDPad: [67],
                ControllerButton.A: [68],
                ControllerButton.RightThumb: [69],
                ControllerButton.RightBumper: [70],
                ControllerButton.LeftThumb: [71]
                }
    
    string_note_mapping = {
            "c3": 48, # 3rd C
            "c#3": 49,
            "d3": 50,
            "d#3": 51,
            "e3": 52,
            "f3": 53,
            "f#3": 54,
            "g3": 55,
            "g#3": 56,
            "a3": 57,
            "a#3": 58,
            "b3": 59,
            "c4": 60, # Middle C
            "c#4": 61,
            "d4": 62,
            "d#4": 63,
            "e4": 64,
            "f4": 65,
            "f#4": 66,
            "g4": 67,
            "g#4": 68,
            "a4": 69,
            "a#4": 70,
            "b4": 71,
            "c5": 72, # 5th C
        }

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
        self.controller = XboxController(self.on_controller_update)
        self.comm_system = MixingCommSystem()
        self.comm_system.registerListener(MessageType.BUTTON_CONFIG_UPDATE, self.change_map)

    # Updates the keymap with a new set of mappings
    def change_map(self, message : Message):
        new_map = message.data
        self.keyMap = {} #wipe old mapping
        for key_name in new_map.keys():
            if(len(new_map[key_name])>0):
                self.change_key(key=new_map[key_name][0],notes=self.string_note_mapping[key_name])
        print(self.keyMap)

    # Updates a single key's mapping or adds a new key mapping if the key lacks a map
    def change_key(self, key, notes):
        # Check if chord or single note
        if isinstance(notes, list):
            if key in self.keyMap.keys():
                self.keyMap[key].append(notes)
            else:
                self.keyMap[key] = notes
        else:
            if key in self.keyMap.keys():
                self.keyMap[key].append(notes) # Make note a chord
            else:
                self.keyMap[key] = [notes]

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
    def on_controller_update(self, button : ControllerButton, state):
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
