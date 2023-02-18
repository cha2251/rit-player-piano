from src.communication.local_comm_system import LocalCommSystem


class OutputCommSystem(LocalCommSystem):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LocalCommSystem, cls).__new__(cls)
        return cls.instance