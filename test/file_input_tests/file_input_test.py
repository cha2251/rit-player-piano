from queue import Queue
from src.common.midi_event import MidiEvent
from src.file_input.MIDI_file_class import MIDIFileObject
from src.file_input.file_input import FileInput
import pytest
import mido

class TestCreate:
    def test_copies_queue(self):
        test_queue = Queue()
        component = FileInput(test_queue)

        actual = component.file_input_queue
        
        assert actual is test_queue


class TestCopyFileToQueue:
    def test_empty_file(self,mocker):
        test_queue = Queue()
        component = FileInput(test_queue)

        test_file = MIDIFileObject('')

        mocker.patch('src.file_input.file_input.FileInput.openFile',return_value=test_file)

        expected = component.file_input_queue
        component.run()
        actual = component.file_input_queue
        
        
        assert actual is expected

    def test_mutiple_notes(self,mocker):
        test_queue = Queue()
        component = FileInput(test_queue)
        expected = Queue()

        test_file = MIDIFileObject('')
        for i in range(10):
            test_file.messages.append(MidiEvent(mido.Message('note_on'),i))
            expected.put(MidiEvent(mido.Message('note_on'),i))

        mocker.patch('src.file_input.file_input.FileInput.openFile',return_value=test_file)

        component.run()
        actual = component.file_input_queue
        
        assert actual.qsize() == expected.qsize()
        for i in range(actual.qsize()):
            assert actual.get().event == expected.get().event

    def test_blacklisted_notes(self,mocker):
        test_queue = Queue()
        component = FileInput(test_queue)
        expected = Queue()

        test_file = MIDIFileObject('')
        for i in range(10):
            test_file.messages.append(MidiEvent(mido.Message('note_on'),i))
            expected.put(MidiEvent(mido.Message('note_on'),i))

        for i in range(10):
            test_file.messages.append(MidiEvent(mido.Message('control_change'),i))

        mocker.patch('src.file_input.file_input.FileInput.openFile',return_value=test_file)

        component.run()
        actual = component.file_input_queue

        
        
        assert actual.qsize() == expected.qsize()
        for i in range(actual.qsize()):
            assert actual.get().event == expected.get().event
    

