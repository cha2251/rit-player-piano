import time
from threading import Thread

import mido

from src.common.midi_event import MidiEvent


class KeyListener(Thread):

    def __init__(self, key, note, queue):
        Thread.__init__(self)
        self.queue = queue
        self.key = key
        self.note = note

    def start(self):
        self.listener.start()

