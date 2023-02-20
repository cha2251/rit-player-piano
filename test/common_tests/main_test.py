from src.common.main import Main
from src.mixing.mixing_comm import MixingCommSystem

class TestSubsystemCreate:
    def test_create_queues(self):
        component = Main()

        assert component.shared_queues is None

        component.create_queues()

        assert component.shared_queues is not None