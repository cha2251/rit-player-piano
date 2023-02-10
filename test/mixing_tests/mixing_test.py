import time
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
    @pytest.mark.timeout(5) #Longer timeout than strictly nesscary, to allow for slower computers
    def test_exits(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        component.start()

        component.deactivate()

        component.join()
    
    @pytest.mark.timeout(5)
    def test_pulls_from_button(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        test_event = MidiEvent(mido.Message(type='note_on'),0)
        component.button_input_queue.put(test_event)

        component.start()
        component.active = True
        component.deactivate()

        actual = component.mixed_output_queue.get()

        assert test_event == actual

    @pytest.mark.timeout(5)
    def test_pulls_from_file(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        test_event = MidiEvent(mido.Message(type='note_on'),0)
        component.file_input_queue.put(test_event)
        component.state = component.State.PLAY

        component.start()
        component.deactivate()
        component.join()

        actual = component.mixed_output_queue.get()

        assert test_event == actual

class TestStateChanges:
    def test_play_when_playing(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        component.play()

        assert component.state == component.State.PLAY

        component.play_pushed()

        assert component.state == component.State.PLAY

    def test_play_when_paused(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        component.pause()

        assert component.state == component.State.PAUSE

        component.play_pushed()

        assert component.state == component.State.PLAY
    
    def test_pause_when_playing(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        component.play()

        assert component.state == component.State.PLAY

        component.pause_pushed()

        assert component.state == component.State.PAUSE
    

    def test_pause_when_paused(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        component.pause()

        assert component.state == component.State.PAUSE

        component.pause_pushed()

        assert component.state == component.State.PLAY
    
    def test_stop_when_playing(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        component.play()

        assert component.state == component.State.PLAY

        component.stop_pushed()

        assert component.state == component.State.STOP

    def test_stop_when_paused(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        component.pause()

        assert component.state == component.State.PAUSE

        component.stop_pushed()

        assert component.state == component.State.STOP

class TestPause:
    def test_pause_turns_off_notes(self):
        test_shared_queues = SharedQueues()
        test_shared_queues.create_queues()
        component = Mixing(test_shared_queues)

        testNote = 80

        component.current_notes = ({testNote:'note_on'})

        assert component.mixed_output_queue.qsize() == 0

        component.pause()

        assert component.mixed_output_queue.peek().event.type == 'note_off'
        assert component.mixed_output_queue.peek().event.note == testNote