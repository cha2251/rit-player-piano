import src.file_input.MIDI_file_class as MIDI_FC
import mido


class TestParse:

    def test_parse_midi_file(self):
        """ This is the test to ensure the function returns the correct list of midi messages.
        TODO: complete this test, test with smaller file
        """
        
        fileObject = MIDI_FC.MIDIFileObject('MIDI_sample.mid')
        val = fileObject.parse_midi_file('MIDI_sample.mid')
        expected = 100

        actual = val


        #assert actual == expected


    def test_parse_midi_file_is_null(self):
        """ This test is to ensure the function returns null if no filename is given.
        """
        fileObject = MIDI_FC.MIDIFileObject('MIDI_sample.mid')
        val = fileObject.parse_midi_file('')
        expected = []
        actual = val

        assert actual == expected

    def test_parse_midi_file_exists(self):
        """ This test is to ensure the function returns null if no filename is given.
        """
        fileObject = MIDI_FC.MIDIFileObject('MIDI_sample.mid')
        
        val = fileObject.parse_midi_file('not_a_real_file.midi')
        expected = []
        actual = val

        assert actual == expected

    
    def test_get_next_message(self):
        """
        
        {'type': 'track_name', 'name': 'Piano', 'time': 0}
        {'type': 'control_change', 'time': 0, 'control': 0, 'value': 121, 'channel': 1}
        """
        fileObject = MIDI_FC.MIDIFileObject('MIDI_sample.mid')

        val = fileObject.get_next_message()
        expected = {'type': 'control_change', 'time': 0, 'control': 0, 'value': 121, 'channel': 1}
        actual = val

        assert actual == expected


    def test_get_curr_message(self):
        """
        Test the first message in a midi file object is valid. The message is a dict containing
        the type of message it is, the name of the track, and the time when it should be sent (0 meaning it should be sent without delay).
        
        {'type': 'track_name', 'name': 'Piano', 'time': 0}
        
        """
        fileObject = MIDI_FC.MIDIFileObject('MIDI_sample.mid')

        val = fileObject.get_curr_message()
        print (val)
        expected = mido.MetaMessage(type='track_name',name='Wikipedia MIDI (extended)', time=0)
        actual = val

        assert actual == expected

    
    def test_get_next_recursive(self):
        fileObject = MIDI_FC.MIDIFileObject('MIDI_sample.mid')

        while(fileObject.has_next()):
            fileObject.get_next_message()

        val = fileObject.get_curr_message()
        expected = {'type': 'end_of_track', 'time': 0}
        actual = val

        assert actual == expected

