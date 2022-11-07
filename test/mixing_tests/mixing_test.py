from src.common.midi_event import MidiEvent
from src.common.shared_queues import SharedQueues
from src.mixing.mixing import Mixing
import pytest
import mido

class TestCreate:
    def test_copies_queues(self):
        test_shared_queues =  SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        assert component.file_input_queue is test_shared_queues.file_input_queue
        assert component.button_input_queue is test_shared_queues.button_input_queue
        assert component.mixed_output_queue is test_shared_queues.mixed_output_queue
    
class TestDeactivate():
    def test_set_false(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        component.active = True
        component.deactivate()

        expected = False
        actual = component.active

        assert expected == actual

class TestRun:
    @pytest.mark.timeout(0.5)
    def test_exits(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        component.start()

        component.deactivate()
    
    @pytest.mark.timeout(1)
    def test_pulls_from_button(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        test_event = MidiEvent(mido.Message(type='note_on'),0)
        component.button_input_queue.put(test_event)


        component.start()
        component.deactivate()

        actual = component.mixed_output_queue.get()

        assert test_event == actual

    @pytest.mark.timeout(1)
    def test_pulls_from_file(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        test_event = MidiEvent(mido.Message(type='note_on'),0)
        component.file_input_queue.put(test_event)


        component.start()
        component.deactivate()

        actual = component.mixed_output_queue.get()

        assert test_event == actual

    
