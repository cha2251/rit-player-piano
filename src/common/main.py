from src.common.midi_event import MidiEvent
from src.mixing.mixing import Mixing
from src.output_queue.output_queue import OutputQueue
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
        print("Creating Output Subsystem")
        self.create_output()

        mido.set_backend("mido.backends.rtmidi")
        print("Using Mido backend: {}".format(mido.backend))

        self.output.select_device()

        self.output.play_test_tones(self.shared_queues.mixed_output_queue, 0.2)

        while True:
            self.output.check_queue(self.shared_queues.mixed_output_queue)

    def create_mixing(self):
        self.mixing = Mixing()

    def create_output(self):
        self.output = OutputQueue()

    def create_queues(self):
        self.shared_queues = SharedQueues()
        self.shared_queues.create_queues()


if __name__ == "__main__":
    main = Main()
    main.main()