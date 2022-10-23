"""
Created by Michael Samodurov 10/22/2022
"""
import mido


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