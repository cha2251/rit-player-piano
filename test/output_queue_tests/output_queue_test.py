import queue
import time
import pytest
import mido
import multiprocessing

from src.common.shared_priority_queue import PeekingPriorityQueue
from src.communication.messages import PlayingState
from src.output_queue.output_queue import OutputQueue
from src.output_queue.synth import SYNTHESIZER_NAME
from src.common.midi_event import MidiEvent

FAR_FUTURE_TIMESTAMP = 1e10
DUMMY_PORT_NAME = "DummyPort"

class DummyPort:
    def __init__(self):
        self.name = DUMMY_PORT_NAME
        self.sent_messages = []

    def close(self):
        pass

    def send(self, msg):
        self.sent_messages += [msg]

@pytest.fixture
def output_queue(mocker):
    output_queue = OutputQueue(multiprocessing.Queue(), multiprocessing.Queue())
    dummy_port = DummyPort()

    mock_get_output_names = mocker.patch("mido.get_output_names")
    mock_get_output_names.return_value = [dummy_port.name]

    mock_open_output = mocker.patch("mido.open_output")
    mock_open_output.return_value = dummy_port
    
    return output_queue

@pytest.fixture
def output_queue_process(mocker):
    output_queue = OutputQueue(multiprocessing.Queue(), multiprocessing.Queue())
    dummy_port = DummyPort()

    mock_get_output_names = mocker.patch("mido.get_output_names")
    mock_get_output_names.return_value = [dummy_port.name]

    mock_open_output = mocker.patch("mido.open_output")
    mock_open_output.return_value = dummy_port

    return output_queue

# class TestPorts: TODO FIX AFTER MERGE WITH SELECTION CHANGES
#     def test_output_queue(self, mocker, output_queue):
#         test_output_devices = ["Output1", "Output2"]

#         mock_get_output_names = mocker.patch("mido.get_output_names")
#         mock_get_output_names.return_value = test_output_devices

#         actual_output_devices = output_queue.get_device_list()

#         assert actual_output_devices == ([SYNTHESIZER_NAME] + test_output_devices)

#     def test_select_bad_device(self, mocker, output_queue):
#         test_output_devices = ["Output1", "Output2"]
#         bad_device_name = "Output 3"

#         mock_get_output_names = mocker.patch("mido.get_output_names")
#         mock_get_output_names.return_value = test_output_devices

#         with pytest.raises(Exception):
#             output_queue.select_device(bad_device_name)

class TestRun:
    @pytest.mark.timeout(5)
    def test_deactivate(self):
        output_queue = OutputQueue(multiprocessing.Queue(), multiprocessing.Queue())
        output_queue.deactivate()
        output_queue.comm_system.deactivate()
    
    def test_empty_queue(self, output_queue_process):
        output_queue_process.select_device(DUMMY_PORT_NAME)
        output_queue_process._check_priority_queue()

        expected_sent_messages = 0
        actual_sent_messages = len(output_queue_process._open_port.sent_messages)

        assert actual_sent_messages is expected_sent_messages

        output_queue_process.comm_system.deactivate()

    def test_no_open_port(self, output_queue_process):
        output_queue_process.queue.put(None)
        output_queue_process._check_priority_queue()

        expected_unsent_messages = 1
        actual_unsent_messages = output_queue_process.queue.qsize()

        assert actual_unsent_messages is expected_unsent_messages

        output_queue_process.comm_system.deactivate()

    def test_one_message(self, output_queue_process):
        test_message = MidiEvent(mido.Message('note_on',note=60,), 42, True)
        output_queue_process.select_device(DUMMY_PORT_NAME)
        output_queue_process.state = PlayingState.PLAY

        output_queue_process.queue.put(test_message)
        output_queue_process._check_priority_queue()

        expected_sent_messages = 1
        expected_sent_event = test_message.event

        actual_sent_messages = len(output_queue_process._open_port.sent_messages)
        actual_sent_event = output_queue_process._open_port.sent_messages[0]

        assert actual_sent_messages is expected_sent_messages
        assert actual_sent_event is expected_sent_event

        output_queue_process.comm_system.deactivate()

    def test_future_message(self, output_queue_process):
        test_message = MidiEvent(mido.Message('note_on',note=60), FAR_FUTURE_TIMESTAMP, True)
        output_queue_process.select_device(DUMMY_PORT_NAME)
        output_queue_process.state = PlayingState.PLAY

        output_queue_process.queue.put(test_message)
        output_queue_process._check_priority_queue()

        expected_sent_messages = 0
        actual_sent_messages = len(output_queue_process._open_port.sent_messages)

        assert actual_sent_messages is expected_sent_messages

        output_queue_process.comm_system.deactivate()

    def test_many_messages(self, output_queue_process):
        expected_past_messages = 5
        expected_future_messages = 3
        past_messages = []
        output_queue_process.state = PlayingState.PLAY

        for i in range(expected_past_messages):
            test_message = MidiEvent(mido.Message('note_on', note=60), 0, True)
            past_messages += [test_message]
            output_queue_process.queue.put(test_message)

        for i in range(expected_future_messages):
            output_queue_process.queue.put(MidiEvent(mido.Message('note_on', note=60), FAR_FUTURE_TIMESTAMP + i * 10, True))

        output_queue_process.select_device(DUMMY_PORT_NAME)
        for i in range(expected_past_messages + expected_future_messages + 1):
            output_queue_process._check_priority_queue()

        actual_sent_messages = len(output_queue_process._open_port.sent_messages)
        actual_unsent_messages = output_queue_process.queue.qsize()

        assert actual_sent_messages is expected_past_messages
        assert actual_unsent_messages is expected_future_messages
    
        # Assert that each past message exists in the sent messages (already length checked)
        for i in range(expected_past_messages):
            assert past_messages[i].event in output_queue_process._open_port.sent_messages

        output_queue_process.comm_system.deactivate()
