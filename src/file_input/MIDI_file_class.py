"""
Created by Michael Samodurov 10/22/2022
"""

import mido

def parse_midi_file(file_name, track_string):
    """Parse the designated MIDI file and retrieve the selected track.
    TODO: implement input handling

    Args:
        file_name (str): The name of the MIDI file to open.
        track_string (str): The name of the track in the MIDI file to retrieve.

    Returns:
        list: A list of mido message dictionary objects
    """
    track_messages = []
    # open midi file
    if not is_file_string_valid(file_name):
        return []

    file_location = 'MIDI_Files/{}'.format(file_name)
    mid_fi = mido.MidiFile(file_location)

    # iterate over midi file
    for i, track in enumerate(mid_fi.tracks):
        print('Track {}: {}'.format(i, track.name))

        # iterate over messages in each track
        if track.name == track_string:
            for msg in track:
                track_messages.append(msg.dict())
                print(msg.dict())
            
    return track_messages

def is_file_string_valid(file_string):

    is_valid = False
    if file_string != '':
        is_valid = True
    
    return is_valid



class MIDIFileObject:
    """
    This is the MIDI_file_class. It creates an object representation
    of a MIDI file.

    NOTE: I have decided to remove the SongObject since 
    it is redundant with the mido object.
    """

    def __init__(self, file_name, track_string):
        """_summary_

        Args:
            file_name (_type_): _description_
            track_string (_type_): _description_
        """

        self.file_name = file_name
        self.track_name = track_string
        self.curr_pos = 0
        self.messages = parse_midi_file(file_name, track_string)


    def __str__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return f"{self.file_name}"

    
    def get_next_message(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        if self.curr_pos < len(self.messages):
            self.curr_pos += 1

        return self.messages[self.curr_pos]

    
    def get_curr_pos(self):
        return self.curr_pos