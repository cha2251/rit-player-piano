from queue import Empty
from src.common.shared_queues import SharedQueues
from src.common.midi_event import MidiEvent
import mido
import pytest

class TestQueuesCreate:
    def test_create_file_queue(self):
        component = SharedQueues()

        assert component.file_input_queue is None

        component.create_queues()

        assert component.file_input_queue is not None

    def test_create_button_queue(self):
        component = SharedQueues()

        assert component.button_input_queue is None

        component.create_queues()

        assert component.button_input_queue is not None

    def test_create_mixed_queue(self):
        component = SharedQueues()

        assert component.mixed_output_queue is None

        component.create_queues()

        assert component.mixed_output_queue is not None

class TestFileQueue:
    def test_put_event(self):
        component = SharedQueues()
        component.create_queues()
        file_queue = component.file_input_queue

        assert file_queue.qsize() == 0

        testEvent = MidiEvent(mido.Message('note_on',note=60), 1)
        file_queue.put(testEvent)

        assert file_queue.qsize() == 1
    
    def test_get_event(self):
        component = SharedQueues()
        component.create_queues()
        file_queue = component.file_input_queue

        with pytest.raises(Empty):
            file_queue.get(block=False) # Empty queue get should throw exception

        testEvent = MidiEvent(mido.Message('note_on',note=60), 1)
        file_queue.put(testEvent)

        assert file_queue.get() is testEvent

    def test_ordering(self):
        component = SharedQueues()
        component.create_queues()
        file_queue = component.file_input_queue

        assert file_queue.qsize() == 0

        testEvent1 = MidiEvent(mido.Message('note_on',note=60), 1)
        testEvent2 = MidiEvent(mido.Message('note_off',note=70), 3)
        testEvent3 = MidiEvent(mido.Message('note_on',note=50), 2)

        file_queue.put(testEvent1)
        file_queue.put(testEvent2)
        file_queue.put(testEvent3)

        assert file_queue.get() is testEvent1
        assert file_queue.get() is testEvent2
        assert file_queue.get() is testEvent3


class TestButtonQueue:
    def test_put_event(self):
        component = SharedQueues()
        component.create_queues()
        button_queue = component.button_input_queue

        assert button_queue.qsize() == 0

        testEvent = MidiEvent(mido.Message('note_on',note=60), 1)
        button_queue.put(testEvent)

        assert button_queue.qsize() == 1
    
    def test_get_event(self):
        component = SharedQueues()
        component.create_queues()
        button_queue = component.button_input_queue

        with pytest.raises(Empty):
            button_queue.get(block=False) # Empty queue get should throw exception

        testEvent = MidiEvent(mido.Message('note_on',note=60), 1)
        button_queue.put(testEvent)

        assert button_queue.get() is testEvent

    def test_ordering(self):
        component = SharedQueues()
        component.create_queues()
        button_queue = component.button_input_queue

        assert button_queue.qsize() == 0

        testEvent1 = MidiEvent(mido.Message('note_on',note=60), 1)
        testEvent2 = MidiEvent(mido.Message('note_off',note=70), 3)
        testEvent3 = MidiEvent(mido.Message('note_on',note=50), 2)

        button_queue.put(testEvent1)
        button_queue.put(testEvent2)
        button_queue.put(testEvent3)

        assert button_queue.get() is testEvent1
        assert button_queue.get() is testEvent2
        assert button_queue.get() is testEvent3

class TestMixingQueue:
    def test_put_event(self):
        component = SharedQueues()
        component.create_queues()
        mixing_queue = component.mixed_output_queue

        assert mixing_queue.qsize() == 0

        testEvent = MidiEvent(mido.Message('note_on',note=60), 1)
        mixing_queue.put(testEvent)

        assert mixing_queue.qsize() == 1
    
    def test_get_event(self):
        component = SharedQueues()
        component.create_queues()
        mixing_queue = component.mixed_output_queue

        with pytest.raises(Empty):
            mixing_queue.get(block=False) # Empty queue get should throw exception

        testEvent = MidiEvent(mido.Message('note_on',note=60), 1)
        mixing_queue.put(testEvent)

        assert mixing_queue.get() is testEvent

    def test_ordering(self):
        component = SharedQueues()
        component.create_queues()
        mixing_queue = component.mixed_output_queue

        assert mixing_queue.qsize() == 0

        testEvent1 = MidiEvent(mido.Message('note_on',note=60), 1)
        testEvent2 = MidiEvent(mido.Message('note_off',note=70), 3)
        testEvent3 = MidiEvent(mido.Message('note_on',note=50), 2)

        mixing_queue.put(testEvent1)
        mixing_queue.put(testEvent2)
        mixing_queue.put(testEvent3)

        assert mixing_queue.get() is testEvent1
        assert mixing_queue.get() is testEvent3 # Ordered by timestamp
        assert mixing_queue.get() is testEvent2 

        