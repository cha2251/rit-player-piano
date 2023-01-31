import pytest
from pynput import keyboard

from src.button_input.button_input import ButtonInput
from src.common.shared_queues import SharedQueues


class TestCreate:
    def test_create_button_input(self):
        testQueues = SharedQueues
        testQueues.create_queues(testQueues)
        component = ButtonInput(testQueues.button_input_queue)
        testDict = {'q': 55, 'w': 56, 'e': 57, 'r': 58, 't': 59,
                    'y': 60, 'u': 61, 'i': 62, 'o': 63, 'p': 64}

        expected = testDict
        actual = component.keyMap

        assert component.button_input_queue is testQueues.button_input_queue
        assert expected == actual

    def test_dict_preset(self):
        testQueues = SharedQueues
        testQueues.create_queues(testQueues)
        testDict = {'q': 1, 'w': 2}
        component = ButtonInput(testQueues.button_input_queue, testDict)

        expected = testDict
        actual = component.keyMap

        assert actual == expected


class TestModify:
    def test_change_map(self):
        testQueues = SharedQueues
        testQueues.create_queues(testQueues)
        component = ButtonInput(testQueues.button_input_queue)
        testDict = {'q': 1, 'w': 2}

        assert component.keyMap != testDict

        component.changeMap(testDict)

        expected = testDict
        actual = component.keyMap

        assert actual == expected


class TestRun:
    @pytest.mark.timeout(1)
    def test_exits(self):
        testQueues = SharedQueues
        testQueues.create_queues(testQueues)
        component = ButtonInput(testQueues.button_input_queue)

        component.start()

        component.deactivate()

        component.join()

    @pytest.mark.timeout(1)
    def test_detect_input(self):
        testQueues = SharedQueues
        testQueues.create_queues(testQueues)
        component = ButtonInput(testQueues.button_input_queue)

        component.start()
        component.on_press(keyboard.KeyCode.from_char('q'))
        component.on_release(keyboard.KeyCode.from_char('q'))
        component.deactivate()

        assert component.button_input_queue.empty() is False
