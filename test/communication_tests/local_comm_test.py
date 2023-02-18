from src.communication.local_comm_system import LocalCommSystem
from src.mixing.mixing_comm import MixingCommSystem
from src.output_queue.output_comm import OutputCommSystem
from src.user_interface.ui_comm import UICommSystem

class TestSingleton:
    def test_singleton(self):
        instance1 = MixingCommSystem()
        instance2 = MixingCommSystem()

        assert instance1 is instance2

    def test_implemented_singleton(self):
        instance1 = MixingCommSystem()
        instance2 = OutputCommSystem()
        instance3 = UICommSystem()


        assert instance1 is not instance2
        assert instance1 is not instance3
        assert instance2 is not instance3
    
    def test_implemented_singleton(self):
        instance1 = MixingCommSystem()
        instance2 = OutputCommSystem()


        assert instance1.input_queue is not instance2.input_queue
        assert instance1.output_queue is not instance2.output_queue
    