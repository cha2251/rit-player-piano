import mido

class FileInput:
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