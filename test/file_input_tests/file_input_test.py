from queue import Queue
from src.common.midi_event import MidiEvent
from src.file_input.MIDI_file_class import MIDIFileObject
from src.file_input.file_input import FileInput
import pytest
import mock
import mido

class TestCreate:
    def test_copies_queue(self):
        test_queue = Queue()
        component = FileInput(test_queue)

        actual = component.file_input_queue
        
        assert actual is test_queue


class TestCopyFileToQueue:
    def test_empty_file(self):
        test_queue = Queue()
        component = FileInput(test_queue)

        test_file = MIDIFileObject('')

        mock.patch('component.openFile',test_file)

        expected = component.file_input_queue
        component.copy_file_to_queue()
        actual = component.file_input_queue
        
        
        assert actual is expected

    def test_mutiple_notes(self):
        test_queue = Queue()
        component = FileInput(test_queue)
        expected = []

        test_file = MIDIFileObject('')
        for i in range(10):
            test_file.messages.append(MidiEvent(mido.Message('note_on'),i))
            expected.append(MidiEvent(mido.Message('note_on'),i))

        mock.patch('component.openFile',test_file)

        component.copy_file_to_queue()
        actual = component.file_input_queue
        
        
        assert actual.qsize == len(expected)

    def test_blacklisted_notes(self):
        test_queue = Queue()
        component = FileInput(test_queue)
        expected = []

        test_file = MIDIFileObject('')
        for i in range(10):
            test_file.messages.append(MidiEvent(mido.Message('note_on'),i))
            expected.append(MidiEvent(mido.Message('note_on'),i))

        for i in range(10):
            test_file.messages.append(MidiEvent(mido.Message('control_change'),i))

        mock.patch('component.openFile',test_file)

        component.copy_file_to_queue()
        actual = component.file_input_queue
        
        
        assert actual.qsize() == len(expected)
    

