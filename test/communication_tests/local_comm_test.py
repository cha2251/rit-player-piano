from src.communication.local_comm_system import LocalCommSystem

class TestSingleton:
    def test_singleton(self):
        instance1 = LocalCommSystem()
        instance2 = LocalCommSystem()

        assert instance1 is instance2
    