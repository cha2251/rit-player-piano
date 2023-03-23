"""
Created by Michael Samodurov 10/22/2022
"""

import time
import mido
from pathlib import Path

from src.common.midi_event import MidiEvent
from mido import merge_tracks, tick2second
from src.communication.messages import Message, MessageType, PianoAssistPlaying
from src.mixing.mixing_comm import MixingCommSystem

class MIDIFileObject:
    """
    This is the MIDI_file_class. It creates an object representation
    of a MIDI file.

    NOTE: I have decided to remove the SongObject since 
    it is redundant with the mido object.
    """

    DEFAULT_TEMPO = 500000
    STARTUP_DELAY = 2.5
    hand_to_play = PianoAssistPlaying.BOTH.value
    

    def __init__(self, file_name):
        """Constructor for MIDIFileObject class. Parses the given file and maintains the messages for the track.

        Args:
            file_name (str): The MIDI file to be parsed. Must be in /MIDI_Files.
            track_string (str): The string name for the track to play within the MIDI file.
        """
        self.file_name = file_name
        self.curr_pos = 0
        self.current_time_delay = None
        #self.comm_system = MixingCommSystem()
        self.end_time = 0
        self.messages = self.parse_midi_file(file_name)


    def __str__(self):
        """String representation of object

        Returns:
            str: printable string
        """
        return f"{self.file_name}"

    def has_next(self):
        if self.curr_pos >= len(self.messages):
            return False

        return True

    
    def get_next_message(self):
        """Return the current position and increment the current.
        This can be called iteratively.

        Returns:
            Mido Message() representation of next message
        """
        
        message = self.messages[self.curr_pos]
        self.curr_pos += 1
        return message

    
    def get_curr_message(self):
        """
        Returns:
            Mido Message() representation of current message
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
        

    def calc_time_delay(self):
        if self.curr_tempo is None or self.curr_time_signature is None:
            return None
        
    
    def is_correct_hand(self, note_num):
        """
        NOTE: The hand_to_play side refers to the side the PIANO is going to play.
        The player would, presumably, be playing the opposite.

        
        If the given note is not on the hand_to_play side return false
        """
        if self.hand_to_play == PianoAssistPlaying.RIGHT.value:    # The piano will play right hand
            if note_num >= 60:
                return True
        elif self.hand_to_play == PianoAssistPlaying.LEFT.value:   # The piano will play left hand
            if note_num <= 60:
                return True
        elif self.hand_to_play == PianoAssistPlaying.BOTH.value:       # The piano will play all
            return True
        elif self.hand_to_play == PianoAssistPlaying.NEITHER.value: # The piano will play nothing
            return False
        return False
        

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
            return [] #TODO: Actual error message

        file_location = 'MIDI_Files/{}'.format(file_name)
        mid_fi = mido.MidiFile(file_location)
        
        # start_time = time.time()+self.STARTUP_DELAY
        curr_time = 0

        tempo = self.DEFAULT_TEMPO # Tempo changes as we go, so default till first tempo event
        ticks_per_beat = mid_fi.ticks_per_beat # Ticks Per Beat is only in header
    
        for msg in merge_tracks(mid_fi.tracks): # merge_tracks merges w/ respect to time
            if msg.time > 0:
                delta = tick2second(msg.time, ticks_per_beat, tempo)
            else:
                delta = 0

            curr_time += delta

            if msg.type == 'note_on':
                if self.is_correct_hand(msg.note):
                    track_messages.append(MidiEvent(msg,curr_time, True))
                else:
                    track_messages.append(MidiEvent(msg,curr_time, False))
            else:
                track_messages.append(MidiEvent(msg,curr_time, True))

            if msg.type == 'set_tempo':
                tempo = msg.tempo
        #print(f'The last message is: {track_messages[-1]}')
        self.end_time = track_messages[-1].timestamp
        #self.comm_system.send(Message(MessageType.SET_DURATION, track_messages[-1].timestamp))
        return track_messages
    
    def get_end_time(self):
        """
        Returns:
            The end time of the song.
        """
        end_time = self.end_time
        return end_time


    def set_hand_to_play(self, hand):
        self.hand_to_play = hand