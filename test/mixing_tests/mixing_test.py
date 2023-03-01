from queue import Queue
import time
from src.common.midi_event import MidiEvent
from src.communication.messages import PlayingState
from src.mixing.mixing import Mixing
import pytest
import mido

class TestDeactivate():
    def test_set_false(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.active = True
        
        component.start()
        time.sleep(.2) #Allow for creation of sub threads

        component.deactivate()

        component.join()

        expected = False
        actual = component.active

        assert expected == actual

class TestRun:
    @pytest.mark.timeout(5) #Longer timeout than strictly nesscary, to allow for slower computers
    def test_exits(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.start()
        time.sleep(.2) #Allow for creation of sub threads

        component.deactivate()

        component.join()
    
    @pytest.mark.timeout(5)
    def test_pulls_from_button(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        test_event = MidiEvent(mido.Message(type='note_on'),0)
        component.button_input_queue.put(test_event)

        component.start()
        time.sleep(.2) #Allow for creation of sub threads
        component.active = True
        component.deactivate()

        actual = component.comm_system.output_queue.get()

        component.join()

        assert test_event == actual

        

    @pytest.mark.timeout(5)
    def test_pulls_from_file(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        test_event = MidiEvent(mido.Message(type='note_on'),0)
        component.file_input_queue.put(test_event)
        component.state = PlayingState.PLAY

        component.start()
        time.sleep(.2) #Allow for creation of sub threads
        component.deactivate()
        component.join()

        actual = component.comm_system.output_queue.get().data

        assert test_event == actual

class TestStateChanges:
    def test_play_when_playing(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.play()

        assert component.state == PlayingState.PLAY

        component.play_pushed()

        assert component.state == PlayingState.PLAY

    def test_play_when_paused(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.pause()

        assert component.state == PlayingState.PAUSE

        component.play_pushed()

        assert component.state == PlayingState.PLAY
    
    def test_pause_when_playing(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.play()

        assert component.state == PlayingState.PLAY

        component.pause_pushed()

        assert component.state == PlayingState.PAUSE
    

    def test_pause_when_paused(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.pause()

        assert component.state == PlayingState.PAUSE

        component.pause_pushed()

        assert component.state == PlayingState.PLAY
    
    def test_stop_when_playing(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.play()

        assert component.state == PlayingState.PLAY

        component.stop_pushed()

        assert component.state == PlayingState.STOP

    def test_stop_when_paused(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.pause()

        assert component.state == PlayingState.PAUSE

        component.stop_pushed()

        assert component.state == PlayingState.STOP
class TestPause:
    def test_pause_turns_off_notes(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        testNote = 80

        component.current_notes = ({testNote:'note_on'})

        assert component.mixed_output_queue.qsize() == 0

        component.pause()

        actual = component.comm_system.output_queue.get().data

        assert actual.event.type == 'note_off'
        assert actual.event.note == testNote