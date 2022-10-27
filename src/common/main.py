import time
from src.common.midi_event import MidiEvent
from src.mixing.mixing import Mixing
from src.common.shared_queues import SharedQueues
import mido
import threading


class Main:
    shared_queues = None
    mixing = None

    def main(self):
        print("Creating Shared Queues ")
        self.create_queues()
        print("Creating Mixing Subsystem")
        self.create_mixing()

        for i in range(1000):
            self.shared_queues.file_input_queue.put(MidiEvent(mido.Message('note_off',note=i%120),time.time()+i))
        
        mixingThread = threading.Thread(target=self.mixing.startup)
        mixingThread.start()

        outputThread = threading.Thread(target=self.test_output)
        outputThread.start()

        while(True):
            input()
            self.shared_queues.button_input_queue.put(MidiEvent(mido.Message('note_on',note=69),time.time()))

    def test_output(self):
        event = self.shared_queues.mixed_output_queue.get()
        while event.timestamp > time.time():
            pass
        print(event)

    def create_mixing(self):
        self.mixing = Mixing(self.shared_queues)

    def create_queues(self):
        self.shared_queues = SharedQueues()
        self.shared_queues.create_queues()


if __name__ == "__main__":
    main = Main()
    main.main()