import time
from src.common.midi_event import MidiEvent
from src.mixing.mixing import Mixing
from src.output_queue.output_queue import OutputQueue
from src.common.shared_queues import SharedQueues
from src.file_input.file_input import FileInput
import mido
import mido.backends.rtmidi # Needed for windows builds w/ pyinstaller


class Main:
    shared_queues = None
    mixing = None
    file_input = None

    def main(self):
        mido.set_backend("mido.backends.rtmidi")
        print("Using Mido backend: {}".format(mido.backend))

        print("Creating Shared Queues")
        self.create_queues()
        print("Creating Output Subsystem")
        self.create_output()
        print("Creating File Subsystem")
        self.create_file_input()
        print("Creating Mixing Subsystem")
        self.create_mixing()

        self.output.start()
        self.mixing.start()
        self.file_input.start()

        print("Type `quit` to quit")

        while(True):
            if input() == 'quit':
                break
            self.shared_queues.button_input_queue.put(MidiEvent(mido.Message('note_on',note=90,velocity=120),time.time()))
        
        self.shutdown()

    def shutdown(self):
        self.output.deactivate()
        self.mixing.deactivate()
        self.shared_queues.deactivate()
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


if __name__ == "__main__":
    main = Main()
    main.main()