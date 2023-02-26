# freeze_support must run before imports
from multiprocessing import Process, freeze_support
freeze_support() # Needed for mulitple processors with pyinstaller

from queue import Queue
from PyQt5.QtWidgets import QApplication
from src.common.shared_priority_queue import SharedQueueSyncManager
from src.communication.comm_system import CommSystem
import src.user_interface.main_page
from src.mixing.mixing import Mixing
from src.output_queue.output_queue import OutputQueue
import mido
import mido.backends.rtmidi # Needed for windows builds w/ pyinstaller

class Main:
    mixing = None
    output = None
    comm_system = None

    def __init__(self):
        pass

    def main(self):
        mido.set_backend("mido.backends.rtmidi")
        print("Using Mido backend: {}".format(mido.backend))
        
        self.register_queues()

        print("Starting Comm Process")
        Process(target=self.create_comm).start()
        print("Starting Output Process")
        Process(target=self.create_output).start()
        print("Starting Mixing Process")
        Process(target=self.create_mixing).start()
        
        print("Starting UI Process")
        self.init_UI()

        self.shutdown()
        

    def shutdown(self):
        #TODO SEND SHUTDOWN MESSAGE
        print("System Shutdown Succesfully")

    def create_comm(self):
        self.comm_system = CommSystem()
        self.comm_system.run()

    def create_mixing(self):
        self.mixing = Mixing()

    def create_output(self):
        self.output = OutputQueue()
        self.output.select_device()

    def register_queues(self):
        SharedQueueSyncManager()
        SharedQueueSyncManager.register("PeekingPriorityQueue", Queue)  # Register Queue as a shareable type

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
        window = src.user_interface.main_page.MainPage(self.shutdown,self.output)
        window.show()
        app.exec_()


if __name__ == "__main__":
    freeze_support()
    main = Main()
    main.main()