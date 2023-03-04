# freeze_support must run before imports
from multiprocessing import Process, freeze_support, Queue
from PyQt5.QtWidgets import QApplication
from src.communication.comm_system import CommSystem
from src.communication.messages import Message, MessageType
import src.user_interface.main_page
from src.mixing.mixing import Mixing
from src.output_queue.output_queue import OutputQueue
import mido
import mido.backends.rtmidi # Needed for windows builds w/ pyinstaller

CONSOLE_MODE = True  # Set to True to allow for console commands


class Main:
    def __init__(self):
        pass

    def main(self):
        mido.set_backend("mido.backends.rtmidi")
        print("Using Mido backend: {}".format(mido.backend))
        
        self.create_queues()
        print("Creating Comm Subsystem")
        self.create_comm()
        print("Creating Output Subsystem")
        self.create_output()
        print("Creating File Subsystem")
        self.create_file_input()
        print("Creating Button Subsystem")
        self.create_button_input()
        print("Creating Mixing Subsystem")
        self.create_mixing()

        self.comm_system.start()
        self.output.start()
        self.file_input.start()
        self.button_input.run()
        self.mixing.start()

        # init UI
        x = Thread(target=self.init_UI)
        x.start()

        # init UI
        x = Thread(target=self.init_UI, args=(self.shutdown,))
        x.start()

        print("Type `quit` to quit")

        while (CONSOLE_MODE and x.is_alive()):
            command = input()
            if command == 'quit':
                break
            if command == 'off':
                self.file_input.deactivate()
                self.shared_queues.file_input_queue.queue.clear()
            if command == 'pause':
                self.mixing.pause_pushed()
            if command == 'play':
                self.mixing.play_pushed()
            if command == 'stop':
                self.mixing.stop_pushed()

        while (x.is_alive()):  # Do not shutdown until UI is closed
            pass

        self.shutdown()


    def create_comm(self, input_queues, output_queues):
        self.comm_system = CommSystem(output_queues, input_queues) # Switch due to naming convetions
        self.comm_system.run()

    def create_mixing(self, input_queue, output_queue):
        self.mixing = Mixing(input_queue, output_queue)
        self.mixing.start()

    def create_output(self, input_queue, output_queue):
        self.output = OutputQueue(input_queue, output_queue)
        self.output.run()

    def create_queues(self):
        # Queues are named relative to local system
        self.mixing_input_queue = Queue()
        self.ui_input_queue = Queue()
        self.output_input_queue = Queue()
        self.mixing_output_queue = Queue()
        self.ui_output_queue = Queue()
        self.output_output_queue = Queue()

    def destroy_queues(self):
        self.mixing_input_queue.close()
        self.ui_input_queue.close()
        self.output_input_queue.close()
        self.mixing_output_queue.close()
        self.ui_output_queue.close()
        self.output_output_queue.close()

    def init_UI(self):
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
        window = src.user_interface.main_page.MainPage(self.ui_input_queue, self.ui_output_queue)
        window.show()
        app.exec_()
        self.destroy_queues()

if __name__ == "__main__":
    freeze_support()
    main = Main()
    main.main()