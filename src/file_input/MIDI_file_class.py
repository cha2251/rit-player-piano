"""
Created by Michael Samodurov 10/22/2022
"""
import mido

def parse_midi_file(file_name):
    file_queue = []
    # open midi file
    mid_fi = mido.MidiFile(file_name)

    # iterate over midi file
    for i, track in enumerate(mid_fi.tracks):
        print('Track []: []'.format(i, track.name))

        # iterate over messages in each track
        for msg in track:
            print(msg)


    return file_queue


class MIDIFileObject:
    """
    This is the MIDI_file_class. It creates an object representation
    of a MIDI file.

    NOTE: I have decided to remove the SongObject since 
    it is redundant with the mido object.
    """

    def __init__(self, file_name):
        self.file_name = file_name
        self.curr_pos = 0


    def __str__(self):
        return f"{self.file_name}"

    
    def get_next_note():
        return 0

    
    def get_curr_pos():
        return 0