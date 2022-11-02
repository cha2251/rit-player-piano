import queue
import time
import pytest

import mido
from src.output_queue.output_queue import OutputQueue
from src.common.midi_event import MidiEvent

FAR_FUTURE_TIMESTAMP = 1e10

class DummyPort:
    def __init__(self):
        self.name = "DummyPort"
        self.sent_messages = []

    def close(self):
        pass

    def send(self, msg):
        self.sent_messages += [msg]

@pytest.fixture
def output_queue(mocker):
    output_queue = OutputQueue(queue.PriorityQueue())
    dummy_port = DummyPort()

    mock_get_output_names = mocker.patch("mido.get_output_names")
    mock_get_output_names.return_value = [dummy_port.name]

    mock_open_output = mocker.patch("mido.open_output")
    mock_open_output.return_value = dummy_port

    return output_queue

class TestPorts:
    def test_output_queue(self, mocker, output_queue):
        test_output_devices = ["Output1", "Output2"]

        mock_get_output_names = mocker.patch("mido.get_output_names")
        mock_get_output_names.return_value = test_output_devices

        actual_output_devices = output_queue.get_device_list()

        assert actual_output_devices is test_output_devices

    def test_select_bad_device(self, mocker, output_queue):
        test_output_devices = ["Output1", "Output2"]
        bad_device_name = "Output 3"

        mock_get_output_names = mocker.patch("mido.get_output_names")
        mock_get_output_names.return_value = test_output_devices

        with pytest.raises(Exception):
            output_queue.select_device(bad_device_name)

class TestRun:
    @pytest.mark.timeout(0.5)
    def test_signal_stop(self, output_queue):
        output_queue.start()
        output_queue.signal_stop()
        output_queue.join()
    
    def test_empty_queue(self, output_queue):
        output_queue.select_device()
        output_queue._check_queue()

        expected_sent_messages = 0
        actual_sent_messages = len(output_queue._open_port.sent_messages)

        assert actual_sent_messages is expected_sent_messages

    def test_no_open_port(self, output_queue):
        output_queue.queue.put(None)
        output_queue._check_queue()

        expected_unsent_messages = 1
        actual_unsent_messages = output_queue.queue.qsize()

        assert actual_unsent_messages is expected_unsent_messages

    def test_one_message(self, output_queue):
        test_message = MidiEvent(mido.Message('note_on',note=60), 42)
        output_queue.select_device()
        output_queue.queue.put(test_message)
        output_queue._check_queue()

        expected_sent_messages = 1
        expected_sent_event = test_message.event

        actual_sent_messages = len(output_queue._open_port.sent_messages)
        actual_sent_event = output_queue._open_port.sent_messages[0]

        assert actual_sent_messages is expected_sent_messages
        assert actual_sent_event is expected_sent_event

    def test_future_message(self, output_queue):
        test_message = MidiEvent(mido.Message('note_on',note=60), FAR_FUTURE_TIMESTAMP)
        output_queue.select_device()
        output_queue.queue.put(test_message)
        output_queue._check_queue()

        expected_sent_messages = 0
        actual_sent_messages = len(output_queue._open_port.sent_messages)

        assert actual_sent_messages is expected_sent_messages

    def test_many_messages(self, output_queue):
        expected_past_messages = 5
        expected_future_messages = 3
        past_messages = []

        for i in range(expected_past_messages):
            test_message = MidiEvent(mido.Message('note_on', note=60), i * 10)
            past_messages += [test_message]
            output_queue.queue.put(test_message)

        for i in range(expected_future_messages):
            output_queue.queue.put(MidiEvent(mido.Message('note_on', note=60), FAR_FUTURE_TIMESTAMP + i * 10))

        output_queue.select_device()
        output_queue._check_queue()

        actual_sent_messages = len(output_queue._open_port.sent_messages)
        actual_unsent_messages = output_queue.queue.qsize()

        assert actual_sent_messages is expected_past_messages
        assert actual_unsent_messages is expected_future_messages
    
        # Assert that each past message exists in the sent messages (already length checked)
        for i in range(expected_past_messages):
            assert past_messages[i].event in output_queue._open_port.sent_messages
