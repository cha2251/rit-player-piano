import time
from threading import Thread

import mido
from pynput import keyboard

from src.common.midi_event import MidiEvent


class KeyListener(Thread):

    def __init__(self, key, note, queue):
        Thread.__init__(self)
        self.queue = queue
        self.key = key
        self.note = note
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def start(self):
        self.listener.start()
        self.listener.join()

    def on_press(self, key):
        print('input received')
        if key == self.key:
            self.queue.put(
                MidiEvent(mido.Message('note_on', note=self.note, velocity=120), time.time()))

    def on_release(self, key):
        if key == self.key:
            self.queue.put(
                MidiEvent(mido.Message('note_off', note=self.note, velocity=120), time.time()))
