from src.common.midi_event import MidiEvent
from src.mixing.mixing import Mixing
from src.common.shared_queues import SharedQueues
import mido


class Main:
    shared_queues = None
    mixing = None

    def main(self):
        print("Creating Shared Queues ")
        self.create_queues()
        print("Creating Mixing Subsystem")
        self.create_mixing()
        print("Sanity Check Pass: "+str(self.mixing.is_even(2)))
        input("Press Enter")

    def create_mixing(self):
        self.mixing = Mixing()

    def create_queues(self):
        self.shared_queues = SharedQueues()
        self.shared_queues.create_queues()


if __name__ == "__main__":
    main = Main()
    main.main()