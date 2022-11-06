"""
Created by Michael Samodurov 10/22/2022
"""

import time
import mido
from pathlib import Path

from src.common.midi_event import MidiEvent
from mido import merge_tracks, tick2second

class MIDIFileObject:
    """
    This is the MIDI_file_class. It creates an object representation
    of a MIDI file.

    NOTE: I have decided to remove the SongObject since 
    it is redundant with the mido object.
    """

    DEFAULT_TEMPO = 500000
    

    def __init__(self, file_name):
        """Constructor for MIDIFileObject class. Parses the given file and maintains the messages for the track.

        Args:
            file_name (str): The MIDI file to be parsed. Must be in /MIDI_Files.
            track_string (str): The string name for the track to play within the MIDI file.
        """

        self.file_name = file_name
        self.curr_pos = 0
        self.curr_tempo = None
        self.curr_time_signature = None
        self.current_time_delay = None
        self.messages = self.parse_midi_file(file_name)


    def __str__(self):
        """String representation of object

        Returns:
            str: printable string
        """
        return f"{self.file_name}"

    def has_next(self):
        has_next = False
        if self.curr_pos < len(self.messages)-1:
            has_next = True

        return has_next

    
    def get_next_message(self):
        """Iterate current position and get the next message.
        This can be called iteratively.

        Returns:
            dict: dictionary representation of next message
        """
        if self.curr_pos < len(self.messages)-1:
            self.curr_pos += 1

        return self.messages[self.curr_pos]

    
    def get_curr_message(self):
        """
        Returns:
            dict: dictionary representation of next message
        """
        return self.messages[self.curr_pos]

    def is_file_string_valid(self, file_string):

        is_valid = False
        file_location = 'MIDI_Files/{}'.format(file_string)
        if file_string != '' and Path(file_location).is_file():
            is_valid = True
        
        return is_valid

    def calc_time_delay(self):
        if self.curr_tempo is None or self.curr_time_signature is None:
            return None
        

    def parse_midi_file(self, file_name):
        """Parse the designated MIDI file and retrieve the selected track.
        TODO: implement input handling

        Args:
            file_name (str): The name of the MIDI file to open.
            track_string (str): The name of the track in the MIDI file to retrieve.

        Returns:
            list: A list of mido message dictionary objects
        """
        track_messages = []
        if not self.is_file_string_valid(file_name):
            return []

        file_location = 'MIDI_Files/{}'.format(file_name)
        mid_fi = mido.MidiFile(file_location)
        
        start_time = time.time()+2
        curr_time = start_time

        tempo = self.DEFAULT_TEMPO
        ticks_per_beat = mid_fi.ticks_per_beat

        for msg in merge_tracks(mid_fi.tracks):
            if msg.time > 0:
                delta = tick2second(msg.time, ticks_per_beat, tempo)
            else:
                delta = 0

            curr_time += delta

            track_messages.append(MidiEvent(msg,curr_time))

            if msg.type == 'set_tempo':
                tempo = msg.tempo

        # for msg in mid_fi:
        #     print(msg)
        #     input_time += msg.time

        #     playback_time = curr_time - start_time
        #     duration_to_next_event = input_time - playback_time

        #     curr_time = duration_to_next_event+curr_time

        #     track_messages.append(MidiEvent(msg,curr_time))

        # for i, track in enumerate(mid_fi.tracks):
        #     current=now
        #     for msg in track:
        #         if msg.type == 'set_tempo':
        #             curr_tempo = msg.tempo
        #             self.calc_time_delay()
        #         if msg.type == 'time_signature':
        #             curr_time_signature = msg
        #             self.calc_time_delay()
        #         print(msg)
        #         current+=(msg.time/180) #TODO figure out why this works
        #         track_messages.append(MidiEvent(msg,current))
                
        return track_messages

