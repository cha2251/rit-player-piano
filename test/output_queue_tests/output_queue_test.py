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

        assert test_output_devices == output_queue.get_device_list()

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

        assert output_queue.check_queue() == 0
        assert len(output_queue._open_port.sent_messages) == 0

    def test_no_open_port(self, output_queue):
        output_queue.queue.put(None)

        assert output_queue.check_queue() == 0

    def test_one_message(self, output_queue):
        test_message = MidiEvent(mido.Message('note_on',note=60), 42)

        output_queue.select_device()
        output_queue.queue.put(test_message)

        assert output_queue.check_queue() == 1
        assert output_queue._open_port.sent_messages[0] == test_message.event

    def test_future_message(self, output_queue):
        test_message = MidiEvent(mido.Message('note_on',note=60), FAR_FUTURE_TIMESTAMP)

        output_queue.select_device()
        output_queue.queue.put(test_message)

        assert output_queue.check_queue() == 0
        assert len(output_queue._open_port.sent_messages) == 0

    def test_many_messages(self, output_queue):
        num_past_messages = 5
        num_future_messages = 3
        past_messages = []

        for i in range(num_past_messages):
            test_message = MidiEvent(mido.Message('note_on', note=60), i * 10)
            past_messages += [test_message]
            output_queue.queue.put(test_message)

        for i in range(num_future_messages):
            output_queue.queue.put(MidiEvent(mido.Message('note_on', note=60), FAR_FUTURE_TIMESTAMP + i * 10))

        output_queue.select_device()

        assert output_queue.check_queue() == num_past_messages
        assert len(output_queue._open_port.sent_messages) == num_past_messages
        assert output_queue.queue.qsize() == num_future_messages

        for i in range(num_past_messages):
            assert output_queue._open_port.sent_messages[i] == past_messages[i].event
