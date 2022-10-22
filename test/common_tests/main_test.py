from src.common.main import Main

class TestSubsystemCreate:
    def test_create_mixing(self):
        component = Main()

        assert component.mixing is None

        component.createMixing()

        assert component.mixing is not None