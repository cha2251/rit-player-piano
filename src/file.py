from time import sleep
import mido

port = mido.open_output('File_Input')
msg = mido.Message('note_on', note=50)
while True:
    port.send(msg)
    sleep(1)