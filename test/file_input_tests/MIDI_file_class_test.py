
import src.file_input.MIDI_file_class as MIDI_FC

class TestParse:

    def test_parse_midi_file(self):
        """ This is the test to ensure the function returns the correct list of midi messages.
        TODO: complete this test
        """
        val = MIDI_FC.parse_midi_file('MIDI_sample.mid', 'Piano')

        expected = 100

        actual = val


        #assert actual == expected


    def test_parse_midi_file_is_null(self):
        """ This test is to ensure the function returns null if no filename is given.
        """
        val = MIDI_FC.parse_midi_file('','Piano')
        expected = []
        actual = val

        assert actual == expected

    
    def test_get_next_note(self):
        """
        
        {'type': 'track_name', 'name': 'Piano', 'time': 0}
        {'type': 'control_change', 'time': 0, 'control': 0, 'value': 121, 'channel': 1}
        """
        fileObject = MIDI_FC.MIDIFileObject('MIDI_sample.mid', 'Piano')

        val = fileObject.get_next_note()
        expected = {'type': 'control_change', 'time': 0, 'control': 0, 'value': 121, 'channel': 1}
        actual = val

        assert actual == expected

