from queue import Queue
import time
from src.common.midi_event import MidiEvent
from src.communication.messages import PlayingState
from src.mixing.mixing import Mixing
import pytest
import mido

class TestDeactivate():
    @pytest.mark.timeout(1)
    def test_set_false(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.active = True
        
        component.start()
        time.sleep(.5) #Allow for creation of sub threads

        component.deactivate()
        component.comm_system.deactivate()

        component.join()

        expected = False
        actual = component.active

        assert expected == actual

class TestStateChanges:
    @pytest.mark.timeout(1)
    def test_play_when_playing(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.play()

        assert component.state == PlayingState.PLAY

        component.play_pushed()

        assert component.state == PlayingState.PLAY

        component.comm_system.deactivate()

    @pytest.mark.timeout(1)
    def test_play_when_paused(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.pause()

        assert component.state == PlayingState.PAUSE

        component.play_pushed()

        assert component.state == PlayingState.PLAY

        component.comm_system.deactivate()
   
    @pytest.mark.timeout(1)
    def test_pause_when_playing(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.play()

        assert component.state == PlayingState.PLAY

        component.pause_pushed()

        assert component.state == PlayingState.PAUSE

        component.comm_system.deactivate()
   
    @pytest.mark.timeout(1)
    def test_pause_when_paused(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.pause()

        assert component.state == PlayingState.PAUSE

        component.pause_pushed()

        assert component.state == PlayingState.PLAY

        component.comm_system.deactivate()
   
    @pytest.mark.timeout(1)
    def test_stop_when_playing(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.play()

        assert component.state == PlayingState.PLAY

        component.stop_pushed()

        assert component.state == PlayingState.STOP

        component.comm_system.deactivate()
   
    @pytest.mark.timeout(1)
    def test_stop_when_paused(self):
        dummy_queue = Queue()
        component = Mixing(dummy_queue, dummy_queue)

        component.pause()

        assert component.state == PlayingState.PAUSE

        component.stop_pushed()

        assert component.state == PlayingState.STOP

        component.comm_system.deactivate()
