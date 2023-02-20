from src.common.main import Main

class TestSubsystemCreate:
    def test_create_queues(self):
        component = Main()

        assert component.shared_queues is None

        component.create_queues()

        assert component.shared_queues is not None