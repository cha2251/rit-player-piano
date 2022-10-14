import mido


def read_ports():
    file_port = mido.open_input('File_Input')
    button_port = mido.open_input('Button_Input')

    for msg in all_ports:
        print(msg)

def is_even(number):
    if number % 2 == 0:
        return True
    return False