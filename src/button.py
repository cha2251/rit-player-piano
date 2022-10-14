from time import sleep
import mido

port = mido.open_output('Button_Input')
msg = mido.Message('note_on', note=60)
while True:
    port.send(msg)
    sleep(1)
