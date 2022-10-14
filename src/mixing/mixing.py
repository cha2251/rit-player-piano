import mido

class Mixing:
    def read_ports(self):
        file_port = mido.open_input('File_Input')
        button_port = mido.open_input('Button_Input')

    # Test fucntions for setting up unit test infra. TODO: Remove in sprint 2.
    def is_even(self, number):
        if number % 2 == 0:
            return True
        return False

    # Test fucntions for setting up unit test infra. TODO: Remove in sprint 2.
    def in_range(self, number):
        lower = 3
        upper = 8
        if number > lower and number < upper:
            return True
        return False