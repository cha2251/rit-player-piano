
import src.file_input.MIDI_file_class as MIDI_FC

class TestParse:

    def test_parse_midi_file(self):
        val = MIDI_FC.parse_midi_file('MIDI_sample.mid', 'Piano')

        expected = 0

        actual = val


        return actual is expected

