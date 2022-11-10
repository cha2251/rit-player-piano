import time
from src.common.midi_event import MidiEvent
from src.mixing.mixing import Mixing
from src.output_queue.output_queue import OutputQueue
from src.common.shared_queues import SharedQueues
from src.file_input.file_input import FileInput
from src.button_input.button_input import ButtonInput
import mido


class Main:
    shared_queues = None
    mixing = None
    file_input = None
    button_input = None

    def main(self):
        mido.set_backend("mido.backends.rtmidi")
        print("Using Mido backend: {}".format(mido.backend))

        print("Creating Shared Queues")
        self.create_queues()
        print("Creating Output Subsystem")
        self.create_output()
        print("Creating File Subsystem")
        self.create_file_input()
        print("Creating Button Subsystem")
        self.create_button_input()
        print("Creating Mixing Subsystem")
        self.create_mixing()

        self.output.start()
        self.file_input.start()
        self.mixing.start()
        self.button_input.start()
        
        # self.output.play_test_tones(self.shared_queues.mixed_output_queue, 0.2)

        print("Type `quit` to quit")

        while(True):
            if input() == 'quit':
                break
        
        self.shutdown()

    def shutdown(self):
        self.output.signal_stop()
        self.button_input.deactivate()
        self.mixing.deactivate()
        print("System Shutdown Succesfully")

    def create_mixing(self):
        self.mixing = Mixing(self.shared_queues)

    def create_output(self):
        self.output = OutputQueue(self.shared_queues.mixed_output_queue)
        self.output.select_device()

    def create_queues(self):
        self.shared_queues = SharedQueues()
        self.shared_queues.create_queues()

    def create_file_input(self):
        self.file_input = FileInput(self.shared_queues.file_input_queue)

    def create_button_input(self):
        self.button_input = ButtonInput(self.shared_queues.button_input_queue)


if __name__ == "__main__":
    main = Main()
    main.main()