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
    @pytest.mark.timeout(5)
    def test_empty_file(self):
        test_queue = Queue()
        component = FileInput(test_queue)

        test_file = MIDIFileObject('')

        expected = component.file_input_queue
        component.start()
        component.deactivate()
        component.join()
        actual = component.file_input_queue
        
        
        assert actual is expected

    @pytest.mark.timeout(5)
    def test_mutiple_notes(self):
        test_queue = Queue()
        component = FileInput(test_queue)
        expected = Queue()

        component.filename = "TestFile"
        component.fileObject = MIDIFileObject('')
        for i in range(10):
            component.fileObject.messages.append(MidiEvent(mido.Message('note_on'),i))
            expected.put(MidiEvent(mido.Message('note_on'),i))

        component.start()
        component.deactivate()
        component.join()

        actual = component.file_input_queue
        
        assert actual.qsize() == expected.qsize()
        for i in range(actual.qsize()):
            assert actual.get().event == expected.get().event

    @pytest.mark.timeout(5)
    def test_blacklisted_notes(self):
        test_queue = Queue()
        component = FileInput(test_queue)
        expected = Queue()

        component.filename = "TestFile"
        component.fileObject = MIDIFileObject('')
        for i in range(10):
            component.fileObject.messages.append(MidiEvent(mido.Message('note_on'),i))
            expected.put(MidiEvent(mido.Message('note_on'),i))

        for i in range(10):
            component.fileObject.messages.append(MidiEvent(mido.Message('control_change'),i))


        component.start()
        component.deactivate()
        component.join()

        actual = component.file_input_queue

        assert actual.qsize() == expected.qsize()
        for i in range(actual.qsize()):
            assert actual.get().event == expected.get().event
    

