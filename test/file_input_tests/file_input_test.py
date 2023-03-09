from queue import Queue
import time
from src.common.midi_event import MidiEvent
from src.communication.messages import Message, MessageType
from src.file_input.MIDI_file_class import MIDIFileObject
from src.file_input.file_input import FileInput
import pytest
import mido

class TestCreate:
    def test_copies_queue(self):
        test_queue = Queue()
        test_queue2 = Queue()
        component = FileInput(test_queue, test_queue2)

        actual = component.file_input_queue
        
        assert actual is test_queue


class TestCopyFileToQueue:
    @pytest.mark.timeout(5)
    def test_empty_file(self):
        test_queue = Queue()
        test_queue2 = Queue()
        component = FileInput(test_queue, test_queue2)

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
        test_queue2 = Queue()
        component = FileInput(test_queue, test_queue2)
        expected = Queue()

        component.filename = "TestFile"
        component.fileObject = MIDIFileObject('')
        for i in range(10):
            component.fileObject.messages.append(MidiEvent(mido.Message('note_on'),i))
            expected.put(MidiEvent(mido.Message('note_on'),i))

        component.start()
        time.sleep(.5) #Allow time to process
        component.deactivate()
        component.join()

        actual = component.file_input_queue
        
        assert actual.qsize() == expected.qsize()
        for i in range(actual.qsize()):
            assert actual.get().event == expected.get().event

    @pytest.mark.timeout(5)
    def test_blacklisted_notes(self):
        test_queue = Queue()
        test_queue2 = Queue()
        component = FileInput(test_queue, test_queue2)
        expected = Queue()

        component.filename = "TestFile"
        component.fileObject = MIDIFileObject('')
        for i in range(10):
            component.fileObject.messages.append(MidiEvent(mido.Message('note_on'),i))
            expected.put(MidiEvent(mido.Message('note_on'),i))

        for i in range(10):
            component.fileObject.messages.append(MidiEvent(mido.Message('control_change'),i))


        component.start()
        time.sleep(.5) #Allow time to process
        component.deactivate()
        component.join()

        actual = component.file_input_queue

        assert actual.qsize() == expected.qsize()
        for i in range(actual.qsize()):
            assert actual.get().event == expected.get().event
    

class TestOpenFile:
    def test_adds_extension(self):
        test_queue = Queue()
        test_queue2 = Queue()
        component = FileInput(test_queue, test_queue2)

        test_file = "TestFile"

        expected = test_file+".mid"

        assert component.filename is None

        component.openFile(Message(MessageType.SONG_UPDATE,test_file))

        actual = component.filename
    
        assert actual == expected
    
    def test_clears_file_object(self):
        test_queue = Queue()
        test_queue2 = Queue()
        component = FileInput(test_queue, test_queue2)

        test_file = "TestFile"

        component.fileObject= "NotARealFileObject"

        component.openFile(Message(MessageType.SONG_UPDATE,test_file))

        actual = component.fileObject
    
        assert actual is None
