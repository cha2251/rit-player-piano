import sys
import time
from threading import Thread
from PyQt5.QtWidgets import QApplication
import src.user_interface.main_page
from src.common.midi_event import MidiEvent
from src.mixing.mixing import Mixing
from src.output_queue.output_queue import OutputQueue
from src.common.shared_queues import SharedQueues
from src.file_input.file_input import FileInput
from src.button_input.button_input import ButtonInput
import mido
import mido.backends.rtmidi  # Needed for windows builds w/ pyinstaller


class Main:
    shared_queues = None
    mixing = None
    file_input = None
    button_input = None
    output = None

    def __init__(self):
        pass

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
        self.button_input.start()
        self.mixing.start()

        #init UI
        x = Thread(target=self.init_UI, args=(self.shutdown,))
        x.start()


        #init UI
        x = Thread(target=self.init_UI, args=(self.shutdown,))
        x.start()


        print("Type `quit` to quit")

        while(True):
            if (False and input() == 'quit') or not x.is_alive():  # Change false when developing in console mode
                break
            # self.shared_queues.button_input_queue.put(MidiEvent(mido.Message('note_on',note=90,velocity=120),time.time()))
        
        self.shutdown()

    def shutdown(self):
        self.output.deactivate()
        self.button_input.deactivate()
        self.mixing.deactivate()
        self.file_input.deactivate()
        self.button_input.deactivate()
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

    def create_button_input(self):
        self.button_input = ButtonInput(self.shared_queues.button_input_queue)

    def init_UI(self, shutdown):
        app = QApplication([])
        style = """
        QWidget {
            background: #2a0b40;
        }
        QLabel{
            color: #fff;
            font: 40px;
        }
        QPushButton{
            color: #fff;
            background-color: #5b2185;
            border-style: outset;
            border-width: 2px;
            border-color: #792cb0;
            max-width: 50em;
            min-width: 5em;
            padding: 5px;
            font-family: "Times New Roman", Times, serif;
            font: bold 15px;
            border-radius: 10px;
        }
        QPushButton:hover{
            background: #792cb0;
        }
        QPushButton:pressed{
            border-style: inset;
        }
        """
        app.setStyleSheet(style)
        window = src.user_interface.main_page.MainPage(shutdown)
        window.show()
        app.exec_()



if __name__ == "__main__":
    main = Main()
    main.main()
